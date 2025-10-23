import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
import joblib
import os
from django.conf import settings

class PerformancePredictor:
    def __init__(self):
        self.model = None
        self.is_trained = False
        
    def train_simple_model(self):
        """Train a simple ML model with sample data"""
        try:
            # Sample training data (hours, activity_percentage -> performance_score)
            X = np.array([
                [9, 95], [8.5, 90], [8, 85], [7.5, 80], [7, 75],
                [6.5, 70], [6, 65], [5.5, 60], [5, 55], [4, 50],
                [8, 90], [7, 80], [6, 70], [9, 80], [5, 90]
            ])
            
            # Corresponding performance scores
            y = np.array([9.2, 8.7, 8.1, 7.6, 7.0, 6.5, 6.0, 5.5, 5.0, 4.0, 8.5, 7.2, 6.3, 8.8, 5.8])
            
            # Train Random Forest model
            self.model = RandomForestRegressor(n_estimators=100, random_state=42)
            self.model.fit(X, y)
            self.is_trained = True
            
            # Save the model
            model_dir = os.path.join(settings.BASE_DIR, 'trained_models')
            os.makedirs(model_dir, exist_ok=True)
            joblib.dump(self.model, os.path.join(model_dir, 'performance_model.pkl'))
            
            print("✅ ML Model trained successfully!")
            return True
            
        except Exception as e:
            print(f"❌ Model training failed: {e}")
            return False
    
    def load_model(self):
        """Load the trained ML model"""
        try:
            model_path = os.path.join(settings.BASE_DIR, 'trained_models', 'performance_model.pkl')
            self.model = joblib.load(model_path)
            self.is_trained = True
            print("✅ ML Model loaded successfully!")
            return True
        except Exception as e:
            print(f"❌ Model loading failed: {e}")
            return False
    
    def predict(self, total_hours, activity_percentage):
        """Predict performance score using ML"""
        if not self.is_trained:
            # Try to load existing model first
            if not self.load_model():
                # If no model exists, train a new one
                print("🔄 Training new ML model...")
                self.train_simple_model()
        
        try:
            # Create feature array
            features = np.array([[total_hours, activity_percentage]])
            
            # Make prediction
            prediction = self.model.predict(features)[0]
            
            # Ensure score is between 0-10
            final_score = max(0, min(10, prediction))
            
            print(f"🎯 ML Prediction: {total_hours}h + {activity_percentage}% = {final_score:.2f}")
            return round(final_score, 2)
            
        except Exception as e:
            print(f"❌ Prediction failed: {e}")
            # Fallback to simple calculation
            return self.fallback_prediction(total_hours, activity_percentage)
    
    def fallback_prediction(self, total_hours, activity_percentage):
        """Fallback calculation if ML fails"""
        score = (total_hours / 10 * 4) + (activity_percentage / 100 * 6)
        return min(10, max(0, round(score, 2)))