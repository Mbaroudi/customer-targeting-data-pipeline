import pandas as pd
import joblib
import os

def load_model(model_path):
    """Load the joblib model and feature names safely."""
    loaded = joblib.load(model_path)
    if 'model' in loaded and 'features' in loaded:
        return loaded['model'], loaded['features']
    else:
        raise ValueError("Loaded data does not contain 'model' and 'features' keys")

def prepare_data(df, features):
    """Prepare the DataFrame to ensure it has the required features."""
    for feature in features:
        if feature not in df.columns:
            df[feature] = 0  # Defaulting to 0 for missing numeric features
    return df[features]

def apply_complex_rules(data, model):
    """Apply complex business rules to the predictions."""
    predictions = model.predict(data)
    results = []
    for idx, prediction in enumerate(predictions):
        customer = data.iloc[idx]
        if prediction == 1 and customer['total_spent'] > 10000:
            campaign = 'Platinum Campaign'
        elif prediction == 1 and customer['transaction_count'] > 15:
            campaign = 'Gold Campaign'
        elif customer['age'] < 30:
            campaign = 'Young Prospects Offer'
        elif customer['age'] > 50:
            campaign = 'Senior Loyalty Program'
        elif prediction == 1:
            campaign = 'Silver Campaign'
        else:
            campaign = 'Standard Campaign'
        results.append(campaign)
    return results

def save_results(data, results, output_dir, filename):
    """Save the campaign results along with customer ID to a CSV file."""
    result_df = pd.DataFrame({
        'customer_id': data['customer_id'],
        'campaign_result': results
    })
    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, filename)
    result_df.to_csv(output_path, index=False)
    print(f"Results saved to {output_path}")  # Corrected to use the defined variable


if __name__ == "__main__":
    model_path = '/app/models/customer_segmentation_model.joblib'
    data_path = '/app/data/processed_customer_data.csv'
    model, features_required = load_model(model_path)
    data = pd.read_csv(data_path)
    data_prepared = prepare_data(data, features_required)
    results = apply_complex_rules(data_prepared, model)
    save_results(data, results, '/app/data/output', 'campaign_results.csv')

