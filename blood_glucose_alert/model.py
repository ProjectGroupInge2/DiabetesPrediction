import numpy as np
import tensorflow as tf
from keras.models import Sequential
from keras.layers import LSTM, Dense, InputLayer, Normalization

class Glucose_Predictor:
	"""
	This class is used to predict the blood glucose level in next hour based on the previous 6 hours of data
	"""
	def __init__(self):
		# create a model to predict next CGM level based on the previous 6 hours of data
		model = Sequential()
		model.add(InputLayer(input_shape=(24, 3)))
		model.add(Normalization())
		model.add(LSTM(64, activation='relu'))
		model.add(Dense(32, activation='relu'))
		model.add(Dense(3))
		
		model.compile(optimizer='adam', loss='mse')

		print(model.summary())

		self.model = model

	def train(self, patient):
		print("Training the model on patient ", patient.ID)
		# train the model with the data from the patient
		input_sequence, output_sequence = patient.process_data()
		self.model.fit(np.array(input_sequence), np.array(output_sequence), epochs=100, batch_size=1)

	# TODO
	def predict(self, patient, time):
		print("Predicting the CGM from patient: ", patient.ID)
		print(patient.get_data().tail())
		# predict the blood glucose level based on the previous 6 hours of data
		last_six_hours = patient.get_last_six_hours()
		# predict the next hour (4 next values)
		predictions = []
		for i in range(time):
			print("Predicting at time t+", 15*(i+1),"min")
			prediction = self.model.predict(last_six_hours)[0]
			# convert the prediction to a boolean value
			prediction[1] = prediction[1] > 0.5
			predictions.append(prediction)
			print("Prediction: ", prediction)
			# update the input sequence with the new prediction
			last_six_hours = np.delete(last_six_hours, 0, axis=1)
			# add prediction add the end of last_six_hours
			last_six_hours = np.append(last_six_hours, [[prediction]], axis=1)

		return np.array(predictions)

	def save(self, name):
		self.model.save(name+'.h5')

	def load(self, name):
		self.model = tf.keras.models.load_model(name+'.h5')