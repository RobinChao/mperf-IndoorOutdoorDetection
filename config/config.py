#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 21 01:11:40 2018

@author: zxxia
"""
import json

sensor_csv_column_names = {
        2:
        ['Timestamp', 'Unknown', 'Percentage', 'Voltage', 'Temperature'],
        3:
        ['Timestamp', 'Latitude', 'Logitude', 'Altitude',
         'Speed', 'Bearing', 'Accuracy'],
        4:
        ['Timestamp', 'Type', 'Confidence'],
        7:
        ['Timestamp', 'Unknown', 'Bx', 'By', 'Bz'],
        8:
        ['Timestamp', 'Unknown', 'Light Intensity'],
        10:
        ['Timestamp', 'Unknown', 'Proximity']
}

config = {
        'Sensor CSV Column Names': sensor_csv_column_names,
        'High Freq Data Dir': '/Users/zxxia/Research/zhengxuxia-data/raw',
        'Low Freq Data Dir': '/Users/zxxia/Research/zhengxuxia-data/lowfrequencydata',
        'Datasources': '/Users/zxxia/Research/zhengxuxia-data/datasources.csv',
        'Groundtruths': '/Users/zxxia/Research/zhengxuxia-data/IOLabel - Kevin Xia.csv'
}


with open('config.json', 'w') as f:
    f.write(json.dumps(config, indent=4))
