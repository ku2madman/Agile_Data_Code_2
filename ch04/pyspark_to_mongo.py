from pyspark.sql import SparkSession

spark = SparkSession.builder.master('local') \
    .config("spark.mongodb.input.uri", "mongodb://127.0.0.1/agile_data_science.on_time_performance") \
    .config("spark.mongodb.output.uri", "mongodb://127.0.0.1/agile_data_science.on_time_performance") \
    .config("spark.jars.packages", "org.mongodb.spark:mongo-spark-connector_2.11:2.4.1") \
    .getOrCreate()

on_time_dataframe = spark.read.parquet('data/on_time_performance.parquet')

# convert "float" to "double", to avoid "FloatType has no matching BsonValue" exception
on_time_dataframe = on_time_dataframe.withColumn("DepDelay", on_time_dataframe["DepDelay"].cast('double'))
on_time_dataframe = on_time_dataframe.withColumn("TaxiOut", on_time_dataframe["TaxiOut"].cast('double'))
on_time_dataframe = on_time_dataframe.withColumn("ArrDelay", on_time_dataframe["ArrDelay"].cast('double'))
on_time_dataframe = on_time_dataframe.withColumn("TaxiIn", on_time_dataframe["TaxiIn"].cast('double'))
on_time_dataframe = on_time_dataframe.withColumn("ArrDelay", on_time_dataframe["ArrDelay"].cast('double'))
on_time_dataframe = on_time_dataframe.withColumn("ArrDelayMinutes", on_time_dataframe["ArrDelayMinutes"].cast('double'))
on_time_dataframe = on_time_dataframe.withColumn("ActualElapsedTime", on_time_dataframe["ActualElapsedTime"].cast('double'))
on_time_dataframe = on_time_dataframe.withColumn("AirTime", on_time_dataframe["AirTime"].cast('double'))
on_time_dataframe = on_time_dataframe.withColumn("Distance", on_time_dataframe["Distance"].cast('double'))
on_time_dataframe = on_time_dataframe.withColumn("CarrierDelay", on_time_dataframe["CarrierDelay"].cast('double'))
on_time_dataframe = on_time_dataframe.withColumn("WeatherDelay", on_time_dataframe["WeatherDelay"].cast('double'))
on_time_dataframe = on_time_dataframe.withColumn("NASDelay", on_time_dataframe["NASDelay"].cast('double'))
on_time_dataframe = on_time_dataframe.withColumn("SecurityDelay", on_time_dataframe["SecurityDelay"].cast('double'))
on_time_dataframe = on_time_dataframe.withColumn("LateAircraftDelay", on_time_dataframe["LateAircraftDelay"].cast('double'))
# print(on_time_dataframe.dtypes)

on_time_dataframe.write.format('mongo').mode('overwrite').save()

df = spark.read.format('mongo').load()
df.show()
