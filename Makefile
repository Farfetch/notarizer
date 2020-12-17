.PHONY: build unit-tests lint codestyle clean package install-dev install-pipenv

build:
	@docker-compose up --build --no-start

unit-tests: build
	@docker-compose up --abort-on-container-exit --exit-code-from unit-tests unit-tests

lint: build
	@docker-compose up --abort-on-container-exit --exit-code-from lint lint

codestyle: build
	@docker-compose up --abort-on-container-exit --exit-code-from codestyle codestyle

clean:
	@docker-compose down

package:
	@pipenv run python setup.py sdist bdist_wheel

install-dev: install-pipenv
	@pipenv install
	@pipenv install --dev
	@pipenv run pip install -e . -r requirements.txt

install-pipenv:
	@pip install pipenv

