import streamlit as st
import requests

col1, col2 = st.columns(2)
with col1:
    curr1 = st.selectbox('Waluta 1', ['CHF','EUR','GBP','PLN','USD'])
with col2:
    curr2 =st.selectbox('Waluta 2', ['CHF', 'EUR', 'GBP', 'PLN', 'USD'])
url = f''
re = requests.get(url)
re = re.json()

one_two = re[f"{curr1}_{curr2}"]
two_one = re[f"{curr2}_{curr1}"]

col1,col2 = st.columns(2)
with col1:
    st.write(f"{curr1} to {curr2}")
    st.success(one_two)
with col2:
    st.write(f"{curr2} to {curr1}")
    st.success(two_one)
col1,col2 = st.columns(2)
with col1:
    amount = st.number_input(curr1)
with col2:
    converted = amount*one_two
    st.text("Wartość po przeliczeniu")
    st.success(converted)
