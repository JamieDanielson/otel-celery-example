# celery

## setup simple celery with redis

```sh
# set up virtual env
python3 -m venv env
source env/bin/activate

# install celery
python3 -m pip install celery

# install redis
python3 -m pip install -U "celery[redis]"

# run redis
docker run -d -p 6379:6379 redis

# run the worker on its own
celery --app=tasks worker --loglevel=INFO
```

## add opentelemetry

```sh
# stop the celery task with ctrl+c
# set API key
export HONEYCOMB_API_KEY=<yourkey>

# install opentelemetry distro and exporter
python3 -m pip install opentelemetry-distro \
  opentelemetry-exporter-otlp

# install instrumentation packages
opentelemetry-bootstrap -a install

# run the agent with the worker
opentelemetry-instrument \
    --traces_exporter console,otlp \
    --metrics_exporter none \
    --service_name "my-celery" \
    --exporter_otlp_protocol "http/protobuf" \
    --exporter_otlp_endpoint "https://api.honeycomb.io" \
    --exporter_otlp_headers "x-honeycomb-team=${HONEYCOMB_API_KEY}" \
    celery --app tasks worker --loglevel=INFO
```

## call the task to generate telemetry

```sh
# in a new terminal, activate env again
source env/bin/activate

# start python3 interpreter
python3

# import add function and delay
>>> from tasks import add
>>> add.delay(4, 4)
```
