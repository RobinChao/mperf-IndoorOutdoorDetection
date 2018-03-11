#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb  5 11:16:30 2018

@author: zxxia
"""
import data_loader
from datetime import datetime, timedelta
from feature_extraction import extract_features, data_in_tw
import pandas as pd
import pytz

from sklearn import svm
from sklearn.feature_extraction import DictVectorizer
from sklearn.preprocessing import LabelEncoder, MinMaxScaler
from sklearn.model_selection import KFold
from sklearn.metrics import confusion_matrix





START_TIMES = ['01/31/2018 0:06', '01/31/2018 10:42', '01/31/2018 10:55',
               '01/31/2018 15:52', '01/31/2018 16:03', '01/31/2018 16:27',
               '01/31/2018 16:47', '01/31/2018 21:07', '01/31/2018 22:14']
END_TIMES = ['01/31/2018 10:42', '01/31/2018 10:55', '01/31/2018 15:52',
             '01/31/2018 16:03', '01/31/2018 16:27', '01/31/2018 16:47',
             '01/31/2018 21:07', '01/31/2018 22:14', '01/31/2018 23:59']
LABELS = ['InDoor', 'OutDoor', 'InDoor', 'OutDoor', 'InDoor',
          'InCar', 'InDoor', 'OutDoor', 'InDoor']

# Size of time window in unit of second.
TIME_WINDOW_SEC = 30


# -------------------------------Load Data from File--------------------------
dsid_type_dict, type_dsid_dict = data_loader.load_datasources()

# Load Groudtruth
tz = pytz.timezone("America/Los_Angeles")
df_labels = data_loader.load_groundtruth(tz)


# Load low frequency data
df_location = data_loader.load_low_freq_data(type_dsid_dict['LOCATION'])
df_activity = data_loader.load_low_freq_data(type_dsid_dict['ACTIVITY_TYPE'])

# %%
visited = set()
features = []
labels = []
for index, row in df_labels.iterrows():
    d = row['Start Timestamp'].date()
    if d not in visited:
        # load high frequency data
        df_battery = data_loader.load_high_freq_data(type_dsid_dict['BATTERY'],
                                                     d)
        df_compass = data_loader.load_high_freq_data(type_dsid_dict['COMPASS'],
                                                     d)
        visited.add(d)

    start = row['Start Timestamp'] + timedelta(seconds=120)
    end = row['End Timestamp'] - timedelta(seconds=120)

    if start >= end:
        continue

    streams = {}
    streams['Battery'] = data_in_tw(df_battery, start, end)
    # streams['Ambient Light'] = data_in_tw(df_light_intensity, start, end)
    # streams['Proximity'] = data_in_tw(df_proximity, start, end)

    streams['Compass'] = data_in_tw(df_compass, start, end)
    streams['Activity'] = data_in_tw(df_activity, start, end)

    streams['Location'] = data_in_tw(df_location, start, end)
    # extract feature and append features
    # extract labels and append labels
    tmp = extract_features(streams, start, end, TIME_WINDOW_SEC)
    features = features + tmp
    labels = labels + [row['Labels']] * len(tmp)


# %% --------------------------------Preprocess------------------------------ #




'''
i = 0

# Parse data based on time segment.
# tz = pytz.timezone("America/Los_Angeles")
 for start, end in zip(START_TIMES, END_TIMES):
    start = tz.localize(datetime.strptime(start, '%m/%d/%Y %H:%M')) + timedelta(seconds=120)
    end = tz.localize(datetime.strptime(end, '%m/%d/%Y %H:%M')) - timedelta(seconds=120)

    if start >= end:
        continue

    streams = {}
    streams['Battery'] = data_in_tw(df_battery, start, end)
    streams['Ambient Light'] = data_in_tw(df_light_intensity, start, end)
    streams['Proximity'] = data_in_tw(df_proximity, start, end)

    streams['Compass'] = data_in_tw(df_compass, start, end)
    streams['Activity'] = data_in_tw(df_activity, start, end)

    streams['Location'] = data_in_tw(df_location, start, end)

    tmp = extract_features(streams, start, end, TIME_WINDOW_SEC)

    labels = labels + [LABELS[i]] * len(tmp)

    features = features + tmp

    i = i + 1
'''



# %%---------------------------Training------------------------------- #
train_features = pd.DataFrame(features)
train_features['Labels'] = pd.DataFrame(labels)

train_features['Battery Charging'].interpolate(method='nearest', inplace=True)
train_features['Max GPS Accuracy'].fillna(500, inplace=True)
train_features = train_features.dropna(axis=0)
train_labels = train_features['Labels']
train_features.drop('Labels', axis=1, inplace=True)

train_features = train_features.to_dict('records')
vec = DictVectorizer()

train_features = vec.fit_transform(train_features).toarray()
scaler = MinMaxScaler(copy=False)
train_features = scaler.fit_transform(train_features)

le = LabelEncoder()
le.fit(['Indoor', 'Outdoor', 'Incar'])
train_labels = le.transform(train_labels)


from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, f1_score
X_train, X_test, y_train, y_test = train_test_split(train_features, train_labels, test_size=0.20, random_state=42)
clf = svm.SVC()
clf.fit(X_train, y_train)
predicted_y = clf.predict(X_test)
confusionmatrix = confusion_matrix(y_test, predicted_y)
print(confusionmatrix)
print(accuracy_score(y_test, predicted_y, normalize=True))
print(f1_score(y_test, predicted_y, average='micro'))
print(f1_score(y_test, predicted_y, average='macro'))
print(f1_score(y_test, predicted_y, average='weighted'))
'''
kf = KFold(n_splits=10, shuffle=True, random_state=42)

clf = svm.SVC()

for train_index, test_index in kf.split(train_features):

    X_train, X_test = train_features[train_index], train_features[test_index]
    y_train, y_test = train_labels[train_index], train_labels[test_index]
    clf.fit(X_train, y_train)
    predicted_y = clf.predict(X_test)

    confusionmatrix = confusion_matrix(y_test, predicted_y)
    print(confusionmatrix)
'''