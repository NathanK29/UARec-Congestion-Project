import request
from datetime import datetime, time
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures 

req = request.Request()
req.fetch()
data = req.images

filtered_data = [[],[],[],[],[],[],[]]
day = 0

for item in data:
    date = item['date']
    date_obj = datetime.strptime(date, '%Y-%m-%d')
    day_of_week = date_obj.weekday()
    
    time_string = item['time']
    time_object = datetime.strptime(time_string, "%H:%M:%S.%f")
    formatted_time = time_object.strftime("%H:%M")
        
    # Append to our list as a tuple (time, count)
    filtered_data[day_of_week].append((formatted_time, item['count']))

# Assuming 'filtered_data' is your list of tuples containing ('Time', 'Count')
df = pd.DataFrame(filtered_data[day], columns=['Time', 'Count'])
df = df.groupby('Time')['Count'].mean().reset_index()

# Convert 'Time' strings to datetime.time objects assuming they are already correctly formatted
df['Time'] = pd.to_datetime(df['Time'], format='%H:%M').dt.time
df['Minutes'] = df['Time'].apply(lambda t: t.hour * 60 + t.minute)

df.sort_values(by='Time', inplace=True)

poly_features = PolynomialFeatures(degree=3, include_bias=False)
X_poly = poly_features.fit_transform(df[['Minutes']])

y = df['Count']
reg = LinearRegression()
reg.fit(X_poly, y)

r_squared = reg.score(X_poly, y)
y_pred = reg.predict(X_poly)

# Plotting
plt.figure(figsize=(12, 6))
plt.scatter([t.strftime('%H:%M') for t in df['Time']], df['Count'], color='blue')

sorted_times = [t.strftime('%H:%M') for t in df.sort_values(by='Minutes')['Time']]
plt.plot([t.strftime('%H:%M') for t in df.sort_values(by='Minutes')['Time']], y_pred[df['Minutes'].argsort()], color='red', label=f'Regression Line (R² = {r_squared:.2f})')

plt.title('Congestion Count for Monday')
plt.xlabel('Time of Day')
plt.ylabel('Congestion Count')
tick_values = [time(hour=h).strftime('%H:%M') for h in range(6, 24)]
plt.xticks(tick_values, tick_values, rotation=45)  # Set both ticks and labels

plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()