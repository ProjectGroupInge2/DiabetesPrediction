from data_manipulation import *
from model import *
import os
import datetime

# thanks to https://www.nature.com/articles/s41597-023-01940-7 for the data

def predict_on(patient, save_name, time=4):
	model = Glucose_Predictor()
	if os.path.exists(save_name+".h5"):
		model.load(save_name)
	else:
		model.train(patient)
		model.save(save_name)
	return model.predict(patient, time)

# open all files in the directory
files = os.listdir("shanghai_monitoring_dataset")
#order the files by number order
files.sort(key=lambda f: int(''.join(filter(str.isdigit, f))))
patients_list = []
for file in files:
	if file != "Shanghai_T1DM_Summary.xlsx":
		patient = Patient_Data(file)
		patients_list.append(patient)


test_patient = patients_list.pop(2)
patients_summary = Patient_Summary("Shanghai_T1DM_Summary.xlsx")

predicted_data = predict_on(test_patient, test_patient.ID+"_model", 30)
# save predicted data in a file
with open(test_patient.ID+"_predicted_data.txt", "w") as file:
	last_time = test_patient.data.index[-1]
	for i in range(len(predicted_data)):
		last_time += datetime.timedelta(minutes=15)
		file.write(last_time.strftime("%Y-%m-%d %H:%M:%S") + "\t" + str(predicted_data[i]) + "\n")


