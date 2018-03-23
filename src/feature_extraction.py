#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 21 00:41:32 2018

@author: zxxia
"""

from datetime import timedelta
from typing import List, Dict
import numpy as np
import pytz
# import pandas as pd
# import json


MORNING_START = 6
MORNING_END = 12

NOON_START = 12
NOON_END = 14

AFTERNOON_START = 14
AFTERNOON_END = 19

EVENING_START = 19
EVENING_END = 22

EARLY_NIGHT_START = 22
EARLY_NIGHT_END = 24
LATE_NIGHT_START = 0
LATE_NIGHT_END = 6


ACTIVITY_TYPES = {
    0: 'STILL',
    1: 'ON_FOOT',
    2: 'TILTING',
    3: 'WALKING',
    4: 'RUNNING',
    5: 'ON_BICYCLE',
    6: 'IN_VEHICLE',
    7: 'UNKNOWN'}


def time_of_day(t, tz) -> str:
    local_t = t.astimezone(tz)
    if local_t.hour >= MORNING_START and local_t.hour < MORNING_END:
        return 'Morning'
    if local_t.hour >= NOON_START and local_t.hour < NOON_END:
        return 'Noon'
    if local_t.hour >= AFTERNOON_START and local_t.hour < AFTERNOON_END:
        return 'Afternoon'
    if local_t.hour >= EVENING_START and local_t.hour < EVENING_END:
        return 'Evening'
    return 'Night'


def data_in_tw(dataframe, start, end):
    ''' Select data in a time window. time window = [start, end)
    Key arguments:
        df    -- Input pandas dataframe
        start -- The start datetime of time window.
        end   -- The end datetime of time window.

    Return values:
        Dataframe within the time window
    '''
    if dataframe is None:
        return None
    mask = (dataframe['Timestamp'] >= start) & (dataframe['Timestamp'] < end)
    return dataframe[mask]


def extract_features_from_tw1(streams, timestamp) -> Dict:
    feature = {}

    # Select features on time of the day
    tz = pytz.timezone("America/Los_Angeles")


    feature['Time of day'] = timestamp.astimezone(tz).hour

    # Select features from battery data
    bt_percent = streams['Battery']['Percentage']
    bt_temp = streams['Battery']['Temperature']

    if bt_percent.size > 0 and bt_percent.iloc[-1] > bt_percent.iloc[0]:
        feature['Battery Charging'] = 1
    elif bt_percent.size > 0 and bt_percent.iloc[-1] < bt_percent.iloc[0]:
        feature['Battery Charging'] = 0
    else:
        feature['Battery Charging'] = np.nan

    #feature['Mean Battery Temperature'] = bt_temp.mean()

    # Select features from ambient light data
    data = streams['Ambient Light']
    feature['Max Light Intensity'] = data['Light Intensity'].max()

    # Select features from proximity data
    #data = streams['Proximity']
    #feature['Mean Proximity'] = data['Proximity'].mean()

    # Select features from compass data
    data = streams['Compass'][['Bx', 'By', 'Bz']]
    compass_var = (np.sqrt(np.square(data).sum(axis=1))).var()
    feature['Magnetic Field Variance'] = compass_var

    # Select features from location data
    data = streams['Location']
    feature['Max GPS Accuracy'] = data['Accuracy'].min()
    feature['Max GPS Speed'] = data['Speed'].max()

    # Select features from activity type
    data = streams['Activity']
    feature['STILL'] = 0
    feature['ON_FOOT'] = 0
    feature['TILTING'] = 0
    feature['WALKING'] = 0
    feature['RUNNING'] = 0
    feature['ON_BICYCLE'] = 0
    feature['IN_VEHICLE'] = 0
    feature['UNKNOWN'] = 0
    if data.size == 0:
        feature['STILL'] = 1
    else:
        feature[ACTIVITY_TYPES[data['Type'].mode().iloc[0]]] = 1

    # Select features from ble beacons
    data = streams['Beacon']
    feature['Beacon'] = 0
    if data is not None and data.shape[0] > 0:
        feature['Beacon'] = 1

    return feature

def extract_features_from_tw(streams, timestamp) -> Dict:
    feature = {}

    # Select features on time of the day
    tz = pytz.timezone("America/Los_Angeles")

    feature['Morning'] = 0
    feature['Noon'] = 0
    feature['Afternoon'] = 0
    feature['Evening'] = 0
    feature['Night'] = 0
    feature[time_of_day(timestamp, tz)] = 1

    # Select features from battery data
    bt_percent = streams['Battery']['Percentage']
    bt_temp = streams['Battery']['Temperature']

    if bt_percent.size > 0 and bt_percent.iloc[-1] > bt_percent.iloc[0]:
        feature['Battery Charging'] = 1
    elif bt_percent.size > 0 and bt_percent.iloc[-1] < bt_percent.iloc[0]:
        feature['Battery Charging'] = 0
    else:
        feature['Battery Charging'] = np.nan

    #feature['Mean Battery Temperature'] = bt_temp.mean()

    # Select features from ambient light data
    data = streams['Ambient Light']
    feature['Mean Light Intensity'] = data['Light Intensity'].mean()

    # Select features from proximity data
    #data = streams['Proximity']
    #feature['Mean Proximity'] = data['Proximity'].mean()

    # Select features from compass data
    data = streams['Compass'][['Bx', 'By', 'Bz']]
    compass_var = (np.sqrt(np.square(data).sum(axis=1))).var()
    feature['Magnetic Field Variance'] = compass_var

    # Select features from location data
    data = streams['Location']
    feature['Max GPS Accuracy'] = data['Accuracy'].min()
    feature['Max GPS Speed'] = data['Speed'].max()

    # Select features from activity type
    data = streams['Activity']
    feature['STILL'] = 0
    feature['ON_FOOT'] = 0
    feature['TILTING'] = 0
    feature['WALKING'] = 0
    feature['RUNNING'] = 0
    feature['ON_BICYCLE'] = 0
    feature['IN_VEHICLE'] = 0
    feature['UNKNOWN'] = 0
    if data.size == 0:
        feature['STILL'] = 1
    else:
        feature[ACTIVITY_TYPES[data['Type'].mode().iloc[0]]] = 1

    # Select features from ble beacons
    data = streams['Beacon']
    feature['Beacon'] = 0
    if data is not None and data.shape[0] > 0:
        feature['Beacon'] = 1


    return feature

def extract_features(streams, start_t, end_t, t_win_s) -> List:
    t1 = start_t
    t2 = t1 + timedelta(seconds=t_win_s)

    features = []

    while t2 < end_t:
        # Extract data within time window
        data = {}
        data['Battery'] = data_in_tw(streams['Battery'], t1, t2)
        data['Location'] = data_in_tw(streams['Location'], t1, t2)
        data['Compass'] = data_in_tw(streams['Compass'], t1, t2)
        data['Activity'] = data_in_tw(streams['Activity'], t1, t2)
        data['Ambient Light'] = data_in_tw(streams['Ambient Light'], t1, t2)
        data['Beacon'] = data_in_tw(streams['Beacon'], t1, t2)

        feature = extract_features_from_tw1(data, t1)
        features.append(feature)

        t1 = t2
        t2 = t1 + timedelta(seconds=t_win_s)
    return features
