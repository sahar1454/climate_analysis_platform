### Canadian Cities Climate Insights Platform

#### Problem Statement
As a weather analyst, I would like to be able to corelate the cities data with the climates data collected around each city. I would like to answer questions such as:
- What is the median/mean temperature across all urban or rural Canadian cities? Or across a province or for a given city
- How much snow a certain province/city/or all Canada recieved on a given date?
- What was the humidity for a given province? Is there a relationship between amount of snow and the humidty?

#### Project Description
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

#### Operational Excelence in ETL Pipeline
- Performance and Scalability:
- Security and Data Privacy:
- Availability:
- Monitoring and Alerting:

#### Files in this project
**etl.py:** Fetches and transforms data from cvs files and inserts them into a final csv file
**test.py**: The test file that prints success or fail depending on test results
**README.md:** The human readable information about the project and what it does


#### Instructions for running

1- Run etl.py to load the files with transformed data ```run etl.py```

2- Run test.py to run the tests and make sure you don't see failures being printed ```run test.py```

NOTE: you can alternatively run the job on an EMR cluster to increase the performance. Copy `etl.py` to the cluster and run ```/usr/bin/spark-submit --master yarn /tmp/etl.py```


### Future Steps
