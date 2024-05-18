from cnn.constants import *
from cnn.data_prepare import create_directory, copy_images

from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D
from tensorflow.keras.layers import Activation, Dropout, Flatten, Dense


def prepare_data():
    create_directory(TRAIN_DIR)
    create_directory(TEST_DIR)

    start_test_data_idx = int(NB_IMAGES * (1 - TEST_DATA_PORTION))
    print(start_test_data_idx)

    copy_images(0, start_test_data_idx, DATA_DIR, TRAIN_DIR)
    copy_images(start_test_data_idx, NB_IMAGES, DATA_DIR, TEST_DIR)


def start():
    prepare_data()

    img_width, img_height = 150, 150
    input_shape = (img_width, img_height, 3)
    epochs = 30
    batch_size = 16
    nb_train_samples = 17500
    nb_validation_samples = 3750
    nb_test_samples = 3750

    model = Sequential()
    model.add(Conv2D(32, (3, 3), input_shape=input_shape))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))

    model.add(Conv2D(32, (3, 3)))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))

    model.add(Conv2D(64, (3, 3)))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))

    model.add(Flatten())
    model.add(Dense(64))
    model.add(Activation('relu'))
    model.add(Dropout(0.5))
    model.add(Dense(1))
    model.add(Activation('sigmoid'))

    model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

    datagen = ImageDataGenerator(rescale=1. / 255)

    train_generator = datagen.flow_from_directory(TRAIN_DIR, target_size=(img_width, img_height), batch_size=batch_size,
                                                  class_mode='binary')

    test_generator = datagen.flow_from_directory(TEST_DIR, target_size=(img_width, img_height), batch_size=batch_size,
                                                 class_mode='binary')

    model.fit_generator(train_generator, steps_per_epoch=nb_train_samples // batch_size, epochs=epochs,
                        validation_steps=nb_validation_samples // batch_size)

    model.save(f'{FIRST_CLASS_NAME}_{SECOND_CLASS_NAME}_model.h5')

    scores = model.evaluate_generator(test_generator, nb_test_samples // batch_size)

    print('Аккуратность на тестовых данных: %.2f%%' % (scores[1] * 100))
