# -*- coding: utf-8 -*-
"""FEATURE_EXTRACTION.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/github/nuradilahf/feature-extraction-revision/blob/main/FEATURE_EXTRACTION.ipynb
"""

!git clone https://github.com/nuradilahf/feature-extraction-revision

import pandas as pd

df_clean = pd.read_csv('/content/feature-extraction-revision/clean.csv')

df_clean.head()

df_clean.shape

df_clean.Sentiment.value_counts()

print(df_clean.isnull().sum())

print(df_clean.isnull().any().any())

df_cleaned = df_clean.dropna()

print (df_cleaned)

df_cleaned.isnull().sum()

import nltk

nltk.download('punkt_tab')

from nltk.tokenize import sent_tokenize

text = "warung ini dimiliki oleh pengusaha pabrik tahu yang sudah puluhan tahun terkenal membuat tahu putih di bandung tahu berkualitas dipadu keahlian memasak dipadu kretivitas jadilah warung yang menyajikan menu utama berbahan tahu ditambah menu umum lain sepe i ayam semuanya selera indonesia harga cukup terjangkau jangan melewati tahu bletoka nya tidak kalah dengan yang asli dari tegal"
text = sent_tokenize(text)
text

from nltk.tokenize import word_tokenize

text = "warung ini dimiliki oleh pengusaha pabrik tahu yang sudah puluhan tahun terkenal membuat tahu putih di bandung tahu berkualitas dipadu keahlian memasak dipadu kretivitas jadilah warung yang menyajikan menu utama berbahan tahu ditambah menu umum lain sepe i ayam semuanya selera indonesia harga cukup terjangkau jangan melewati tahu bletoka nya tidak kalah dengan yang asli dari tegal"
text = word_tokenize(text)
text

import re

text = "warung ini dimiliki oleh pengusaha pabrik tahu yang sudah puluhan tahun terkenal membuat tahu putih di bandung tahu berkualitas dipadu keahlian memasak dipadu kretivitas jadilah warung yang menyajikan menu utama berbahan tahu ditambah menu umum lain sepe i ayam semuanya selera indonesia harga cukup terjangkau jangan melewati tahu bletoka nya tidak kalah dengan yang asli dari tegal"
text = re.sub(r'[^\w\s]', '', text)
text

text = "warung ini dimiliki oleh pengusaha pabrik tahu yang sudah puluhan tahun terkenal membuat tahu putih di bandung tahu berkualitas dipadu keahlian memasak dipadu kretivitas jadilah warung yang menyajikan menu utama berbahan tahu ditambah menu umum lain sepe i ayam semuanya selera indonesia harga cukup terjangkau jangan melewati tahu bletoka nya tidak kalah dengan yang asli dari tegal"
text = re.sub(r'\d+', '', text)
text

stopwords = ["ini", "oleh", "yang", "sudah", "di", "cukup", "jadilah", "dari", "nya"]
text = "warung ini dimiliki oleh pengusaha pabrik tahu yang sudah puluhan tahun terkenal membuat tahu putih di bandung tahu berkualitas dipadu keahlian memasak dipadu kretivitas jadilah warung yang menyajikan menu utama berbahan tahu ditambah menu umum lain sepe i ayam semuanya selera indonesia harga cukup terjangkau jangan melewati tahu bletoka nya tidak kalah dengan yang asli dari tegal"

words = text.split(' ')
for word in words:
  if word not in stopwords:
    print(word)

empty_rows = df_cleaned['Sentiment'].str.strip().eq('')
print (empty_rows)
print ({empty_rows.sum()})

data_preprocessed = df_cleaned.Text_Bersih.tolist()

data_preprocessed

data_preprocessed_series = pd.Series(data_preprocessed)

null_count = data_preprocessed_series.isnull().sum()

print(null_count)

import numpy as np

data_preprocessed = [x for x in data_preprocessed if x is not np.nan and x is not None and (isinstance(x, str) or isinstance(x, bytes) or (isinstance(x, float) and not pd.isna(x)))]

data_preprocessed_series = pd.Series(data_preprocessed)
null_count = data_preprocessed_series.isnull().sum()
print(null_count)

from sklearn.feature_extraction.text import CountVectorizer

count_vect = CountVectorizer()
count_vect.fit(data_preprocessed)

count_vect.vocabulary_

from sklearn.model_selection import train_test_split
classes = df_cleaned.Sentiment
classes

classes.shape[0]

num_nan = classes.isnull().sum()
print( num_nan)

X = count_vect.transform(data_preprocessed)

X.shape

print ("Feature Extraction selesai")

import pickle
with open("feature.p", "wb") as file:
  pickle.dump(count_vect, file)

X_train, X_test, y_train, y_test = train_test_split(X, classes, test_size=0.2)

# Create DataFrames for train and test data
train_data = pd.DataFrame(X_train.toarray(), index=y_train.index)
train_data['Sentiment'] = y_train

test_data = pd.DataFrame(X_test.toarray(), index=y_test.index)
test_data['Sentiment'] = y_test

print("X_train shape:", X_train.shape)
print("y_train shape:", y_train.shape)
print("train_data shape:", train_data.shape)

y_train = y_train.reset_index(drop=True)
y_test = y_test.reset_index(drop=True)

X_train_dense = X_train.toarray()
X_test_dense = X_test.toarray()

train_data = pd.DataFrame(X_train_dense)
train_data['Sentiment'] = y_train.values

test_data = pd.DataFrame(X_test_dense)
test_data['Sentiment'] = y_test.values

train_data.to_csv('train_data.csv', index=False)
test_data.to_csv('test_data.csv', index=False)

print("Train and Test data have been exported successfully!")

df_train = pd.read_csv('train_data.csv')

df_train.head()

df_train.shape

df_test = pd.read_csv('test_data.csv')

df_test.head()

df_test.shape

print(df_train.isnull().sum())

print(df_test.isnull().sum())

vector_columns = df_train.columns.difference(['Sentiment']).tolist()

mean_values = df_train[vector_columns].mean(axis=1)
max_values = df_train[vector_columns].max(axis=1)
min_values = df_train[vector_columns].min(axis=1)

print (mean_values)

print (min_values)

print(max_values)

"""Proses Neural Network"""

from sklearn.neural_network import MLPClassifier
model = MLPClassifier()
model. fit(X_train, y_train)
print ("Training selesai")

pickle. dump(model, open ("model-p", "wb"))

from sklearn.metrics import classification_report
test = model.predict(X_test)
print ("Testing selesai")
print(classification_report(y_test, test))
print(classification_report(y_test, test))

import numpy as np
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import classification_report
from sklearn.metrics import accuracy_score
from sklearn.model_selection import KFold

kf = KFold(n_splits=5, random_state=42, shuffle=True)

accuracies = []

y = classes  # Pastikan 'classes' sudah didefinisikan sebelumnya

for iteration, data in enumerate(kf.split(X), start=1):
    # Use .iloc to access data by position
    data_train = X[data[0]]
    target_train = y.iloc[data[0]]  # Use .iloc for positional indexing

    data_test = X[data[1]]
    target_test = y.iloc[data[1]]  # Use .iloc for positional indexing

    clf = MLPClassifier()
    clf.fit(data_train, target_train)

    preds = clf.predict(data_test)

    accuracy = accuracy_score(target_test, preds)

    print("Training ke-", iteration)
    print(classification_report(target_test, preds))
    print("======================================")

    accuracies.append(accuracy)

average_accuracy = np.mean(accuracies)

print()
print()
print("Rata-rata Accuracy:", average_accuracy)

import re

def cleansing(text):
    # Remove punctuation
    text = re.sub(r'[^\w\s]', '', text)
    # Lowercase the text
    text = text.lower()
    return text

original_text = '''
Rasa syukur, cukup.
'''

text = count_vect.transform([cleansing(original_text)])

result = model.predict(text)[0]
print("Sentiment:")
print()
print(result)

filename_model = 'trained_model.pkl'
filename_vectorizer = 'trained_vectorizer.pkl'

pickle.dump(model, open(filename_model, 'wb'))
pickle.dump(count_vect, open(filename_vectorizer, 'wb'))

print(f"Model saved to: {filename_model}")
print(f"Vectorizer saved to: {filename_vectorizer}")

# prompt: buatkan kodingan dengan menggunakan neural network yang dapat memnetukan kalimat tersebnut memiliki sentimen positif,negatif atau neutral dengan menggunakan rnn atau cnn

import nltk
import re
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, LSTM, Dense, Dropout
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences

# Download necessary NLTK resources (if not already downloaded)
nltk.download('punkt')
nltk.download('stopwords')  # Download the stopwords data

# Load the preprocessed data (assuming it's in 'df_cleaned')
# ... (your existing data loading code) ...


# 1. Text Preprocessing (Enhancements)
def preprocess_text(text):
    # Lowercase
    text = text.lower()
    # Remove punctuation (more robust)
    text = re.sub(r'[^\w\s]', '', text)
    # Tokenization
    tokens = nltk.word_tokenize(text)
    # Remove stopwords (customize your stopwords list)
    stop_words = set(nltk.corpus.stopwords.words('indonesian'))  # Indonesian stopwords
    tokens = [word for word in tokens if word not in stop_words]
    return " ".join(tokens)

df_cleaned['Text_Bersih'] = df_cleaned['Text_Bersih'].apply(preprocess_text)


# 2. Feature Extraction using TF-IDF
vectorizer = TfidfVectorizer()  # Using TF-IDF instead of CountVectorizer
X = vectorizer.fit_transform(df_cleaned['Text_Bersih'])
y = df_cleaned['Sentiment']


# 3. Data Splitting
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)


# 4. RNN (LSTM) Model
# Tokenize text data for embedding layer (using only the training data)
tokenizer = Tokenizer(num_words=5000)  # Adjust num_words as needed
tokenizer.fit_on_texts(df_cleaned['Text_Bersih'])

# Use only training data for text to sequences and padding
X_train_seq = tokenizer.texts_to_sequences(X_train) # Changed to X_train
X_train_padded = pad_sequences(X_train_seq, maxlen=100)  # Adjust maxlen

# ... (rest of your model code) ...

#Evaluation, you need to pad the X_test as well
X_test_seq = tokenizer.texts_to_sequences(X_test)
X_test_padded = pad_sequences(X_test_seq, maxlen=100) # Adjust maxlen

loss, accuracy = model.evaluate(X_test_padded, y_test_num)
print(f"Accuracy: {accuracy*100:.2f}%")



# 5. Prediction
def predict_sentiment(text, model, vectorizer, tokenizer):
    text = preprocess_text(text)
    sequence = tokenizer.texts_to_sequences([text])
    padded = pad_sequences(sequence, maxlen=100)
    prediction = model.predict(padded)
    sentiment_labels = ['positive', 'negative', 'neutral'] # Update to your labels
    predicted_label = sentiment_labels[np.argmax(prediction)]
    return predicted_label

#Example usage
new_text = "Makanan ini sangat enak dan lezat!"
predicted_sentiment = predict_sentiment(new_text, model, vectorizer, tokenizer)
print(f"Predicted sentiment: {predicted_sentiment}")

# Assuming your original DataFrame is 'df_cleaned', use that:
neg_label = df_cleaned.loc[df_cleaned['Sentiment'] == 'negative'].Sentiment.tolist()
neu_label = df_cleaned.loc[df_cleaned['Sentiment'] == 'neutral'].Sentiment.tolist()
pos_label = df_cleaned.loc[df_cleaned['Sentiment'] == 'positive'].Sentiment.tolist()

# The following lines are incorrect as 'target_variable' column doesn't exist
# Remove or comment them out
#neg_label = df.loc[df['Sentiment'] == 'negative'].target_variable.tolist()
#neu_label = df.loc[df['Sentiment'] == 'neutral'].target_variable.tolist()
#pos_label = df.loc[df['Sentiment'] == 'positive'].target_variable.tolist()

# Assuming you have the pos_label, neu_label, and neg_label lists from previous cells
pos = len(pos_label)  # Assign the length of pos_label to pos
neu = len(neu_label)  # Assign the length of neu_label to neu
neg = len(neg_label)  # Assign the length of neg_label to neg

total_data = pos + neu + neg  # Calculate total data
labels = pos_label + neu_label + neg_label  # Combine labels

print("Pos: %s, Neu: %s, Neg: %s" % (len(pos_label), len(neu_label), len(neg_label)))  # Print label counts
print("Total data: %s" % total_data)  # Print total data count directly, without using len()

import pickle
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from collections import defaultdict

max_features = 100000
tokenizer = Tokenizer(num_words=max_features, split=' ', lower=True)

# Replace 'df' with 'df_cleaned' to use your preprocessed data
tokenizer.fit_on_texts(df_cleaned['Text_Bersih'])  # Using 'Text_Bersih' column

with open('tokenizer.pickle', 'wb') as handle:
    pickle.dump(tokenizer, handle, protocol=pickle.HIGHEST_PROTOCOL)
    print("tokenizer.pickle has created!")

# Now, you need to transform the text data into sequences
X = tokenizer.texts_to_sequences(df_cleaned['Text_Bersih']) # Using 'Text_Bersih' column
vocab_size = len(tokenizer.word_index)
maxlen = max(len(x) for x in X)

X = pad_sequences(X)
with open('x_pad_sequences.pickle', 'wb') as handle:
    pickle.dump(X, handle, protocol=pickle.HIGHEST_PROTOCOL)
    print("x_pad_sequences.pickle has created!")

Y = pd.get_dummies(labels)
Y = Y.values

with open('y_labels.pickle', 'wb') as handle:
    pickle.dump(Y, handle, protocol=pickle.HIGHEST_PROTOCOL)
    print("y_labels.pickle has created!")

import pickle
import pandas as pd
from sklearn.model_selection import train_test_split

# Load X data
file = open("x_pad_sequences.pickle", 'rb')
X = pickle.load(file)
file.close()

# Load Y data
file = open("y_labels.pickle", 'rb')
Y = pickle.load(file)
file.close()

# Ensure X and Y have the same number of samples before splitting
min_samples = min(X.shape[0], Y.shape[0])
X = X[:min_samples]
Y = Y[:min_samples]


# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.2, random_state=1)

import numpy as np
from tensorflow.keras import layers
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Embedding, LSTM, SpatialDropout1D, SimpleRNN #
from tensorflow.keras import optimizers
from tensorflow.keras.callbacks import EarlyStopping, TensorBoard
from tensorflow.keras.layers import Flatten
from tensorflow.keras import backend as K

embed_dim = 100
units = 64

model = Sequential()
model.add(Embedding(max_features, embed_dim, input_length=X.shape[1]))
model.add(SimpleRNN(units, dropout=0.2))
model.add(Dense(3, activation='softmax'))

# Use 'learning_rate' instead of 'lr'
adam = optimizers.Adam(learning_rate=0.001)
model.compile(loss='categorical_crossentropy', optimizer=adam, metrics=['accuracy'])

es = EarlyStopping(monitor='val_loss', mode='min', verbose=1)
history = model.fit(X_train, y_train, epochs=10, batch_size=10, validation_data=(X_test, y_test), verbose=1, callbacks=[es])

from sklearn import metrics

predictions = model.predict(X_test)
y_pred = predictions
matrix_test = metrics.classification_report(y_test.argmax(axis=1), y_pred.argmax(axis=1))
print("Testing selesai")
print(matrix_test)

import numpy as np
from sklearn.metrics import classification_report, accuracy_score
from sklearn.model_selection import KFold

kf = KFold(n_splits=5, random_state=42, shuffle=True)

accuracies = []

y = Y

embed_dim = 100
units = 64

for iteration, data in enumerate(kf.split(X), start=1):
    data_train = X[data[0]]
    target_train = y[data[0]]

    data_test = X[data[1]]
    target_test = y[data[1]]

    model = Sequential()
    model.add(Embedding(max_features, embed_dim, input_length=X.shape[1]))
    model.add(SimpleRNN(units, dropout=0.2))
    model.add(Dense(3, activation='softmax'))

    # Change 'lr' to 'learning_rate'
    adam = optimizers.Adam(learning_rate=0.001)
    # Remove this line as it's redundant and uses the incorrect 'lr'
    # sgd = optimizers.Adam(lr=0.001)

    # Use the same optimizer for both compile calls
    model.compile(loss='binary_crossentropy', optimizer=adam, metrics=['accuracy']) # You might need to change this loss to 'categorical_crossentropy' if your target is one-hot encoded
    #model.compile(loss='categorical_crossentropy', optimizer=adam, metrics=['accuracy']) # This line is now redundant

    es = EarlyStopping(monitor='val_loss', mode='min', verbose=1)
    history = model.fit(data_train, target_train, epochs=10, batch_size=10, validation_data=(data_test, target_test), verbose=1, callbacks=[es])

    predictions = model.predict(data_test)
    y_pred = predictions

import pickle
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
from sklearn.model_selection import KFold  # Import KFold here
import numpy as np
from tensorflow.keras import layers
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Embedding, LSTM, SpatialDropout1D, SimpleRNN #
from tensorflow.keras import optimizers
from tensorflow.keras.callbacks import EarlyStopping, TensorBoard
from tensorflow.keras.layers import Flatten
from tensorflow.keras import backend as K

# Define kf within the current scope
kf = KFold(n_splits=5, random_state=42, shuffle=True)

accuracies = []

embed_dim = 100
units = 64

# Define max_features here
max_features = 100000  # Or whatever value you used earlier


# Load X data
file = open("x_pad_sequences.pickle", 'rb')
X = pickle.load(file)
file.close()

# Load Y data
file = open("y_labels.pickle", 'rb')
Y = pickle.load(file) # This line loads the Y variable
file.close()

# Ensure X and Y have the same number of samples before splitting
min_samples = min(X.shape[0], Y.shape[0])
X = X[:min_samples]
Y = Y[:min_samples]

y = Y # Now you can assign Y to y


for iteration, data in enumerate(kf.split(X), start=1):
    data_train = X[data[0]]
    target_train = y[data[0]]

    data_test = X[data[1]]
    target_test = y[data[1]]

    model = Sequential()
    # Now max_features is defined in this scope
    model.add(Embedding(max_features, embed_dim, input_length=X.shape[1]))
    model.add(SimpleRNN(units, dropout=0.2))
    model.add(Dense(3, activation='softmax'))

    # Change 'lr' to 'learning_rate'
    adam = optimizers.Adam(learning_rate=0.001)

    model.compile(loss='categorical_crossentropy', optimizer=adam, metrics=['accuracy']) # You might need to change this loss to 'categorical_crossentropy' if your target is one-hot encoded

    es = EarlyStopping(monitor='val_loss', mode='min', verbose=1)
    history = model.fit(data_train, target_train, epochs=10, batch_size=10, validation_data=(data_test, target_test), verbose=1, callbacks=[es])

    predictions = model.predict(data_test)
    y_pred = predictions

    # Use target_test instead of y_test for accuracy calculation
    accuracy = accuracy_score(target_test.argmax(axis=1), y_pred.argmax(axis=1))

    print("Training ke-", iteration)
    # Use target_test instead of y_test for classification report
    print(classification_report(target_test.argmax(axis=1), y_pred.argmax(axis=1)))
    print("=============================================")

    accuracies.append(accuracy)

average_accuracy = np.mean(accuracies)

print()
print()
print()
print("Rata-rata Accuracy: ", average_accuracy)

import re
import numpy as np
import pickle
import matplotlib.pyplot as plt
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences

# Fungsi cleansing untuk preprocessing teks
def cleansing(text):
    text = re.sub(r'[^\w\s]', '', text)  # Remove punctuation
    text = text.lower()  # Lowercase the text
    return text

# Load tokenizer
with open('tokenizer.pickle', 'rb') as handle:
    tokenizer = pickle.load(handle)

# Daftar sentimen yang digunakan (pastikan sesuai dengan data pelatihan)
sentiment = ['negative', 'neutral', 'positive']

# Load model yang sudah dilatih
model = load_model('model_rnn.h5')

# Input teks untuk prediksi sentimen
text_input = "biasa saja"  # Ganti dengan teks yang ingin diuji

# Preprocess teks input
text = [cleansing(text_input)]  # Cleansing teks

# Mengubah teks menjadi urutan numerik
predicted = tokenizer.texts_to_sequences(text)

# Memastikan panjang padding sesuai dengan yang digunakan saat pelatihan
maxlen = 100  # Pastikan ini sesuai dengan panjang padding saat pelatihan
guess = pad_sequences(predicted, maxlen=maxlen)

# Membuat prediksi sentimen
prediction = model.predict(guess)

# Menentukan polaritas berdasarkan argmax
polarity = np.argmax(prediction[0])

# Kata-kata negatif yang harus diperhatikan
negative_keywords = ['buruk', 'tolol', 'jelek', 'parah', 'sampah', 'bodoh']

# Logika tambahan untuk penalti pada prediksi positif jika ada kata negatif
if any(word in text[0] for word in negative_keywords) and polarity == 2:  # 2 = positive
    print("Warning: Positive sentiment detected, but negative keywords found.")
    polarity = 0  # Override ke negative

# Menampilkan hasil
print("Text: ", text[0])
print("Sentiment: ", sentiment[polarity])
print("Prediction probabilities: ", prediction[0])

# Visualisasi

# prompt: buat confusion matrixnya

import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix
import pickle
import pandas as pd
from sklearn.model_selection import train_test_split


# Load X data
file = open("x_pad_sequences.pickle", 'rb')
X = pickle.load(file)
file.close()

# Load Y data
file = open("y_labels.pickle", 'rb')
Y = pickle.load(file)  # This line loads the Y variable
file.close()

# Ensure X and Y have the same number of samples before splitting
min_samples = min(X.shape[0], Y.shape[0])
X = X[:min_samples]
Y = Y[:min_samples]


# Before the KFold loop: Split data for final evaluation
# This will create your y_test
X_train_final, X_test_final, y_train_final, y_test_final = train_test_split(
    X, Y, test_size=0.2, random_state=1  # Use the same random_state as before
)


# Assuming y_test and y_pred are defined from your previous code
# y_test should contain the true labels (integers or one-hot encoded)
# y_pred should contain the predicted labels (integers or probabilities)


# Replace y_test with y_test_final and y_pred with your actual predictions on X_test_final
# Example:
from tensorflow.keras.models import load_model

model = load_model('model_rnn.h5') # Assuming you saved your model as 'model_rnn.h5'
y_pred = model.predict(X_test_final)  # Make predictions on your test data



# If y_test is one-hot encoded, convert it back to class labels
if len(y_test_final.shape) > 1 and y_test_final.shape[1] > 1:
    y_true = y_test_final.argmax(axis=1)  # Convert one-hot to class labels
else:
    y_true = y_test_final #y_test is already class labels

# If y_pred is probabilities, convert them to class labels
if len(y_pred.shape) > 1 and y_pred.shape[1] > 1:
    y_predicted = y_pred.argmax(axis=1)  # Convert probabilities to class labels
else:
    y_predicted = y_pred # y_pred is already class labels

cm = confusion_matrix(y_true, y_predicted)
plt.figure(figsize=(8, 6))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
            xticklabels=['Negative', 'Neutral', 'Positive'],
            yticklabels=['Negative', 'Neutral', 'Positive'])
plt.xlabel('Predicted')
plt.ylabel('Actual')
plt.title('Confusion Matrix')
plt.show()

# prompt: buat model visualisainya

import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix
from tensorflow.keras.models import load_model
from tensorflow.keras.callbacks import EarlyStopping




# Assuming y_test and y_pred are defined from your previous code
# y_test should contain the true labels (integers or one-hot encoded)
# y_pred should contain the predicted labels (integers or probabilities)


# Replace y_test with y_test_final and y_pred with your actual predictions on X_test_final
# Example:

model = load_model('model_rnn.h5') # Assuming you saved your model as 'model_rnn.h5'
y_pred = model.predict(X_test_final)  # Make predictions on your test data



# If y_test is one-hot encoded, convert it back to class labels
if len(y_test_final.shape) > 1 and y_test_final.shape[1] > 1:
    y_true = y_test_final.argmax(axis=1)  # Convert one-hot to class labels
else:
    y_true = y_test_final #y_test is already class labels

# If y_pred is probabilities, convert them to class labels
if len(y_pred.shape) > 1 and y_pred.shape[1] > 1:
    y_predicted = y_pred.argmax(axis=1)  # Convert probabilities to class labels
else:
    y_predicted = y_pred # y_pred is already class labels

cm = confusion_matrix(y_true, y_predicted)
plt.figure(figsize=(8, 6))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
            xticklabels=['Negative', 'Neutral', 'Positive'],
            yticklabels=['Negative', 'Neutral', 'Positive'])
plt.xlabel('Predicted')
plt.ylabel('Actual')
plt.title('Confusion Matrix')
plt.show()

import matplotlib.pyplot as plt



# Mengambil data loss dan accuracy
loss = history['loss']
val_loss = history['val_loss']
accuracy = history['accuracy']
val_accuracy = history['val_accuracy']
epochs = range(1, len(loss) + 1)

# Membuat plot Loss per Epoch
plt.figure(figsize=(12, 5))

plt.subplot(1, 2, 1)  # Grafik pertama (Loss)
plt.plot(epochs, loss, label='Training Loss', color='blue')
plt.plot(epochs, val_loss, label='Validation Loss', color='orange')
plt.title('Loss per Epoch')
plt.xlabel('Epochs')
plt.ylabel('Loss')
plt.legend()

# Membuat plot Accuracy per Epoch
plt.subplot(1, 2, 2)  # Grafik kedua (Accuracy)
plt.plot(epochs, accuracy, label='Training Accuracy', color='blue')
plt.plot(epochs, val_accuracy, label='Validation Accuracy', color='orange')
plt.title('Accuracy per Epoch')
plt.xlabel('Epochs')
plt.ylabel('Accuracy')
plt.legend()

# Tampilkan plot
plt.tight_layout()
plt.show()


