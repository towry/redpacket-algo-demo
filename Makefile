
all:
	python main.py && make index

index:
	python ./scripts/index.py

dev: index
	python -m SimpleHTTPServer 8900

rm:
	rm -rf _results && mkdir _results

.PYONY: clean rm
