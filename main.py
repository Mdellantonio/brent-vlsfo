from src.data_processing.data_processing import df_brent, df_vlsfo, df_comparison

import pandas as pd
import streamlit as st
import altair as alt


st.set_page_config(
    page_title='Simulador VLSFO',
    layout='wide',
    initial_sidebar_state='expanded'
)

df_comparison = df_comparison


