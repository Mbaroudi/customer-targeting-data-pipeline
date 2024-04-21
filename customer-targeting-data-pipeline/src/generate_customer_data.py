import pandas as pd
import numpy as np
import os
from faker import Faker

def generate_data(num_records):
    fake = Faker()
    Faker.seed(0)  # For reproducibility
    np.random.seed(0)

    # Define the categories for preferred_product_category
    product_categories = [
        'electronics', 'clothing', 'home_goods', 'books', 'beauty',
        'toys', 'jewelry', 'sports', 'outdoor', 'automotive',
        'office supplies', 'baby products', 'health', 'groceries',
        'pet supplies', 'footwear', 'apparel', 'garden', 'furniture',
        'software'
    ]

    # Additional features for customer analytics
    countries = ["USA", "Canada", "UK", "Germany", "France", "Australia"]
    days_of_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

    # Generate random dates within the last year
    dates = pd.date_range(start='2022-01-01', end='2022-12-31', periods=num_records)
    date_array = np.array(dates)  # Convert to numpy array for shuffling
    np.random.shuffle(date_array)  # Shuffle the array to ensure random distribution

    # Generate data
    data = {
        'customer_id': range(1, num_records + 1),
        'age': np.random.randint(18, 65, size=num_records),  # Ages between 18 and 65
        'income': np.random.randint(30000, 100000, size=num_records),  # Income between $30,000 and $100,000
        'transaction_count': np.random.randint(1, 10, size=num_records),  # Transaction count between 1 and 10
        'last_purchase_date': date_array,  # Use shuffled date array
        'preferred_product_category': np.random.choice(product_categories, num_records, replace=True),
        'total_spent': np.random.uniform(100, 10000, size=num_records),  # Total amount spent
        'country': np.random.choice(countries, num_records, replace=True),  # Customer's country
        'clv': np.random.uniform(1000, 50000, size=num_records)  # Simulated Customer Lifetime Value
    }

    # Convert dates to DataFrame to manipulate further
    df = pd.DataFrame(data)
    df['last_purchase_day_of_week'] = df['last_purchase_date'].dt.day_name()  # Get day name
    df['month_of_last_purchase'] = df['last_purchase_date'].dt.month  # Extract month from the last purchase date

    # Interaction terms
    df['income_per_transaction'] = df['income'] / df['transaction_count']  # Income distributed per transaction
    df['transactions_per_age_year'] = df['transaction_count'] / df['age']  # Transactions frequency relative to age

    return df

def save_data(df, directory, filename):
    # Check if the directory exists, if not, create it
    if not os.path.exists(directory):
        os.makedirs(directory)
    # Full path for the csv file
    full_path = os.path.join(directory, filename)
    df.to_csv(full_path, index=False)
    print(f"Generated data saved to '{full_path}'.")

if __name__ == "__main__":
    df = generate_data(10000)  # Generate 10,000 records
    save_data(df, '../data', 'customer_data.csv')  # Save the data to a CSV file in the specified directory

