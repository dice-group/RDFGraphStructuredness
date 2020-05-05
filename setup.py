import setuptools

with open("readme.MD", "r") as fh:
	long_description = fh.read()

setuptools.setup(
	name="RDFGraphStructuredness",
	version="0.1.0",
	author="Alexander Bigerl",
	author_email="bigerl@mail.upb.de",
	description='Calculate the structuredness or coherence of a RDF dataset.',
	long_description=long_description,
	long_description_content_type="text/markdown",
	url="https://github.com/dice-group/RDFGraphStructuredness",
	packages=setuptools.find_packages(),
	py_modules=['RDFGraphStructuredness'],
	classifiers=[
		"Programming Language :: Python :: 3",
		"Operating System  :: POSIX :: Linux",
	],
	python_requires='>=3.6',
	entry_points='''
		[console_scripts]
		RDFGraphStructuredness=RDFGraphStructuredness:cli
	''',
	install_requires=['sparqlwrapper', 'click']

)
