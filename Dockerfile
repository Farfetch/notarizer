FROM python:3.8.5-alpine AS build

COPY requirements.txt /tmp

USER root
RUN apk add --no-cache gcc musl-dev libffi-dev openssl-dev coreutils && \
    pip install -r /tmp/requirements.txt

COPY . /app

WORKDIR /app
ENV PYTHONPATH=/app

FROM build AS unit-tests
CMD [ "python", "-m", "unittest", "-v"]

FROM build AS notarizer
RUN rm -r /app/notarizer/test
ENTRYPOINT [ "python", "notarizer/cli.py"]
