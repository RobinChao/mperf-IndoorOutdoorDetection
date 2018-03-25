#!/bin/bash

# This script takes the directory which contains .csv.gz files as an 
# argument and and decompress them into a folder called csvfiles.

DIR=$1

gzip -dk $DIR/*.csv.gz
mkdir $DIR/csvfiles
mv $DIR/*.csv $DIR/csvfiles
