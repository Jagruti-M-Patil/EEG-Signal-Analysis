# Import necessary libraries
import os
import numpy as np
import pandas as pd
import tensorflow as tf

import Parameters
import modules.Load_EEG_Data as Load_EEG_Data
import modules.Seizure_Period as Seizure_Period

# Define the input shape
input_shape = (len(Parameters.EEG_Channels), Parameters.window_len)  # (number of channels, 

# Define the model architecture
model = tf.keras.Sequential(
    [
        tf.keras.layers.Conv1D(32, kernel_size=3, activation="relu", input_shape=input_shape),
        tf.keras.layers.MaxPooling1D(pool_size=2),
        tf.keras.layers.Flatten(),
        tf.keras.layers.Dense(64, activation="relu"),
        tf.keras.layers.Dense(1, activation="sigmoid"),
    ]
)

# Compile the model
model.compile(loss="binary_crossentropy", optimizer="adam", metrics=["accuracy"])

train_files_db_path = os.path.join(Parameters.save_path, 'edf-file-train.csv')
train_files_df = pd.read_csv(train_files_db_path)

# Train the model iteratively in batches
batch_size = 32
epochs = 1

for epoch in range(epochs):

	print("Epoch {}/{}".format(epoch + 1, epochs))

	for file_no, row in train_files_df.loc[train_files_df['Train']].iterrows() :

		edf_data = Load_EEG_Data.getEdfData(row['File Name'])

		signal_data = Load_EEG_Data.getSignalData(edf_data)

		labels = Load_EEG_Data.getSignalLabels(edf_data, row['File Name'])

		scalar_output = np.zeros_like(labels, dtype=float)
		scalar_output[labels == Seizure_Period.label.Preictal] = 1.

		train_indices, = np.nonzero(labels != Seizure_Period.label.Ictal)

		for step in range(train_indices.shape[0] // batch_size):

			batch_indices = train_indices[step * batch_size : (step + 1) * batch_size]

			batch_x = Load_EEG_Data.generateInputSignalBatch(signal_data, batch_indices)
			batch_y = scalar_output[batch_indices]

			loss, acc = model.train_on_batch(batch_x, batch_y)

# # Evaluate the model
# test_loss, test_acc = model.evaluate(x_test, y_test)
# print("Test accuracy:", test_acc)

# # Make predictions
# predictions = model.predict(x_test)
