from data_manipulation import *
from model import *
import os
import datetime

# thanks to https://www.nature.com/articles/s41597-023-01940-7 for the data

def predict_on(patient, time=4):
	save_name = patient.ID+"_model"
	model = Glucose_Predictor()
	if os.path.exists(save_name+".h5"):
		model.load(save_name)
	else:
		model.train(patient)
		model.save(save_name)
	return model.predict(patient, time)

def train_on_all(patients_list):
	if os.path.exists("all_patients_model.h5"):
		return None
	model = Glucose_Predictor()
	for patient in patients_list:
		model.train(patient)
	model.save("all_patients_model")

def predict_using_all(patient, time=4):
	model = Glucose_Predictor()
	model.load("all_patients_model")
	return model.predict(patient, time)


def save_prediction(predictions, patient):
	with open(patient.ID+"_predicted_data.txt", "w") as file:
		last_time = patient.data.index[-1]
		for i in range(len(predictions)):
			last_time += datetime.timedelta(minutes=15)
			file.write(last_time.strftime("%Y-%m-%d %H:%M:%S") + "\t" + str(predictions[i]) + "\n")

def main():
	# open all files in the directory
	files = os.listdir("shanghai_monitoring_dataset")
	#order the files by number order
	files.sort(key=lambda f: int(''.join(filter(str.isdigit, f))))
	patients_list = []
	for file in files:
		if file != "Shanghai_T1DM_Summary.xlsx":
			patient = Patient_Data(file)
			patients_list.append(patient)


	test_patient = patients_list.pop(1) # patient 3 is used for testing
	patients_summary = Patient_Summary("Shanghai_T1DM_Summary.xlsx")


	pred = predict_on(test_patient)
	save_prediction(pred, test_patient)

if __name__ == "__main__":
	main()