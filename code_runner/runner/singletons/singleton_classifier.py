import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout

class ClassifierSingleton:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = cls.load_model()  # Load and assign the model instance
        return cls._instance

    @staticmethod
    def load_model():
        # Define the model
        model = Sequential([
            Dense(256, input_dim=1024, activation='relu', kernel_regularizer=tf.keras.regularizers.l2(0.01)),
            Dropout(0.5),  # Dropout layer to reduce overfitting
            Dense(128, activation='relu', kernel_regularizer=tf.keras.regularizers.l2(0.01)),
            Dropout(0.5),  # Dropout layer to reduce overfitting
            Dense(1, activation='sigmoid')  # Adjust output layer for binary/multi-class classification
        ])

        # Compile the model
        model.compile(optimizer='adam',
                           loss='binary_crossentropy',
                           metrics=['accuracy'])

        # Load the best model weights
        model_path = r"C:\Users\123\Desktop\django_python_ide\code_runner\runner\load_from\balanced_dataset_yes_replicated_model (1).h5"
        model.load_weights(model_path)

        return model