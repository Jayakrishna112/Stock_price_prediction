from prophet import Prophet


class ModelTrainer:

    def __init__(self):
        self.daily_seasonality = False
        self.changepoint_prior_scale = 0.01
        self.holidays_prior_scale = 0.1
        self.seasonality_prior_scale = 1
        self.error = False

    def build_model(self, holidays):
        try:
            model = Prophet(holidays=holidays,
                            changepoint_prior_scale=self.changepoint_prior_scale,
                            daily_seasonality=self.daily_seasonality,
                            holidays_prior_scale=self.holidays_prior_scale,
                            seasonality_prior_scale=self.seasonality_prior_scale)
            self.error = False
            return model
        except Exception as e:
            self.error = True
            print(e, 24)

    def model_fit(self, model, data):
        try:
            data.drop(columns=['Open_Price', 'High_Price', 'Low_Price'], inplace=True)
            data.rename(columns={'Date': 'ds', 'Close_Price': 'y'}, inplace=True)
            if not self.error:
                model.fit(data)
                self.error = False

        except Exception as e:
            self.error = True
            print(e, 'jaya')
