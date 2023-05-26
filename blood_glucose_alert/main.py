from data_manipulation import *
from model import *
import os

# thanks to https://www.nature.com/articles/s41597-023-01940-7 for the data


# open all files in the directory
files = os.listdir("shanghai_monitoring_dataset")
#order the files by number order
files.sort(key=lambda f: int(''.join(filter(str.isdigit, f))))
patients_list = []
for file in files:
	if file != "Shanghai_T1DM_Summary.xlsx":
		patient = Patient_Data(file)
		patients_list.append(patient)


test_patient = patients_list.pop(0)
patients_summary = Patient_Summary("Shanghai_T1DM_Summary.xlsx")

model = Glucose_Predictor()

# train the model
SAVE_NAME = "model_solo"

if os.path.exists(SAVE_NAME+".h5"):
	model.load(SAVE_NAME)
else:
	model.train(patients_list[0])
	model.save(SAVE_NAME)


# PREDICT data
predictions_test = model.predict(test_patient)


print(predictions_test)

"""for i, prediction in enumerate(predictions_test):
    print(f"Prediction at t+{15 * (i+1)} minutes: {prediction:.2f}")"""