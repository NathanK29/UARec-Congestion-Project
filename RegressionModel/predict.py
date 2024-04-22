import request
from datetime import datetime
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures 
import matplotlib.pyplot as plt

# Data fetching
req = request.Request()
req.fetch()
data = req.images

filtered_data = [[] for _ in range(7)]
for item in data:
    date_obj = datetime.strptime(item['date'], '%Y-%m-%d')
    time_obj = datetime.strptime(item['time'], "%H:%M:%S.%f")
    formatted_time = time_obj.strftime("%H:%M")
    filtered_data[date_obj.weekday()].append((formatted_time, item['count']))

# Train a model for each day
models = []
poly_features_list = []
for day_data in filtered_data:
    df = pd.DataFrame(day_data, columns=['Time', 'Count'])
    df['Time'] = pd.to_datetime(df['Time'], format='%H:%M').dt.time
    df['Minutes'] = df['Time'].apply(lambda t: t.hour * 60 + t.minute)
    df.sort_values(by='Time', inplace=True)

    poly_features = PolynomialFeatures(degree=2, include_bias=False)
    X_poly = poly_features.fit_transform(df[['Minutes']])
    y = df['Count']
    
    reg = LinearRegression()
    reg.fit(X_poly, y)
    
    models.append(reg)
    poly_features_list.append(poly_features)

def predict_congestion(day, time_str, poly_features_list, models):
    time_obj = datetime.strptime(time_str, "%H:%M").time()
    minutes = time_obj.hour * 60 + time_obj.minute
    minutes_poly = poly_features_list[day].transform([[minutes]])
    prediction = models[day].predict(minutes_poly)
    return prediction[0]

day = 0
time_input = "21:30"
predicted_count = predict_congestion(day, time_input, poly_features_list, models)
print(f"Predicted congestion for Monday at {time_input}: {predicted_count:.2f}")
