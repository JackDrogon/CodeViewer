run:
	@PYTHONPATH=${PWD} ./bin/code-viewer.py test_data/leveldb.json

test:
	python3 -m unittest discover tests -p "*_test.py" -v
