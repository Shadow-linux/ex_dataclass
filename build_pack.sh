#!/usr/bin/env bash

echo "clear old pack file..."
rm -rf build dist ex_dataclass.egg-info


python3 setup.py sdist bdist_wheel
twine upload dist/*