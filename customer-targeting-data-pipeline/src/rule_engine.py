import pandas as pd
import joblib
import os
from pyke import knowledge_engine, krb_traceback

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
    return df.loc[:, features]

def init_knowledge_engine():
    try:
        engine = knowledge_engine.engine(__file__)
        engine.load_krb_files(['./forward_rules.krb', './backward_rules.krb'])
        engine.activate('forward_chaining')
        return engine
    except Exception as e:
        print("Failed to initialize the Pyke knowledge engine:", e)
        krb_traceback.print_exc()
        raise

def assert_facts(engine, data, predictions):
    """Asserts necessary facts into the Pyke knowledge engine."""
    for idx, prediction in enumerate(predictions):
        customer = data.iloc[idx]
        engine.assert_('context', 'customer', (customer['customer_id'], prediction, customer['total_spent'], customer['transaction_count'], customer['age']))

def activate_rules(engine):
    """Activates the rule engine and returns the results."""
    try:
        engine.activate('forward_chaining')
        results = list(engine.prove_1_goal('backward_chaining.check_discount_eligibility($customer_id, $campaign)'))
        return {fact[1][0]: fact[1][1] for fact in results}
    except:
        krb_traceback.print_exc()
        exit(1)

def save_results(data, results, output_dir, filename):
    """Save the campaign results along with customer ID to a CSV file."""
    result_df = pd.DataFrame({
        'customer_id': data['customer_id'],
        'campaign_result': [results.get(cid, 'Standard Campaign') for cid in data['customer_id']]
    })
    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, filename)
    result_df.to_csv(output_path, index=False)
    print(f"Results saved to {output_path}")

if __name__ == "__main__":
    engine = init_knowledge_engine()
    model_path = '/app/models/customer_segmentation_model.joblib'
    data_path = '/app/data/processed_customer_data.csv'
    model, features_required = load_model(model_path)
    data = pd.read_csv(data_path)
    data_prepared = prepare_data(data, features_required)
    
    predictions = model.predict(data_prepared)
    assert_facts(engine, data_prepared, predictions)
    campaign_results = activate_rules(engine)
    
    save_results(data_prepared, campaign_results, '/app/data/output', 'campaign_results.csv')

