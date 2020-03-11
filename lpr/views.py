from django.shortcuts import render
from django.views import View
from django.http import JsonResponse
from django.conf import settings
from django.db import connection
from typing import Dict, Any

from django.db.models import Count
from lpr.models import LPRCamera
from lpr.models import LPRCamera_reports
from lpr.models import LPRCamera_allowed_plates

import tensorflow as tf
# IMAGE TO STRING
from django.core.serializers import serialize
import base64
import re
import urllib
import json
import time
import numpy as np
from datetime import datetime, timedelta
from cerebro_lpr import load_plate_models, detect_plates
import cv2
import subprocess
# Create your views here.


#net, meta, wpod_net=load_plate_models()

#graph = tf.get_default_graph()
class BaseView(View):
    def global_context(self, request=None):
        return {
            'DEBUG': settings.DEBUG,
            'view': f'{self.__module__}.{self.__class__.__name__}',
            'sql_queries': len(connection.queries),
        }

    def render_template(self, request, context=None, template=None):
        return render(request, template or self.template, {
            **self.global_context(),
            **(context or {}),
        })

    def render_json(self, json_dict: Dict[str, Any], **kwargs):
        return JsonResponse(json_dict, **kwargs)

class LPR_View(BaseView):
    template = 'lpr/home.html'

    def context(self):
        allowed_plates=[]
        for i in LPRCamera_allowed_plates.objects.all().values():
            allowed_plates.append(i["allowed_plate"])
            print(i["allowed_plate"])
        allowed_plates="{"+f"\"allowed_plates\":{allowed_plates}"+"}"
        allowed_plates=allowed_plates.replace("'", "\"")
        print(allowed_plates)
        allowed_plates=json.loads(allowed_plates)
#        print(LPRCamera.objects.all().values()[0])

        return {
            'MAP_API': settings.MAP_API,
            'LPRCamera': LPRCamera.objects.all().values()[0] if LPRCamera.objects.all().count()!=0 else [0, 0, 0, 0],
            'LPRCamera_allowed_plates':allowed_plates
        }

    def get(self, request):
        return self.render_template(request, self.context())

def decode_base64(data, altchars=b'+/'):
    """Decode base64, padding being optional.

    :param data: Base64 data as an ASCII byte string
    :returns: The decoded byte string.

    """
    data = re.sub(rb'[^a-zA-Z0-9%s]+' % altchars, b'', data)  # normalize
    missing_padding = len(data) % 4
    if missing_padding:
        data += b'='* (4 - missing_padding)
    return base64.b64decode(data, altchars)

def fecthLPR(request):
    # url_cam = request.GET.get('url')
    # img = request.GET.get('img')
    # req = urllib.request.urlopen(url_cam)
    # print(req)
    # arr = np.asarray(bytearray(req.read()), dtype=np.uint8)
    # frame = cv2.imdecode(arr, -1) # 'Load it as it is'
    
    # lp_threshold=0.7
    # letter_threshold=0.4
    # print(url_cam)
    # cap= cv2.VideoCapture(url_cam)
    # ret, frame=cap.read()
    # frame = cv2.resize(frame, (600,300), interpolation = cv2.INTER_CUBIC)
    # detected_plates=[]
    # with graph.as_default():
    #     detected_plates=detect_plates(frame,net,meta, wpod_net,lp_threshold,letter_threshold)
    #     print("detect_plates\n")
    #     print(detected_plates)
    # #cap.release()
    #     if detected_plates!=[]:
    #         for i in detected_plates:
    #             LPRAux_reports=LPRCamera_reports(
    #                 detected_plate=i)
    #             LPRAux_reports.save()   
    # cap.release()
    return JsonResponse({"ok": "ok"}, safe=False)

def add_new_allowed_plate(request):
    new_allowed_plate = request.GET.get('new_allowed_plate')
    print(new_allowed_plate)
    allowed_plates=LPRCamera_allowed_plates(allowed_plate=new_allowed_plate)
    print(allowed_plates.save())
    return JsonResponse({"ok": "ok"}, safe=False)

def remove_allowed_plate(request):
    plate_to_remove = request.GET.get('plate_to_remove')
    print(plate_to_remove)
    print(LPRCamera_allowed_plates.objects.filter(allowed_plate=plate_to_remove).delete())
    return JsonResponse({"ok": "ok"}, safe=False)

def save_url(request):
    url_cam = request.GET.get('url')
    LPRCamera_obj = LPRCamera.objects.update(url=url_cam)
    print(f"\n\n  {url_cam}  \n\n")
    print(f"\n\n asfagagadgr \n\n")
    return JsonResponse({"ok": "ok"}, safe=False)

def edit_roi(request):
    x = request.GET.get('x')
    y = request.GET.get('y')
    width = request.GET.get('width')
    height = request.GET.get('height')
    
    LPRCamera_obj = LPRCamera.objects.update(detection_zone=[x, y, width, height])
    return JsonResponse({"ok": "ok"}, safe=False)

def update_ip(request):
    eth_ip = request.GET.get('eth_ip')
    eth_gateway = request.GET.get('eth_gateway')
    eth_mask = request.GET.get('eth_mask')
    LPRCamera_obj = LPRCamera.objects.update(eth_ip=eth_ip,eth_gateway=eth_gateway,eth_mask=eth_mask)

    subprocess.check_call(['static/scripts/CHANGE_IP.sh', eth_ip, eth_gateway, eth_mask])
    subprocess.check_call(['sudo reboot'])
    
    return JsonResponse({"ok": "ok"}, safe=False)


def config(request):

    eth_ip = list(LPRCamera.objects.values('eth_ip'))[0]['eth_ip']
    eth_gateway = list(LPRCamera.objects.values('eth_gateway'))[0]['eth_gateway']
    eth_mask = list(LPRCamera.objects.values('eth_mask'))[0]['eth_mask']

    context = {"eth_ip": eth_ip, "eth_gateway": eth_gateway,"eth_mask":eth_mask}
    return render(request, 'configuration/config.html', context=context)


def dashboard(request):

    today = datetime.now()
    timestamp_to = datetime.now() + timedelta(days=3)
    timestamp_from = datetime.now() - timedelta(days=3)
    print('\ntimestamp_to\n')
    print(timestamp_to)
    print('\ntimestamp_from\n')
    print(timestamp_from)

    # read data
    values = []
    categories=[]
    lpr_reports = LPRCamera_reports.objects.values('detected_plate').annotate(total=Count('detected_plate'))

    #lpr_reports = json.loads(serialize('json', lpr_reports))

    print(lpr_reports)

    for i in lpr_reports:
        values.append(i['total'])
        categories.append(i['detected_plate'])
    
    context = {"categories": categories, 'values': values}
    print(context)
    return render(request, 'lpr/dashboard.html', context=context)
