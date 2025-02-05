
build-wheel:
	rm -rf build dist && \
	python setup.py bdist_wheel


add-extension:
	az extension add --source ./dist/apim_trace-0.0.4-py2.py3-none-any.whl --yes --upgrade