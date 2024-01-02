import pandas as pd
import numpy as np
from statsmodels.tsa.api import VAR
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import python_scripts.data_handling.data_handler as dd
import python_scripts.analysis.fourier as ff
from sklearn.preprocessing import StandardScaler

file_path = "src/data/daten.csv"
user_data = pd.read_csv(file_path, decimal=',')
columns = dd.get_column_names(user_data)
start_date = "2021-02-01"
end_date = "2021-02-15"

# Select the specified column
# Convert timestamps to datetime objects
timestamps = pd.to_datetime(user_data['timestamp'])
dataList = []


for i in range(len(columns)-2):
    
    # Filter data based on the specified date range
    mask = (timestamps >= start_date) & (timestamps <= end_date)
    
    # Select the column and reset the index
    column_values = user_data.loc[mask, columns[i]].reset_index(drop=True)
    
    # Append the selected column to the list
    dataList.append(column_values)

# Convert the list of selected columns to a NumPy array
data = np.array(dataList).T  # Transpose to get the desired shape

# Create a dataframe with the column names
columns = [f'Signal_{i}' for i in range(1, 14)]
df = pd.DataFrame(data, columns=columns)
print(df)

# Fraction of observations to be considered as anomalies.
outliers_fraction = 0.01

# Estimation of VAR Model
correlation_matrix = df.corr()
print(correlation_matrix)
model = VAR(df)
results = model.fit()

# Recover residuals from the VAR model
residuals = results.resid

# Check residue length
min_length = min(len(residuals), len(df))

# Apply Isolation Forest to residues
scaler = StandardScaler()
residuals_scaled = scaler.fit_transform(residuals.iloc[:min_length, :])  # Utilisez seulement les résidus disponibles
isolation_forest = IsolationForest(contamination=outliers_fraction)
outlier_labels = isolation_forest.fit_predict(residuals_scaled)

# Adding an 'Anomaly' column to the DataFrame
df['Anomaly'] = 0
df['Anomaly'].iloc[:min_length] = np.where(outlier_labels == -1, 1, 0)

# Signal plot with red dots for anomalies
plt.figure(figsize=(12, 8))

for i in range(13):
    plt.subplot(13, 1, i+1)
    plt.plot(df.index, df[f'Signal_{i+1}'], label=f'Signal_{i+1}')
    anomalies = df[df['Anomaly'] == 1]
    plt.scatter(anomalies.index, anomalies[f'Signal_{i+1}'], color='red', label='Anomaly', marker='o')
    plt.legend()
    plt.title(f'Signal_{i+1} with Anomalies')

plt.tight_layout()
plt.show()

for i in range(13):
    plt.subplot(1, 1, 1)  # Vous pouvez ajuster le nombre de lignes et de colonnes selon vos besoins
    plt.plot(df.index, df[f'Signal_{i+1}'], label=f'Signal_{i+1}')
    anomalies = df[df['Anomaly'] == 1]
    plt.scatter(anomalies.index, anomalies[f'Signal_{i+1}'], color='red', label='Anomaly', marker='o')
    plt.legend()
    plt.title(f'Signal_{i+1} with Anomalies')
    plt.show()