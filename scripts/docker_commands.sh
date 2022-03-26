pytest -q /code/etl/test.py
python /code/etl/etl.py
mkdir -p /code/data/results/canada_climate_stats/
cp /code/tmp/canada_climate_stats/*.csv /code/data/results/canada_climate_stats/canada.csv
cp /code/tmp/canada_cities_climate_stats/*.csv /code/data/results/canada_climate_stats/cities.csv

uvicorn api.main:app --host 0.0.0.0 --port 8020