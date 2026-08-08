# CyberCortex AI - Machine Learning Architecture

## Overview

The ML architecture provides predictive capabilities for risk assessment and attack path prediction. It uses traditional ML models for interpretability and explainability, with the option to integrate deep learning models if needed.

## Design Principles

1. **Interpretability**: Models must be explainable to security analysts
2. **Performance**: Models must provide real-time or near-real-time predictions
3. **Accuracy**: Models must achieve meaningful accuracy on security data
4. **Extensibility**: Architecture must support adding new models
5. **Monitoring**: Model performance must be continuously monitored

## ML Pipeline Architecture

```
Data Collection
    ↓
Feature Engineering
    ↓
Model Training
    ↓
Model Evaluation
    ↓
Model Deployment
    ↓
Prediction Service
    ↓
Monitoring & Retraining
```

## ML Models

### 1. Risk Prediction Model

**Purpose**: Predict the risk level of security events, alerts, or incidents.

**Target Variable**: Risk score (0-100) or risk category (CRITICAL, HIGH, MEDIUM, LOW)

**Features**:

#### Temporal Features
- Time of day
- Day of week
- Time since last similar event
- Event frequency in time window

#### Source Features
- Source IP reputation
- Source geolocation
- Source type (internal/external)
- Source device criticality

#### Target Features
- Target asset criticality
- Target vulnerability exposure
- Target user role
- Target access level

#### Event Features
- Event type
- Event severity
- Protocol
- Port
- Payload size
- User agent

#### Context Features
- Number of related alerts
- MITRE technique severity
- IOC match count
- Threat intelligence score

#### Graph Features
- Node degree in knowledge graph
- Centrality measures
- Path length to critical assets
- Number of vulnerable connections

**Models**:

#### Baseline: Logistic Regression
```python
from sklearn.linear_model import LogisticRegression

class RiskLogisticRegression:
    def __init__(self):
        self.model = LogisticRegression(
            multi_class='multinomial',
            max_iter=1000,
            class_weight='balanced'
        )
    
    def train(self, X_train, y_train):
        self.model.fit(X_train, y_train)
    
    def predict(self, X):
        return self.model.predict(X)
    
    def predict_proba(self, X):
        return self.model.predict_proba(X)
    
    def get_feature_importance(self):
        return self.model.coef_
```

#### Advanced: Random Forest
```python
from sklearn.ensemble import RandomForestClassifier

class RiskRandomForest:
    def __init__(self):
        self.model = RandomForestClassifier(
            n_estimators=100,
            max_depth=10,
            class_weight='balanced',
            random_state=42
        )
    
    def train(self, X_train, y_train):
        self.model.fit(X_train, y_train)
    
    def predict(self, X):
        return self.model.predict(X)
    
    def predict_proba(self, X):
        return self.model.predict_proba(X)
    
    def get_feature_importance(self):
        return self.model.feature_importances_
```

#### Alternative: XGBoost
```python
from xgboost import XGBClassifier

class RiskXGBoost:
    def __init__(self):
        self.model = XGBClassifier(
            n_estimators=100,
            max_depth=6,
            learning_rate=0.1,
            objective='multi:softprob',
            num_class=4,
            random_state=42
        )
    
    def train(self, X_train, y_train):
        self.model.fit(X_train, y_train)
    
    def predict(self, X):
        return self.model.predict(X)
    
    def predict_proba(self, X):
        return self.model.predict_proba(X)
    
    def get_feature_importance(self):
        return self.model.feature_importances_
```

**Evaluation Metrics**:
- Accuracy
- Precision, Recall, F1-score (per class)
- Confusion matrix
- ROC-AUC (one-vs-rest)
- Log loss

---

### 2. Attack Path Prediction Model

**Purpose**: Predict the likelihood of attack progression and next likely attack stages.

**Target Variable**: Probability of attack stage progression (0-1)

**Features**:

#### Current State Features
- Current attack stage
- Time spent in current stage
- Number of compromised assets
- Lateral movement success rate

#### Path Features
- Path length to critical assets
- Number of available attack paths
- Path diversity
- Blast radius

#### Vulnerability Features
- Number of exploitable vulnerabilities
- Average CVSS score
- Exploit availability
- Patch coverage

#### Network Features
- Network segmentation
- Firewall rules
- Network topology complexity
- East-west traffic volume

#### Historical Features
- Historical attack success rate
- Similar attack patterns
- Attacker sophistication level
- Past attack duration

**Models**:

#### Baseline: Logistic Regression
```python
class AttackPathLogisticRegression:
    def __init__(self):
        self.model = LogisticRegression(
            max_iter=1000,
            class_weight='balanced'
        )
    
    def train(self, X_train, y_train):
        self.model.fit(X_train, y_train)
    
    def predict_progression_probability(self, X):
        return self.model.predict_proba(X)[:, 1]
    
    def predict_next_stage(self, X):
        # For multi-class next stage prediction
        return self.model.predict(X)
```

#### Advanced: Random Forest
```python
class AttackPathRandomForest:
    def __init__(self):
        self.model = RandomForestClassifier(
            n_estimators=100,
            max_depth=15,
            class_weight='balanced',
            random_state=42
        )
    
    def train(self, X_train, y_train):
        self.model.fit(X_train, y_train)
    
    def predict_progression_probability(self, X):
        return self.model.predict_proba(X)[:, 1]
    
    def predict_next_stage(self, X):
        return self.model.predict(X)
    
    def get_stage_probabilities(self, X):
        return self.model.predict_proba(X)
```

#### Sequence Model: LSTM (Optional for Advanced Use)
```python
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout

class AttackPathLSTM:
    def __init__(self, sequence_length=10, num_features=20, num_stages=7):
        self.model = Sequential([
            LSTM(128, input_shape=(sequence_length, num_features), return_sequences=True),
            Dropout(0.2),
            LSTM(64, return_sequences=False),
            Dropout(0.2),
            Dense(32, activation='relu'),
            Dense(num_stages, activation='softmax')
        ])
        self.model.compile(
            optimizer='adam',
            loss='categorical_crossentropy',
            metrics=['accuracy']
        )
    
    def train(self, X_train, y_train, epochs=50, batch_size=32):
        self.model.fit(X_train, y_train, epochs=epochs, batch_size=batch_size)
    
    def predict_next_stage(self, X_sequence):
        return self.model.predict(X_sequence)
```

**Attack Stage Mapping**:
```python
ATTACK_STAGES = {
    0: "RECONNAISSANCE",
    1: "INITIAL_ACCESS",
    2: "EXECUTION",
    3: "PERSISTENCE",
    4: "PRIVILEGE_ESCALATION",
    5: "DEFENSE_EVASION",
    6: "CREDENTIAL_ACCESS",
    7: "DISCOVERY",
    8: "LATERAL_MOVEMENT",
    9: "COLLECTION",
    10: "EXFILTRATION",
    11: "COMMAND_AND_CONTROL",
    12: "IMPACT"
}
```

**Evaluation Metrics**:
- Stage prediction accuracy
- Progression probability calibration
- Brier score
- Mean absolute error
- Stage ranking accuracy

---

### 3. Anomaly Detection Model (Optional)

**Purpose**: Detect anomalous behavior patterns in security events.

**Models**:

#### Isolation Forest
```python
from sklearn.ensemble import IsolationForest

class AnomalyIsolationForest:
    def __init__(self, contamination=0.1):
        self.model = IsolationForest(
            contamination=contamination,
            random_state=42
        )
    
    def train(self, X_train):
        self.model.fit(X_train)
    
    def predict_anomaly(self, X):
        # Returns -1 for anomaly, 1 for normal
        return self.model.predict(X)
    
    def get_anomaly_score(self, X):
        # Returns anomaly score (lower = more anomalous)
        return self.model.score_samples(X)
```

#### One-Class SVM
```python
from sklearn.svm import OneClassSVM

class AnomalyOneClassSVM:
    def __init__(self, nu=0.1):
        self.model = OneClassSVM(nu=nu)
    
    def train(self, X_train):
        self.model.fit(X_train)
    
    def predict_anomaly(self, X):
        return self.model.predict(X)
    
    def get_anomaly_score(self, X):
        return self.model.score_samples(X)
```

---

## Feature Engineering Pipeline

### 1. Feature Extraction

```python
class FeatureExtractor:
    def __init__(self):
        self.graph_client = None
        self.mongo_client = None
    
    def extract_temporal_features(self, event):
        """Extract temporal features from event"""
        pass
    
    def extract_source_features(self, event):
        """Extract source-related features"""
        pass
    
    def extract_target_features(self, event):
        """Extract target-related features"""
        pass
    
    def extract_graph_features(self, event):
        """Extract graph-based features"""
        pass
    
    def extract_context_features(self, event):
        """Extract context features"""
        pass
```

### 2. Feature Transformation

```python
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer

class FeatureTransformer:
    def __init__(self):
        self.preprocessor = ColumnTransformer(
            transformers=[
                ('num', StandardScaler(), numeric_features),
                ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_features)
            ]
        )
    
    def fit(self, X):
        self.preprocessor.fit(X)
    
    def transform(self, X):
        return self.preprocessor.transform(X)
```

### 3. Feature Selection

```python
from sklearn.feature_selection import SelectKBest, f_classif, RFE

class FeatureSelector:
    def __init__(self, method='univariate', k=20):
        self.method = method
        self.k = k
        if method == 'univariate':
            self.selector = SelectKBest(f_classif, k=k)
        elif method == 'rfe':
            self.selector = RFE(estimator=LogisticRegression(), n_features_to_select=k)
    
    def fit(self, X, y):
        self.selector.fit(X, y)
    
    def transform(self, X):
        return self.selector.transform(X)
    
    def get_selected_features(self, feature_names):
        return [feature_names[i] for i in self.selector.get_support(indices=True)]
```

---

## Training Pipeline

### 1. Data Collection

```python
class DataCollector:
    def __init__(self, mongo_client):
        self.mongo_client = mongo_client
    
    def collect_training_data(self, start_date, end_date):
        """Collect historical data for training"""
        pass
    
    def collect_labels(self, start_date, end_date):
        """Collect labels (risk scores, attack stages)"""
        pass
    
    def merge_features_labels(self, features, labels):
        """Merge features with labels"""
        pass
```

### 2. Data Preprocessing

```python
class DataPreprocessor:
    def __init__(self):
        pass
    
    def handle_missing_values(self, data):
        """Handle missing values"""
        pass
    
    def handle_outliers(self, data):
        """Handle outliers"""
        pass
    
    def balance_classes(self, X, y):
        """Balance imbalanced classes"""
        pass
    
    def split_train_test(self, X, y, test_size=0.2):
        """Split data into train and test sets"""
        pass
```

### 3. Model Training

```python
class ModelTrainer:
    def __init__(self, model_type='random_forest'):
        self.model_type = model_type
        self.model = self._get_model(model_type)
    
    def _get_model(self, model_type):
        """Initialize model based on type"""
        pass
    
    def train(self, X_train, y_train):
        """Train the model"""
        self.model.fit(X_train, y_train)
    
    def cross_validate(self, X, y, cv=5):
        """Perform cross-validation"""
        pass
```

### 4. Model Evaluation

```python
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.metrics import confusion_matrix, classification_report, roc_auc_score

class ModelEvaluator:
    def __init__(self):
        pass
    
    def evaluate_classification(self, y_true, y_pred, y_proba=None):
        """Evaluate classification model"""
        metrics = {
            'accuracy': accuracy_score(y_true, y_pred),
            'precision': precision_score(y_true, y_pred, average='weighted'),
            'recall': recall_score(y_true, y_pred, average='weighted'),
            'f1': f1_score(y_true, y_pred, average='weighted'),
            'confusion_matrix': confusion_matrix(y_true, y_pred),
            'classification_report': classification_report(y_true, y_pred)
        }
        if y_proba is not None:
            metrics['roc_auc'] = roc_auc_score(y_true, y_proba, multi_class='ovr')
        return metrics
    
    def evaluate_regression(self, y_true, y_pred):
        """Evaluate regression model"""
        from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
        return {
            'mse': mean_squared_error(y_true, y_pred),
            'mae': mean_absolute_error(y_true, y_pred),
            'r2': r2_score(y_true, y_pred)
        }
```

---

## Prediction Service

### 1. Risk Prediction Service

```python
class RiskPredictionService:
    def __init__(self, model, feature_extractor, feature_transformer):
        self.model = model
        self.feature_extractor = feature_extractor
        self.feature_transformer = feature_transformer
    
    async def predict_risk(self, event):
        """Predict risk score for an event"""
        # Extract features
        features = self.feature_extractor.extract_all(event)
        
        # Transform features
        features_transformed = self.feature_transformer.transform(features)
        
        # Predict
        risk_category = self.model.predict(features_transformed)[0]
        risk_probability = self.model.predict_proba(features_transformed)[0]
        
        return {
            'risk_category': risk_category,
            'risk_probability': risk_probability,
            'confidence': max(risk_probability)
        }
```

### 2. Attack Path Prediction Service

```python
class AttackPathPredictionService:
    def __init__(self, model, feature_extractor):
        self.model = model
        self.feature_extractor = feature_extractor
    
    async def predict_attack_progression(self, current_state):
        """Predict attack progression"""
        # Extract features
        features = self.feature_extractor.extract_attack_path_features(current_state)
        
        # Predict progression probability
        progression_prob = self.model.predict_progression_probability(features)
        
        # Predict next stage
        next_stage = self.model.predict_next_stage(features)
        
        # Get stage probabilities
        stage_probs = self.model.get_stage_probabilities(features)
        
        return {
            'progression_probability': progression_prob[0],
            'predicted_next_stage': next_stage[0],
            'stage_probabilities': stage_probs[0]
        }
```

---

## Model Monitoring

### 1. Performance Monitoring

```python
class ModelMonitor:
    def __init__(self):
        self.predictions = []
        self.actuals = []
    
    def log_prediction(self, prediction, actual):
        """Log prediction and actual value"""
        self.predictions.append(prediction)
        self.actuals.append(actual)
    
    def calculate_drift(self):
        """Calculate model drift"""
        pass
    
    def generate_report(self):
        """Generate performance report"""
        pass
```

### 2. Data Drift Detection

```python
from evidently import ColumnMapping
from evidently.report import Report
from evidently.metric_preset import DataDriftPreset

class DataDriftMonitor:
    def __init__(self):
        self.reference_data = None
        self.current_data = None
    
    def detect_drift(self, reference_data, current_data):
        """Detect data drift"""
        drift_report = Report(metrics=[DataDriftPreset()])
        drift_report.run(reference_data=reference_data, current_data=current_data)
        return drift_report
```

---

## Model Retraining Strategy

### 1. Scheduled Retraining
- Retrain models weekly/monthly
- Use latest data for training
- Evaluate new model before deployment

### 2. Triggered Retraining
- Retrain when performance drops below threshold
- Retrain when significant data drift detected
- Retrain when new attack patterns emerge

### 3. Continuous Learning (Optional)
- Online learning for incremental updates
- Active learning for label acquisition
- Human-in-the-loop for feedback

---

## Explainability

### 1. Feature Importance

```python
class ModelExplainer:
    def __init__(self, model):
        self.model = model
    
    def get_feature_importance(self):
        """Get feature importance from model"""
        if hasattr(self.model, 'feature_importances_'):
            return self.model.feature_importances_
        elif hasattr(self.model, 'coef_'):
            return abs(self.model.coef_[0])
        else:
            return None
    
    def explain_prediction(self, features):
        """Explain individual prediction"""
        pass
```

### 2. SHAP Values (Optional)

```python
import shap

class SHAPExplainer:
    def __init__(self, model, background_data):
        self.explainer = shap.TreeExplainer(model, background_data)
    
    def explain_prediction(self, instance):
        """Explain prediction using SHAP values"""
        shap_values = self.explainer.shap_values(instance)
        return shap_values
```

---

## Model Storage

### 1. Model Versioning

```python
import joblib
import os
from datetime import datetime

class ModelStorage:
    def __init__(self, storage_path='./models'):
        self.storage_path = storage_path
        os.makedirs(storage_path, exist_ok=True)
    
    def save_model(self, model, model_name, version):
        """Save model with version"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{model_name}_v{version}_{timestamp}.pkl"
        filepath = os.path.join(self.storage_path, filename)
        joblib.dump(model, filepath)
        return filepath
    
    def load_model(self, filepath):
        """Load model from file"""
        return joblib.load(filepath)
    
    def list_models(self, model_name):
        """List all versions of a model"""
        pass
```

---

## ML Configuration

### Model Configuration

```python
ML_CONFIG = {
    "risk_prediction": {
        "model_type": "random_forest",
        "features": {
            "temporal": True,
            "source": True,
            "target": True,
            "graph": True,
            "context": True
        },
        "hyperparameters": {
            "n_estimators": 100,
            "max_depth": 10,
            "min_samples_split": 5
        },
        "retraining_schedule": "weekly",
        "performance_threshold": 0.85
    },
    "attack_path_prediction": {
        "model_type": "random_forest",
        "features": {
            "current_state": True,
            "path": True,
            "vulnerability": True,
            "network": True,
            "historical": True
        },
        "hyperparameters": {
            "n_estimators": 100,
            "max_depth": 15,
            "min_samples_split": 5
        },
        "retraining_schedule": "monthly",
        "performance_threshold": 0.80
    }
}
```

---

## Integration with Agent Framework

### Agent-ML Integration

```python
class AgentWithML(BaseAgent):
    def __init__(self, name, ml_service):
        super().__init__(name)
        self.ml_service = ml_service
    
    async def analyze(self, context):
        """Analyze using ML predictions"""
        # Get ML predictions
        risk_prediction = await self.ml_service.predict_risk(context['event'])
        
        # Use predictions in analysis
        findings = self._analyze_with_predictions(context, risk_prediction)
        
        return findings
```

---

## Future Enhancements

### 1. Deep Learning Models
- Graph Neural Networks (GNNs) for knowledge graph analysis
- Transformers for sequence analysis
- Autoencoders for anomaly detection

### 2. Reinforcement Learning
- Automated response optimization
- Adaptive investigation strategies

### 3. Federated Learning
- Privacy-preserving model training
- Collaborative learning across organizations

### 4. Online Learning
- Incremental model updates
- Adaptation to new threats
