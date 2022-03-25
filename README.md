## Canadian Cities Climate Insights Platform

### Problem Statement
As a weather analyst, I would like to be able to corelate the cities data with the climates data collected around each city. I would like to answer questions such as:
- What is the median/mean temperature across all urban or rural Canadian cities? Or across a province or for a given city
- How much snow a certain province/city/or all Canada recieved on a given date?
- What was the humidity for a given province? Is there a relationship between amount of snow and the humidty?
- Which month of the year is the coldest/windiest/snowiest per province/city?
- Is there a correlation between wind and humidity? e.g. the windier days are more likely to be drier?

DISCLAIMER: I do not know what the flags in the climate.csv are for (e.g. min_temp_flag,etc so I ignored their value in this excersise)

### Project Description
This project has three main components:
- ETL pipeline (etl.py): Takes the data from cities and climate files, cleans and transformes the data and loads them into a csv file for consumption
- API: Provides REST endpoints to get the data from the final csv file and returns a JSON response including the requested data
- Frontend: The view layer for data visualization and user interaction 

#### Source Data
**data/sources/cities.csv**: Includes data about Canadian cities (we only care about `city`, `lat`, `lng`, `population`, `proper_population` columns in this project)- Demographic information about Canadian cities and includes the majority of Canada's urban population.
**data/sources/climate.csv**: Includes data about Canadian weather stations (we only care about `lat`, `lng`, `mean_temperature`, `min_temperature`, `max_temperature` in this project) - climate information for a few weeks in early 2021 collected at weather stations around Canada.

#### ETL Process And Assumptions
During the ETL process, data is loaded from cities and climate csv files into PySpark dataframes to be processed in memory.

I defined `Urban cities` based on https://www2.census.gov/geo/pdfs/reference/GARM/Ch12GARM.pdf as follows (logically doesn't make sense to me because it will consider a city of 2500 population with 2500 proper population urban whereas it doesn't consider a city of 49000 proper poulation with 50000 population as urban but going to assume this is correct for the assignment):
- A city with proper population of more than 50000
- A city with population of between 2500 and 50000 where the population is concentrated in one area (proper_population == population)

The two source datasets (cities.csv and climate.csv) are joined based on latitude and longitude. Since the lat and long values in cities.csv file are taken from the center of the city and weather stations can be scattered around a city (lat and long in climates.csv), there is no exact match between the values in the two files. In order to correlate the weather stations to cities, I rounded the values to 1 decimal point with the margin error of `0.1` (0.1 ~= 11km) which will include the stations up to 11km away from the city center.

The ETL process calculates two different stats:
- Calculates the mean and median temperature across all canadian cities per day (The result data gets saved into `data/results/canada_climate_stats/canada.csv`)
- Calculates the mean and median temperature per urban city per day (The result data gets saved into `data/results/canada_climate_stats/cities.csv`). 

#### Final Database Schema
Based on the requirements, I have decided to do the pre-aggregations and calculate the stats prior to inserting it into the new files (analytics datastore). The data model will change if we want a more generic-purpose analytics datastore for doing adhoc reports/analytics (we can design a star schema instead if the end users are comfortable using SQL to run their reports with fact tables and dimensions).

The data model for this project is designed based on two assumptions/use cases:
- We need to query the median/mean temperature across all canada for a given date
- We need to query the median/mean temperature for each urban city for a given date
It includes two tables/file structures:
- canada.csv (can be called canada_climate_stats if it was a table): it includes `date`, `mean`, `median` columns (would be better to rename mean and median to mean_temperature and median_temperature to be more descriptive)
- cities.csv (can be called urban_cities_climate_stats if it was a table:): it includs `date`, `city`, `mean`, `median` columns (would be better to rename mean and median to mean_temperature and median_temperature to be more descriptive)

![alt text](https://github.com/sahar1364/climate_analysis_platform/tree/master/images/emr.jpg?raw=true)

#### Important Files In This Project
**etl/etl.py:** Fetches and transforms data from cvs files and inserts them into two final csv file in `data/results/canada_climate_stats` directory
**etl/test.py**: The test file that does a couple of unit tests (it is not comprehensive but just a placeholder to add more tests in future)
**api/main.py**: Uses FastApi library to define the endpoints for getting the calculated data from csv files
**scripts/setup-environment.sh**: Installs all dependencies, run the etl script and the tests, launches the API endpoints
**scripts/setup-python-venv.sh**: Installs python virtual environment in case it is needed

### Operational Excelence in ETL Pipeline
- Performance and Scalability: The etl script in written in PySpark which enables us to run it on a distributed environment and take advantage of Spark's offerings in terms of Scalability and Performance. For instance, if we use AWS as the cloud provider, we can run the job on an EMR cluster which will distribute it on EC2 instances (nodes) of the EMR and will enhance the performance and scalability. If the data size increases, we can easily scale up the EMR cluster or we can enable EMR's auto-scaling (Elastic Scaling). If the size of data increases, we need to move the result dataset out of csv files and into a proper OLAP datastore (such as Pinot, Druid, Rockset depending on the use case and requirements)
- Security and Data Privacy: This project does not include any sensitive information to be concerned about data privacy. Using cloud providers such as AWS, we can take advantage of the out-of-box encryption services both at rest and in transit to enhance the security.
- Availability: Not a concern in this batch ETL pipeline as it runs once and populates the data
- Monitoring and Alerting: We can send some metrics to monitoring and alerting tools such as DataDog and create dashboards and alerts based on those metrics. Or we can take advantage of cloud native solutions such as AWS CloudWatch depending on our stack.

### Instructions For Running The Application
I used python version `3.7.3` to run and test this project. If you need to keep your current version of python (i.e. python 2.x), you can install `venv` and run this project within your virtual python environment:

```
$ ./scripts/setup-python-venv.sh
```
This should activate the `venv` in your terminal. If not, run `source venv/bin/activate` manually.

Once you are ready to run the python program, run the following script which installs all the depencies, runs the `etl` script to generate the required data and brings up the api on `http://127.0.0.1:8000/`:

```
$ ./scripts/setup-environment.sh
```

**Testing the API Directly**:
```
# return mean/median for overall Canada for a given date (date format is YYYY-MM-DD)
$ curl http://127.0.0.1:8000/stats/canada/2021-01-01
# return mean/median for all Canadian urban cities for a given date
$ curl http://127.0.0.1:8000/stats/cities/2021-01-01
# return mean/median for a given urban city for a given date (city is case sensitive)
$ curl http://127.0.0.1:8000/stats/cities/Calgary/2021-01-01
```

If you are in virtual environment, run `conda deactivate` to exit.

### Future Steps
- Instead of sinking the data into csv files, insert them into a database (i.e. PostGres or an OLAP datastore depending on requirements and size of data)
- Add PySpark specific tests to test the joins
- Containarize the app
