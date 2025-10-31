from functools import lru_cache
from typing import Optional
import requests
import pandas as pd
import numpy as np
from io import StringIO


lru_cache()
def obter_tabela_singapore_VLSFO() -> Optional[pd.DataFrame]:
    base_url = 'https://shipandbunker.com/prices/apac/sea/sg-sin-singapore'
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    try:
        response = requests.get(base_url, headers=headers, timeout=15)
        response.raise_for_status()
        response.encoding = 'latin1'

        tables = pd.read_html(
            StringIO(response.text),
            attrs={'class': 'price-table VLSFO'}
        )

        if not tables:
            print("Erro: Tabela com class='price-table VLSFO' não encontrada.")
            return None

        return tables[0]

    except requests.RequestException as e:
        print(f'Erro de rede/HTPP: {e}')
        return None
    except ValueError as e:
        print(f'Erro de parsing (pandas): {e}')
        return None
    except Exception as e:
        print(f'Erro inesperado: {e}')

def processar_tabela_singapore_VLSFO():
    df_result = obter_tabela_singapore_VLSFO()
    if df_result is None:
        raise ValueError('Falha ao processar a tabela VLSFO. Retorno Nulo.')

    df_data: pd.DataFrame = df_result

    cleander_dates_str = df_data['Date'].str.strip().str[2:]

    today = pd.Timestamp.now().normalize()
    current_year = today.year

    dates_with_current_year = pd.to_datetime(
        cleander_dates_str + f" {current_year}",
        format="%b %d %Y"
    )

    dates_with_previous_year = pd.to_datetime(
        cleander_dates_str + f" {current_year-1}",
        format="%b %d %Y"
    )

    df_data['Date'] = np.where(
        dates_with_current_year > today,
        dates_with_previous_year, # Se verdadeiro
        dates_with_current_year # Se falso
    )

    return df_data


if __name__ == '__main__':
    df_vlsfo = processar_tabela_singapore_VLSFO()

    if df_vlsfo is not None:
        print(df_vlsfo.head())
    else:
        print(f'Falha ao extrair a tabela VLSFO.')
