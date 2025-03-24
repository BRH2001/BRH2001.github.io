import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.express as px

def fetch_stock_data(ticker, start="2023-01-01", end="2024-01-01"):
    """Fetch historical stock data from Yahoo Finance."""
    stock = yf.Ticker(ticker)
    data = stock.history(start=start, end=end)
    
    # Fetch additional key statistics
    info = stock.info
    stats = {
        "Current Price": info.get("currentPrice", "N/A"),
        "Market Cap": info.get("marketCap", "N/A"),
        "52 Week High": info.get("fiftyTwoWeekHigh", "N/A"),
        "52 Week Low": info.get("fiftyTwoWeekLow", "N/A"),
        "P/E Ratio": info.get("trailingPE", "N/A"),
        "Dividend Yield": info.get("dividendYield", "N/A"),
    }
    
    return data, stats

# Streamlit UI
st.set_page_config(page_title="AI Trading Bot", layout="wide")
st.title("📈 AI Trading Dashboard")

# User input for stock ticker
ticker = st.text_input("Enter Stock Ticker:", "AAPL").upper()

# Fetch stock data
if ticker:
    stock_data, stock_stats = fetch_stock_data(ticker)
    
    # Display key stock statistics
    st.subheader("Stock Overview")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Current Price", stock_stats["Current Price"])
    col2.metric("Market Cap", stock_stats["Market Cap"])
    col3.metric("52 Week High", stock_stats["52 Week High"])
    col4.metric("52 Week Low", stock_stats["52 Week Low"])
    
    # Plot stock price history
    st.subheader("Stock Price Chart")
    fig = px.line(stock_data, x=stock_data.index, y="Close", title=f"{ticker} Closing Prices")
    st.plotly_chart(fig)
    
    # Show stock data table
    st.subheader("Raw Stock Data")
    st.dataframe(stock_data)
