.PHONY: install pasos run extra limpiar

install:
	pip install -e .

pasos: install
	pipeline-sklearn --listar-pasos

run: install
	pipeline-sklearn

extra: install
	pip install -e plugin_extra
	pipeline-sklearn --listar-pasos

limpiar:
	pip uninstall -y entrypoints-sklearn-pipeline pipeline-paso-extra
