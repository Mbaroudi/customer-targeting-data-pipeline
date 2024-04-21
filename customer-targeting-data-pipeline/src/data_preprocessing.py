import pandas as pd
from sklearn.preprocessing import StandardScaler

def load_data(filepath):
    return pd.read_csv(filepath)

def preprocess_data(df):
    # Assume 'age' and 'income' need scaling
    scaler = StandardScaler()
    df[['age', 'income']] = scaler.fit_transform(df[['age', 'income']])
    return df

if __name__ == "__main__":
    data = load_data('../data/customer_data.csv')
    processed_data = preprocess_data(data)
    processed_data.to_csv('../data/processed_customer_data.csv', index=False)

