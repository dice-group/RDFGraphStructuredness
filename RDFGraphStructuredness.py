from collections import defaultdict
from string import Template
from typing import Set, Dict
import SPARQLWrapper

import click


def run_query(endpoint, query_string) -> dict:
	sparql = SPARQLWrapper.SPARQLWrapper(endpoint)
	sparql.setQuery(query_string)
	sparql.setReturnFormat(SPARQLWrapper.JSON)
	results = sparql.query().convert()
	return results


def get_count(results: dict, key) -> int:
	return int(results["results"]["bindings"][0][key]["value"])


def get_iri_set(results: dict, key) -> Set[str]:
	return {result[key]["value"] for result in results["results"]["bindings"]}


def get_types_predicates(endpoint: str, named_graph: str) -> Dict[str, Set[str]]:
	query_string: str = Template("""
		SELECT DISTINCT ?type ?typePred $named_graph
		WHERE {
			?s a ?type .
			OPTIONAL{ ?s ?typePred [] .
			FILTER (?typePred != <http://www.w3.org/1999/02/22-rdf-syntax-ns#type>) 
			}
		}
		""").substitute(named_graph="FROM <{}>".format(named_graph) if named_graph is not None else "",
						type=type)

	results = run_query(endpoint, query_string)
	types_predicates: Dict[str, Set[str]] = defaultdict(set)
	for binding in results["results"]["bindings"]:
		type_predicates = types_predicates[binding["type"]["value"]]
		if "typePred" in binding:
			type_predicates.add(binding["typePred"]["value"])
	return types_predicates


def get_rdf_types(endpoint: str, named_graph: str) -> Set[str]:
	query_string: str = Template("""
	SELECT DISTINCT ?type $named_graph
	WHERE {
		?s a ?type .
	}
	""").substitute(named_graph="FROM <{}>".format(named_graph) if named_graph is not None else "")

	results = run_query(endpoint, query_string)
	types = get_iri_set(results, "type")
	return types


def sum_predicates_used_by_typed(endpoint: str, type: str, named_graph: str) -> int:
	query_string: str = Template("""
		SELECT (COUNT(DISTINCT *) as ?occurrences) $named_graph
		WHERE {
			SELECT DISTINCT ?s ?predicate {
				?s a <$type> .
				?s ?predicate [] .
				FILTER (?predicate != <http://www.w3.org/1999/02/22-rdf-syntax-ns#type>)
			}
		}
		""").substitute(named_graph="FROM <{}>".format(named_graph) if named_graph is not None else "",
						type=type)
	results = run_query(endpoint, query_string)
	return get_count(results, "occurrences")


def count_instances_by_type(endpoint: str, named_graph: str) -> Dict[str, int]:
	query_string: str = Template("""
		SELECT (COUNT(DISTINCT ?s)  as ?cnt) ?type $named_graph
		WHERE {
			?s a ?type .
			FILTER (?type != <http://www.w3.org/1999/02/22-rdf-syntax-ns#type>)
		} GROUP BY ?type
		""").substitute(named_graph="FROM <{}>".format(named_graph) if named_graph is not None else "",
						type=type)
	results = run_query(endpoint, query_string)
	bindings = results["results"]["bindings"]
	return {entry["type"]["value"]: int(entry["cnt"]["value"]) for entry in bindings}


def get_structuredness_value(endpoint: str, named_graph: str):
	types: Set[str] = get_rdf_types(endpoint, named_graph)
	types_predicates: Dict[str, Set[str]] = get_types_predicates(endpoint, named_graph)
	types_instances_size: Dict[str, int] = count_instances_by_type(endpoint, named_graph)
	weighted_denom_sum: float = float(
		sum(len(predicates) for predicates in types_predicates) +
		sum(instances_size for instances_size in types_instances_size.values())
	)
	structuredness: float = 0
	for type in types:
		type_predicates: Set[str] = types_predicates[type]

		occurrences_sum: int = sum_predicates_used_by_typed(endpoint, type, named_graph)

		type_instances_size: int = types_instances_size[type]

		denom: float = float(len(type_predicates) * type_instances_size if len(type_predicates) != 0 else 1)

		coverage: float = occurrences_sum / denom
		weighted_coverage: float = (len(type_predicates) + type_instances_size) / weighted_denom_sum
		structuredness += (coverage * weighted_coverage)

	return structuredness


@click.command()
@click.option('--endpoint', required=True, help='Endpoint holding the RDF graph.')
@click.option('--named', default=None, help='If the named graph is set, only the named graph is considered.')
def cli(endpoint, named):
	"""
	Calculate the structuredness or coherence of an RDF dataset as defined in Duan et al. paper "Apples and Oranges: A Comparison of RDF Benchmarks and Real RDF Datasets". The structuredness is measured in the interval [0,1] with values close to 0 corresponding to low structuredness, and 1 corresponding to perfect structuredness. The paper concluded that synthetic datasets have high structuredness as compared to real datasets.
	"""

	coherence: float = get_structuredness_value(endpoint, named)
	print(coherence)


if __name__ == '__main__':
	cli()
