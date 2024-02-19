from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from Scheduler import Scheduler, my_task
from plot_plotly_user import PlotPlotly, ModelPlotPlotly
import warnings

warnings.filterwarnings("ignore")

app = Flask(__name__)

scheduler = BackgroundScheduler()
scheduler.start()

my_schedule = Scheduler()

if my_schedule.df is None and my_schedule.model is None:
    my_schedule.pre_loader()

candle_plot = PlotPlotly()
predict_plot = ModelPlotPlotly()
fig1 = candle_plot.plotting_data(df=my_schedule.df).to_html(full_html=False)
fig2 = predict_plot.plot_plotly(my_schedule.model).to_html(full_html=False)


@app.route('/')
def index():
    global fig1, fig2
    if fig1 is None:
        fig1 = candle_plot.plotting_data(
            df=my_schedule.df).to_html(full_html=False)
    if fig2 is None:
        fig2 = predict_plot.plot_plotly(
            my_schedule.model).to_html(full_html=False)
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
            fig2 = predict_plot.plot_plotly(
                my_schedule.model, uncertainty=True, trend=True).to_html(full_html=False)

        if trend and not interval:
            fig2 = predict_plot.plot_plotly(
                my_schedule.model, uncertainty=False, trend=True).to_html(full_html=False)

        if not trend and interval:
            fig2 = predict_plot.plot_plotly(
                my_schedule.model, uncertainty=True, trend=False).to_html(full_html=False)

        return redirect(url_for('index'))


def generate_sitemap():
    urls = [
        {"loc": "https://stockpriceprediction.azurewebsites.net/", "priority": 0.8},
        # Add more URLs as needed
    ]
    current_date = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S+00:00")
    for url in urls:
        url["lastmod"] = current_date
    return render_template('sitemap.xml', urls=urls)


@app.route('/sitemap.xml', methods=['GET'])
def sitemap():
    return generate_sitemap()


@scheduler.scheduled_job('cron', id='my_scheduled_task', day_of_week='mon-fri', hour=17)
def scheduled_task():
    global fig1, fig2
    arg1 = my_schedule
    my_task(arg1)
    fig1 = candle_plot.plotting_data(
        df=my_schedule.df).to_html(full_html=False)
    fig2 = predict_plot.plot_plotly(my_schedule.model).to_html(full_html=False)
    generate_sitemap()


if __name__ == '__main__':
    app.run()
