# Data Preparation

# Download data from kaggle (must have the json file from kaggle)
!kaggle datasets download -d suryadeepti/movie-lens-dataset

# Import Library
import os
import zipfile
import pandas as pd
import numpy as np
import nltk
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.feature_extraction.text import TfidfVectorizer
from collections import defaultdict

import tensorflow as tf
import keras
from keras.models import Model
from keras import layers
from tensorflow.keras.optimizers import Adam
from keras.layers import Add, Activation, Lambda, BatchNormalization, Concatenate, Dropout, Input, Embedding, Dot, Reshape, Dense, Flatten
from tensorflow.keras.callbacks import Callback, ModelCheckpoint, LearningRateScheduler, TensorBoard, EarlyStopping, ReduceLROnPlateau


# Extract Zip File 
zip_file = 'movie-lens-dataset.zip'
zip_file = zipfile.ZipFile(zip_file, 'r')
zip_file.extractall()
zip_file.close()

# Creating Data frames
data_movie = pd.read_csv(r'Data\movies.csv')
data_ratings = pd.read_csv(r'Data\ratings.csv')

# Exploring Data Movie
data_movie.head()
data_movie.info()
np.sum(data_movie.isnull())

# Exploring Data Ratings
data_ratings.head()
data_ratings.info()
np.sum(data_ratings.isnull())

# Data Preprocessing
## Merge Data
data = data_ratings.merge(data_movie, how='inner', on='movieId')

## Remove Missing Value
# Karena tidak relevant
data_ratings = data_ratings.drop(['timestamp'], axis=1)

## Normalize data
batas_bawah = min(data['rating'])
batas_atas = max(data['rating'])
data['rating'] = data['rating'].apply(lambda x : (x - batas_bawah) / (batas_atas - batas_bawah)).values.astype(np.float32)
avg_rating = np.mean(data['rating'])

userId = data['userId'].unique().tolist()
encoderUser = { x : i for i, x in enumerate(userId)}

encodertoUser = { i : x for i, x in enumerate(userId)}

data['user'] = data['userId'].map(encoderUser)
n_user = len(encoderUser)

movieId = data['movieId'].unique().tolist()

encoderMovie = { x: i for i, x in enumerate(movieId)}
encodertoMovie = { i : x for i, x in enumerate(movieId)}

data['movie'] = data['movieId'].map(encoderMovie)
n_movie = len(encoderMovie)

## Data Split
X = data[['user', 'movie']].values
y = data['rating']

# membagi data
test_size = int(2e5)
indices = data.shape[0] - test_size
X_train, X_test, y_train, y_test = (X[:indices], X[indices:], y[:indices], y[indices:])

X_train = [X_train[:, 0], X_train[:, 1]]
X_test = [X_test[:, 0], X_test[:, 1]]

## Modeling
def model_architecture():
    user = Input(name='user', shape=[1])
    user_embed = Embedding(name='user_embedding', input_dim= n_user, output_dim=128)(user)
    
    movie = Input(name='movie', shape=[1])
    movie_embed = Embedding(name = 'movie_embedding', input_dim=n_movie, output_dim=128)(movie)
    
    X = Dot(name = 'dot_product', normalize=True, axes=2)([user_embed, movie_embed])
    X = Flatten()(X)
    X = Dense(1, kernel_initializer='he_normal')(X)
    X = Activation('sigmoid')(X)
    
    model = Model(inputs = [user, movie], outputs = X)
    model.compile(loss= 'binary_crossentropy',
                  metrics = ['mse', tf.keras.metrics.Precision(), tf.keras.metrics.Recall()],
                  optimizer = 'Adam')
    return model

# Correcting the filepath to match the expected format
model_checkpoint = ModelCheckpoint(filepath='./weight.weights.h5',
                             save_weights_only=True,
                             monitor='val_loss',
                             mode='min',
                             save_best_only=True)

early_stopping = EarlyStopping(patience=1, 
                               monitor='mse', 
                               mode='min', 
                               restore_best_weights=True)

my_callbacks = [model_checkpoint, early_stopping]
model = model_architecture()
model.summary()
history = model.fit(x = X_train,
                    y = y_train,
                    validation_data = (X_test, y_test),
                    epochs = 30,
                    batch_size = 32,
                    verbose = 1,
                    callbacks = my_callbacks)

# Evaluation

## Loss Function
plt.title('Model Loss Performance')
plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.ylabel('loss')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper right')
plt.show()

## MSE
plt.title('Model MSE Performance')
plt.plot(history.history['mse'])
plt.plot(history.history['val_mse'])
plt.ylabel('loss')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper right')
plt.show()

## Precision
plt.title('Model Precision Performance')
plt.plot(history.history['precision'])
plt.plot(history.history['val_precision'])
plt.ylabel('loss')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper right')
plt.show()

## Recall
plt.title('Model Recall Performance')
plt.plot(history.history['recall'])
plt.plot(history.history['val_recall'])
plt.ylabel('loss')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper right')
plt.show()

## Load model
def weight_model(name, model):
    weight = model.get_layer(name).get_weights()[0]
    weight = weight / np.linalg.norm(weight, axis = 1).reshape((-1, 1))
    return weight

movie_weight = weight_model('movie_embedding', model)
user_weight = weight_model('user_embedding', model)


## Get Similar Users
def get_similar_users(tempId, n = 10):
      index = tempId
      weights = user_weight
      dists = np.dot(weights, weights[encoderUser.get(index)])
      sortedDists = np.argsort(dists)
      n += 1
      closest = sortedDists[-n:]
      print('User that similar to user #{}'.format(tempId))
      
      SimilarArr = []
      
      for close in closest:
          similarity = dists[closest]

          if isinstance(tempId, int):
              SimilarArr.append({"similar_users" : encodertoUser.get(close), "similarity" : similarity})

      Frame = pd.DataFrame(SimilarArr)
      return Frame
  
get_similar_users(393)['similar_users']

## Get Similar Movies Preference
def movie_preference(userId, plot = False, temp = 1):
  
  # menentukan batas rating terendah movie
  low_rating = np.percentile(data[data['userId'] == userId]['rating'], 75)
  data[data['userId'] == userId] = data[data['userId'] == userId][data[data['userId'] == userId]['rating'] >= low_rating]
  top_movie_refference = (data[data['userId'] == userId].sort_values(by = "rating", ascending = False)['movieId'].values)
  
  user_pref_df = data[data["movieId"].isin(top_movie_refference)]
  user_pref_df = user_pref_df[["movieId","title", "genres"]]
  
  if temp != 0:
      print("Berikut ini adalah list rekomendasi film dari user dengan id #{} yang telah mereview {} film dengan rata-rata ratingnya adalah = {:.1f}/5.0".format(
        userId, len(data[data['userId']==userId]),
        data[data['userId']==userId]['rating'].mean()*5,
      ))

  return user_pref_df
     
     
reff_user = movie_preference(393, plot = True)
reff_user = pd.DataFrame(reff_user)
reff_user.head(10)