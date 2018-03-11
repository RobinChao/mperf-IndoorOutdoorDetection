#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 22 15:30:19 2018

@author: zxxia
"""

import matplotlib.pyplot as plt
import pandas as pd

df_battery = pd.read_csv('battery/20180131_2.csv',
                         header=None,
                         names=['Timestamp', 'Unknown', 'Percentage',
                                'Voltage', 'Temperature'])
df_battery['Timestamp'] = pd.to_datetime(df_battery['Timestamp'], unit='ms')

df_light_intensity = pd.read_csv('ambientlight/20180131_8.csv',
                                 header=None,
                                 names=['Timestamp', 'Unknown',
                                        'Light Intensity'])
df_light_intensity['Timestamp'] = pd.to_datetime(
        df_light_intensity['Timestamp'], unit='ms')

df_proximity = pd.read_csv('proximity/20180129_10.csv',
                           header=None,
                           names=['Timestamp', 'Unknown', 'Proximity'])
df_proximity['Timestamp'] = pd.to_datetime(df_proximity['Timestamp'],
                                           unit='ms')

f, ax_arr = plt.subplots(4, sharex=True)

ax_arr[0].plot_date(df_light_intensity['Timestamp'],
                    df_light_intensity['Light Intensity'],
                    tz='US/Pacific-New')
ax_arr[0].set_title('Light Intensity')
ax_arr[0].set_ylabel('lx')

ax_arr[1].plot_date(df_proximity['Timestamp'],
                    df_proximity['Proximity'],
                    tz='US/Pacific-New')
ax_arr[1].set_title('Proximity')
ax_arr[1].set_ylabel('cm')

ax_arr[2].plot_date(df_battery['Timestamp'],
                    df_battery['Percentage'],
                    tz='US/Pacific-New')
ax_arr[2].set_title('Battery Percentage')
ax_arr[2].set_ylabel('%')

ax_arr[3].plot_date(df_battery['Timestamp'], df_battery['Voltage'],
                    tz='US/Pacific-New')
ax_arr[3].set_title('Battery Voltage')
ax_arr[3].set_ylabel('mV')
