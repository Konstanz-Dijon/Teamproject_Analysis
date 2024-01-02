import pandas as pd
from statsmodels.tsa.api import VAR
from statsmodels.tsa.stattools import adfuller
from python_scripts.analysis import aidaAnalysis as ad
# Function designed to check stationary of data
def check_stationarity(series):
    result = adfuller(series.dropna())
    return result[1] <= 0.05  # value of p TODO

# Function to determine the optimal number of LAGS based on AIC or BIC
def select_lags(data, max_lags, criterion='aic'):
    best_aic_bic = float('inf')
    best_lags = 0

    for lags in range(1, max_lags + 1):
        model = VAR(data)
        results = model.fit(lags)

        if criterion == 'aic':
            value = results.aic
        elif criterion == 'bic':
            value = results.bic
        else:
            raise ValueError("Invalid parameter. Choose 'aic' or 'bic'.")

        if value < best_aic_bic:
            best_aic_bic = value
            best_lags = lags

    return best_lags

# Load data
# path = "C:\\Users\\Viktoria Stiem\\Documents\\htwg Konstanz\\2324Wise\\teamprojekt\\Daten_pandas_2_weeks.csv"
dataframe, winterframe = ad.get_seasons;
dataframe['timestamp'] = pd.to_datetime(dataframe['timestamp'])

# Print data types before modification
print("Data Types Before:")
print(dataframe.dtypes)

# Check stationary and do transformation if needed
for column in dataframe.columns:
    if column != 'timestamp' and not check_stationarity(dataframe[column]):
        print(column, " is not stationary. Calculating discrete difference..")
        dataframe[column] = dataframe[column].diff().dropna()

# Separate timestamp column
timestamp_column = dataframe['timestamp']
dataframe = dataframe.drop('timestamp', axis=1)

# Drop non-numeric columns
dataframe = dataframe.select_dtypes(include='number')

# Print data types after modification
print("\nData Types After:")
print(dataframe.dtypes)

# Determine the optimal number of Lags based on AIC
optimal_lags_aic = select_lags(dataframe, max_lags=15, criterion='aic')

# Determine the optimal number of Lags based on BIC
optimal_lags_bic = select_lags(dataframe, max_lags=15, criterion='bic')

print(f"\nOptimal Number of Lags based on AIC: {optimal_lags_aic}")
print(f"\nOptimal Number of Lags based on BIC: {optimal_lags_bic}")

# Re-add timestamp column after fitting the VAR model
dataframe['timestamp'] = timestamp_column.diff().dropna()

# You can further process the dataframe as needed.
