from data_manipulation import *
import os

# thanks to https://www.nature.com/articles/s41597-023-01940-7 for the data


# open all files in the directory
files = os.listdir("shanghai_monitoring_dataset")
#order the files by number order
files.sort(key=lambda f: int(''.join(filter(str.isdigit, f))))
print(files)
patients_list = []
for file in files:
	if file != "Shanghai_T1DM_Summary.xlsx":
		patient = Patient_Data(file)
		patients_list.append(patient)

patients_summary = Patient_Summary("Shanghai_T1DM_Summary.xlsx")

print(patients_summary.data.head())

random_patient = patients_list[0]

print("We take patient number", random_patient.ID)

patient_data = random_patient.data

print(patient_data.head())