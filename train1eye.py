# import os
# import numpy as np
# import tensorflow as tf
# from tensorflow.keras.preprocessing.image import ImageDataGenerator
# from tensorflow.keras.applications import InceptionV3
# from tensorflow.keras.models import Model
# from tensorflow.keras.layers import Dense, Dropout
# from tensorflow.keras.optimizers import Adam
# from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau
#
# # --- Set parameters manually ---
# image_dir =  r'C:\Users\angel\OneDrive\Desktop\NUTRITION_DEFICIENCY (3)\dataset\nutretion\archive (7)\dataset'
# output_graph = 'maincode/output_graph.h5'
# output_labels = 'maincode2/output_labels.txt'
# how_many_training_steps = 5
# learning_rate = 0.0001
# train_batch_size = 32
# final_tensor_name = 'final_result'
# flip_left_right = True
# test_image_path = r'h94_png_jpg.rf.b01c7839a1a2186b2b5536eef16de8bb.jpg'
#
#
# # --- Create model ---
# def create_inception_graph(num_classes):
#     base_model = InceptionV3(weights='imagenet', include_top=False, input_shape=(224, 224, 3), pooling='avg')
#
#     for layer in base_model.layers[-50:]:
#         layer.trainable = True
#
#     x = base_model.output
#     x = Dense(1024, activation='relu')(x)
#     x = Dropout(0.5)(x)
#     predictions = Dense(num_classes, activation='softmax', name=final_tensor_name)(x)
#
#     model = Model(inputs=base_model.input, outputs=predictions)
#     return model
#
# # ---  Prepare data generators ---
# def prepare_data_generators():
#     train_datagen = ImageDataGenerator(
#         rescale=1. / 255,
#         rotation_range=30,
#         width_shift_range=0.2,
#         height_shift_range=0.2,
#         zoom_range=0.2,
#         brightness_range=[0.8, 1.2],
#         horizontal_flip=flip_left_right
#     )
#
#     val_datagen = ImageDataGenerator(rescale=1. / 255)
#
#     train_generator = train_datagen.flow_from_directory(
#         image_dir,
#         target_size=(224, 224),
#         batch_size=train_batch_size,
#         class_mode='categorical'
#     )
#
#     validation_generator = val_datagen.flow_from_directory(
#         image_dir,
#         target_size=(224, 224),
#         batch_size=train_batch_size,
#         class_mode='categorical'
#     )
#
#     return train_generator, validation_generator
#
#
# # --- Predict a single image ---
# def predict_image(model, label_path, image_path):
#     image_data = tf.io.read_file(image_path)
#     image = tf.image.decode_jpeg(image_data, channels=3)
#     image = tf.image.resize(image, [224, 224])
#     image = image / 255.0
#     image = tf.expand_dims(image, axis=0)
#
#     predictions = model.predict(image)
#
#     label_lines = [line.strip() for line in open(label_path)]
#     top_class_id = np.argmax(predictions[0])
#     top_class_label = label_lines[top_class_id]
#     confidence = float(predictions[0][top_class_id])
#
#     print(f"\n Prediction on image: {image_path}")
#     print(f"  Predicted: {top_class_label}, Confidence: {confidence:.4f}")
#     return top_class_label
# # ---  Main Flow ---
# print(" Loading dataset...")
# num_classes = len(os.listdir(image_dir))
#
# print(" Creating model...")
# model = create_inception_graph(num_classes)
#
# print(" Preparing data...")
# train_generator, validation_generator = prepare_data_generators()
#
# model.compile(optimizer=Adam(learning_rate=learning_rate),
#               loss='categorical_crossentropy',
#               metrics=['accuracy'])
#
# early_stop = EarlyStopping(monitor='val_loss', patience=5, restore_best_weights=True)
# reduce_lr = ReduceLROnPlateau(monitor='val_loss', factor=0.2, patience=3, min_lr=1e-6)
#
# print(" Training...")
# history = model.fit(
#     train_generator,
#     steps_per_epoch=len(train_generator),
#     epochs=how_many_training_steps,
#     validation_data=validation_generator,
#     validation_steps=len(validation_generator),
#     callbacks=[early_stop, reduce_lr]
# )
#
#
# #  Save model and labels
# os.makedirs(os.path.dirname(output_graph), exist_ok=True)
# os.makedirs(os.path.dirname(output_labels), exist_ok=True)
#
# print(f" Saving model to {output_graph}")
# model.save(output_graph)
#
# print(f" Saving labels to {output_labels}")
# with open(output_labels, 'w') as f:
#     for class_label in train_generator.class_indices:
#         f.write(f"{class_label}\n")
#
# print(" Training complete!")
#
# #  Prediction
# pathh=r'h94_png_jpg.rf.b01c7839a1a2186b2b5536eef16de8bb.jpg'
# if os.path.exists(pathh):
#     predict_image(model, output_labels, pathh)
# else:
#     print(" No test image provided or file not found.")
#
#     #D:\AI\DATA_SET\Covid19-dataset\train\Covid\07.jpg
#     #D:\AI\DATA_SET\Covid19-dataset\train\Normal\06.jpeg
#     #D:\AI\DATA_SET\Covid19-dataset\train\Viral Pneumonia\012.jpeg
#
#
#
# import matplotlib.pyplot as plt
# print(history.history)
# # Accuracy graph
# plt.figure(figsize=(8,5))
# plt.plot(history.history['accuracy'], label='Train Accuracy')
# plt.plot(history.history['val_accuracy'], label='Val Accuracy')
# plt.title("Model Accuracy")
# plt.xlabel("Epochs")
# plt.ylabel("Accuracy")
# plt.legend()
# plt.grid(True)
# plt.show()
#
# # Loss graph
# plt.figure(figsize=(8,5))
# plt.plot(history.history['loss'], label='Train Loss')
# plt.plot(history.history['val_loss'], label='Val Loss')
# plt.title("Model Loss")
# plt.xlabel("Epochs")
# plt.ylabel("Loss")
# plt.legend()
# plt.grid(True)
# plt.show()
#
# import os
#
# bad_files = []
# for root, dirs, files in os.walk(image_dir):
#     for file in files:
#         if not file.lower().endswith(('.jpg', '.jpeg', '.png')):
#             bad_files.append(os.path.join(root, file))
#
# print("Bad files:")
# for f in bad_files:
#     print(f)
#
#
#
#
import os
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt

from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications import InceptionV3
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau


# =========================
# PATHS & PARAMETERS
# =========================
image_dir = r'C:\Users\angel\OneDrive\Desktop\NUTRITION_DEFICIENCY (3)\dataset\nutretion\archive (7)\dataset'
output_graph = r'maincode\output_graph.h5'
output_labels = r'maincode2\output_labels.txt'
test_image_path = r'C:\FULL\PATH\TO\YOUR\TEST\IMAGE.jpg'  # change this

IMG_SIZE = (224, 224)
BATCH_SIZE = 32
EPOCHS = 5
LEARNING_RATE = 0.0001
FINAL_TENSOR_NAME = 'final_result'


# =========================
# MODEL CREATION
# =========================
def create_inception_model(num_classes):
    base_model = InceptionV3(
        weights='imagenet',
        include_top=False,
        input_shape=(224, 224, 3),
        pooling='avg'
    )

    # Fine-tune last layers
    for layer in base_model.layers[-50:]:
        layer.trainable = True

    x = base_model.output
    x = Dense(1024, activation='relu')(x)
    x = Dropout(0.5)(x)
    output = Dense(num_classes, activation='softmax', name=FINAL_TENSOR_NAME)(x)

    model = Model(inputs=base_model.input, outputs=output)
    return model


# =========================
# DATA GENERATORS
# =========================
def prepare_data_generators():
    datagen = ImageDataGenerator(
        rescale=1./255,
        validation_split=0.2,
        rotation_range=30,
        width_shift_range=0.2,
        height_shift_range=0.2,
        zoom_range=0.2,
        horizontal_flip=True
    )

    train_gen = datagen.flow_from_directory(
        image_dir,
        target_size=IMG_SIZE,
        batch_size=BATCH_SIZE,
        class_mode='categorical',
        subset='training'
    )

    val_gen = datagen.flow_from_directory(
        image_dir,
        target_size=IMG_SIZE,
        batch_size=BATCH_SIZE,
        class_mode='categorical',
        subset='validation',
        shuffle=false
    )

    return train_gen, val_gen


# =========================
# SINGLE IMAGE PREDICTION
# =========================
def predict_image(model, label_path, image_path):
    image = tf.keras.preprocessing.image.load_img(image_path, target_size=IMG_SIZE)
    image = tf.keras.preprocessing.image.img_to_array(image)
    image = image / 255.0
    image = np.expand_dims(image, axis=0)

    preds = model.predict(image)

    with open(label_path, 'r') as f:
        labels = [line.strip() for line in f.readlines()]

    idx = np.argmax(preds[0])
    print("\nPrediction Result")
    print("-----------------")
    print("Class :", labels[idx])
    print("Confidence :", float(preds[0][idx]))


# =========================
# MAIN EXECUTION
# =========================
print("Preparing data...")
train_generator, validation_generator = prepare_data_generators()

num_classes = train_generator.num_classes
print("Number of classes:", num_classes)

print("Creating model...")
model = create_inception_model(num_classes)

model.compile(
    optimizer=Adam(learning_rate=LEARNING_RATE),
    loss='categorical_crossentropy',
    metrics=['accuracy']
)

early_stop = EarlyStopping(
    monitor='val_loss',
    patience=5,
    restore_best_weights=True
)

reduce_lr = ReduceLROnPlateau(
    monitor='val_loss',
    factor=0.2,
    patience=3,
    min_lr=1e-6
)

print("Training model...")
history = model.fit(
    train_generator,
    epochs=EPOCHS,
    validation_data=validation_generator,
    callbacks=[early_stop, reduce_lr]
)
from sklearn.metrics import confusion_matrix
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# Predict on validation data
y_pred_prob = model.predict(validation_generator)
y_pred = np.argmax(y_pred_prob, axis=1)

# True labels
y_true = validation_generator.classes

# Confusion matrix
cm = confusion_matrix(y_true, y_pred)

# Plot
plt.figure(figsize=(6,5))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
plt.xlabel("Predicted Class")
plt.ylabel("Actual Class")
plt.title("Confusion Matrix – Eye Model")
plt.savefig("confusion_matrix_eye.png")
plt.show()


# =========================
# SAVE MODEL & LABELS
# =========================
os.makedirs(os.path.dirname(output_graph), exist_ok=True)
os.makedirs(os.path.dirname(output_labels), exist_ok=True)

model.save(output_graph)
print("Model saved at:", output_graph)

with open(output_labels, 'w') as f:
    for label in train_generator.class_indices.keys():
        f.write(label + "\n")

print("Labels saved at:", output_labels)


# =========================
# PREDICTION
# =========================
if os.path.exists(test_image_path):
    predict_image(model, output_labels, test_image_path)
else:
    print("Test image not found, skipping prediction.")


# =========================
# PLOTS (RESULTS & DISCUSSION)
# =========================
plt.figure(figsize=(8, 5))
plt.plot(history.history['accuracy'], label='Training Accuracy')
plt.plot(history.history['val_accuracy'], label='Validation Accuracy')
plt.xlabel('Epochs')
plt.ylabel('Accuracy')
plt.title('Model Accuracy')
plt.legend()
plt.grid(True)
plt.show()

plt.figure(figsize=(8, 5))
plt.plot(history.history['loss'], label='Training Loss')
plt.plot(history.history['val_loss'], label='Validation Loss')
plt.xlabel('Epochs')
plt.ylabel('Loss')
plt.title('Model Loss')
plt.legend()
plt.grid(True)
plt.show()
