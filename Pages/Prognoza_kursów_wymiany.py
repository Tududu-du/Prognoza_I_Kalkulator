import streamlit as st
from datetime import date

import yfinance as yf
from prophet import Prophet
from prophet.plot import plot_plotly
from plotly import graph_objs as go

START = "2020-01-01"
TODAY = date.today().strftime("%Y-%m-%d")

st.title('Prognoza kursów wymiany')

rates = ('EURUSD=X', 'EURCHF=X', 'EURPLN=X', 'EURGBP=X')
selected_rate= st.selectbox('Wybierz waluty', rates)

n_years = st.slider('Okres przewidywań:', 1, 5)
period = n_years * 365


@st.cache_data
def load_data(ticker):
    data = yf.download(ticker, START, TODAY)
    data.reset_index(inplace=True)
    return data


data_load_state = st.text('Ładowanie...')
data = load_data(selected_rate)
data_load_state.text('Załadowane!')

st.subheader('Dane')
st.write(data.tail())


# Plot raw data
def plot_raw_data():
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data['Date'], y=data['Open'], name="kurs_otwarcie"))
    fig.add_trace(go.Scatter(x=data['Date'], y=data['Close'], name="kurs_zamknięcie"))
    fig.layout.update(title_text='Time Series Data z okresem przewidywań', xaxis_rangeslider_visible=True)
    st.plotly_chart(fig)


plot_raw_data()

# Predict forecast with Prophet.
df_train = data[['Date', 'Close']]
df_train = df_train.rename(columns={"Date": "ds", "Close": "y"})

m = Prophet()
m.fit(df_train)
future = m.make_future_dataframe(periods=period)
forecast = m.predict(future)

# Show and plot forecast
st.subheader('Dane prognozy')
st.write(forecast.tail())

st.write(f'Prognoza na {n_years} lat')
fig1 = plot_plotly(m, forecast)
st.plotly_chart(fig1)

st.write("Elementy prognozy")
fig2 = m.plot_components(forecast)
st.write(fig2)

