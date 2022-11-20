This repository contains a few scripts I use to pull my personal expenses from Mint and organize them in a google sheets document.

1. Import Recent Transactions - adds all recent transactions to the google sheet if they're not already there.

Note: Always use a python virtual environment to run this so that I don't have dependency issues.

To create the virtual env: 'python3 -m venv {virtual_environment_name}'

To activate: 'source {virtual_environment_name}/bin/activate'

Then update pip packages if necessary

Then run: 'python main.py'

To deactivate: 'deactivate'
