import numpy as np
import pandas as pd
from datetime import datetime
import calendar
from dateutil.relativedelta import relativedelta
from flask import Flask,render_template,request

app = Flask(__name__)
   
@app.route('/', methods=['GET', 'POST'])
def input_page():
	if request.method == 'GET':
		return render_template('stock_main.html')
	else:
		ticker = request.form['ticker']
		date = datetime.strptime(request.form['date'], '%Y-%m-%d')
		result_df = read_result("news_result.csv")
		result_idx = locate_date(ticker, date, result_df)
		actual = translate_surprise(result_df.loc[result_idx, 'label'])
		forecast = translate_surprise(result_df.loc[result_idx, 'predict'])
		headlines = result_df.loc[result_idx, 'headlines']
		return render_template('result.html', actual=actual, forecast=forecast, headlines=headlines)

def locate_date(ticker, date, result_df):
	match = result_df[(result_df['TICKER'] == ticker) & \
					  (result_df['start_date'] <= date)]
	return int(match.index[-1]) + 1

def translate_surprise(label):
	if label == 1:
		return "Positive"
	elif label == -1:
		return "Negative"
	else:
		return "Hold"

def read_result(path):
	news_df = pd.read_csv(path, index_col=0)
	news_df.loc[:, 'start_date'] = pd.to_datetime(news_df.loc[:, 'start_date'], format='%Y/%m/%d')
	news_df.loc[:, 'end_date'] = pd.to_datetime(news_df.loc[:, 'end_date'], format='%Y/%m/%d')
	news_df = news_df.dropna()
	return news_df

if __name__ == "__main__":
	app.run(debug=True)


