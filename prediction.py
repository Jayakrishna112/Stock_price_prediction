import pandas as pd


def predict(m, df: pd.DataFrame = None, vectorized: bool = True) -> pd.DataFrame:
    if m.history is None:
        raise Exception('Model has not been fit.')
    if df is None:
        df = m.history.copy()
    else:
        if df.shape[0] == 0:
            raise ValueError('Dataframe has no rows.')
        df = m.setup_dataframe(df.copy())

    df['trend'] = m.predict_trend(df)
    seasonal_components = m.predict_seasonal_components(df)[['additive_terms']]
    if m.uncertainty_samples:
        intervals = m.predict_uncertainty(df, vectorized)[['yhat_lower', 'yhat_upper']]
    else:
        intervals = None
    cols = ['ds', 'trend']
    # Add in forecast components
    df2 = pd.concat((df[cols], intervals, seasonal_components), axis=1)
    df2['yhat'] = (
            df2['trend']
            + df2['additive_terms']
    )
    return df2
