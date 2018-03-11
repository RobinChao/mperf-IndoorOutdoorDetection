#!/bin/bash

DIR=$1

gzip -dk $DIR/*.csv.gz
mkdir $DIR/csvfiles
mv $DIR/*.csv $DIR/csvfiles
