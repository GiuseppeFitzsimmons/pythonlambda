#!/bin/bash
set -eo pipefail
rm -rf deploy_function
cd dev_function
pip3 install --target ../deploy_function_dev -r requirements.txt
cp -R lambda_function.py ../deploy_function_dev
cp -R redirect.json ../deploy_function_dev