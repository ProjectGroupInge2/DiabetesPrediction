import numpy as np
import tensorflow as tf
from keras.models import Sequential
from keras.layers import LSTM, Dense, Normalization, InputLayer

class Glucose_Predictor:
	"""
	This class is used to predict the blood glucose level in next hour based on the previous 6 hours of data
	"""
	def __init__(self):
		# create a model to predict next CGM level based on the previous 6 hours of data
		model = Sequential()
		model.add(InputLayer(input_shape=(24, 3)))
		model.add(Normalization())
		model.add(LSTM(128, activation='relu', return_sequences=True))
		model.add(LSTM(128, activation='relu'))
		model.add(Dense(1))

		"""
		model = Sequential()
		model.add(InputLayer(input_shape=(24, 3)))
		model.add(Normalization())
		model.add(LSTM(64, return_sequences=True))
		model.add(Dense(8, activation='relu'))
		model.add(Dense(1)) # linear activation because we are predicting a continuous variable
		#TODO: why the output is not a single value ??
		"""
		
		model.compile(optimizer='adam', loss='mse')

		print(model.summary())

		self.model = model

	def train(self, patient):
		print("Training the model with patient: ", patient.ID)
		# train the model with the data from the patient
		input_sequence, output_sequence = patient.process_data()
		self.model.fit(np.array(input_sequence), np.array(output_sequence), epochs=10, batch_size=32)

	# TODO
	def predict(self, patient):
		print("Predicting the CGM from patient: ", patient.ID)
		print(patient.get_data().tail())
		# predict the blood glucose level based on the previous 6 hours of data
		input_sequence, output_sequence = patient.process_data()

		last_six_hours = input_sequence[-1]  # Use the last 6 hours of data
		last_six_hours = last_six_hours.reshape((1, 24, 3))  # reshape to fit the model
		# predict the next hour (4 next values)
		predictions = []
		for i in range(4):
			print("Predicting at time t+", i+1)
			prediction = self.model.predict(last_six_hours)
			predictions.append(prediction[0][0])
			print("Prediction: ", prediction)
			# update the input sequence with the new prediction
			# abberant value, TODO: fix this in the model
		
		return np.array(predictions).flatten()

	def save(self, name):
		self.model.save(name+'.h5')

	def load(self, name):
		self.model = tf.keras.models.load_model(name+'.h5')