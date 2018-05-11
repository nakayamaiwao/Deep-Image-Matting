import os

import keras
from keras.callbacks import ModelCheckpoint, EarlyStopping, ReduceLROnPlateau

import migrate
import new_start
from utils import train_gen, valid_gen

if __name__ == '__main__':
    img_rows, img_cols = 320, 320
    channel = 4
    batch_size = 64
    epochs = 1000
    patience = 50
    num_samples = 43100
    num_train_samples = 34480
    num_valid_samples = 8620    # num_samples - num_train_samples

    # Load our model
    model_path = 'models/model_weights.h5'
    if os.path.exists(model_path):
        model = new_start.autoencoder(img_rows, img_cols, channel)
        model.load_weights(model_path)
    else:
        model = migrate.migrate_model(img_rows, img_cols, channel)

    print(model.summary())

    # Callbacks
    tensor_board = keras.callbacks.TensorBoard(log_dir='./logs', histogram_freq=0, write_graph=True, write_images=True)
    trained_models_path = 'models/model'
    model_names = trained_models_path + '.{epoch:02d}-{val_loss:.2f}.hdf5'
    model_checkpoint = ModelCheckpoint(model_names, monitor='val_loss', verbose=1, save_best_only=True)
    early_stop = EarlyStopping('val_loss', patience=patience)
    reduce_lr = ReduceLROnPlateau('val_loss', factor=0.1, patience=int(patience / 4), verbose=1)
    callbacks = [tensor_board, model_checkpoint, early_stop, reduce_lr]

    # Start Fine-tuning
    model.fit_generator(train_gen(),
                        steps_per_epoch=num_train_samples // batch_size,
                        validation_data=valid_gen(),
                        validation_steps=num_valid_samples / batch_size,
                        epochs=epochs,
                        verbose=1
                        )
