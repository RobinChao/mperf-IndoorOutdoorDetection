#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 21 13:29:37 2018

@author: zxxia
"""

import pandas as pd
from datetime import datetime, time
import pytz
import gzip
import os
import json

with open('/Users/zxxia/Research/src/config/config.json') as f:
    CONFIG = json.load(f)
DATASOURCES = CONFIG['Datasources']
GROUNDTRUTH = CONFIG['Groundtruths']
HIGH_FREQ_DATA_DIR = CONFIG['High Freq Data Dir']
LOW_FREQ_DATA_DIR = CONFIG['Low Freq Data Dir']
COLUMN_NAMES = CONFIG['Sensor CSV Column Names']

def load_data_from_file(filename: str, column_names: list):

    ''' Load data from a file
    Key arguments:
        filename     -- File name of raw data.
                        filename should be in type of either '.csv' or
                        '.gz.csv'.
        column_names -- The name of columns in dataframe.
                        Timestamps are loaded as datetime object with
                        tzinfo=UTC.

    Return values:
        Data loaded in format of pandas dataframe.
    '''
    if type(filename) is not str:
        raise TypeError('filename must be a string.')

    if type(column_names) is not list:
        raise TypeError('column_names must be a list.')

    if filename[-4:] == '.csv':
        df = pd.read_csv(filename,
                         header=None,
                         names=column_names,
                         parse_dates=['Timestamp'],
                         date_parser=lambda x:
                         pd.to_datetime(x, utc=True, box=True, unit='ms'))
    elif filename[-7:] == '.csv.gz':
        try:
            with gzip.open(filename, 'rb') as csvfile:
                df = pd.read_csv(csvfile,
                                 header=None,
                                 names=column_names,
                                 parse_dates=['Timestamp'],
                                 date_parser=lambda x:
                                     pd.to_datetime(x, utc=True, box=True, unit='ms'))
        except EOFError:
            return None
    else:
        raise ValueError("filename must be in format of '.csv' or '.csv.gz'.")

    return df


def filter_data(df,
                start_dt=pd.Timestamp.min.replace(tzinfo=pytz.utc),
                end_dt=pd.Timestamp.max.replace(tzinfo=pytz.utc),
                start_t=time.min,
                end_t=time.max,
                tz=pytz.utc,
                weekdays=[0, 1, 2, 3, 4, 5, 6]):

    '''Filter a data based on timing constraints.

    Keyword arguments:
    df       -- Input pandas dateframe

    start_dt -- Starting datetime object.
                (default 1677-09-21 00:12:43.145225+00:00)
                start_dt can be either timezone-aware datetime object or
                timezone-unware datetime object. If start_dt is
                timezone-unware, tz will be used to localize it.

    end_dt   -- Ending datetime object
                (default 2262-04-11 23:47:16.854775807+00:00)
                end_dt can be either timezone-aware datetime object or timezone
                -unware datetime object. If end_dt is timezone-unware, tz will
                be used to localize it.

    start_t  -- starting time of day. (default time(0, 0, 0, 0))
                start_t is always chekced in timezone tz.

    end_t    -- ending time of day. (default time(23, 59, 59, 999999))
                end_t is always chekced in timezone tz.

    tz       -- timezone object. (default UTC)

    weekdays -- list of integers. Mon: 0, Sun: 6.
                (default: [0, 1, 2, 3, 4, 5, 6])
                weekdays are always checked in timezone tz.

    Return Values:
    dataframe with timestamp ts satisfying
    start_dt <= ts < end_dt and
    start_t <= ts.time_of_day in tz < end_t and
    ts.weekday in weekdays
    '''

    if start_dt.tzinfo is None:
        start_dt = tz.localize(start_dt)

    if end_dt.tzinfo is None:
        end_dt = tz.localize(end_dt)

    constraints = pd.Series([
            (ts >= start_dt) &
            (ts < end_dt) &
            (ts.astimezone(tz).time() >= start_t) &
            (ts.astimezone(tz).time() < end_t) &
            (ts.astimezone(tz).weekday() in weekdays)
            for ts in df['Timestamp']])

    return df[constraints.values]


def load_groundtruth(tz):
    df = pd.read_csv(GROUNDTRUTH,
                     parse_dates={'Start Timestamp': ['Date', 'Start Time'],
                                  'End Timestamp': ['Date', 'End Time']},
                     date_parser=lambda date, t:
                     tz.localize(datetime.strptime(date+' '+t,
                                                   '%m/%d/%Y %H:%M')))
    return df


def load_datasources():
    df = pd.read_csv(DATASOURCES)
    dsid_type_dict = dict()
    type_dsid_dict = dict()
    for index, row in df.iterrows():
        if row['platform_type'] == 'PHONE':
            dsid_type_dict[row['ds_id']] = row['datasource_type']
            type_dsid_dict[row['datasource_type']] = str(row['ds_id'])

    return dsid_type_dict, type_dsid_dict


def load_low_freq_data(sid: str):
    prefix = sid + '_'
    for file in os.listdir(LOW_FREQ_DATA_DIR):
        if file.startswith(prefix):
            return load_data_from_file(LOW_FREQ_DATA_DIR + '/' + file,
                                       COLUMN_NAMES[sid])


def load_high_freq_data(sid: str, d):
    date_str = d.strftime("%Y%m%d")
    data_dir = HIGH_FREQ_DATA_DIR + '/raw' + sid
    file_list = os.listdir(data_dir)
    file_list.sort()
    results = []
    for file in file_list:
        if file.startswith(date_str):
            df = load_data_from_file(data_dir + '/' + file, COLUMN_NAMES[sid])
            results.append(df)
    return pd.concat(results)
