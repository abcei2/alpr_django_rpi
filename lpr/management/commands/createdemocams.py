from django.core.management.base import BaseCommand

from lpr.models import LPRCamera
from lpr.models import LPRCamera_allowed_plates

lpr_camera_data = {  # River parking
        'geopoint': '-75.378712,6.148837',  # 6ta etapa
        'url': "http://75.147.0.206/mjpg/video.mjpg"

    }


class Command(BaseCommand):
    help = 'Create demo cameras data for testing'

    def handle(self, *args, **kwargs):
        LPRAux=LPRCamera(
             url=lpr_camera_data['url'],detection_zone=[200,100,200,100])
        LPRAux.save()
        allowed_plates=LPRCamera_allowed_plates(allowed_plate="xxx215")
        allowed_plates.save()
        print("[!] Data created succesfully")
