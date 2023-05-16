import pandas as pd
import os
from datetime import datetime
from datetime import timedelta
from datetime import date
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# thanks to https://www.nature.com/articles/s41597-023-01940-7 for the data


def open_file(file_name):
	# Set the working directory
	file_path = "shanghai_monitoring_dataset/" + file_name
	print("Opened file: " + file_name)
	df = pd.read_excel(file_path)
	
	# Drop the columns that are not needed
	df.drop(['饮食', 'Blood Ketone (mmol / L)', 'Non-insulin hypoglycemic agents'], axis=1, inplace=True)

	# Convert the date column to datetime format
	df['Date'] = pd.to_datetime(df['Date'])

	# Set the date column as the index
	df.set_index('Date', inplace=True)

	# Replace Dietary intake with True if data is present and False if not
	df['Dietary intake'] = df['Dietary intake'].notnull()

	#rename columns for easier access
	df.rename(columns={'Dietary intake': 'Meal'}, inplace=True)
	df.rename(columns={'CGM (mg / dl)': 'CGM'}, inplace=True)
	df.rename(columns={'CBG (mg / dl)': 'CBG'}, inplace=True)

	return df

def show_meal_insuline(df):
	# print the evolution of CGM on a day
	fig, ax = plt.subplots()
	ax.plot(df.index, df['CGM'], color='gray')

	# add red points for meals
	for i in range(len(df)):
		if df['Meal'][i]:
			ax.scatter(df.index[i], df['CGM'][i], color='red')

	# add green points when insulin is not nan
	for i in range(len(df)):
		if not pd.isnull(df['Insulin dose - s.c.'][i]):
			ax.scatter(df.index[i], df['CGM'][i], color='blue')

	# format the ticks
	ax.xaxis.set_major_locator(mdates.DayLocator(interval=1))
	ax.xaxis.set_major_formatter(mdates.DateFormatter('%d-%m-%Y'))
	fig.autofmt_xdate()

	plt.show()


# open all files in the directory
files = os.listdir("shanghai_monitoring_dataset")
#order the files by number order
files.sort(key=lambda f: int(''.join(filter(str.isdigit, f))))
print(files)
data_of_patient = []
for file in files:
	data_of_patient.append(open_file(file))

print("Select of file "+files[1])
patient_test = data_of_patient[1]

print(patient_test.info())

show_meal_insuline(patient_test)