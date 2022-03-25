from fastapi import FastAPI
import pandas as pd

app = FastAPI()


@app.get("/stats/canada/{date}")
async def root(date: str):
    df = pd.read_csv('../data/results/canada_climate_stats/canada.csv', usecols= ['date','mean', 'median'])
    date_filter = df['date'] == date
    df_for_date = df[date_filter].fillna('')
    return {df_for_date.to_json(orient = 'table', index=False) }

@app.get("/stats/cities/{date}")
async def root(date: str):
    df = pd.read_csv('../data/results/canada_climate_stats/cities.csv', usecols= ['date','mean', 'median', 'city'])
    date_filter = df['date'] == date
    df_for_date = df[date_filter].fillna('')
    return {df_for_date.to_json(orient = 'table', index=False)}

@app.get("/stats/cities/{city}/{date}")
async def root(city: str, date: str):
    df = pd.read_csv('../data/results/canada_climate_stats/cities.csv', usecols= ['date','mean', 'median', 'city'])
    date_filter = (df['date'] == date) & (df['city'] == city)
    df_for_date_and_city = df[date_filter].fillna('')
    return {df_for_date_and_city.to_json(orient = 'table', index=False)}

@app.get("/cities")
async def root():
    df = pd.read_csv('../data/sources/cities.csv', usecols= ['city'])
    return {df.to_json(orient = 'table', index=False)}
