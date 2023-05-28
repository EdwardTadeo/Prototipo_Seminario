import pandas as pd
import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.optimizers import Adam
import matplotlib.pyplot as plt
from sklearn.preprocessing import LabelEncoder
from tensorflow.keras.utils import to_categorical

# Cargar los datos desde el archivo CSV
data = pd.read_csv('data_entranamiento_credit_risk.csv')

data = data.drop('Total de Puntos', axis=1)

# Convertir las etiquetas a numéricas
encoder = LabelEncoder()
etiquetas_numerico = encoder.fit_transform(data['Clasificación de Riesgo'])

# One hot encoding para las etiquetas
etiquetas_onehot = to_categorical(etiquetas_numerico)

# Obtener las variables de entrada (características)
variables_entrada = data.drop('Clasificación de Riesgo', axis=1).values

# Definir la arquitectura de la red neuronal multicapa
model = Sequential()
model.add(Dense(3, input_dim=variables_entrada.shape[1], activation='relu'))
model.add(Dense(3, activation='relu'))
model.add(Dense(3, activation='softmax'))  # 3 nodos en la capa de salida porque tenemos 3 clases

# Compilar el modelo
optimizer = Adam(learning_rate=0.01)
model.compile(loss='categorical_crossentropy', optimizer=optimizer, metrics=['accuracy'])

# Normalizar variables de entrada
variables_entrada_norm = variables_entrada / np.max(variables_entrada)

# Entrenar el modelo con retropropagación
print("Iniciando el entrenamiento...")
history = model.fit(variables_entrada_norm, etiquetas_onehot, epochs=200, verbose=0)
print("Entrenamiento finalizado")

# Graficar la pérdida durante el entrenamiento
plt.plot(history.history['loss'])
plt.title('Model loss')
plt.ylabel('Loss')
plt.xlabel('Epoch')
plt.show()

# Predecir el riesgo crediticio para nuevas variables
nuevas_variables = np.array([[2, 2, 1, 1, 4, 1, 1, 1, 1, 2, 1, 1, 2, 2, 2, 2, 1]])
nuevas_variables_norm = nuevas_variables / np.max(variables_entrada)

riesgo_crediticio = model.predict(nuevas_variables_norm)
print(riesgo_crediticio)
riesgo_crediticio_clase = encoder.inverse_transform([np.argmax(riesgo_crediticio)])

print(f"La clase de riesgo crediticio es: {riesgo_crediticio_clase[0]}")

# Imprimir los pesos de la última capa
print("Pesos de la última capa:")
print(model.layers[-1].get_weights())
accuracy = model.evaluate(variables_entrada_norm, etiquetas_onehot)[1]
print(f"Precisión del modelo: {accuracy * 100:.2f}%")
