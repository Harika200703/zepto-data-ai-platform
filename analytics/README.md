# Titanic Data Analytics and Machine Learning

## Overview

This module performs exploratory data analysis and machine learning on the Titanic dataset.

## Contents

- `titanic.csv` — Offline fallback Titanic dataset
- `titanic_clean.csv` — Cleaned Titanic dataset
- `titanic_eda.ipynb` — Complete EDA and machine learning notebook
- `titanic_final_pipeline.joblib` — Saved tuned Random Forest pipeline

## Analysis Performed

### Exploratory Data Analysis

- Missing-value handling
- Duplicate checking
- Data type inspection
- Outlier detection using IQR
- Survival analysis by sex and passenger class
- Correlation analysis
- Multivariate visualizations
- Exploratory z-score standardization

### Machine Learning

The following classification models were trained and evaluated:

- Logistic Regression
- Decision Tree
- Random Forest

Evaluation metrics included:

- Accuracy
- Precision
- Recall
- F1-score
- ROC-AUC
- Confusion matrix

### Imbalance Handling

The following approaches were compared:

- Original models
- `class_weight="balanced"`
- SMOTE

### Hyperparameter Tuning

GridSearchCV was used to tune the Random Forest model.

The selected configuration was:

- `n_estimators = 100`
- `max_depth = 10`
- `max_features = sqrt`

The tuned model achieved an OOB score of `0.8062`.

### Regression

A multivariate Linear Regression model was trained to predict passenger fare.

Metrics reported:

- MAE
- RMSE
- R²
- Adjusted R²

## Running the Notebook

From the project root, activate the virtual environment:

```powershell
.\.venv\Scripts\Activate.ps1