#!/bin/bash

echo "MyPy"
mypy backend/app/app
echo "ISort"
isort backend/app/app
echo "Flake8"
flake8 backend/app/app
echo "Pytest"
pytest backend/app/app/tests