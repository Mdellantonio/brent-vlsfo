import pandas as pd
import streamlit as st
import altair as alt
from src.data_processing.data_processing import df_comparison

st.set_page_config(
    page_title='Simulador VLSFO',
    layout='wide',
)

if df_comparison.empty:
    st.error("O DataFrame está vazio. Não é possível carregar o dashboard.")
    st.stop()


# --- CENTRALIZAÇÃO COM st.columns ---
st.markdown("<h1 style='text-align: center;'>Simulador VLSFO</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center;'>Filtro da Calculadora</h3>", unsafe_allow_html=True)

col_spacer1, col_selectbox, col_spacer2 = st.columns([1, 1.5, 1])

with col_selectbox:
    selected_date = st.selectbox(
        'Selecione a Data',
        options=df_comparison.index,
        index=len(df_comparison.index) - 1,
        label_visibility='collapsed',
        format_func=lambda date: date.strftime('%d/%m/%Y')
    )

st.divider()

# --- Calculator (KPIs) ---
data_from_selected_day = df_comparison.loc[selected_date]

vlsfo_price = data_from_selected_day['VLSFO Close']
brent_price = data_from_selected_day['Brent Close']
boe_premium = data_from_selected_day['Premium $']
premium_perc = data_from_selected_day['Premium %']

col_precos, col_premios = st.columns(2)

with col_precos:
    st.markdown("<h3 style='text-align: center;'>Preços</h3>", unsafe_allow_html=True)
    with st.container(border=True):
        sub_col1, sub_col2 = st.columns(2)
        with sub_col1:
            st.metric(label='Singapore VLSFO ($/boe)', value=f'{vlsfo_price:,.2f}')
        with sub_col2:
            st.metric(label='Brent ($/boe)', value=f'{brent_price:,.2f}')

with col_premios:
    st.markdown("<h3 style='text-align: center;'>Prêmios</h3>", unsafe_allow_html=True)
    with st.container(border=True):
        sub_col3, sub_col4 = st.columns(2)
        with sub_col3:
            st.metric(label="Prêmio ($/boe)", value=f"{boe_premium:,.2f}")
        with sub_col4:
            st.metric(label="Prêmio (%)", value=f"{premium_perc:.2%}")

st.markdown("""
<style>
[data-testid="stMetric"] {
    display: flex;
    flex-direction: column;
    align-items: center;
}
</style>
""", unsafe_allow_html=True)


st.divider()

# --- Gráficos de Linha ---
st.markdown("<h2 style='text-align: center;'>Histórico de Prêmios</h2>", unsafe_allow_html=True)

df_chart = df_comparison.reset_index()

# Gráfico 1: Prêmio ($/boe)
st.markdown("<h3 style='text-align: center;'>Prêmio ($/boe)</h3>", unsafe_allow_html=True)
chart_boe = alt.Chart(df_chart).mark_line(point=True).encode(
    # CORREÇÃO DA FORMATAÇÃO:
    x=alt.X('Date', title='Data', axis=alt.Axis(format="%d/%m/%Y")),
    y=alt.Y('Premium $', title='Prêmio ($/boe)', scale=alt.Scale(zero=False)),
    tooltip=[
        # CORREÇÃO DA FORMATAÇÃO:
        alt.Tooltip('Date', title='Data', format='%d/%m/%Y'), 
        alt.Tooltip('Premium $', title='Prêmio ($/boe)', format=',.2f')
    ]
).interactive()
st.altair_chart(chart_boe, width='stretch')


# Gráfico 2: Prêmio (%)
st.markdown("<h3 style='text-align: center;'>Prêmio (%)</h3>", unsafe_allow_html=True)
chart_perc = alt.Chart(df_chart).mark_line(point=True, color='orange').encode(
    # CORREÇÃO DA FORMATAÇÃO:
    x=alt.X('Date', title='Data', axis=alt.Axis(format="%d/%m/%Y")),
    y=alt.Y('Premium %', title='Prêmio (%)', axis=alt.Axis(format='%')),
    tooltip=[
        # CORREÇÃO DA FORMATAÇÃO:
        alt.Tooltip('Date', title='Data', format='%d/%m/%Y'), 
        alt.Tooltip('Premium %', title='Prêmio (%)', format='.2%')
    ]
).interactive()
st.altair_chart(chart_perc, width='stretch')


with st.expander("Ver dados brutos completos"):
    st.dataframe(df_comparison, width='stretch')
