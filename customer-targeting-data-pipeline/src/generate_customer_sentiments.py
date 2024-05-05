import pandas as pd
import numpy as np
from faker import Faker
from textblob import TextBlob

faker = Faker()

def generate_customer_data(num_records):
    # Create a DataFrame with customer demographic data
    customer_data = {
        'customer_id': range(1, num_records + 1),
        'age': np.random.randint(18, 70, num_records),
        'income': np.random.randint(30000, 100000, num_records),
        # Add more demographic fields as necessary
    }
    customer_df = pd.DataFrame(customer_data)

    # Generate psychographic data
    interests = ['health', 'technology', 'sports', 'fashion', 'travel']
    values = ['innovation', 'tradition', 'competition', 'creativity']

    customer_df['interests'] = [np.random.choice(interests) for _ in range(num_records)]
    customer_df['values'] = [np.random.choice(values) for _ in range(num_records)]

    # Generate sentiment data using text analysis on fake reviews
    customer_df['reviews'] = [faker.text() for _ in range(num_records)]
    customer_df['sentiment_score'] = customer_df['reviews'].apply(lambda review: TextBlob(review).sentiment.polarity)

    return customer_df

# Generate synthetic customer data
num_records = 1000  # Number of records you want to generate
customer_df = generate_customer_data(num_records)
customer_df.to_csv('generated_customer_data.csv', index=False)
