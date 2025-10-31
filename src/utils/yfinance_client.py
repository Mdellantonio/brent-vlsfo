import yfinance as yf
import pandas as pd
from typing import List, Optional
from datetime import datetime


def get_ticker_history(ticker_symbol: str, data_inicial: Optional[datetime], data_final: Optional[datetime]) -> Optional[pd.DataFrame]:
    """
    Busca o histórico de cotações (OHLCV) para um ticker no Yahoo Finance.

    Se data_inicial ou data_final forem fornecidas, busca o intervalo específico.
    Se ambas forem None, busca o histórico completo.
    Se data_inicial for fornecida e data_final for None, busca de data_inicial até a data atual.

    Args:
        data_inicial: Data de Início (Opcional)
        data_final: Data de Fim (Opcional)
        ticker_symbol: O símbolo do ticker (ex: "BRAV3.SA", "MSFT").

    Returns:
        Um pandas.DataFrame com os dados históricos (OHLCV) ou None se o ticker for inválido ou a API falhar.
    """
    try:
        ticker = yf.Ticker(ticker_symbol)

        params = {
            'start': data_inicial,
            'end': data_final,
            'period': 'max' if data_inicial is None and data_final is None else None,
            'auto_adjust': True
        }

        if params['period'] is None:
            del params['period']

        data = ticker.history(**params)

        if data.empty:
            print(f'Aviso: Nenhum dado histórico encontrado para {ticker_symbol}')
            return None

        return data

    except Exception as e:
        print(f'Erro ao buscar dados para {ticker_symbol}: {e}')
        return None

def get_full_option_chain_long(ticker_symbol: str) -> Optional[pd.DataFrame]:
    """
    Busca a cadeia de opções completa (todas as calls e puts de todos os vencimentos futuros) para um ticker no Yahoo Finance, retorno no formato 'longo' (uma linha por contrato)

    Args:
        ticker_symbol: O símbolo do ticker (ex: 'MSFT')

    Returns:
        Um pandas.DataFrame contendo todas as opções com clunas adicionais 'expirationDate' e 'optionType' ('call' ou 'put'), ou None se nenhuma opção for encontrada.
    """
    try:
        ticker = yf.Ticker(ticker_symbol)
        expirations = ticker.options
        if not expirations:
            print(f'Aviso: Nenhuma data de vencimento encontrada para {ticker_symbol}.')
            return None

        all_options_list: List[pd.DataFrame] = []

        for exp_date in expirations:
            try:
                chain = ticker.option_chain(exp_date)
            except Exception as e:
                print(f'Aviso: Falha ao buscar cadeia para {exp_date}: {e}')
                continue

            if not chain.calls.empty:
                chain.calls['expirationDate'] = exp_date
                chain.calls['optionType'] = 'call'
                all_options_list.append(chain.calls)

            if not chain.puts.empty:
                chain.puts['expirationDate'] = exp_date
                chain.puts['OptionType'] = 'put'
                all_options_list.append(chain.puts)

            if not all_options_list:
                print(f'Aviso: A cadeia de opções estava vazia para {ticker_symbol}.')
                return None

            full_chain_df = pd.concat(all_options_list, ignore_index=True)
            return full_chain_df

    except Exception as e:
        print(f'Erro ao buscar dados de opção para {ticker_symbol}: {e}')
        return None

if __name__ == '__main__':
    ticker_brav3 = 'BRAV3.SA'
    data_inicial = datetime(day=10, month=10, year=2025)
    history = get_ticker_history(
        ticker_symbol=ticker_brav3,
        data_inicial=data_inicial,
        data_final=None
    )

    if history is not None:
        print(f'--- Histórico de {ticker_brav3} ---')
        print('Início dos Dados:')
        print(history.head())

        print('\nFim dos Dados:')
        print(history.tail())
    else:
        print(f'A consulta não retornou nada.')

