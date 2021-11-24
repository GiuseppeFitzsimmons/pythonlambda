#!/bin/bash
set -eo pipefail
rm -rf deploy_function
cd function
pip3 install --target ../deploy_function -r requirements.txt
cp -R lambda_function.py ../deploy_function
cp -R redirect.json ../deploy_function