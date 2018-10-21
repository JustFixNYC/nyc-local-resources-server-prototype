FROM python:3.7

RUN apt-get update \
  && apt-get install -y \
    postgresql-client \
    binutils \
    libproj-dev \
    gdal-bin \
  && rm -rf /var/lib/apt/lists/* \
  && rm -rf /src/*.deb

COPY requirements.txt /app/requirements.txt

RUN pip install -r /app/requirements.txt
