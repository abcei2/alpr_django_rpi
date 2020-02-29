from ctypes import *
import math
import random
import cv2
from cerebro_lpr.src.keras_utils import load_model, detect_lp
from cerebro_lpr.src.utils import im2single
import numpy as np
from datetime import datetime


def sample(probs):
    s = sum(probs)
    probs = [a/s for a in probs]
    r = random.uniform(0, 1)
    for i in range(len(probs)):
        r = r - probs[i]
        if r <= 0:
            return i
    return len(probs)-1


def c_array(ctype, values):
    arr = (ctype*len(values))()
    arr[:] = values
    return arr


class BOX(Structure):
    _fields_ = [("x", c_float),
                ("y", c_float),
                ("w", c_float),
                ("h", c_float)]


class DETECTION(Structure):
    _fields_ = [("bbox", BOX),
                ("classes", c_int),
                ("prob", POINTER(c_float)),
                ("mask", POINTER(c_float)),
                ("objectness", c_float),
                ("sort_class", c_int)]


class IMAGE(Structure):
    _fields_ = [("w", c_int),
                ("h", c_int),
                ("c", c_int),
                ("data", POINTER(c_float))]


class METADATA(Structure):
    _fields_ = [("classes", c_int),
                ("names", POINTER(c_char_p))]


#lib = CDLL("/home/pjreddie/documents/darknet/libdarknet.so", RTLD_GLOBAL)
lib = CDLL(
    "/home/santi/ECUADOR/alpr-unconstrained/darknet/libdarknet.so", RTLD_GLOBAL)
lib.network_width.argtypes = [c_void_p]
lib.network_width.restype = c_int
lib.network_height.argtypes = [c_void_p]
lib.network_height.restype = c_int

predict = lib.network_predict
predict.argtypes = [c_void_p, POINTER(c_float)]
predict.restype = POINTER(c_float)

set_gpu = lib.cuda_set_device
set_gpu.argtypes = [c_int]

make_image = lib.make_image
make_image.argtypes = [c_int, c_int, c_int]
make_image.restype = IMAGE

get_network_boxes = lib.get_network_boxes
get_network_boxes.argtypes = [c_void_p, c_int, c_int,
                              c_float, c_float, POINTER(c_int), c_int, POINTER(c_int)]
get_network_boxes.restype = POINTER(DETECTION)

make_network_boxes = lib.make_network_boxes
make_network_boxes.argtypes = [c_void_p]
make_network_boxes.restype = POINTER(DETECTION)

free_detections = lib.free_detections
free_detections.argtypes = [POINTER(DETECTION), c_int]

free_ptrs = lib.free_ptrs
free_ptrs.argtypes = [POINTER(c_void_p), c_int]

network_predict = lib.network_predict
network_predict.argtypes = [c_void_p, POINTER(c_float)]

reset_rnn = lib.reset_rnn
reset_rnn.argtypes = [c_void_p]

load_net = lib.load_network
load_net.argtypes = [c_char_p, c_char_p, c_int]
load_net.restype = c_void_p

do_nms_obj = lib.do_nms_obj
do_nms_obj.argtypes = [POINTER(DETECTION), c_int, c_int, c_float]

do_nms_sort = lib.do_nms_sort
do_nms_sort.argtypes = [POINTER(DETECTION), c_int, c_int, c_float]

free_image = lib.free_image
free_image.argtypes = [IMAGE]

letterbox_image = lib.letterbox_image
letterbox_image.argtypes = [IMAGE, c_int, c_int]
letterbox_image.restype = IMAGE

load_meta = lib.get_metadata
lib.get_metadata.argtypes = [c_char_p]
lib.get_metadata.restype = METADATA

load_image = lib.load_image_color
load_image.argtypes = [c_char_p, c_int, c_int]
load_image.restype = IMAGE

rgbgr_image = lib.rgbgr_image
rgbgr_image.argtypes = [IMAGE]

predict_image = lib.network_predict_image
predict_image.argtypes = [c_void_p, IMAGE]
predict_image.restype = POINTER(c_float)

# srand = lib.srand
# srand.argtypes = [c_int]
# nnp_initialize = lib.nnp_initialize


def classify(net, meta, im):
    out = predict_image(net, im)
    res = []
    for i in range(meta.classes):
        res.append((meta.names[i], out[i]))
    res = sorted(res, key=lambda x: -x[1])
    return res


def detect(net, meta, image, thresh=.5, hier_thresh=.5, nms=.45):
    im = load_image(image, 0, 0)
    num = c_int(0)
    pnum = pointer(num)
    predict_image(net, im)
    dets = get_network_boxes(net, im.w, im.h, thresh,
                             hier_thresh, None, 0, pnum)
    num = pnum[0]
    if (nms):
        do_nms_obj(dets, num, meta.classes, nms)

    res = []
    for j in range(num):
        for i in range(meta.classes):
            if dets[j].prob[i] > 0:
                b = dets[j].bbox
                res.append(
                    (meta.names[i], dets[j].prob[i], (b.x, b.y, b.w, b.h)))
    res = sorted(res, key=lambda x: -x[1])
    wh = (im.w, im.h)
    free_image(im)
    free_detections(dets, num)
    return res, wh


def load_plate_models():

    net = load_net(b"cerebro_lpr/data/ocr/ocr-net.cfg",
                   b"cerebro_lpr/data//ocr/ocr-net.weights", 0)
    meta = load_meta(b"cerebro_lpr/data/ocr/ocr-net.data")

    wpod_net_path = 'cerebro_lpr/data/lp-detector/wpod-net_update1.h5'
    wpod_net = load_model(wpod_net_path)

    return net, meta, wpod_net


temp_plates=[]
temp_counter_plates=[]
temp_timestamp=[]

def detect_plates(frame, net, meta, wpod_net, lp_threshold, letter_threshold):

    ratio = float(max(frame.shape[:2]))/min(frame.shape[:2])*4
    side = int(ratio*288.)
    bound_dim = min(side + (side % (2**4)), 608.)

    print("\t\tBound dim: %d, ratio: %f" % (bound_dim, ratio))
    Llp, LlpImgs, _ = detect_lp(wpod_net, im2single(
        frame), bound_dim, 2**4, (240, 80), lp_threshold)
    # print("Llp[0]")
    # print(Llp[0])
    print(frame.shape)
    plates = []
    for i in range(len(LlpImgs)):
        Ilp = LlpImgs[i]
        plate_pts = Llp[i].pts
        Ilp = Ilp*255
        Ilp = Ilp.astype(np.uint8)
        cv2.imwrite('photo.jpg', Ilp)
        nnp_initialize()
        r = detect(net, meta, b"photo.jpg", letter_threshold)
        # print(r)
        posicion = []
        letra = []
        # cv2.rectangle(
        #         frame,
        #         (int(box[0]-box[2]/2), int(box[1]-box[3]/2)),
        #         (int(box[0]+box[2]/2), int(box[1]+box[3]/2)),
        #         (0, 255, 0),
        #         3
        #     )
        for det in r[0]:
            posicion.append(det[2][0])
            letra.append(det[0])
            box = [int(kk) for kk in det[2]]
            cv2.rectangle(
                Ilp,
                (int(box[0]-box[2]/2), int(box[1]-box[3]/2)),
                (int(box[0]+box[2]/2), int(box[1]+box[3]/2)),
                (0, 255, 0),
                3
            )

            cv2.putText(Ilp,
                        str(det[0])[2],
                        (int(box[0]), int(box[1])),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.5,
                        (255, 255, 255),
                        1
                        )
        while 0 in posicion:
            posicion.remove(0)
        desorganizado = posicion.copy()
        posicion.sort()  # posicion organizada
#        print(desorganizado)

        matricula = []
        bad_format=False
        counter_i=0
        for i in posicion:
            Letter=str(letra[desorganizado.index(i)])[2]
            if counter_i <3:
                try:
                    a=int(Letter)+3
                    print(f"WITH NUMBERS AT FIRST LETTER: {Letter}")
                    break
                except:
                    a=1
            else:                        
                try:
                    int(Letter)
                except:
                    print(f"WITH LETTERS AT END : {Letter}")
                    break

            matricula.append(Letter)
            counter_i+=1
        
        if len(matricula)==6 and not bad_format:
            matricula=''.join(matricula)
            if matricula in temp_plates:
                temp_counter_plates[temp_plates.index(matricula)]+=1
            else:
                temp_plates.append(matricula)
                temp_counter_plates.append(0)
                temp_timestamp.append(datetime.now()) 	
                #cv2.imwrite(f"detected_plates/{matricula}.jpg",frame_to_save)
                
    return plates

# for det in r[0]: