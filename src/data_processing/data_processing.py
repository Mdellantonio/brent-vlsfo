from src.utils.singapore_vlsfo_scraping import processar_tabela_singapore_VLSFO
from src.utils.yfinance_client import get_ticker_history

import pandas as pd
from datetime import datetime

BUNKER_BBL_PER_MT = 6.35

df_vlsfo = processar_tabela_singapore_VLSFO()
df_brent = pd.DataFrame()
df_comparison = pd.DataFrame()

if df_vlsfo is not None and not df_vlsfo.empty:

    latest_update: datetime = df_vlsfo['Date'].max().to_pydatetime()
    oldest_update: datetime = df_vlsfo['Date'].min().to_pydatetime()

    df_vlsfo['Price $/boe'] = df_vlsfo['Price $/mt'] / BUNKER_BBL_PER_MT
    df_vlsfo['Date'] = pd.to_datetime(df_vlsfo['Date'])
    df_vlsfo = df_vlsfo.set_index('Date')

    df_brent = get_ticker_history(
        ticker_symbol='BZ=F',
        data_inicial=oldest_update,
        data_final=None
    )
    if df_brent is not None:
        df_brent.index = pd.to_datetime(df_brent.index).tz_localize(None).normalize()
        df_brent.index.name = 'Date'

        df_comparison = df_brent[['Close']].join(df_vlsfo[['Price $/boe']], how='inner')
        df_comparison.rename(columns={'Close': 'Brent Close', 'Price $/boe': 'VLSFO Close'}, inplace=True)
        df_comparison['Premium %'] = df_comparison['VLSFO Close'] / df_comparison['Brent Close'] -1
        df_comparison['Premium $'] = df_comparison['VLSFO Close'] - df_comparison['Brent Close'] 

else:
    print('Aviso: Dados do VLSFO não puderam ser carregados.')


if __name__ == '__main__':
    print(df_brent)
    print(df_vlsfo)
    print(df_comparison)
