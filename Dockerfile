# 
FROM openjdk:8
COPY --from=python:3.7 / / 

ENV PYSPARK_MAJOR_PYTHON_VERSION=3

# 
WORKDIR /code

# 
COPY ./requirements.txt /code/requirements.txt

# 
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# 
COPY ./api /code/api
COPY ./etl /code/etl

#
COPY ./data/sources/cities.csv /code/data/sources/cities.csv
COPY ./data/sources/climate.csv /code/data/sources/climate.csv
COPY ./scripts/docker_commands.sh /code/scripts/docker_commands.sh

CMD sh /code/scripts/docker_commands.sh
