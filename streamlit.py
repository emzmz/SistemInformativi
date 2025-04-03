import pandas as pd
import numpy as np
import streamlit as st
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

def load_data():
    df = pd.read_excel(r"C:\Users\hp\Desktop\UNIVERSITY\sistemi informativi\Real estate valuation data set.xlsx")
    df = df.rename(columns={
        'X1 transaction date': 'transaction_date',
        'X2 house age': 'house_age',
        'X3 distance to the nearest MRT station': 'distance_to_mrt',
        'X4 number of convenience stores': 'num_convenience',
        'X5 latitude': 'latitude',
        'X6 longitude': 'longitude',
        'Y house price of unit area': 'price_per_unit_area'})
    return df

df = load_data()

# Modello1: Predizione con latitudine e longitudine
def train_model1(df):
    X = df[['latitude', 'longitude']]
    y = df['price_per_unit_area']
    model = RandomForestRegressor(random_state=42)
    model.fit(X, y)
    return model

# Modello2: Predizione con house_age, distance_to_mrt, num_convenience
def train_model2(df):
    X = df[['house_age', 'distance_to_mrt', 'num_convenience']]
    y = df['price_per_unit_area']
    model = RandomForestRegressor(random_state=42)
    model.fit(X, y)
    return model

model1 = train_model1(df)
model2 = train_model2(df)

# Streamlit

st.title("Predizione dei Prezzi Immobiliari")
st.write(" #### Questo studio si concentra nell'area geografica di Sindian Dist., New Taipei City, Taiwan")

scelta_modello = st.radio('Scegliere il modello con cui fare la prediction del prezzo:',
                           ('Modello 1: usa Latitudine e Longitudine.',
                            "Modello 2: usa l'Età della casa, la Distanza dalla stazione MRT più vicina e il Numero di minimarket vicini."))

# Modello 1
if scelta_modello == 'Modello 1: usa Latitudine e Longitudine.':
    st.header(" Modello 1 - Previsione con Latitudine e Longitudine")
    latitude = st.number_input("Inserisci la latitudine, NB: deve essere nel range [24.93207, 25.01459]", min_value=24.93207, max_value=25.01459)
    longitude = st.number_input("Inserisci la longitudine, NB: deve essere nel range [121.47353, 121.56627]", min_value=121.47353, max_value=121.56627)
    if (24.93207 <= latitude <= 25.01459) and (121.47353 <= longitude <= 121.56627):
        if st.button('Predict Price'):
            prediction1 = model1.predict([[latitude, longitude]])[0]
            st.success(f"Prezzo Predetto: {prediction1:.2f} NT$/Ping ")
    else:
        if st.button('Predict Price'):
            st.success(f'Valori di latitudine o longitudine fuori dal range')
            

# Modello 2
elif scelta_modello == "Modello 2: usa l'Età della casa, la Distanza dalla stazione MRT più vicina e il Numero di minimarket vicini.": 
    st.header(" Modello 2 - Previsione con Età della Casa, Distanza dalla stazione MRT più vicina e Numero di minimarket vicini")
    house_age = st.number_input("Inserisci l'età della casa:", min_value=0)
    distance_to_mrt = st.number_input("Inserisci la distanza dalla stazione MRT più vicina (in metri):", min_value=0)
    num_convenience = st.number_input("Inserisci il numero di minimarket nelle vicinanze della casa:", step=1)
    if st.button('Predict Price'):
        prediction2 = model2.predict([[house_age, distance_to_mrt, num_convenience]])[0]
        st.success(f"Prezzo Predetto: {prediction2:.2f} NT$/Ping")
