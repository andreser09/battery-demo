# Setup: Import libraries
import pandas as pd
import scipy.io as sio
from lifelines import CoxPHFitter
import pickle

# Step 1: Load the covariate data from .mat file
mat_data = sio.loadmat('covariates.mat')  # Path to your exported file
data_struct = mat_data['data_struct']

# Create DataFrame
df = pd.DataFrame({
    'DischargeTime': [row[0][3][0][0] for row in data_struct],  # DTime
    'Temperature': [row[0][0][0][0] for row in data_struct],
    'Load': [row[0][1][0][0] for row in data_struct],
    'Manufacturer': [row[0][2][0] for row in data_struct]
})
df['Manufacturer'] = df['Manufacturer'].astype('category')

# Step 2: Encode categorical variable (Manufacturer)
df_encoded = pd.get_dummies(df, columns=['Manufacturer'], drop_first=True)

# Step 3: Fit the Cox model
cph = CoxPHFitter()
cph.fit(df_encoded, duration_col='DischargeTime')  # No censoring assumed
# print("Model Summary:")
# cph.print_summary()

# Step 4: Save the model to a file
with open('battery_survival_model.pkl', 'wb') as f:
    pickle.dump(cph, f)
print("Model saved as 'battery_survival_model.pkl'")

def predict_remaining_life(test_data, model_path='battery_survival_model.pkl'):
    """
    Predicts remaining battery life given test data and a saved Cox model.

    Parameters:
    - test_data (dict or pd.DataFrame): Input with 'DischargeTime', 'Temperature',
      'Load', 'Manufacturer_B', 'Manufacturer_C' (e.g., {'DischargeTime': 30, ...}).
    - model_path (str): Path to the saved model file (default: 'battery_survival_model.pkl').

    Returns:
    - float: Remaining life in hours (median total life - current usage).
    """
    # Load the saved model
    with open(model_path, 'rb') as f:
        cph = pickle.load(f)

    # Convert test_data to DataFrame if it's a dict
    if isinstance(test_data, dict):
        test_df = pd.DataFrame([test_data])
    else:
        test_df = test_data

    # Ensure required columns are present
    required_cols = ['DischargeTime', 'Temperature', 'Load', 'Manufacturer_B', 'Manufacturer_C']
    for col in required_cols:
        if col not in test_df.columns:
            raise ValueError(f"Missing column: {col}")

    # Predict median life
    median_life = cph.predict_median(test_df)

    # Calculate remaining life
    remaining_life = median_life - test_df['DischargeTime'][0]

    return remaining_life

# Code to call API here: 
# need to call for a given timestamp the temperature reading and the power reading 
# need to call based on sensor_id the equipment_id and from that get the manufacturer data

# hs: the amount of hours the battery has been on since installation
# temperature: current temperature reading 
# load: current power reading
# manufacturer_B: 1 if it is 0 if it isn't
# manufacturer_C: 1 if it is 0 if it isn't

# EXAMPLE
test_input = {
    'Hs': 30,  # Hours used
    'Temperature': 60,    # °C
    'Load': 25,           # kW
    'Manufacturer_B': 1,  # Manufacturer B
    'Manufacturer_C': 0   # Not C 
}

remaining_life = predict_remaining_life(test_input)
print(f"Predicted Remaining Life: {remaining_life:.2f} hours")