.ONESHELL:
docs: # Generate Sphinx HTML documentation.
	cd doc
	make clean && make html
	cd ..
	
test_unit:
	pytest tests/unit/ --cov=skspatial --cov-report=html

test_docs: # Run all doctests in documentation.
	sphinx-build -b doctest doc/source/ doc/build/

test_readme:
	python -m doctest README.rst
