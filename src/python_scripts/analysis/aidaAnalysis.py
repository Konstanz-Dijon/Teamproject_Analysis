## Aida's code
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np


#from statsmodels.tsa.stattools import grangercausalitytests
#from statsmodels.tsa.stattools import adfuller
#import statsmodels.api as sm
#from statsmodels.tsa.api import VAR

mpl.rcParams['figure.figsize'] = (10,8)
mpl.rcParams['axes.grid'] = False

df = pd.read_csv('src/data/daten.csv')
df['timestamp'] = pd.to_datetime(df['timestamp'])
#df.set_index('timestamp', inplace=True)


numeric_columns = [
    "RM_ERRECHNETE_RAUMTEMPERATUR_DSP_POINT_ID_Value",
    "RM_RBG_RAUMTEMPERATUR_POINT_ID_Value",
    "RM_ANSTEUERUNG_DSP_VENTIL_POINT_ID_Value",
    "DSP_FLOOR_DISTRIBUTOR_DURCHFLUSS_EQUIPMENT_ID_Value",
    "DSP_FLOOR_DISTRIBUTOR_RUECKLAUFTEMPERATUR_EQUIPMENT_ID_Value",
    "DSP_FLOOR_DISTRIBUTOR_VORLAUFTEMPERATUR_EQUIPMENT_ID_Value",
    "DSP_FLOOR_DISTRIBUTOR_LEISTUNG_EQUIPMENT_ID_Value",
    "DSP_HK_CIRCUIT_DURCHFLUSS_EQUIP_ID_Value",
    "DSP_HK_CIRCUIT_LEISTUNG_EQUIP_ID_Value",
    "DSP_KK_CIRCUIT__24A1_AUSSENTEMPERATUR_EQUIP_ID_Value",
    "DSP_KK_CIRCUIT_DS_VL_TEMPERATUR_EQUIP_ID_Value",
    "DSP_KK_CIRCUIT_DS_RL_TEMPERATUR_EQUIP_ID_Value",
    "DSP_KK_CIRCUIT_DS_VENTIL_V2_MISCHVENTIL__EQUIP_ID_Value",
    "sunhour_value"
]

for column in numeric_columns:
    df[column] = df[column].str.replace(',', '.').astype(float)


#split data into summer and winter
def divide_seasons(dataset, temp_column_name, summer_temp_threshold=19.2):
    result_df = dataset.copy()

    result_df['Season'] = result_df[temp_column_name].apply(
        lambda temp: 'Summer' if temp >= summer_temp_threshold else 'Winter'
    )

    summer_df = result_df[result_df['Season'] == 'Summer'].drop(columns=['Season'])
    winter_df = result_df[result_df['Season'] == 'Winter'].drop(columns=['Season'])

    return summer_df, winter_df

def get_seasons():
    summer_df, winter_df = divide_seasons(df, 'DSP_KK_CIRCUIT__24A1_AUSSENTEMPERATUR_EQUIP_ID_Value')
    return summer_df, winter_df

#summer_df, winter_df = divide_seasons(df, 'DSP_KK_CIRCUIT__24A1_AUSSENTEMPERATUR_EQUIP_ID_Value')


numeric_columns = [
    "RM_ERRECHNETE_RAUMTEMPERATUR_DSP_POINT_ID_Value",
    "RM_RBG_RAUMTEMPERATUR_POINT_ID_Value",
    "RM_ANSTEUERUNG_DSP_VENTIL_POINT_ID_Value",
    "DSP_FLOOR_DISTRIBUTOR_DURCHFLUSS_EQUIPMENT_ID_Value",
    "DSP_FLOOR_DISTRIBUTOR_RUECKLAUFTEMPERATUR_EQUIPMENT_ID_Value",
    "DSP_FLOOR_DISTRIBUTOR_VORLAUFTEMPERATUR_EQUIPMENT_ID_Value",
    "DSP_FLOOR_DISTRIBUTOR_LEISTUNG_EQUIPMENT_ID_Value",
    "DSP_HK_CIRCUIT_DURCHFLUSS_EQUIP_ID_Value",
    "DSP_HK_CIRCUIT_LEISTUNG_EQUIP_ID_Value",
    "DSP_KK_CIRCUIT__24A1_AUSSENTEMPERATUR_EQUIP_ID_Value",
    "DSP_KK_CIRCUIT_DS_VL_TEMPERATUR_EQUIP_ID_Value",
    "DSP_KK_CIRCUIT_DS_RL_TEMPERATUR_EQUIP_ID_Value",
    "DSP_KK_CIRCUIT_DS_VENTIL_V2_MISCHVENTIL__EQUIP_ID_Value",
    "sunhour_value"
]

# Ersetzen Sie ',' durch '.' und konvertieren Sie die Spalten in numerische Werte
# for column in numeric_columns:
#     df[column] = df[column].str.replace(',', '.').astype(float)

# color_list = [
#     "blue",
#     "orange",
#     "green",
#     "purple",
#     "brown",
#     "pink",
#     "gray",
#     "olive",
#     "cyan"
# ]


# def Visualize(data):
#     features = df.select_dtypes(include=[np.number]).columns.values
#     features_size = len(features)
    
#     # Berechne die Anzahl der Zeilen und Spalten für die Subplots
#     rows = int(np.ceil(features_size / 2))
#     cols = 2
    
#     # Erstelle Subplots
#     fig, axes = plt.subplots(nrows=rows, ncols=cols, figsize=(14, rows * 2), dpi=80, facecolor="w", edgecolor="k")

#     # Iteriere über die Features und plotte sie
#     for i in range(features_size):
#         row_index = i // cols
#         col_index = i % cols
#         key = features[i]
#         c = color_list[i % len(color_list)]
#         t_data = data[key]
        
#         # Zugriff auf das richtige Axes-Objekt
#         ax = axes[row_index, col_index]
        
#         # Plot
#         t_data.plot(ax=ax, color=c, title="{}".format(key), rot=25)
#         ax.legend([key])
    
#     # Justiere das Layout
#     plt.tight_layout()

# Visualize(df)


       



