#!/bin/bash

rm -R venv
python3 -m virtualenv venv
venv/bin/python -m pip install -r requirements.txt
