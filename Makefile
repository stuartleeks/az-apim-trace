
build-wheel:
	python setup.py bdist_wheel


add-extension:
	az extension add --source ./dist/apim_trace-0.0.3-py2.py3-none-any.whl --yes --upgrade