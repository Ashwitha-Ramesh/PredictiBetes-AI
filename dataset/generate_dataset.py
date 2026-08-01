import os
import numpy as np
import pandas as pd

def generate_diabetes_dataset(filename="dataset/diabetes.csv", num_samples=768, seed=42):
    np.random.seed(seed)
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    
    # Target distribution: ~35% diabetic (Outcome = 1)
    outcome = np.random.choice([0, 1], size=num_samples, p=[0.65, 0.35])
    
    # Feature distributions conditioned on outcome to maintain correlation
    age = np.where(
        outcome == 1,
        np.random.normal(37, 10.5, num_samples),
        np.random.normal(31, 10.0, num_samples)
    ).astype(int)
    age = np.clip(age, 21, 81)
    
    pregnancies = np.where(
        outcome == 1,
        np.random.poisson(4.8, num_samples),
        np.random.poisson(3.2, num_samples)
    )
    pregnancies = np.clip(pregnancies, 0, 17)
    
    # Glucose: Normal (70-130), Diabetic (110-199)
    glucose = np.where(
        outcome == 1,
        np.random.normal(142, 29, num_samples),
        np.random.normal(110, 24, num_samples)
    ).astype(int)
    glucose = np.clip(glucose, 50, 199)
    # Add ~1% zero missing values (typical of Pima dataset)
    glucose[np.random.choice(num_samples, int(num_samples * 0.007), replace=False)] = 0
    
    # Blood Pressure
    bp = np.where(
        outcome == 1,
        np.random.normal(74, 12, num_samples),
        np.random.normal(68, 11, num_samples)
    ).astype(int)
    bp = np.clip(bp, 40, 122)
    bp[np.random.choice(num_samples, int(num_samples * 0.045), replace=False)] = 0
    
    # Skin Thickness
    skin = np.where(
        outcome == 1,
        np.random.normal(25, 11, num_samples),
        np.random.normal(20, 10, num_samples)
    ).astype(int)
    skin = np.clip(skin, 10, 99)
    skin[np.random.choice(num_samples, int(num_samples * 0.297), replace=False)] = 0
    
    # Insulin
    insulin = np.where(
        outcome == 1,
        np.random.normal(100, 75, num_samples),
        np.random.normal(68, 55, num_samples)
    ).astype(int)
    insulin = np.clip(insulin, 15, 846)
    insulin[np.random.choice(num_samples, int(num_samples * 0.487), replace=False)] = 0
    
    # BMI
    bmi = np.where(
        outcome == 1,
        np.random.normal(35.3, 6.5, num_samples),
        np.random.normal(30.3, 6.2, num_samples)
    )
    bmi = np.round(np.clip(bmi, 18.2, 67.1), 1)
    bmi[np.random.choice(num_samples, int(num_samples * 0.014), replace=False)] = 0.0
    
    # Diabetes Pedigree Function
    dpf = np.where(
        outcome == 1,
        np.random.gamma(2.5, 0.22, num_samples),
        np.random.gamma(2.0, 0.20, num_samples)
    )
    dpf = np.round(np.clip(dpf, 0.078, 2.42), 3)
    
    df = pd.DataFrame({
        'Pregnancies': pregnancies,
        'Glucose': glucose,
        'BloodPressure': bp,
        'SkinThickness': skin,
        'Insulin': insulin,
        'BMI': bmi,
        'DiabetesPedigreeFunction': dpf,
        'Age': age,
        'Outcome': outcome
    })
    
    df.to_csv(filename, index=False)
    print(f"Dataset generated with shape {df.shape} at {filename}")

if __name__ == '__main__':
    generate_diabetes_dataset()
