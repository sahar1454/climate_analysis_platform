#!/usr/bin/env bash

# install PySpark dependency
pip3 install pyspark

# run etl job
python3 etl/etl.py
cp tmp/canada_climate_stats/*.csv data/results/canada_climate_stats/canada.csv
cp tmp/canada_cities_climate_stats/*.csv data/results/canada_climate_stats/cities.csv

# install FastApi dependency
pip3 install "fastapi[all]"

# install panda dependency
pip3 install pandas

cd api

# launch the api server
uvicorn main:app --reload