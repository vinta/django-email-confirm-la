FROM vinta/python:2.7

MAINTAINER Vinta Chen <vinta.chen@gmail.com>

RUN apt-get update && \
    apt-get install -y \
    -o APT::Install-Recommends=false -o APT::Install-Suggests=false \
    build-essential \
    libyaml-dev && \
    rm -rf /var/cache/apt/archives/* /var/lib/apt/lists/*

RUN mkdir -p /app/
WORKDIR /app/

COPY requirements*.txt /app/
RUN pip install -r requirements_test.txt

CMD ["coverage", "run", "setup.py", "test"]
