import os
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '../', '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

SENDING_PHOTO, = range(1)

CLASSES_NAME = ['rose', 'sunflower']
CLASSES_NAME_RUS = ['роза', 'подсолнух']

MODEL_NAME = f'models/{CLASSES_NAME[0]}_{CLASSES_NAME[1]}_model.h5'
