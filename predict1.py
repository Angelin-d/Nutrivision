import tensorflow as tf
import numpy as np

from tensorflow.keras.models import load_model
import shap
def predict_nail_fn(img):

    # ---------- Load Model ----------
    model_path = r"C:\NUTRITION_DEFICIENCY (3)\NUTRITION_DEFICIENCY\myapp\hkslog/output_graph.h5"  # or .keras
    labels_path = r"C:\NUTRITION_DEFICIENCY (3)\NUTRITION_DEFICIENCY\myapp\hkslog2/output_labels.txt"

    print("Loading model...")
    model = load_model(model_path)
    print("Model loaded successfully!")


    # ---------- Load Labels ----------
    with open(labels_path, 'r') as f:
        labels = [line.strip() for line in f.readlines()]


    # ---------- Prediction Function ----------
    def predict_image(model, image_path, labels):
        image_data = tf.io.read_file(image_path)
        image = tf.image.decode_image(image_data, channels=3)
        image = tf.image.resize(image, [224, 224])
        image = image / 255.0
        image = tf.expand_dims(image, axis=0)

        preds = model.predict(image)
        print(preds,"===========")
        top_id = np.argmax(preds[0])
        label = labels[top_id]
        confidence = float(preds[0][top_id])

        print("\n=== Prediction Result ===")
        print(f"Image: {image_path}")
        print(f"Predicted Class : {label}")
        print(f"Confidence      : {confidence:.4f}")

        return label, confidence


    # ---------- Test Prediction ----------
    test_img = img

    return predict_image(model, test_img, labels)
