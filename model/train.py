import os
import joblib
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix

def train_and_save_model():
    print("Loading Iris dataset...")
    iris = load_iris()
    X, y = iris.data, iris.target
    feature_names = iris.feature_names
    target_names = list(iris.target_names)

    print(f"Features: {feature_names}")
    print(f"Classes: {target_names}")

    # Split dataset: 80% train, 20% test
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    # Train Random Forest Classifier
    print("Training Random Forest Classifier...")
    model = RandomForestClassifier(n_estimators=100, max_depth=4, random_state=42)
    model.fit(X_train, y_train)

    # Evaluate
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"\nModel Evaluation:")
    print(f"Accuracy: {accuracy * 100:.2f}%\n")
    print("Classification Report:")
    print(classification_report(y_test, y_pred, target_names=target_names))
    print("Confusion Matrix:")
    print(confusion_matrix(y_test, y_pred))

    # Package model with metadata
    model_artifact = {
        "model": model,
        "feature_names": feature_names,
        "target_names": target_names,
        "model_version": "1.0.0",
        "algorithm": "RandomForestClassifier",
        "accuracy": float(accuracy)
    }

    # Save artifact
    output_dir = os.path.dirname(os.path.abspath(__file__))
    model_path = os.path.join(output_dir, "iris_model.joblib")
    joblib.dump(model_artifact, model_path)
    print(f"\nModel saved successfully to: {model_path}")

    # Also save a copy inside app/ directory so the app container can access it directly
    app_dir = os.path.join(os.path.dirname(output_dir), "app")
    app_model_path = os.path.join(app_dir, "iris_model.joblib")
    joblib.dump(model_artifact, app_model_path)
    print(f"Model copy saved to: {app_model_path}")

if __name__ == "__main__":
    train_and_save_model()
