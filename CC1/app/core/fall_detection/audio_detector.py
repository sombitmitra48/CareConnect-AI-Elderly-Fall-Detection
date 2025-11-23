import numpy as np
import logging
from typing import Tuple, List

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Try to import required libraries, but make them optional
try:
    import librosa
    LIBROSA_AVAILABLE = True
except Exception as e:
    logger.warning(f"Librosa not available: {e}. Audio fall detection will be limited.")
    LIBROSA_AVAILABLE = False
    librosa = None

try:
    from sklearn.model_selection import train_test_split
    from sklearn.svm import SVC
    from sklearn.metrics import classification_report
    SKLEARN_AVAILABLE = True
except Exception as e:
    logger.warning(f"Scikit-learn not available: {e}. Audio fall detection will be limited.")
    SKLEARN_AVAILABLE = False
    train_test_split = None
    SVC = None
    classification_report = None

class AudioFallDetector:
    def __init__(self):
        """
        Initialize the AudioFallDetector with SVM classifier
        """
        if SKLEARN_AVAILABLE:
            self.model = SVC(kernel='rbf', probability=True)
        else:
            self.model = None
        self.is_trained = False
        self.sample_rate = 22050  # Standard sample rate
        self.n_mfcc = 13  # Number of MFCC features
        
        logger.info("AudioFallDetector initialized")

    def extract_features(self, audio_data: np.ndarray, sample_rate: int) -> np.ndarray:
        """
        Extract MFCC features from audio data
        
        Args:
            audio_data: Audio signal data
            sample_rate: Sample rate of the audio
            
        Returns:
            MFCC features
        """
        if not LIBROSA_AVAILABLE:
            logger.warning("Librosa not available, returning empty features")
            return np.array([])
            
        # Extract MFCC features
        mfccs = librosa.feature.mfcc(y=audio_data, sr=sample_rate, n_mfcc=self.n_mfcc)
        
        # Calculate mean and standard deviation of MFCCs
        mfccs_mean = np.mean(mfccs.T, axis=0)
        mfccs_std = np.std(mfccs.T, axis=0)
        
        # Combine mean and std features
        features = np.hstack((mfccs_mean, mfccs_std))
        
        return features

    def load_training_data(self, fall_audio_files: List[str], 
                          normal_audio_files: List[str]) -> Tuple[np.ndarray, np.ndarray]:
        """
        Load and preprocess training data
        
        Args:
            fall_audio_files: List of paths to fall sound audio files
            normal_audio_files: List of paths to normal sound audio files
            
        Returns:
            Tuple of (features, labels)
        """
        features = []
        labels = []
        
        # Load fall sound samples
        for file_path in fall_audio_files:
            try:
                audio_data, sr = librosa.load(file_path, sr=self.sample_rate)
                feature_vector = self.extract_features(audio_data, sr)
                features.append(feature_vector)
                labels.append(1)  # 1 for fall sound
            except Exception as e:
                logger.warning(f"Could not load {file_path}: {str(e)}")
        
        # Load normal sound samples
        for file_path in normal_audio_files:
            try:
                audio_data, sr = librosa.load(file_path, sr=self.sample_rate)
                feature_vector = self.extract_features(audio_data, sr)
                features.append(feature_vector)
                labels.append(0)  # 0 for normal sound
            except Exception as e:
                logger.warning(f"Could not load {file_path}: {str(e)}")
        
        return np.array(features), np.array(labels)

    def train_model(self, features: np.ndarray, labels: np.ndarray) -> dict:
        """
        Train the SVM classifier
        
        Args:
            features: Feature vectors
            labels: Corresponding labels (0: normal, 1: fall)
            
        Returns:
            Training results dictionary
        """
        if not SKLEARN_AVAILABLE:
            logger.warning("Scikit-learn not available, training not possible")
            return {}
        
        # Split data into training and testing sets
        X_train, X_test, y_train, y_test = train_test_split(
            features, labels, test_size=0.2, random_state=42, stratify=labels
        )
        
        # Train the model
        self.model.fit(X_train, y_train)
        self.is_trained = True
        
        # Evaluate the model
        y_pred = self.model.predict(X_test)
        report = classification_report(y_test, y_pred, output_dict=True)
        
        results = {
            "accuracy": report["accuracy"],
            "precision_fall": report["1"]["precision"],
            "recall_fall": report["1"]["recall"],
            "f1_fall": report["1"]["f1-score"]
        }
        
        logger.info(f"Model trained with accuracy: {results['accuracy']:.2f}")
        return results

    def detect_fall_sound(self, audio_data: np.ndarray, sample_rate: int) -> Tuple[bool, float]:
        """
        Detect if the audio contains a fall sound
        
        Args:
            audio_data: Audio signal data
            sample_rate: Sample rate of the audio
            
        Returns:
            Tuple of (is_fall_detected, confidence_score)
        """
        if not self.is_trained:
            logger.warning("Model not trained yet")
            return False, 0.0
            
        # Extract features
        features = self.extract_features(audio_data, sample_rate)
        
        # Predict
        prediction = self.model.predict([features])[0]
        probabilities = self.model.predict_proba([features])[0]
        
        # Get confidence score (probability of positive class)
        confidence_score = probabilities[1] if len(probabilities) > 1 else 0.0
        
        is_fall = bool(prediction)
        
        return is_fall, confidence_score

    def save_model(self, filepath: str):
        """
        Save the trained model to disk
        
        Args:
            filepath: Path to save the model
        """
        import joblib
        if not self.is_trained:
            raise ValueError("Model not trained yet")
            
        joblib.dump(self.model, filepath)
        logger.info(f"Model saved to {filepath}")

    def load_model(self, filepath: str):
        """
        Load a trained model from disk
        
        Args:
            filepath: Path to load the model from
        """
        import joblib
        self.model = joblib.load(filepath)
        self.is_trained = True
        logger.info(f"Model loaded from {filepath}")

# Example usage
if __name__ == "__main__":
    # This would be used during training phase
    detector = AudioFallDetector()
    
    # Example of how to train the model (paths would need to be actual files)
    # fall_sounds = ["data/fall_thud1.wav", "data/fall_thud2.wav"]
    # normal_sounds = ["data/talking1.wav", "data/walking1.wav"]
    # features, labels = detector.load_training_data(fall_sounds, normal_sounds)
    # results = detector.train_model(features, labels)
    # detector.save_model("fall_detector_model.pkl")
    
    # For inference, you would load the model:
    # detector.load_model("fall_detector_model.pkl")
    pass