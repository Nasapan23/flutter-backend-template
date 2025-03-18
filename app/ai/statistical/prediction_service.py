from typing import List, Dict, Any, Optional
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import joblib
import os
import asyncio
from pathlib import Path

# Define model storage directory
MODEL_DIR = Path("./models/statistical")
MODEL_DIR.mkdir(parents=True, exist_ok=True)


async def train_linear_regression(
    X_train: List[List[float]],
    y_train: List[float],
    model_name: str = "linear_regression"
) -> Dict[str, Any]:
    """
    Train a linear regression model
    """
    try:
        # Convert to numpy arrays
        X = np.array(X_train)
        y = np.array(y_train)
        
        # Train model in a separate thread
        loop = asyncio.get_event_loop()
        
        def _train_model():
            model = LinearRegression()
            model.fit(X, y)
            
            # Save the model
            model_path = MODEL_DIR / f"{model_name}.joblib"
            joblib.dump(model, model_path)
            
            # Get model metrics
            score = model.score(X, y)
            coef = model.coef_.tolist()
            intercept = float(model.intercept_)
            
            return {
                "model_name": model_name,
                "score": score,
                "coefficients": coef,
                "intercept": intercept,
                "model_path": str(model_path)
            }
        
        return await loop.run_in_executor(None, _train_model)
    
    except Exception as e:
        raise Exception(f"Error training linear regression model: {str(e)}")


async def predict_linear_regression(
    X_test: List[List[float]],
    model_name: str = "linear_regression"
) -> List[float]:
    """
    Make predictions with a trained linear regression model
    """
    try:
        # Convert to numpy array
        X = np.array(X_test)
        
        # Load model and predict in a separate thread
        loop = asyncio.get_event_loop()
        
        def _predict():
            model_path = MODEL_DIR / f"{model_name}.joblib"
            
            if not model_path.exists():
                raise FileNotFoundError(f"Model {model_name} not found")
            
            model = joblib.load(model_path)
            predictions = model.predict(X).tolist()
            
            return predictions
        
        return await loop.run_in_executor(None, _predict)
    
    except Exception as e:
        raise Exception(f"Error making predictions: {str(e)}")


async def perform_clustering(
    data: List[List[float]],
    n_clusters: int = 3,
    model_name: str = "kmeans_clustering"
) -> Dict[str, Any]:
    """
    Perform KMeans clustering on data
    """
    try:
        # Convert to numpy array
        X = np.array(data)
        
        # Perform clustering in a separate thread
        loop = asyncio.get_event_loop()
        
        def _cluster():
            # Standardize data
            scaler = StandardScaler()
            X_scaled = scaler.fit_transform(X)
            
            # Train KMeans model
            kmeans = KMeans(n_clusters=n_clusters, random_state=42)
            kmeans.fit(X_scaled)
            
            # Save models
            model_path = MODEL_DIR / f"{model_name}.joblib"
            scaler_path = MODEL_DIR / f"{model_name}_scaler.joblib"
            
            joblib.dump(kmeans, model_path)
            joblib.dump(scaler, scaler_path)
            
            # Get results
            labels = kmeans.labels_.tolist()
            centroids = kmeans.cluster_centers_.tolist()
            inertia = float(kmeans.inertia_)
            
            return {
                "model_name": model_name,
                "n_clusters": n_clusters,
                "labels": labels,
                "centroids": centroids,
                "inertia": inertia,
                "model_path": str(model_path)
            }
        
        return await loop.run_in_executor(None, _cluster)
    
    except Exception as e:
        raise Exception(f"Error performing clustering: {str(e)}")


async def analyze_timeseries(
    dates: List[str],
    values: List[float],
    freq: str = "D",
    periods_to_forecast: int = 10
) -> Dict[str, Any]:
    """
    Analyze and forecast time series data
    """
    try:
        # Process and forecast in a separate thread
        loop = asyncio.get_event_loop()
        
        def _analyze():
            # Create dataframe
            df = pd.DataFrame({"date": pd.to_datetime(dates), "value": values})
            df.set_index("date", inplace=True)
            
            # Resample to ensure regular time intervals
            df = df.resample(freq).mean()
            
            # Simple forecasting with linear regression
            df["time_idx"] = np.arange(len(df))
            model = LinearRegression()
            model.fit(df[["time_idx"]], df["value"])
            
            # Forecast future periods
            future_idx = np.arange(len(df), len(df) + periods_to_forecast)
            future_df = pd.DataFrame({"time_idx": future_idx})
            future_df["forecast"] = model.predict(future_df[["time_idx"]])
            
            # Calculate statistics
            mean = float(df["value"].mean())
            std = float(df["value"].std())
            min_val = float(df["value"].min())
            max_val = float(df["value"].max())
            
            return {
                "statistics": {
                    "mean": mean,
                    "std": std,
                    "min": min_val,
                    "max": max_val
                },
                "forecast": future_df["forecast"].tolist(),
                "forecast_dates": [
                    (df.index[-1] + pd.Timedelta(i + 1, unit=freq.lower())).strftime("%Y-%m-%d")
                    for i in range(periods_to_forecast)
                ]
            }
        
        return await loop.run_in_executor(None, _analyze)
    
    except Exception as e:
        raise Exception(f"Error analyzing time series: {str(e)}") 