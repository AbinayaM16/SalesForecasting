from flask import Flask, request,jsonify, send_file, make_response
from flask_cors import CORS
import os
import json
import pandas as pd
from prophet import Prophet
import matplotlib.pyplot as plt
from sklearn.metrics import mean_absolute_error, mean_absolute_percentage_error, mean_squared_error, accuracy_score
import base64

app = Flask(__name__)
CORS(app)

@app.route('/upload-csv', methods=['POST'])
def forecast():

    csv_file = request.files['salesDataset']
    frequency = request.form.get('frequency')
    forecast_period = request.form.get('forecastPeriod')
    filename = csv_file.filename
    filename_without_ext = os.path.splitext(filename)[0]

    filename = csv_file.filename
    filepath = os.path.join(app.root_path, filename)
    csv_file.save(filepath)

    # cleaning the dataset
    df = pd.read_csv(filepath,  encoding='ISO-8859-1')
    df.dropna(inplace=True)
    
    print(df.columns)
    df = df.loc[:, ['date', 'sales']]
    df.rename(columns={'date': 'ds', 'sales': 'y'}, inplace=True)
    df['ds'] = pd.to_datetime(df['ds'])
    df['year'] = df['ds'].dt.year
    df.sort_values(by='ds', ascending=True, inplace=True)

    if frequency == 'daily':
            time_freq = 'D'
    elif frequency == 'weekly':
            time_freq = 'W'
    elif frequency == 'monthly':
            time_freq = 'M'
    elif frequency == 'yearly':
            time_freq = 'Y'
    else:
            raise ValueError('Invalid periodicity')


    #selecting some time period 
    forecast_data = df.tail(int(forecast_period))

    #train the model
    model = Prophet()
    model.fit(df.iloc[:-int(forecast_period)])

    try:
            # Predict the future sales using Prophet model
            future = model.make_future_dataframe(periods=int(forecast_period), freq=time_freq)
            forecast = model.predict(future)
            forecast = forecast.tail(int(forecast_period))
            forecast[['ds', 'yhat']].to_csv('predicted_sales.csv', index=False)

    except Exception as e:
            response = {'error': str(e)}
            return jsonify(response), 500

    # Filter the forecast to only include the time period of interest
    forecast = forecast.tail(int(forecast_period))

# Plot the forecast and actual sales
    fig, ax = plt.subplots()
    ax.plot(df['ds'], df['y'], label='Actual')
    ax.plot(forecast['ds'], forecast['yhat'], label='Forecast')
    ax.fill_between(forecast['ds'], forecast['yhat_lower'], forecast['yhat_upper'], alpha=0.3)
    ax.legend()
    
    # store the image in your directory
    plot_filename = "image.png"
    plot_filepath = os.path.join("C:/Users/91637/Documents/kaar-pro/angular-login/src/assets", plot_filename)
    plt.savefig(plot_filepath)
    
    
    # Calculate the model validation metrics
    y_true = forecast_data['y'].values
    y_pred = forecast['yhat'].values
    mape = mean_absolute_percentage_error(y_true, y_pred)
    rmse = mean_squared_error(y_true, y_pred, squared=False)
    mae = mean_absolute_error(y_true, y_pred)

    response = make_response(send_file(plot_filepath, mimetype='image/png'))
    response.headers['Content-Disposition'] = 'attachment; filename=image.png'
    print("hello")

    return send_file('C:/Users/91637/Documents/kaar-pro/angular-login/src/assets/image.png', mimetype='image/png')
    return {"src":"hello"}
if __name__ == '__main__':
    app.run(debug=True)
