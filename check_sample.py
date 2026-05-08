# import tensorflow as tf
# import numpy as np
# import shap
# import matplotlib.pyplot as plt
# from tensorflow.keras.models import load_model
#
# # ---------- Paths ----------
# MODEL_PATH = r"C:\degree readymade\vjec\NUTRITION_DEFICIENCY\NUTRITION_DEFICIENCY\myapp\hkslog/output_graph.h5"
# LABELS_PATH = r"C:\degree readymade\vjec\NUTRITION_DEFICIENCY\NUTRITION_DEFICIENCY\myapp\hkslog2/output_labels.txt"
# TEST_IMAGE = r"C:\degree readymade\vjec\NUTRITION_DEFICIENCY\NUTRITION_DEFICIENCY\myapp\1 - Copy (2).PNG"
#
# # ---------- Load Model ----------
# model = load_model(MODEL_PATH)
#
# # ---------- Load Labels ----------
# with open(LABELS_PATH, 'r') as f:
#     labels = [line.strip() for line in f.readlines()]
#
# # ---------- Preprocess Image ----------
# def preprocess_image(img_path):
#     img = tf.io.read_file(img_path)
#     img = tf.image.decode_image(img, channels=3)
#     img = tf.image.resize(img, (224, 224))
#     img = img / 255.0
#     return img.numpy()
#
# image = preprocess_image(TEST_IMAGE)
# image_batch = np.expand_dims(image, axis=0)
#
# # ---------- Model Prediction ----------
# preds = model.predict(image_batch)
# predicted_class = np.argmax(preds[0])
# confidence = preds[0][predicted_class]
#
# print("\n===== MODEL PREDICTION =====")
# print(f"Predicted Nutrition Deficiency : {labels[predicted_class]}")
# print(f"Confidence Score               : {confidence:.4f}")
#
# # ---------- SHAP Background ----------
# background = np.random.rand(30, 224, 224, 3)
#
# # ---------- SHAP Explainer ----------
# explainer = shap.GradientExplainer(model, background)
#
# # ---------- SHAP Values ----------
# shap_values = explainer.shap_values(image_batch)
#
# # ---------- SHAP Visualization ----------
# shap.image_plot(
#     [shap_values[predicted_class]],
#     image_batch,
#     labels=[labels[predicted_class]],
#     show=False
# )
#
# # ---------- Save Figure ----------
# plt.savefig("result.png", bbox_inches='tight', dpi=300)
# plt.close()
#
# # ---------- Result Support Statement ----------
# print("\n===== RESULT SUPPORT (SHAP) =====")
# print(
#     f"The SHAP explanation highlights the critical regions in the nail image "
#     f"that strongly influenced the prediction of '{labels[predicted_class]}'. "
#     f"Red-colored regions represent features that positively contributed to the "
#     f"model's decision, while blue regions indicate negative influence. "
#     f"This confirms that the model focused on biologically relevant nail patterns "
#     f"associated with the predicted nutritional deficiency."
# )


import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
import cv2
from tensorflow.keras.models import load_model

# ======================================================
# PATHS
# ======================================================
MODEL_PATH = r"C:\Users\angel\OneDrive\Desktop\NUTRITION_DEFICIENCY (3)\NUTRITION_DEFICIENCY\myapp\hkslog/output_graph.h5"
LABELS_PATH = r"C:\Users\angel\OneDrive\Desktop\NUTRITION_DEFICIENCY (3)\NUTRITION_DEFICIENCY\myapp\hkslog2/output_labels.txt"
TEST_IMAGE = r"C:\Users\angel\OneDrive\Desktop\NUTRITION_DEFICIENCY (3)\NUTRITION_DEFICIENCY\myapp\1 - Copy (2).PNG"

# ======================================================
# LOAD MODEL & LABELS
# ======================================================
model = load_model(MODEL_PATH)

with open(LABELS_PATH, 'r') as f:
    labels = [line.strip() for line in f.readlines()]

# ======================================================
# IMAGE PREPROCESSING
# ======================================================
def preprocess_image(img_path):
    img = tf.io.read_file(img_path)
    img = tf.image.decode_image(img, channels=3)
    img = tf.image.resize(img, (224, 224))
    img = img / 255.0
    return img.numpy()

image = preprocess_image(TEST_IMAGE)
image_batch = np.expand_dims(image, axis=0)

# ======================================================
# MODEL PREDICTION
# ======================================================
preds = model.predict(image_batch)
predicted_class = np.argmax(preds[0])
confidence = preds[0][predicted_class]

print("\n===== MODEL PREDICTION =====")
print(f"Predicted Nutrition Deficiency : {labels[predicted_class]}")
print(f"Confidence Score               : {confidence:.4f}")

# ======================================================
# FIND LAST CONVOLUTION LAYER
# ======================================================
def get_last_conv_layer(model):
    for layer in reversed(model.layers):
        if len(layer.output.shape) == 4:
            return layer.name
    raise ValueError("No convolutional layer found")

LAST_CONV_LAYER = get_last_conv_layer(model)
print(f"Using last conv layer: {LAST_CONV_LAYER}")

# ======================================================
# HEATMAP OVERLAY FUNCTION
# ======================================================
def overlay_heatmap(heatmap, image, alpha=0.4):
    heatmap = cv2.resize(heatmap, (image.shape[1], image.shape[0]))
    heatmap = np.uint8(255 * heatmap)
    heatmap = cv2.applyColorMap(heatmap, cv2.COLORMAP_JET)
    overlay = heatmap * alpha + (image * 255)
    return np.uint8(overlay)

# ======================================================
# GRAD-CAM
# ======================================================
def grad_cam(model, image, class_index, layer_name):
    grad_model = tf.keras.models.Model(
        [model.inputs],
        [model.get_layer(layer_name).output, model.output]
    )

    with tf.GradientTape() as tape:
        conv_outputs, predictions = grad_model(image)
        loss = predictions[:, class_index]

    grads = tape.gradient(loss, conv_outputs)
    pooled_grads = tf.reduce_mean(grads, axis=(0, 1, 2))

    conv_outputs = conv_outputs[0]
    heatmap = tf.reduce_sum(conv_outputs * pooled_grads, axis=-1)

    heatmap = tf.maximum(heatmap, 0)
    heatmap /= tf.reduce_max(heatmap)
    return heatmap.numpy()

# ======================================================
# GRAD-CAM++
# ======================================================
def grad_cam_plus(model, image, class_index, layer_name):
    grad_model = tf.keras.models.Model(
        [model.inputs],
        [model.get_layer(layer_name).output, model.output]
    )

    with tf.GradientTape() as tape1:
        with tf.GradientTape() as tape2:
            with tf.GradientTape() as tape3:
                conv_output, predictions = grad_model(image)
                loss = predictions[:, class_index]

            grads = tape3.gradient(loss, conv_output)
        grads2 = tape2.gradient(grads, conv_output)
    grads3 = tape1.gradient(grads2, conv_output)

    global_sum = tf.reduce_sum(conv_output, axis=(0, 1, 2))
    alpha = grads2 / (2.0 * grads2 + grads3 * global_sum + 1e-10)

    weights = tf.reduce_sum(tf.maximum(grads, 0) * alpha, axis=(0, 1))
    heatmap = tf.reduce_sum(weights * conv_output[0], axis=-1)

    heatmap = tf.maximum(heatmap, 0)
    heatmap /= tf.reduce_max(heatmap)
    return heatmap.numpy()

# ======================================================
# CLASS ACTIVATION MAP (CAM)
# Works only if model uses GAP before Dense
# ======================================================
def cam(model, image, class_index, layer_name):
    conv_layer = model.get_layer(layer_name)
    cam_model = tf.keras.models.Model(model.inputs, conv_layer.output)

    conv_output = cam_model(image)[0]
    weights = model.layers[-1].get_weights()[0][:, class_index]

    heatmap = tf.reduce_sum(conv_output * weights, axis=-1)
    heatmap = tf.maximum(heatmap, 0)
    heatmap /= tf.reduce_max(heatmap)
    return heatmap.numpy()

# ======================================================
# GENERATE HEATMAPS
# ======================================================
gradcam_map = grad_cam(model, image_batch, predicted_class, LAST_CONV_LAYER)
gradcampp_map = grad_cam_plus(model, image_batch, predicted_class, LAST_CONV_LAYER)

try:
    cam_map = cam(model, image_batch, predicted_class, LAST_CONV_LAYER)
    cam_available = True
except:
    cam_available = False

# ======================================================
# VISUALIZATION
# ======================================================
plt.figure(figsize=(18,5))

plt.subplot(1,4 if cam_available else 3,1)
plt.imshow(image)
plt.title("Original Image")
plt.axis("off")

plt.subplot(1,4 if cam_available else 3,2)
plt.imshow(overlay_heatmap(gradcam_map, image))
plt.title("Grad-CAM")
plt.axis("off")

plt.subplot(1,4 if cam_available else 3,3)
plt.imshow(overlay_heatmap(gradcampp_map, image))
plt.title("Grad-CAM++")
plt.axis("off")

if cam_available:
    plt.subplot(1,4,4)
    plt.imshow(overlay_heatmap(cam_map, image))
    plt.title("CAM")
    plt.axis("off")

plt.tight_layout()
plt.show()
