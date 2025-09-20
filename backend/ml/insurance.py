import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def insur(val):
    # Load training data
    data = pd.read_csv(r"D:\Insurance\backend\ml\insurance.csv")
    
    # Split data
    from sklearn.model_selection import train_test_split
    train_set, test_set = train_test_split(data, test_size=0.2, random_state=42)
    
    X_train = train_set.drop('charges', axis=1)
    Y_train = train_set['charges']
    
    # Prepare training data
    from sklearn.preprocessing import LabelEncoder, StandardScaler
    
    # Encode categorical variables
    le_sex = LabelEncoder()
    le_smoker = LabelEncoder()
    le_region = LabelEncoder()
    
    X_train_processed = X_train.copy()
    X_train_processed['sex'] = le_sex.fit_transform(X_train['sex'])
    X_train_processed['smoker'] = le_smoker.fit_transform(X_train['smoker'])
    X_train_processed['region'] = le_region.fit_transform(X_train['region'])
    
    # Scale numerical features
    scaler = StandardScaler()
    X_train_processed[['age', 'bmi']] = scaler.fit_transform(X_train_processed[['age', 'bmi']])
    
    # Process input data the same way
    val_processed = val.copy()
    val_processed['sex'] = le_sex.transform([val['sex'].iloc[0]])
    val_processed['smoker'] = le_smoker.transform([val['smoker'].iloc[0]])
    val_processed['region'] = le_region.transform([val['region'].iloc[0]])
    val_processed[['age', 'bmi']] = scaler.transform(val_processed[['age', 'bmi']])
    
    # Train model
    from xgboost import XGBRegressor
    model = XGBRegressor(
        min_child_weight=5,
        n_estimators=51,
        learning_rate=0.1,
        random_state=42,
        max_depth=3,
        colsample_bytree=1
    )
    
    model.fit(X_train_processed, Y_train)
    
    # Make prediction
    prediction = model.predict(val_processed)
    
    return round(float(prediction[0]), 2)
