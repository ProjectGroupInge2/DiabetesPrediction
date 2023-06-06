import pandas as pd
import numpy as np
import re
import matplotlib.pyplot as plt
import matplotlib.dates as mdates


class Patient_Data:
	def __init__(self, file_name):
		# Set the working directory
		file_path = "shanghai_monitoring_dataset/" + file_name
		print("Opened file: " + file_name)		
		# TODO : value in all row for merged cells
		df = pd.read_excel(file_path)
		df["CSII - basal insulin (Novolin R, IU / H)"].fillna(method='ffill', inplace=True)
		
		# Drop the columns that are not needed
		df.drop(['饮食', 'Blood Ketone (mmol / L)', 'Non-insulin hypoglycemic agents', 'CBG (mg / dl)'], axis=1, inplace=True)

		# Convert the date column to datetime format
		df['Date'] = pd.to_datetime(df['Date'])

		# Set the date column as the index
		df.set_index('Date', inplace=True)

		# Replace Dietary intake with True if data is present and False if not
		df['Dietary intake'] = df['Dietary intake'].notnull()

		#rename columns for easier access
		df.rename(columns={'Dietary intake': 'Meal'}, inplace=True)
		df.rename(columns={'CGM (mg / dl)': 'CGM'}, inplace=True)

		# replace nan values with 0 for the insulin columns
		df['Insulin dose - s.c.'].fillna(0, inplace=True)
		df['Insulin dose - i.v.'].fillna(0, inplace=True)
		df['CSII - bolus insulin (Novolin R, IU)'].fillna(0, inplace=True)
		df['CSII - basal insulin (Novolin R, IU / H)'].fillna(0, inplace=True)

		df['Insulin dose - s.c.'] = self._convert_to_float(df['Insulin dose - s.c.'])
		df['Insulin dose - i.v.'] = self._convert_to_float(df['Insulin dose - i.v.'])
		df['CSII - bolus insulin (Novolin R, IU)'] = self._convert_to_float(df['CSII - bolus insulin (Novolin R, IU)'])
		df['CSII - basal insulin (Novolin R, IU / H)'] = self._convert_to_float(df['CSII - basal insulin (Novolin R, IU / H)'])

		# sumarize all insuline takes into one column, and drop the other columns
		df['Insulin'] = df['Insulin dose - s.c.']
		df['Insulin'] += df['Insulin dose - i.v.']
		df['Insulin'] += df['CSII - bolus insulin (Novolin R, IU)']
		df['Insulin'] += df['CSII - basal insulin (Novolin R, IU / H)']
		
		df.drop(['Insulin dose - s.c.', 'Insulin dose - i.v.', 'CSII - bolus insulin (Novolin R, IU)', 'CSII - basal insulin (Novolin R, IU / H)'], axis=1, inplace=True)

		self.data = df
		self.ID = file_name.split('.')[0]


	def show_CGM(self):
		# plot the CGM
		fig, ax = plt.subplots(figsize=(15, 5))
		ax.plot(self.data.index, self.data['CGM'], color='red')
		ax.set(xlabel="Date", ylabel="CGM", title="CGM graph for patient " + self.ID)
		ax.xaxis.set_major_locator(mdates.DayLocator(interval=1))
		ax.xaxis.set_major_formatter(mdates.DateFormatter('%d-%m-%Y'))
		plt.show()


	def _convert_to_float(self, column):
		# convert every element of a column to float with special case for every type of value
		converted_column = []
		
		for value in column:
			if value == ' ':
				converted_column.append(0)
			elif isinstance(value, str):
				numbers = re.findall(r'\d+', value)
				converted_column.append(float(numbers[0]) if numbers else 0)
			elif isinstance(value, float):
				converted_column.append(float(value))
			else:
				converted_column.append(value)
		return converted_column


	def get_patients_info(self, patient_summary):
		return patient_summary.data.loc[self.ID]
	

	def get_data(self, to_numpy=False):
		if to_numpy:
			return self.data.to_numpy()
		return self.data
	
	def process_data(self):
		# Preprocess the data
		data = self.data.to_numpy()
		cgm_levels = data[:, 0].astype(float)
		meal_intake = data[:, 1].astype(bool)
		insulin = data[:, 2].astype(float)

		# Prepare the input and output sequences
		input_sequence = []
		output_sequence = []
		sequence_length = 24  # 6 hours (24 * 15 minutes)

		for i in range(len(self.data) - sequence_length):
			input_sequence.append(np.column_stack((
				cgm_levels[i:i+sequence_length],
				meal_intake[i:i+sequence_length],
				insulin[i:i+sequence_length]
			)))
			# edited output to include the 3 values
			output_sequence.append(np.column_stack((
				cgm_levels[i+sequence_length],
				meal_intake[i+sequence_length],
				insulin[i+sequence_length]
			)))

		# Convert the input and output sequences to numpy arrays
		input_sequence = np.array(input_sequence)
		output_sequence = np.array(output_sequence)

		return input_sequence, output_sequence
	
	def get_last_six_hours(self):
		# get the last six hours of data
		data = self.data.to_numpy()
		cgm_levels = data[:, 0].astype(float)
		meal_intake = data[:, 1].astype(bool)
		insulin = data[:, 2].astype(float)

		# Prepare the input and output sequences
		input_sequence = []
		output_sequence = []
		sequence_length = 24

		input_sequence.append(np.column_stack((
			cgm_levels[-sequence_length:],
			meal_intake[-sequence_length:],
			insulin[-sequence_length:]
		)))

		return np.array(input_sequence)


	def get_possible_entries(self, entrie_name):
		# return all possible entries for a given entrie_name removing np.nan
		column_list = self.data[entrie_name].to_list()
		column_list = [x for x in column_list if pd.isnull(x) == False]
		column_list = list(set(column_list))
		column_list.sort()
		return column_list
	

	



class Patient_Summary:

	def __init__(self, file_name):
		self.data = pd.read_excel("shanghai_monitoring_dataset/Shanghai_T1DM_Summary.xlsx").set_index("Patient Number")
		self.data.rename(columns={"Alcohol Drinking History (drinker/non-drinker)": "Alcohol Drinking History"}, inplace=True)
		# replace non-drinker by False and drinker by True
		self.data["Alcohol Drinking History"].replace({"drinker" : True, "non-drinker": False})

	def get_possible_entries(self, entrie_name):
		column_list = self.data[entrie_name].to_list()
		column_list_splited = []
		for element in column_list:
			if "," in element:
				splited_elements = element.split(",")
				# strip all elements in splited_elements
				splited_elements = [x.strip() for x in splited_elements]
				column_list_splited += splited_elements
		column_list_splited = list(set(column_list_splited))
		column_list_splited.sort()
		return column_list_splited