### Canadian Cities Climate Insights Platform

### Problem Statement
As a weather analyst, I would like to be able to corelate the cities data with the climates data collected around each city. I would like to answer questions such as:
- What is the median/mean temperature across all urban or rural Canadian cities? Or across a province or for a given city
- How much snow a certain province/city/or all Canada recieved on a given date?
- What was the humidity for a given province? Is there a relationship between amount of snow and the humidty?

### Project Description
This project has three main components:
- ETL pipeline (etl.py): Takes the data from cities and climate files, cleans and transformes the data and loads them into a csv file for consumption
- API: Provides REST endpoints to get the data from the final csv file and returns a JSON response including the requested data
- Frontend: The view layer for data visualization and user interaction 

#### Source Data
**cities**: 
**climate**:

#### Final Database schema
The data model follows star schema to make analysis more intuitive and easier. We have the following tables:

**Fact Tables:**

 
**Dimension Tables:**

![alt text](images/data_model.png)

#### ETL Process
During the ETL process, data is loaded from cities and climate csv files into PySpark dataframes to be processed in memory. 

#### Files in this project
**etl.py:** Fetches and transforms data from cvs files and inserts them into a final csv file
**test.py**: The test file that prints success or fail depending on test results
**README.md:** The human readable information about the project and what it does

### Operational Excelence in ETL Pipeline
- Performance and Scalability:
- Security and Data Privacy:
- Availability:
- Monitoring and Alerting:


### Instructions for running
I used python version `3.7.3` to run and test this project. If you need to keep your current version of python (i.e. python 2.x), you can install `venv` and run this project within your virtual python environment:

```
$ ./scripts/setup-python-venv.sh
```

Once you are ready to run the python program, run the following script which installs all the depencies, runs the `etl` script to generate the required data and brings up the api on `http://127.0.0.1:8000/`:

```
$ ./scripts/setup-environment.sh
```

If you are in virtual environment, run `conda deactivate` to exit.

### Future Steps
- Instead of sinking the data into csv files, insert them into a database (i.e. PostGres or an OLAP datastore depending on requirements and size of data)
- Containarize the app
