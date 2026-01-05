import pandas as pd
import pickle
from sklearn.ensemble import RandomForestRegressor
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer

# Load data
df = pd.read_csv('src/cars24_cleaned.csv')

# Load data and explicitly define column names to avoid hidden character issues
df = pd.read_csv('src/cars24_cleaned.csv')

# Standard names we want
std_columns = ['index', 'KM Driven', 'Fuel Type', 'Transmission Type', 'Ownership', 
               'Selling Price (in Lakhs)', 'Brand', 'Model_Only', 'Car Age']

# Force rename all columns based on order
if len(df.columns) == len(std_columns):
    df.columns = std_columns
else:
    print(f"Warning: Expected {len(std_columns)} columns, found {len(df.columns)}")
    # Just clean whatever we have
    df.columns = df.columns.str.replace('\r', '', regex=False).str.replace('\n', '', regex=False).str.strip()

# Numeric and categorical features (names now guaranteed to match app)
numeric_features = ['KM Driven', 'Ownership', 'Car Age']
categorical_features = ['Fuel Type', 'Transmission Type', 'Brand', 'Model_Only']
target = 'Selling Price (in Lakhs)'

X = df[numeric_features + categorical_features]
y = df[target]

print(f"Dataset Shape: {df.shape}")
print(f"Target Column: {target}")
print(f"Features: {X.columns.tolist()}")



# Preprocessor - must use 'num' and 'cat' as labels for naming consistency
preprocessor = ColumnTransformer(
    transformers=[
        ('num', StandardScaler(), numeric_features),
        ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_features)
    ]
)

# Pipeline - must use 'preprocessor' and 'regressor' as labels
pipeline = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('regressor', RandomForestRegressor(n_estimators=100, random_state=42))
])

# Fit the model
print("Training the model... please wait.")
pipeline.fit(X, y)

# Save the model pipeline
with open('src/car_price_predictor.pkl', 'wb') as f:
    pickle.dump(pipeline, f)

print("Model trained and successfully saved to src/car_price_predictor.pkl")
