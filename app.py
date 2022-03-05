# -*- coding: utf-8 -*-
"""
Created on Wed Feb 27 2022
@author: Tony Kipkemboi
"""

# import dependencies
# import os
# import json
import requests
import pandas as pd
import plotly.express as px
import streamlit as st

# # load dotenv
# from dotenv import load_dotenv
# load_dotenv()
MY_API = st.secrets["API_KEY"]


# Variable to hold dataframes from api queries
data = []

# API endpoints to query
urls = ['https://api.glassnode.com/v1/metrics/market/mvrv',
        'https://api.glassnode.com/v1/metrics/market/price_usd_close',
        ]


def get_data(symbol, API_KEY):
    '''Queries API endpoints to get data'''
    for url in urls:
        label = url.split('/')[-1]
        # make API request
        res = requests.get(url, params={'a': symbol, 'api_key': API_KEY})
        # convert to pandas dataframe
        df = pd.read_json(res.text, convert_dates=['t'])
        df.set_index('t', inplace=True)
        df.rename(columns={'v': label}, inplace=True)
        data.append(df)
        # create a dataframe from list of results generated from the API
        data_df = pd.concat(data, axis=1)
    return data_df


def main():
    '''Main function to run app'''

    st.set_page_config(page_title='MVRV - Dashboard',
                       layout='wide', page_icon='📈')

    # this is the header
    t1, t2 = st.columns((0.2, 1))

    t1.image('https://media.giphy.com/media/rM0wxzvwsv5g4/giphy.gif', width=200)
    t2.title("MVRV Dashboard")
    t2.markdown(
        " **github:** https://github.com/tonykipkemboi **| email:** iamtonykipkemboi@gmail.com")

    # Expander with explanation
    with st.expander('What\'s this app about? 😕'):
        st.write("""
        **MVRV (Market Value to Realized Value)** ratio is defined as *an asset's market cap divided by realized cap*. By comparing two valuation methods, 
        the MVRV ratio can tell us to get a sense of whether the price is fair or not, which means it is useful to get market tops and bottoms. 
        It is important to note that historically, it has been an outstanding indicator to spot market top/bottom or local top/bottom that occurred through three halvings. 
        This metric was created by David Puell and Murad Muhmudov.
        The chart below shows the MVRV ratio for selected tokens(**BTC, ETH, & LTC**). [**I have not subscribed to Glassnode's API Pro Plan hence data will not be upto date**]
        For more info about MVRV check out this user guide by [CryptoQuant](https://dataguide.cryptoquant.com/market-data-indicators/mvrv-ratio#:~:text=Definition,capitalization%20divided%20by%20realized%20capitalization.)""")
        latext = r'''
        $$
        MVRV = \frac {Market Cap}{Realized Cap}
        '''
        st.write(latext)
        st.image('https://1139253730-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2F-MBHQ44vVRUAbLIaMwGN-1972196547%2Fuploads%2FwSpLdVKSM5VEHAhvxslI%2Fimage.png?alt=media&token=07ec7f9f-5def-4e5e-9800-4b9e5d019f26')
    # Queriable token list
    tokens = ['BTC', 'ETH', 'LTC']

    # Token options
    st.header("Market Value to Realized Value Ratio (MVRV)")
    selection = st.selectbox('Pick Token', tokens)

    # Data loading and notification
    data_load_state = st.text('Loading data...')
    data_df = get_data(selection, MY_API)
    data_load_state.text("Done!")

    # Plot graph
    fig = px.line(data_df, title="{} (MVRV Ratio vs Price)".format(selection))
    st.plotly_chart(fig)

    # Display raw data
    if st.checkbox('Show raw data'):
        st.subheader('Raw data')
        st.write(data_df.style.highlight_max(axis=0))

    st.write('''
    Buy me a [coffee](https://www.buymeacoffee.com/tonykip) 🙏 ❤️ 
    ''')


if __name__ == "__main__":
    main()
