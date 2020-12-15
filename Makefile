.PHONY: build unit-tests lint codestyle clean

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