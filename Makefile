.PHONY: run
run:
	gunicorn -c proxy_mock/etc/gunicorn.conf.py

docker_run:
	docker build -t proxy_mock --build-arg CMD_ARG="gunicorn -c proxy_mock/etc/gunicorn.conf.py" .
	docker run -p 5000:5000 proxy_mock

lint:
	yapf -dpr .
	flake8
	isort . -c

lint_fix:
	yapf -ipr .
	isort .

kill_proxy_mock:
	sudo netstat -tnlp | grep ':5000' | awk '{print $$7}' | awk -F'/' '{print $$1}' | xargs kill -9 | true
	sudo netstat -tnlp | grep ':5000' | awk '{print $$7}' | awk -F'/' '{print $$1}' | xargs kill -9 | true

test:
	pytest --cov=client --cov=proxy_mock