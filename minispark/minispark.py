# minispark.py
# This script reads a text file and computes the maximum number of words in a line.
# Chet Russell

from pyspark.sql import SparkSession
from pyspark.sql import functions as sf

# Initialize SparkSession
spark = SparkSession.builder.appName("WordCount").getOrCreate()

# Read the text file
textFile = spark.read.text("testREADME.md")

# Compute the maximum number of words in a line
result = (
    textFile
    .select(sf.size(sf.split(textFile.value, "\s+")).alias("numWords"))
    .agg(sf.max(sf.col("numWords")))
    .collect()
)

print(result)