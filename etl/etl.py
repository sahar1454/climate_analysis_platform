from pyspark.sql import SparkSession
from pyspark.sql.functions import col, col, avg, to_date
from pyspark.sql.functions import *
from pyspark.sql import SQLContext


def create_spark_session():
    spark = SparkSession \
        .builder \
        .config("spark.jars.packages", "org.apache.hadoop:hadoop-aws:2.7.0") \
        .config("spark.sql.crossJoin.enabled", "true") \
        .getOrCreate()

    return spark


def process_climate_data(
        spark,
        input_data_cities,
        input_data_climate):
    """
     Description: Processes cities and climate files and inserts mean/median data into final csv file

     Arguments:
         spark: spark context object
         input_data_cities: the path to cities file
         input_data_climate: the path to climate file

     Returns:
         None
    """
    df_climate = spark.read.option("header", "true").csv(input_data_climate)

    df_climate_sub = df_climate.select(col("lng").alias("longtitude"), col("lat").alias("latitude"), col("MIN_TEMPERATURE").alias("min_temp"), col(
        "MAX_TEMPERATURE").alias("max_temp"), col("MEAN_TEMPERATURE").alias("mean_temperature"), to_date(col("LOCAL_DATE")).alias("date"))
    df_climate_sub.show(10)

    df_cities = spark.read.option("header", "true").csv(input_data_cities)
    df_cities_sub = df_cities.filter((col("population_proper") > 50000) | ((col("population_proper") <= 50000) & (col("population_proper") >= 2500) & (col(
        "population_proper") == col("population")))).select(col("city"), col("lat").alias("latitude"), col("lng").alias("longtitude"), col("population"), col("population_proper"))

    df_cities_sub.show(10)

    df_cities_sub.select('city').distinct().repartition(1).write.mode("overwrite").option(
        "header", "true").csv("tmp/canada_cities")

    join_condition = [((round(df_climate_sub.longtitude, 1) == round(df_cities_sub.longtitude, 1)) | ((round(df_climate_sub.longtitude, 1) + 0.1) == round(df_cities_sub.longtitude, 1)) | (round(df_climate_sub.longtitude, 1) == (round(df_cities_sub.longtitude, 1) + 0.1))),
                      ((round(df_climate_sub.latitude, 1) == round(df_cities_sub.latitude, 1)) | ((round(df_climate_sub.latitude, 1) + 0.1) == round(df_cities_sub.latitude, 1)) | (round(df_climate_sub.latitude, 1) == (round(df_cities_sub.latitude, 1) + 0.1)))]

    df_final = df_cities_sub.join(df_climate_sub, join_condition, "inner").select(
        col("city"), col("mean_temperature"), col("date"))
    df_final.show(10)

    df_mean = df_final.groupBy(col('date')).agg(
        avg(col("mean_temperature")).alias("mean"))
    df_mean.show()

    sqlContext = SQLContext(spark.sparkContext)
    df_final.registerTempTable("df")
    df_median = sqlContext.sql(
        "select date as median_date, percentile_approx(mean_temperature,0.50) as median from df group by date")
    df_median.show()

    df = df_mean.join(df_median, df_median.median_date == df_mean.date).select(
        col("median"), col("mean"), col("date")).orderBy(col("date"))
    df.show()

    df.repartition(1).write.mode("overwrite").option(
        "header", "true").csv("tmp/canada_climate_stats")

    # Calculate for each city based on its weather stations
    df_city_mean = df_final.groupBy(col('city'), col('date')).agg(
        avg(col("mean_temperature")).alias("mean"))
    df_city_mean.show()

    df_city_median = sqlContext.sql(
        "select date as median_date, percentile_approx(mean_temperature,0.50) as median, city as median_city from df group by city,date")
    df_city_median.show()

    df_city = df_city_mean.join(df_city_median, (df_city_median.median_date == df_city_mean.date) & (df_city_mean.city == df_city_median.median_city)).select(
        col("median"), col("mean"), col("date"), col("city")).orderBy(col("city")).orderBy(col("date"))
    df_city.show()

    df_city.repartition(1).write.mode("overwrite").option(
        "header", "true").csv("tmp/canada_cities_climate_stats")


def main():
    spark = create_spark_session()

    process_climate_data(spark, "data/sources/cities.csv",
                         "data/sources/climate.csv")


if __name__ == "__main__":
    main()
