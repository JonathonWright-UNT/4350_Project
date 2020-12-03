.DEFAULT_GOAL := help

.PHONY: help
help:  ## This help dialog (from https://marmelab.com/blog/2016/02/29/auto-documented-makefile.html)
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.PHONY: pipenv
pipenv:	 ## Install pip dependencies
	pip install --upgrade pip
	pip install pipenv --upgrade
	pipenv install

.PHONY: launch
launch:  ## Launch blood bank site
	source app-env
	pipenv run python run.py