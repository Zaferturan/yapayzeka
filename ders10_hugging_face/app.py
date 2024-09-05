#!/usr/bin/env python
# coding: utf-8

# # Car Prediction #
# İkinci el araç fiyatlarını (özelliklerine göre) tahmin eden modeller oluşturma ve MLOPs ile Hugging Face üzerinden yayımlayacağız.
# 

# In[1]:
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_squared_error
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.pipeline import Pipeline
import streamlit as st

# Veri dosyasını yükle
df = pd.read_excel('cars.xls')

# Veri ön işleme
X = df.drop('Price', axis=1)  # fiyat sütunu çıkar fiyata etki edenler kalsın
y = df['Price']  # tahmin

# Veri setini bölme
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# ColumnTransformer tanımla
preprocess = ColumnTransformer(
    transformers=[
        ('num', StandardScaler(), ['Mileage', 'Cylinder', 'Liter', 'Doors']),
        ('cat', OneHotEncoder(handle_unknown='ignore'), ['Make', 'Model', 'Trim', 'Type'])
    ]
)

# Pipeline oluştur
my_model = LinearRegression()
pipe = Pipeline(steps=[('preprocessor', preprocess), ('model', my_model)])

# Pipeline fit
pipe.fit(X_train, y_train)

# Tahmin yapma
y_pred = pipe.predict(X_test)
print('RMSE', mean_squared_error(y_test, y_pred)**0.5)
print('R2', r2_score(y_test, y_pred))

# price tahmin fonksiyonu tanımla
def price(make, model, trim, mileage, car_type, cylinder, liter, doors, cruise, sound, leather):
    input_data = pd.DataFrame({
        'Make': [make],
        'Model': [model],
        'Trim': [trim],
        'Mileage': [mileage],
        'Type': [car_type],
        'Cylinder': [cylinder],
        'Liter': [liter],
        'Doors': [doors],
        'Cruise': [cruise],
        'Sound': [sound],
        'Leather': [leather]
    })
    prediction = pipe.predict(input_data)[0]
    return prediction

# Streamlit arayüzü
st.title("Otomobil Fiyatı Tahmin:red_car: @zaferturan")
st.write('Özellikleri Seçiniz')
make = st.selectbox('Marka', df['Make'].unique())
model = st.selectbox('Model', df[df['Make'] == make]['Model'].unique())
trim = st.selectbox('Trim', df[(df['Make'] == make) & (df['Model'] == model)]['Trim'].unique())
mileage = st.number_input('Kilometre', 100, 200000)
car_type = st.selectbox('Araç Tipi', df[(df['Make'] == make) & (df['Model'] == model) & (df['Trim'] == trim)]['Type'].unique())
cylinder = st.selectbox('Silindir Sayısı', df['Cylinder'].unique())
liter = st.number_input('Yakıt hacmi', 1, 10)
doors = st.selectbox('Kapı sayısı', df['Doors'].unique())
cruise = st.radio('Hız Sbt.', [True, False])
sound = st.radio('Ses Sis.', [True, False])
leather = st.radio('Deri döşeme.', [True, False])

if st.button('Yaklaşık Fiyat Tahmini'):
    pred = price(make, model, trim, mileage, car_type, cylinder, liter, doors, cruise, sound, leather)
    st.write('Fiyat:$', round(pred, 2))

