# -*- coding: utf-8 -*-
"""TF2.0 Linear Regression Medical Cost.ipynb

Automatically generated by Colaboratory.

"""

# Import required libraries
import tensorflow as tf
import pandas as pd
import matplotlib.pyplot as plt

# Read in the insurance dataset
insurance = pd.read_csv("https://raw.githubusercontent.com/stedy/Machine-Learning-with-R-datasets/master/insurance.csv")

insurance.head()

# Lets one hot encode the dataframe so its in numbers
insurance_one_hot = pd.get_dummies(insurance)
insurance_one_hot.head()

# Create X and y Values
X = insurance_one_hot.drop("charges", axis=1)
y = insurance_one_hot["charges"]

X.head()

y.head()

# Create training and testing sets
from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
X_train.shape, X_test.shape

# build the model architecture

# set the random seed
tf.random.set_seed(42)

# Build the model
insurance_model = tf.keras.Sequential([
    tf.keras.layers.Dense(10),
    tf.keras.layers.Dense(1)
])

# Compile the model
insurance_model.compile(loss = tf.keras.losses.mae,
                        optimizer = tf.keras.optimizers.SGD(),
                        metrics = ['mae'])

# Fit the model
insurance_model.fit(X_train, y_train, epochs=100)

# Check the results on test data
insurance_model.evaluate(X_test, y_test)

# build the model architecture

# set the random seed
tf.random.set_seed(42)

# Build the model
insurance_model_2 = tf.keras.Sequential([
    tf.keras.layers.Dense(100),
    tf.keras.layers.Dense(10),
    tf.keras.layers.Dense(1)
])

# Compile the model
insurance_model_2.compile(loss = tf.keras.losses.mae,
                        optimizer = tf.keras.optimizers.Adam(),
                        metrics = ['mae'])

# Fit the model
insurance_model_2.fit(X_train, y_train, epochs=100)

# Evaluate the model
insurance_model_2.evaluate(X_test, y_test)

## Build the third model
# set the ranodm seed
tf.random.set_seed(42)

# Build the architectire
insurance_model_3 = tf.keras.Sequential([
    tf.keras.layers.Dense(128),
    tf.keras.layers.Dense(64),
    tf.keras.layers.Dense(32),
    tf.keras.layers.Dense(1)
])

# Compile the model
insurance_model_3.compile(loss = tf.keras.losses.mae,
                          optimizer = tf.keras.optimizers.Adam(),
                          metrics = ['mae'])

# Fit the model
history = insurance_model_3.fit(X_train, y_train, epochs = 200)

# Evaluate the model
insurance_model_3.evaluate(X_test, y_test)

# Plot the history
pd.DataFrame(history.history).plot()
plt.xlabel("Loss")
plt.ylabel("Epochs")

"""## Preprocessing Data - Normalization and standardization"""

from sklearn.preprocessing import MinMaxScaler, StandardScaler, OneHotEncoder
from sklearn.compose import make_column_transformer

# make a column transformer
ct = make_column_transformer(
    (MinMaxScaler(), ["age", "bmi", "children"]),
    (OneHotEncoder(handle_unknown="ignore"), ["sex", "smoker", "region"] )
)


## Read in the insurance dataset
insurance = pd.read_csv("https://raw.githubusercontent.com/stedy/Machine-Learning-with-R-datasets/master/insurance.csv")

X = insurance.drop("charges", axis = 1)
y = insurance["charges"]

# Build the train and test data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Fit the column transformer on training data
# Fist fit on the training data and then transform the testing data
ct.fit(X_train)

# Transform the training and testing data with normalization and OneHotEncoding
X_train_normal = ct.transform(X_train)
X_test_normal = ct.transform(X_test)

X_train_normal[0]

## Build the new model

# Set the random seed
tf.random.set_seed(42)

# Create the architecture
insurance_model_4 = tf.keras.Sequential([
    #tf.keras.layers.Dense(64),
    tf.keras.layers.Dense(64),
    tf.keras.layers.Dense(32),
    tf.keras.layers.Dense(1)
])

# Compile the model
insurance_model_4.compile(loss = tf.keras.losses.mae,
                          optimizer = tf.keras.optimizers.SGD(),
                          metrics = ['mae'])

# Fit the model
insurance_model_4.fit(X_train_normal, y_train, epochs=200)

# Evaluate the model
insurance_model_4.evaluate(X_test_normal, y_test)