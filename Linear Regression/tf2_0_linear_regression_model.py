# -*- coding: utf-8 -*-
"""TF2.0 Linear Regression Model.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Y_skHjgiqGX4A6RFS8D-vEUTtMyV-goa
"""

# Import necessary packages
import numpy as np
import tensorflow as tf
tf.__version__

# Make a bigger dataset
X = np.arange(-100, 100, 4)
X

# Make labels for the dataset (adhering to the same pattern as before)
y = np.arange(-90, 110, 4)
y

# Split data into train and test sets
X_train = X[:40] # first 40 examples (80% of data)
y_train = y[:40]

X_test = X[40:] # last 10 examples (20% of data)
y_test = y[40:]

len(X_train), len(X_test)

"""## 1. Create first model"""

# Set random seed
tf.random.set_seed(42)

## Create a model
model = tf.keras.Sequential(
    [
        tf.keras.layers.Dense(1)
    ]

)

## Compile the model
model.compile(loss = tf.keras.losses.mae,
              optimizer = tf.keras.optimizers.SGD(),
              metrics = ['mae']
              )

## Fit the model
model.fit(tf.expand_dims(X_train, axis=-1), y_train, epochs=100)

"""Model Summary"""

model.summary()

from tensorflow.keras.utils import plot_model

plot_model(model, show_shapes=True)

# Make predictions
y_preds = model.predict(X_test)

# View the predictions
y_preds

def plot_predictions(train_data=X_train,
                     train_labels=y_train,
                     test_data=X_test,
                     test_labels=y_test,
                     predictions=y_preds):
  """
  Plots training data, test data and compares predictions.
  """
  import matplotlib.pyplot as plt
  plt.figure(figsize=(10, 7))
  # Plot training data in blue
  plt.scatter(train_data, train_labels, c="b", label="Training data")
  # Plot test data in green
  plt.scatter(test_data, test_labels, c="g", label="Testing data")
  # Plot the predictions in red (predictions were made on the test data)
  plt.scatter(test_data, predictions, c="r", label="Predictions")
  # Show the legend
  plt.legend();

plot_predictions(train_data=X_train,
                 train_labels=y_train,
                 test_data=X_test,
                 test_labels=y_test,
                 predictions=y_preds)

# Evaluate the model on the test set
model.evaluate(X_test, y_test)

# Check the tensor shapes
y_test.shape, y_preds.shape

# Calcuate the MAE
mae = tf.metrics.mean_absolute_error(y_true=y_test,
                                     y_pred=y_preds.squeeze()) # use squeeze() to make same shape
mae

# Calculate the MSE
mse = tf.metrics.mean_squared_error(y_true=y_test,
                                    y_pred=y_preds.squeeze())
mse

def mae(y_test, y_pred):
  """
  Calculuates mean absolute error between y_test and y_preds.
  """
  return tf.metrics.mean_absolute_error(y_test,
                                       tf.squeeze( y_pred))

def mse(y_test, y_pred):
  """
  Calculates mean squared error between y_test and y_preds.
  """
  return tf.metrics.mean_squared_error(y_test,
                                       tf.squeeze(y_pred))

"""## Running experiments to improve the results

1. model_1 - same as original model, 1 layer, trained for 100 epochs.
2. model_2 - 2 layers, trained for 100 epochs.
3. model_3 - 2 layers, trained for 500 epochs.

## 1. Build `model_1`
"""

# set random seed
tf.random.set_seed(42)

# Build the model
model_1 = tf.keras.Sequential([
    tf.keras.layers.Dense(1)
])

# Compile the model
model_1.compile(loss=tf.keras.losses.mae,
              optimizer=tf.keras.optimizers.SGD(),
              metrics = ['mae'])

# Fit the model
model_1.fit(tf.expand_dims(X_train, axis=-1), y_train, epochs=100)

# Make and plot the model predictions
y_preds_1 = model_1.predict(X_test)
plot_predictions(predictions=y_preds_1)

# Evaluate the model_1
mae_1 = mae(y_test, (y_preds_1))
mse_1 = mse(y_test, (y_preds_1))

mae_1, mse_1

"""## Build `model_2`

- 2 Dense Layers,
- Trained for 100 epochs
"""

# Set the random seed
tf.random.set_seed(42)

# build the model_2
model_2 = tf.keras.Sequential([
    tf.keras.layers.Dense(10),
    tf.keras.layers.Dense(1)
])

# Compile the model
model_2.compile(loss= tf.keras.losses.mae,
                optimizer= tf.keras.optimizers.SGD(),
                metrics= ['mae','mse'])

# Fit the model
model_2.fit(tf.expand_dims(X_train, axis=-1), y_train, epochs=100)

# Make and plot the predictions
y_preds_2 = model_2(X_test)
plot_predictions(predictions=y_preds_2)

# Calculate the mae and mse
mae_2 = mae(y_test, y_preds_2)
mse_2 = mse(y_test, y_preds_2)

mae_2, mse_2

# Evaluate the model
model_2.evaluate(X_test, y_test)

"""## Build `model_3`

- 2 Layers
- 500 Epochs
"""

# Set the random seed
tf.random.set_seed(42)

# build the model_3
model_3 = tf.keras.Sequential([
    tf.keras.layers.Dense(10),
    tf.keras.layers.Dense(1)
])

# Compile the model
model_3.compile(loss= tf.keras.losses.mae,
                optimizer= tf.keras.optimizers.SGD(),
                metrics= ['mae','mse'])

# Fit the model
model_3.fit(tf.expand_dims(X_train, axis=-1), y_train, epochs=500)

# Make and plot predictions
y_preds_3 = model_3.predict(X_test)
plot_predictions(predictions=y_preds_3)

mae_3 = mae(y_test, y_preds_3)
mse_3 = mse(y_test, y_preds_3)

mae_3, mse_3

model_3.evaluate(X_test, y_test)

"""### Comparing the results of experiments

"""

# Lets compare the results of our models using pandas
import pandas as pd

model_results = [["model_1", mae_1.numpy(), mse_1.numpy()],
                 ["model_2", mae_2.numpy(), mse_2.numpy()],
                 ["model_3", mae_3.numpy(), mse_3.numpy()]]

all_results = pd.DataFrame(model_results, columns=["Model", "MAE", "MSE"])
all_results

"""**Looks like model 2 performs better**"""

model_2.summary()

"""## Save Model"""

model_2.save("best_model")

# Save a model using the HDF5 format
model_2.save("best_model_HDF5_format.h5")

"""## Load Model"""

## Load he saved model
saved_model = tf.keras.models.load_model("/content/best_model")
saved_model.summary()

# Load a model from the HDF5 format
loaded_h5_model = tf.keras.models.load_model("best_model_HDF5_format.h5")
loaded_h5_model.summary()

# Compare model_2 with the loaded HDF5 version (should return True)
h5_model_preds = loaded_h5_model.predict(X_test)
h5_model_preds

model2_preds = model_2.predict(X_test)
load_model_preds = saved_model.predict(X_test)

#model2_preds == load_model_preds

model2_preds.squeeze()

load_model_preds.squeeze()

model2_preds.squeeze()  == load_model_preds.squeeze()