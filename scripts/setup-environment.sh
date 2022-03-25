#!/usr/bin/env bash

# install PySpark dependency
pip install pyspark

# run etl job
python etl/etl.py
cp tmp/canada_climate_stats/*.csv data/results/canada_climate_stats/canada.csv
cp tmp/canada_cities_climate_stats/*.csv data/results/canada_climate_stats/cities.csv

# install FastApi dependency
pip install "fastapi[all]"

cd api

# launch the api server
uvicorn main:app --reload