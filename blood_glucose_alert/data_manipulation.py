import pandas as pd
import os
from datetime import datetime
from datetime import timedelta
from datetime import date
import matplotlib.pyplot as plt
import matplotlib.dates as mdates


class Patient_Data:
	def __init__(self, file_name):
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

		self.data = df
		self.ID = file_name.split('.')[0]


	def show_meal_insuline_takes(self):
		# print the evolution of CGM on a day
		fig, ax = plt.subplots()
		ax.plot(self.data.index, self.data['CGM'], color='gray')

		# add red points for meals
		for i in range(len(self.data)):
			if self.data['Meal'][i]:
				ax.scatter(self.data.index[i], self.data['CGM'][i], color='red')

		# add green points when insulin is not nan
		for i in range(len(self.data)):
			if not pd.isnull(self.data['Insulin dose - s.c.'][i]):
				ax.scatter(self.data.index[i], self.data['CGM'][i], color='blue')

		# format the ticks
		ax.xaxis.set_major_locator(mdates.DayLocator(interval=1))
		ax.xaxis.set_major_formatter(mdates.DateFormatter('%d-%m-%Y'))
		fig.autofmt_xdate()

		plt.show()



class Patient_Summary:

	def __init__(self, file_name):
		self.data = pd.read_excel("shanghai_monitoring_dataset/Shanghai_T1DM_Summary.xlsx").set_index("Patient Number")