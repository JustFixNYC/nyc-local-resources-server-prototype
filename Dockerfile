FROM python:3.7

RUN apt-get update \
  && apt-get install -y \
    postgresql-client \
    binutils \
    libproj-dev \
    gdal-bin \
  && rm -rf /var/lib/apt/lists/* \
  && rm -rf /src/*.deb

RUN pip install \
  django==2.1.2 \
  dj-database-url \
  psycopg2-binary
