# ⚠️ This is buggy! -- results produced are not correct ⚠️

# RDF Graph Structuredness

Calculate the structuredness or coherence of an RDF dataset as defined in Duan et al. paper "Apples and Oranges: A Comparison of RDF Benchmarks and Real RDF Datasets" [1]. The structuredness is measured in the interval [0,1] with values close to 0 corresponding to low structuredness, and 1 corresponding to perfect structuredness. The paper concluded that synthetic datasets have high structuredness as compared to real datasets.

[1] Songyun Duan, Anastasios Kementsietsidis, Kavitha Srinivas, and Octavian Udrea. 2011. Apples and oranges: a comparison of RDF benchmarks and real RDF datasets. In Proceedings of the 2011 ACM SIGMOD International Conference on Management of data (SIGMOD ’11). Association for Computing Machinery, New York, NY, USA, 145–156. DOI:https://doi.org/10.1145/1989323.1989340

## install 

Clone it 
```shell script
git clone https://github.com/dice-group/RDFGraphStructuredness.git
```
and enter the cloned folder 
```shell script
cd RDFGraphStructuredness
```
Install it with 
```shell script
pip3 install -U .
```

## run 

Run it with:
```shell script
RDFGraphStructuredness.py [OPTIONS]
```
The tool provides the following commandline [OPTIONS]:
```
  --endpoint TEXT  Endpoint holding the RDF graph.  [required]
  --named TEXT     If the named graph is set, only the named graph is
                   considered.

  --help           Show this message and exit.
```

If it runs successfully, the output is just the structuredness, nothing else. 

## docker
A docker image is available at: https://hub.docker.com/r/dicegroup/rdfgraphstructuredness
