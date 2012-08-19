import os

from django.test import TestCase
from django.conf import settings
from busitizer.core.tasks import busitize

class TestBusitizerTask(TestCase):
        
    def test_basic(self):
        test_images = [os.path.join(settings.TEST_IMAGES, filename) for filename in os.listdir(settings.TEST_IMAGES)]
        for image_path in test_images:
            response = busitize.delay(image_path)