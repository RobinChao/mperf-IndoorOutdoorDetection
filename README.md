# mperf Indoor/Outdoor Detection

## Repository Structure
* bin/ - contains the executable files which helps extract data.
* clf/ - contains the pretrained classfier object.
* config/ - contains the configuration files.
* src/ - contains the development and testing code for IO Detection.

## Data streams used
1. Location (LOCATION--org.md2k.phonesensor--PHONE)
2. Activity Type (ACTIVITY_TYPE--org.md2k.phonesensor--PHONE)
3. Ambient Light (AMBIENT_LIGHT--org.md2k.phonesensor--PHONE)
4. Phone battery (BATTERY--org.md2k.phonesensor--PHONE)
5. Car Beacon (BEACON--org.md2k.beacon--BEACON--CAR)
6. Home Beacon (BEACON--org.md2k.beacon--BEACON--HOME)
7. Office Beacon (BEACON--org.md2k.beacon--BEACON--OFFICE)
8. Work 1 Beacon (BEACON--org.md2k.beacon--BEACON--WORK 1)
9. Work 2 Beacon (BEACON--org.md2k.beacon--BEACON--WORK 2)

## Important functions
src/feature_extraction.py:  
extract_features, extact_features_tw

src/SVM_training.ipynb:  
normalize, predict_labels
