import secrets
import string
from database.func import add,checker,update_valid,is_valid
import PySimpleGUI as sg
import cv2
import numpy as np
from pyzbar.pyzbar import decode
import json

def decoder(image):
    gray_img = cv2.cvtColor(image,0) 
    barcode = decode(gray_img) #function form pybazar used

    for obj in barcode:
        points = obj.polygon
        (x,y,w,h) = obj.rect
        pts = np.array(points, np.int32)
        pts = pts.reshape((-1, 1, 2))
        cv2.polylines(image, [pts], True, (0, 255, 0), 3)
        barcodeData = obj.data.decode("utf-8")
        barcodeType = obj.type
        return barcodeData
        
sg.theme("LightPurple")
layout = [
    [sg.Text('CANTEEN SCANNER', text_color="Red", border_width=4, background_color="White", justification='center', expand_x='True', relief='solid', size=(10,3), p=((10,10),(20,20)))],
    [sg.Button('SCAN QR', auto_size_button='True', expand_x="True")],
    [sg.Text(key='-TXT-', text_color="Red")],
    [sg.Button('Cancel', expand_x="True")],
]
window = sg.Window('CANTEEN ORDER SYSTEM', layout,icon=r'"D:\TE Mini Project\ADBMS\canteen_order_system-main\Canteen-automation-system-1.png"', size=(500, 500))
while True:
    event, values = window.read()
    if event is None or event == 'Cancel':
        break
    if event == "SCAN QR":
        cap = cv2.VideoCapture(0)
        while True:
            ret, frame = cap.read()
            lol = decoder(frame)
            cv2.imshow('Image', frame)
            cv2.waitKey(1)
            if lol:
                cap.release()
                cv2.destroyWindow('Image')
                break
        lol=lol.replace("'", '"')
        print(lol)
        lol = json.loads(lol)
        key=lol.get("key")
        res=lol["dict"]
        is_parcel=lol.get("is_parcel")
        if checker(key) and is_valid(key).get("isvalid")==True:
            txt="RECEIPES ORDER LIST:\n\nRECEIPE\t\tQUANTITY\n"
            for x in res:
                txt+=f"{x}\t\t{res.get(x)}\n"
            if is_parcel=="True":
                txt+="\nOrder Type: Take Away"
            else:
                txt+=f"\nOrder Type: Dine-IN"
            print(txt)
            update_valid(key)
        else:
            sg.popup('QR is Inavlid')