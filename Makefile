.PHONY: test_run
test_run:
	@echo 'test run'


.PHONY: setup
setup:
	sudo pip3 install virtualenv; \
	virtualenv -p python3.7 --always-copy --system-site-packages venv; \
	. venv/bin/activate; pip3 install -r requirements/requirements.txt


.PHONY: test
test:
	coverage run -m unittest

.PHONY: report_test
report_test:
	coverage report -m --omit=/usr/*


.PHONY: liq_migrate
liq_migrate:
	./migrations/liquibase --url=jdbc:postgresql://localhost/whreports \
	--driver=org.postgresql.Driver \
	--classpath=./migrations/jdbcdrivers/postgresql-42.2.5.jar \
	--username=postgres \
	--password=admin \
	--changeLogFile=/migrations/changelog.xml migrate