from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report

# Load the generated customer data
customer_df = pd.read_csv('generated_customer_data.csv')

# Prepare your feature matrix `X` and target vector `y`
X = customer_df.drop(columns=['customer_id', 'reviews', 'sentiment_score'])
y = customer_df['sentiment_score'] > 0  # Example binary target: positive sentiment

# Encode categorical data and split into training and testing sets
X = pd.get_dummies(X, columns=['interests', 'values'])
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Train a Random Forest classifier
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Evaluate the model
predictions = model.predict(X_test)
print(classification_report(y_test, predictions))

# Save the trained model
joblib.dump(model, 'customer_sentiment_model.joblib')
