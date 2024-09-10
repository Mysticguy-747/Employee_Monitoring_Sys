# Install the required libraries first:
# pip install pynput pandas scikit-learn

from pynput import mouse, keyboard
import pandas as pd
import numpy as np
import time
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
from datetime import datetime

# Data storage
mouse_data = []
keyboard_data = []

# File to log predictions
log_file = 'input_log.txt'

# Mouse Listener
def on_move(x, y):
    mouse_data.append(['move', x, y, time.time(), None, None])

def on_click(x, y, button, pressed):
    mouse_data.append(['click', x, y, time.time(), str(button), pressed])

def on_scroll(x, y, dx, dy):
    mouse_data.append(['scroll', x, y, time.time(), dx, dy])

# Keyboard Listener
def on_press(key):
    keyboard_data.append(['press', str(key), time.time()])

def on_release(key):
    keyboard_data.append(['release', str(key), time.time()])

# Start listeners
mouse_listener = mouse.Listener(on_move=on_move, on_click=on_click, on_scroll=on_scroll)
keyboard_listener = keyboard.Listener(on_press=on_press, on_release=on_release)

mouse_listener.start()
keyboard_listener.start()

try:
    print("Collecting data... Press Ctrl+C to stop.")
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    # Stop listeners
    mouse_listener.stop()
    keyboard_listener.stop()

    # Save the data to CSV files
    mouse_df = pd.DataFrame(mouse_data, columns=['action', 'x', 'y', 'timestamp', 'extra1', 'extra2'])
    keyboard_df = pd.DataFrame(keyboard_data, columns=['action', 'key', 'timestamp'])

    mouse_df.to_csv('mouse_data.csv', index=False)
    keyboard_df.to_csv('keyboard_data.csv', index=False)
    print("Data saved to 'mouse_data.csv' and 'keyboard_data.csv'.")

# Load the data
mouse_df = pd.read_csv('mouse_data.csv')
keyboard_df = pd.read_csv('keyboard_data.csv')

# Feature extraction function
def extract_mouse_features(df):
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s')
    df['time_diff'] = df['timestamp'].diff().dt.total_seconds().fillna(0)
    df['distance'] = np.sqrt(df['x'].diff()**2 + df['y'].diff()**2).fillna(0)
    df['speed'] = df['distance'] / df['time_diff'].replace(0, np.nan)
    return df[['speed']].fillna(0)

def extract_keyboard_features(df):
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s')
    df['time_diff'] = df['timestamp'].diff().dt.total_seconds().fillna(0)
    df['keypress_rate'] = 1 / df['time_diff'].replace(0, np.nan)
    return df[['keypress_rate']].fillna(0)

# Extract features
mouse_features = extract_mouse_features(mouse_df)
keyboard_features = extract_keyboard_features(keyboard_df)

# Save processed features
mouse_features.to_csv('mouse_features.csv', index=False)
keyboard_features.to_csv('keyboard_features.csv', index=False)
print("Features extracted and saved.")

# Mock function to generate synthetic data
def generate_synthetic_data(n_samples=1000):
    np.random.seed(42)
    data = {
        'speed': np.random.normal(0.5, 0.1, n_samples),  # Mouse speed
        'keypress_rate': np.random.normal(5, 2, n_samples),  # Key press rate
        'source': np.random.choice([0, 1], n_samples)  # 0 for user, 1 for application
    }
    return pd.DataFrame(data)

# Generate synthetic data
data = generate_synthetic_data()
X = data[['speed', 'keypress_rate']]
y = data['source']

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Train the model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Evaluate the model
y_pred = model.predict(X_test)
print("Accuracy:", accuracy_score(y_test, y_pred))
print("Classification Report:\n", classification_report(y_test, y_pred))

# Function to predict input source
def predict_input_source(mouse_speed, keypress_rate):
    input_features = pd.DataFrame([[mouse_speed, keypress_rate]], columns=['speed', 'keypress_rate'])
    prediction = model.predict(input_features)
    result = "Application Generated" if prediction[0] == 1 else "User Generated"
    
    # Log prediction with timestamp
    with open(log_file, 'a') as f:
        log_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"{log_time}: {result}\n")
    
    print(f"{log_time}: {result}")
    return result

# Simulating real-time predictions based on collected features
# This part can be integrated to run during data collection in a live system
for _, row in zip(mouse_features['speed'], keyboard_features['keypress_rate']):
    predict_input_source(row, row)  # Replace with real-time feature values

print(f"Input source logged in '{log_file}'.")
