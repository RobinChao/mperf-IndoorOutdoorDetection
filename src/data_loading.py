# -*- coding: utf-8 -*-
"""
Created on Thu Mar  8 16:30:32 2018

@author: aungkon
"""

import os
import json
import gzip
import zlib
import pandas as pd
import numpy as np
# this finds our json files

# input directory (the folder I told you to remember)
DATA_PATH = '/Users/zxxia/Research/field-data'

# output directory where the data will be saved
OUTPUT_PATH = '/Users/zxxia/Research/field-data-output'
participant_dir = list(os.listdir(DATA_PATH))


def list_all_frames(filenames, col_count):
    results = []
    for filename in filenames:
        try:
            dataframe = pd.read_csv(filename, compression='gzip',
                                    sep=',', quotechar='"',
                                    names=[str(i) for i in range(col_count)])
        except (EOFError, zlib.error):
            continue
        results.append(dataframe)
    return results



for participant in participant_dir:
    if participant.startswith('.'):
        continue
    path_to_date = DATA_PATH + '/' + str(participant)
    date_dir = list(os.listdir(path_to_date))

    if date_dir == []:
        continue
    for date in date_dir:
        if date.startswith('.'):
            continue
        os.makedirs(OUTPUT_PATH + str(participant) + '/' + str(date))

        list_activity_type = []
        list_ambient_light = []
        list_battery = []
        list_location = []
        list_beacon_home = []
        list_beacon_car = []
        list_beacon_office = []
        list_beacon_work1 = []
        list_beacon_work2 = []
        list_geofence_home = []
        list_geofence_office = []
        list_geofence_work1 = []
        list_geofence_work2 = []

        path_to_uid = path_to_date + '/' + str(date)

        for uid in os.listdir(path_to_uid):
            if uid.startswith('.'):
                continue
            path_to_json = path_to_uid + '/' + str(uid)
            file_list = os.listdir(path_to_json)
            json_list = list(filter(lambda x: str(x).endswith('.json'),
                                    file_list))
            json_path = path_to_json + '/' + str(json_list[0])

            gz_list = list(filter(lambda x: str(x).endswith('.gz'), file_list))
            gz_list = [path_to_json + '/' + x for x in gz_list]
            try:
                data = json.load(open(json_path, 'r'))
                if data['name'] == 'ACTIVITY_TYPE--org.md2k.phonesensor--PHONE':
                    list_activity_type += gz_list
                if data['name'] == 'AMBIENT_LIGHT--org.md2k.phonesensor--PHONE':
                    list_ambient_light += gz_list
                if data['name'] == 'BATTERY--org.md2k.phonesensor--PHONE':
                    list_battery += gz_list
                if data['name'] == 'LOCATION--org.md2k.phonesensor--PHONE':
                    list_location += gz_list
                if data['name'] == 'BEACON--org.md2k.beacon--BEACON--CAR':
                    list_beacon_car += gz_list
                if data['name'] == 'BEACON--org.md2k.beacon--BEACON--HOME':
                    list_beacon_home += gz_list
                if data['name'] == 'BEACON--org.md2k.beacon--BEACON--OFFICE':
                    list_beacon_office += gz_list
                if data['name'] == 'BEACON--org.md2k.beacon--BEACON--WORK1':
                    list_beacon_work1 += gz_list
                if data['name'] == 'BEACON--org.md2k.beacon--BEACON--WORK2':
                    list_beacon_work2 += gz_list

                if data['name'] == 'GEOFENCE--Home--org.md2k.phonesensor--PHONE':
                    list_geofence_home += gz_list
                if data['name'] == 'GEOFENCE--work satellite office --org.md2k.phonesensor--PHONE':
                    list_geofence_office += gz_list
                if data['name'] == 'GEOFENCE--Work--org.md2k.phonesensor--PHONE':
                    list_geofence_work1 += gz_list
                if data['name'] == 'GEOFENCE--work2--org.md2k.phonesensor--PHONE':
                    list_geofence_work2 += gz_list
            except:
                print('Error occured')
        print(date, 'act type', len(list_activity_type))
        print(date, 'light', len(list_ambient_light))
        print(date, 'bat', len(list_battery))
        print(date, 'loc', len(list_location))
        print(date, 'beacon home', len(list_beacon_home))
        print(date, 'beacon car', len(list_beacon_car))
        print(date, 'beacon office', len(list_beacon_office))
        print(date, 'beacon work1', len(list_beacon_work1))
        print(date, 'beacon work2', len(list_beacon_work2))
        print(date, 'geofence home', len(list_geofence_home))
        print(date, 'geofence office', len(list_geofence_office))
        print(date, 'geofence work1', len(list_geofence_work1))
        print(date, 'geofence work2', len(list_geofence_work2))

        frames_activity_type = list_all_frames(list_activity_type, 4)
        frames_ambient_light = list_all_frames(list_ambient_light, 3)
        frames_battery = list_all_frames(list_battery, 5)
        frames_location = list_all_frames(list_location, 7)

        if frames_activity_type:
            df_activity_type = pd.concat(frames_activity_type).sort_values(by=['0'])
            np.savetxt(OUTPUT_PATH + str(participant) + '/' + str(date) + '/activity_type.csv',
                       df_activity_type.as_matrix(), delimiter=',', fmt='%13d')
            print(participant, date, 'activity_type')
        if frames_ambient_light:
            df_ambient_light = pd.concat(frames_ambient_light).sort_values(by=['0'])
            np.savetxt(OUTPUT_PATH + str(participant) + '/' + str(date) + '/ambient_light.csv',
                       df_ambient_light.as_matrix(), delimiter=',', fmt='%13d')
            print(participant, date, 'ambient light')
        if frames_battery:
            df_battery = pd.concat(frames_battery).sort_values(by=['0'])
            try:
                np.savetxt(OUTPUT_PATH + str(participant) + '/' + str(date) + '/battery.csv',
                           df_battery.as_matrix(), delimiter=',', fmt='%13d')
            except ValueError:
                print(df_battery)
            print(participant, date, 'battery')
        if frames_location:
            df_location = pd.concat(frames_location).sort_values(by=['0'])
            np.savetxt(OUTPUT_PATH + str(participant) + '/' + str(date) + '/location.csv',
                       df_location.as_matrix(), delimiter=',', fmt='%.15f')
            print(participant, date, 'location')
