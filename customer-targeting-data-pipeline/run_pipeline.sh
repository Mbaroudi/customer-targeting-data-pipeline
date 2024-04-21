#!/bin/bash

# Navigate to the src directory
cd src

# Execute Python scripts in the specified order
echo "Generating customer data..."
python generate_customer_data.py

echo "Preprocessing data..."
python data_preprocessing.py

echo "Training model..."
python model_training.py

echo "Applying rules and generating output..."
python rule_engine.py

# Display the top 10 lines of the output CSV
echo "Displaying the top 10 campaign results:"
head -10 ../data/output/campaign_results.csv

