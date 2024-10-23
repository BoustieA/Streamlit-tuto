# -*- coding: utf-8 -*-
"""
Created on Mon Oct 21 14:14:22 2024

@author: adrie
"""

import streamlit as st
import pandas as pd
import seaborn as sns

import matplotlib.pyplot as plt

import logging
from contextlib import contextmanager, redirect_stdout
from io import StringIO

@contextmanager
def st_capture(output_func):
    # Use StringIO to capture print output
    with StringIO() as stdout, redirect_stdout(stdout):
        yield stdout  # This will allow us to access the printed output string
  # Display in Streamlit UI

# Initialize Streamlit placeholders
if __name__=="__main__":
    output = st.empty()
            
    
    # Set up logging configuration
    logging.basicConfig(level=logging.ERROR,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S',
                        filename='file_changes.log',
                        filemode='w')
    
    # Test logging
    logging.info("Logging is working.")
    
    
    tab1,tab2, tab3 = st.tabs(["main","plot_kde","plot_hist"])
    
    @st.cache_data
    def load_data(file):
        df = pd.read_csv(file)
        df.loc[:,"Age"]=df.loc[:,"Age"].fillna(df.loc[:,"Age"].mean())
        return df
    
    
    with tab1:
        uploaded_file=st.file_uploader("csv to read")
        if uploaded_file is not None:
            df=load_data(uploaded_file) 
            with st_capture(output.code) as captured_stdout:
                df.info()
                infos=captured_stdout.getvalue()
            st.title("Main")
            col1,col2 = st.columns([0.5,0.5])
            with col1:
                st.dataframe(df)
                st.table(df.head(5))
                columns_to_display=st.multiselect("colonnes a utiliser",df.columns)
                st.dataframe(df[columns_to_display])
            with col2:
                
                st.table(df.describe())
                    
                st.text(infos)
            
    with tab2:
        figure = plt.figure()
        if uploaded_file is not None:
        
            filter_column=st.selectbox("colonne a filtrer",df.columns)
            filter_=st.multiselect("filtre colonne Pclass",df.loc[:,filter_column].unique())
            if filter_== []:
                plot = sns.kdeplot(data=df, x="Age",hue="Survived")
                
            else:
                logging.error(filter_)
                df_filtered=df.loc[df.loc[:,filter_column].isin(filter_)]
                
                plot = sns.kdeplot(data=df_filtered
                                   , x="Age",hue="Survived")
                                                   
        st.pyplot(fig=figure)
    with tab3:
        if uploaded_file is not None:
            figure = plt.figure()
            colonne_histogram=st.selectbox("colonne histogram",df.columns)
            colonne_groupe=st.selectbox("groupe histogram",df.columns)
            if colonne_histogram ==colonne_groupe:
                plt.title("No filter")
                plot = sns.histplot(data=df, x=colonne_histogram)
                
            else:
                plt.title("filtered")
                plot = sns.histplot(data=df
                                        , x = colonne_histogram
                                        , hue = colonne_groupe)
        
            st.pyplot(fig=figure)
    
