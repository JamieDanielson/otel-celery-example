# celery

## setup django and redis

```sh
# set up virtual env
python3 -m venv env
source env/bin/activate

# install all the things
python3 -m pip install -r requirements.txt

# run redis in (detached) docker
docker run -d -p 6379:6379 redis

# navigate to mysite directory
cd mysite

# start server
python3 manage.py runserver
```

## run celery with otel

```sh
# in a new terminal, activate env again
source env/bin/activate

# set API key
export HONEYCOMB_API_KEY=<yourkey>

# navigate to site direcotry
cd mysite

# run the agent with the worker
opentelemetry-instrument \
    --traces_exporter console,otlp \
    --metrics_exporter none \
    --service_name "my-celery" \
    --exporter_otlp_protocol "http/protobuf" \
    --exporter_otlp_endpoint "https://api.honeycomb.io" \
    --exporter_otlp_headers "x-honeycomb-team=${HONEYCOMB_API_KEY}" \
    celery --app=mysite worker --loglevel=INFO
```

## curl the endpoint to generate telemetry

```sh
# this endpoint triggers a task in celery
curl localhost:8000/polls/
```

NOTE: If Redis is too noisy, disable when setting the API Key:

```sh
export OTEL_PYTHON_DISABLED_INSTRUMENTATIONS=redis
```
