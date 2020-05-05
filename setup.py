import setuptools

with open("readme.MD", "r") as fh:
	long_description = fh.read()

setuptools.setup(
	name="RDFGraphStructuredness",
	version="0.1.0",
	author="Alexander Bigerl",
	author_email="bigerl@mail.upb.de",
	description='Calculate the structuredness or coherence of a dataset as defined in Duan et al. paper titled '
				'"Apples and Oranges: A Comparison of RDF Benchmarks and Real RDF Datasets". The structuredness is '
				'measured in interval [0,1] with values close to 0 corresponding to low structuredness, '
				'and 1 corresponding to perfect structuredness. The paper concluded that synthetic datasets have high '
				'structurenes as compared to real datasets.',
	long_description=long_description,
	long_description_content_type="text/markdown",
	url="https://github.com/dice-group/RDFGraphStructuredness",
	packages=setuptools.find_packages(),
	classifiers=[
		"Programming Language :: Python :: 3",
		"Operating System  :: POSIX :: Linux",
	],
	python_requires='>=3.6',
	scripts=['RDFGraphStructuredness.py'],
	install_requires=['sparqlwrapper', 'click']

)
