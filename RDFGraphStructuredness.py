from string import Template
from typing import Set
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


def count_type_predicates(endpoint: str, type: str, named_graph: str) -> int:
	query_string: str = Template("""
		SELECT DISTINCT (Count(?typePred) AS ?cnt) $named_graph
		WHERE {
			?s <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <$type> .
			?s ?typePred ?o .
		}
		""").substitute(named_graph="From <{}>".format(named_graph) if named_graph is not None else "",
						type=type)

	results = run_query(endpoint, query_string)
	return get_count(results, "cnt")  # -1 for rdf:type


def get_type_predicates(endpoint: str, type: str, named_graph: str) -> Set[str]:
	query_string: str = Template("""
		SELECT DISTINCT ?typePred $named_graph
		WHERE {
			?s <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <$type> .
			?s ?typePred ?o .
		}
		""").substitute(named_graph="From <{}>".format(named_graph) if named_graph is not None else "",
						type=type)

	results = run_query(endpoint, query_string)
	types = get_iri_set(results, "typePred")
	types.remove("http://www.w3.org/1999/02/22-rdf-syntax-ns#type")
	return types


def get_rdf_types(endpoint: str, named_graph: str) -> Set[str]:
	query_string: str = Template("""
	SELECT DISTINCT ?type $named_graph
	WHERE {
		?s <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> ?type .
	}
	""").substitute(named_graph="From <{}>".format(named_graph) if named_graph is not None else "")

	results = run_query(endpoint, query_string)
	types = get_iri_set(results, "type")
	return types


def count_occurrences(endpoint: str, predicate: str, type: str, named_graph: str) -> int:
	query_string: str = Template("""
		SELECT (Count(Distinct ?s) as ?occurrences) $named_graph
		WHERE {
			?s <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <$type> .
			?s <$predicate> ?o .
		}
		""").substitute(named_graph="From <{}>".format(named_graph) if named_graph is not None else "",
						type=type,
						predicate=predicate)
	results = run_query(endpoint, query_string)
	return get_count(results, "occurrences")


def count_type_instances(endpoint: str, type: str, named_graph: str) -> int:
	query_string: str = Template("""
		SELECT (Count(DISTINCT ?s)  as ?cnt) $named_graph
		WHERE {
			?s <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <$type> .
		}
		""").substitute(named_graph="From <{}>".format(named_graph) if named_graph is not None else "",
						type=type)
	results = run_query(endpoint, query_string)
	return get_count(results, "cnt")


def calc_types_weighted_denom_sum(endpoint: str, types: Set[str], named_graph: str) -> float:
	sum: int = 0

	for type in types:
		typeInstancesSize: int = count_type_instances(endpoint, type, named_graph)
		typePredicatesSize: int = count_type_predicates(endpoint, type, named_graph)
		sum += typeInstancesSize + typePredicatesSize
	return sum


def get_structuredness_value(endpoint: str, named_graph: str):
	types: Set[str] = get_rdf_types(endpoint, named_graph)
	weighted_denom_sum: float = calc_types_weighted_denom_sum(endpoint, types, named_graph)
	structuredness: float = 0
	for type in types:
		occurence_sum: int = 0
		type_predicates: Set[str] = get_type_predicates(endpoint, type, named_graph)

		for predicate in type_predicates:
			occurence_sum += count_occurrences(endpoint, predicate, type, named_graph)

		type_instances_size: int = count_type_instances(endpoint, type, named_graph)

		denom: int = len(type_predicates) * type_instances_size if len(type_predicates) != 0 else 1

		coverage: float = float(occurence_sum) / float(denom)
		weighted_coverage: float = (len(type_predicates) + type_instances_size) / weighted_denom_sum
		structuredness += (coverage * weighted_coverage)

	return structuredness


@click.command()
@click.option('--endpoint', required=True, help='Endpoint holding the RDF graph.')
@click.option('--named', default=None, help='If the named graph is set, only the named graph is considered.')
def cli(endpoint, named):
	"""
	Calculate the structuredness or coherence of a dataset as defined in Duan et al. paper titled "Apples and Oranges: A Comparison of RDF Benchmarks and Real RDF Datasets". The structuredness is measured in interval [0,1] with values close to 0 corresponding to low structuredness, and 1 corresponding to perfect structuredness. The paper concluded that synthetic datasets have high structurenes as compared to real datasets.
	"""

	coherence: float = get_structuredness_value(endpoint, named)
	print(coherence)


if __name__ == '__main__':
	cli()
