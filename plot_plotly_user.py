import pandas as pd
import plotly.graph_objs as go
import prophet.forecaster
from prediction import predict


class PlotPlotly:
    def __init__(self):
        self.prediction_color = '#5DF909'
        self.error_color = 'rgba(0, 114, 178, 0.5)'  # '#0072B2' with 0.2 opacity
        self.actual_color = '#270082'
        self.trend_color = '#B23B00'
        self.line_width = 2
        self.marker_size = 4
        self.layout = dict(
            template='plotly_dark',
            showlegend=False,
            yaxis=dict(
                title='Stock Prices'
            ),
            xaxis=dict(
                title='Date',
                type='date',
                rangeslider=dict(
                    visible=False
                ),
            ),
        )

    def plotting_data(self, df: pd.DataFrame):
        data = [go.Candlestick(x=df['Date'],
                               open=df['Open_Price'],
                               high=df['High_Price'],
                               low=df['Low_Price'],
                               close=df['Close_Price'])]
        fig = go.Figure(data=data, layout=self.layout)

        return fig


class ModelPlotPlotly(PlotPlotly):

    def __init__(self):
        super().__init__()

    def plot_plotly(self, model: prophet.forecaster.Prophet, uncertainty=False, trend=False):

        fcst = predict(model, model.make_future_dataframe(periods=365))

        data = [go.Scatter(
            name='Actual',
            x=model.history['ds'],
            y=model.history['y'],
            marker=dict(color=self.actual_color, size=self.marker_size),
            mode='markers'
        )]
        # Add actual
        # Add lower bound
        if uncertainty and model.uncertainty_samples:
            data.append(go.Scatter(
                x=fcst['ds'],
                y=fcst['yhat_lower'],
                mode='lines',
                line=dict(width=0),
                hoverinfo='skip'
            ))
        # Add prediction
        data.append(go.Scatter(
            name='Predicted',
            x=fcst['ds'],
            y=fcst['yhat'],
            mode='lines',
            line=dict(color=self.prediction_color, width=self.line_width),
            fillcolor=self.error_color,
            fill='tonexty' if uncertainty and model.uncertainty_samples else 'none'
        ))
        # Add upper bound
        if uncertainty and model.uncertainty_samples:
            data.append(go.Scatter(
                x=fcst['ds'],
                y=fcst['yhat_upper'],
                mode='lines',
                line=dict(width=0),
                fillcolor=self.error_color,
                fill='tonexty',
                hoverinfo='skip'
            ))
        # Add trend
        if trend:
            data.append(go.Scatter(
                name='Trend',
                x=fcst['ds'],
                y=fcst['trend'],
                mode='lines',
                line=dict(color=self.trend_color, width=self.line_width),
            ))

        fig = go.Figure(data=data, layout=self.layout)
        return fig
