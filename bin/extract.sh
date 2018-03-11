#!/bin/bash

# Take the 1st arguemnt as the database file.
DATABASE=$1

# Extract all low frequency data from database.
java -jar DataExporter-all-1.5.0.jar -c -d $DATABASE

# Extract the datasource id and type into a csv file.
sqlite3 -header -csv $DATABASE "select * from datasources;" > datasources.csv
