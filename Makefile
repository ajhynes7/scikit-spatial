.ONESHELL:
docs: # Generate Sphinx HTML documentation.
	cd doc
	make clean && make html
	cd ..
	
test_docs: # Run all doctests in documentation.
	sphinx-build -b doctest doc/source/ doc/build/
