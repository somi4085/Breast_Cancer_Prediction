import pandas as pd
import pickle

from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression

# Load Dataset
data = load_breast_cancer()

df = pd.DataFrame(data.data, columns=data.feature_names)

# Selected Features
X = df[[
    'mean radius',
    'mean texture',
    'mean perimeter',
    'mean area',
    'mean smoothness',
    'worst radius'
]]

y = data.target

# Split Data
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

# Train Model
model = LogisticRegression(max_iter=10000)

model.fit(X_train, y_train)

# Save Model
pickle.dump(model, open("breast_model.pkl", "wb"))

print("Model Saved Successfully")