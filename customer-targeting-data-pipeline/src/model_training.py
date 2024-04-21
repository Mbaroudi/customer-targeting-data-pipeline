from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import pandas as pd
import joblib
import os

def train_model(df, target_column):
    """Train a RandomForest model on the specified target with automatic preprocessing for categorical data."""
    
    # Handle date-time data by extracting useful components
    df['year_of_last_purchase'] = df['last_purchase_date'].dt.year
    df['month_of_last_purchase'] = df['last_purchase_date'].dt.month
    df['day_of_last_purchase'] = df['last_purchase_date'].dt.day

    # Remove the original datetime column to avoid issues during modeling
    df.drop(columns=['last_purchase_date'], inplace=True)

    # Setup predictors and response
    X = df.drop(target_column, axis=1)
    y = df[target_column]

    # Identify categorical columns for one-hot encoding
    categorical_cols = [col for col in X.columns if X[col].dtype == 'object']

    # Setup preprocessing pipeline for categorical data
    preprocessor = ColumnTransformer(
        transformers=[
            ('cat', OneHotEncoder(), categorical_cols)
        ], remainder='passthrough')

    # Combine preprocessing with RandomForest classifier in a pipeline
    pipeline = Pipeline([
        ('preprocessor', preprocessor),
        ('classifier', RandomForestClassifier(n_estimators=100, random_state=42))
    ])

    # Split data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Train the model
    pipeline.fit(X_train, y_train)

    return pipeline, X_train.columns.tolist()

def save_results(model, features, output_dir, filename):
    """Save the trained model and its feature names to disk."""
    os.makedirs(output_dir, exist_ok=True)
    model_path = os.path.join(output_dir, filename)
    joblib.dump({'model': model, 'features': features}, model_path)
    print(f"Model and features saved to {model_path}")

if __name__ == "__main__":
    # Path to the input data
    data_path = '../data/processed_customer_data.csv'
    output_dir = '../models'
    output_filename = 'customer_segmentation_model.joblib'

    # Load data
    df = pd.read_csv(data_path, parse_dates=['last_purchase_date'])

    # Train the model
    model, features = train_model(df, 'preferred_product_category')

    # Save the trained model and features
    save_results(model, features, output_dir, output_filename)

