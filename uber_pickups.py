import streamlit as st
import pandas as pd
import numpy as np



st.title('Uber Pickups in NYC')

DATE_COLUMN = 'date/time'
DATA_URL = ('https://s3-us-west-2.amazonaws.com/'
         'streamlit-demo-data/uber-raw-data-sep14.csv.gz')


#caching the load data
@st.cache
#load_data downloads data, puts into pandas dataframe
#and converts date column from text to datetime
#function accepts single parameter(nrows) = specifies # of rows to load
def load_data(nrows):
    data = pd.read_csv(DATA_URL, nrows=nrows)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
    return data
    

# create a text element and let user know the data is loading
data_load_state = st.text('Loading data...')
#load 10,000 rows of data into the dataframe
data = load_data(10000)
# Notify the reader that the data was successfully loaded
data_load_state.text("Done! (using st.cache)")

if st.checkbox('Show raw data'): # add checkbox to show/hide raw data table
    st.subheader('Raw data') #prinout of the raw data to the app
#passing a dataframe into st.write()
    st.write(data)

st.subheader('Number of pickups by hour')

#use NumPy (np) to generate a histogram
hist_values = np.histogram(
    #DATE_COLUMN is made load_data function converting date column from text to date/time format
    #.dt = calling the combined data/time property & .hour breaks data by the hour
    data[DATE_COLUMN].dt.hour, bins=24, range=(0,24))[0]

#streamlit method to draw histogram made from above
st.bar_chart(hist_values)

# redraw map to show the concentration of pickups at 17:00 (5pm)
# use st.slider() to add silder filter for map
hour_to_filter = st.slider('hour',0,23,17) # min: 0h, max: 23h, default: 17h
filtered_data = data[data[DATE_COLUMN].dt.hour == hour_to_filter]

st.subheader(f'Map of all pickups at {hour_to_filter}:00')

st.map(filtered_data)







