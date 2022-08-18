run:
	@PYTHONPATH=${PWD} ./bin/code-viewer.py test_data/leveldb.json

# alias
t: test

test:
	python3 -m unittest discover tests -p "*_test.py" -v

count:
	wc -l tests/*.py code_viewer/*.py bin/*.py
