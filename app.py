from flask import Flask, render_template, request, redirect, url_for
from flask_apscheduler import APScheduler
from Scheduler import Scheduler, my_task
from plot_plotly_user import PlotPlotly, ModelPlotPlotly
import warnings

warnings.filterwarnings("ignore")


app = Flask(__name__)

# Configure the Flask-APScheduler extension
app.config['SCHEDULER_API_ENABLED'] = True
scheduler = APScheduler()
scheduler.init_app(app)

my_schedule = Scheduler()

if my_schedule.df is None and my_schedule.model is None:
    my_task(my_schedule)

candle_plot = PlotPlotly()
predict_plot = ModelPlotPlotly()
fig1 = candle_plot.plotting_data(df=my_schedule.df).to_html(full_html=False)
fig2 = predict_plot.plot_plotly(my_schedule.model).to_html(full_html=False)


@app.route('/')
def index():
    global fig1, fig2
    if fig1 is None:
        fig1 = candle_plot.plotting_data(df=my_schedule.df).to_html(full_html=False)
    if fig2 is None:
        fig2 = predict_plot.plot_plotly(my_schedule.model).to_html(full_html=False)
    return render_template('index.html',
                           plot=fig1,
                           predicted=fig2)


@app.route('/details', methods=['POST'])
def detailer():
    global fig1, fig2
    if request.method == 'POST':
        trend = request.form.get('trend') == 'on'
        interval = request.form.get('intervals') == 'on'
        if trend and interval:
            fig2 = predict_plot.plot_plotly(my_schedule.model, uncertainty=True, trend=True).to_html(full_html=False)

        if trend and not interval:
            fig2 = predict_plot.plot_plotly(my_schedule.model, uncertainty=False, trend=True).to_html(full_html=False)

        if not trend and interval:
            fig2 = predict_plot.plot_plotly(my_schedule.model, uncertainty=True, trend=False).to_html(full_html=False)

        return redirect(url_for('index'))


@scheduler.task('cron', id='my_scheduled_task', day_of_week='mon-fri', hour=17)
def scheduled_task():
    arg1 = my_schedule  # Set your argument here
    my_task(arg1)


if __name__ == '__main__':
    app.run()
