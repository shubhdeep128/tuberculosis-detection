import flask 
import werkzeug
import time	
import cv2
import os
import time
import urllib
import numpy as np
import boto3, botocore
import io

import numpy as np
from matplotlib import pyplot as plt

s3 = boto3.client(
   "s3",
   aws_access_key_id=os.environ.get("S3_ACCESS_KEY_ID"),
   aws_secret_access_key=os.environ.get("S3_SECRET_ACCESS_KEY")
)



app = flask.Flask(__name__)


@app.route('/', methods = ['GET', 'POST'])
def handle_request():
    files_ids = list(flask.request.files)
    print("\nNumber of Received Images : ", len(files_ids))
    image_num = 1
    for file_id in files_ids:
        print("\nSaving Image ", str(image_num), "/", len(files_ids))
        imagefile = flask.request.files[file_id]
        filename = werkzeug.utils.secure_filename(imagefile.filename)
        print("Image Filename : " + imagefile.filename)
        timestr  =  time.strftime("%Y%m%d-%H%M%S")
        #Filename1 = timestr+'_'+filename
        #global Filename
       # Filename = "WTF"
        imagefile.save("test")
        image_num = image_num + 1
    print("\n")
    return "Image(s) Uploaded Successfully. Come Back Soon."

# @app.route('/Binary', methods=['GET', 'POST'])
# def Binary():
#     print("Its working canny Binary")
#     image = cv2.imread('/home/jathin/Desktop/Projects/Boils FInal/test')
#     # scale_percent = 20 # percent of original size
#     # width = int(image.shape[1] * scale_percent / 100)
#     # height = int(image.shape[0] * scale_percent / 100)
#     # dim = (width, height)
#     # img = cv2.resize(image, dim, interpolation = cv2.INTER_AREA) 
#     ret,thresh1 = cv2.threshold(image,127,255,cv2.THRESH_BINARY)
#     cv2.imshow('Original image',image)
#     cv2.imshow('Gray image', thresh1)
#     # ret,thresh2 = cv2.threshold(img,127,255,cv2.THRESH_BINARY_INV)
#     # ret,thresh3 = cv2.threshold(img,127,255,cv2.THRESH_TRUNC)
#     # ret,thresh4 = cv2.threshold(img,127,255,cv2.THRESH_TOZERO)
#     # ret,thresh5 = cv2.threshold(img,127,255,cv2.THRESH_TOZERO_INV)
#     # titles = ['Original Image','BINARY','BINARY_INV','TRUNC','TOZERO','TOZERO_INV']
#     # images = [img, thresh1, thresh2, thresh3, thresh4, thresh5]
#     # for i in range(6):
#     #     plt.subplot(2,3,i+1),plt.imshow(images[i],'gray')
#     #     plt.title(titles[i])
#     #     plt.xticks([]),plt.yticks([])

#     return "Success"

    image_num = 1
    for file_id in files_ids:
        print("\nSaving Image ", str(image_num), "/", len(files_ids))
        imagefile = flask.request.files[file_id]
        filename = werkzeug.utils.secure_filename(imagefile.filename)
        print("Image Filename : " + imagefile.filename)
        timestr  =  time.strftime("%Y%m%d-%H%M%S")
        #Filename1 = timestr+'_'+filename
        #global Filename
       # Filename = "WTF"
        imagefile.save("test")
        image_num = image_num + 1
        image = cv2.imread('/home/jathin/Desktop/Projects/Boils FInal/test')
#     gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
#     cv2.imshow('Original image',image)
#     cv2.imshow('Gray image', gray)
#     cv2.waitKey(0)
#     cv2.destroyAllWindows()
#     print("Working")
#     return "Success"


@app.route('/sobelx', methods=['GET', 'POST'])
def SobelX():
    # print(flask.request.get_json()["url"])
    req = urllib.request.urlopen(flask.request.get_json()["url"])
    arr = np.asarray(bytearray(req.read()), dtype=np.uint8)
    image = cv2.imdecode(arr, -1)
    # image = cv2.imread('./preProcessImages/test.png')
    scale_percent = 100 # percent of original size
    width = int(image.shape[1] * scale_percent / 100)
    height = int(image.shape[0] * scale_percent / 100)
    dim = (width, height)
    img = cv2.resize(image, dim, interpolation = cv2.INTER_AREA) 
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray,(3,3),0)
    edges = cv2.Sobel(blur,cv2.CV_64F,1,0,ksize=5)
    # cv2.imshow('Original image',img)
    # cv2.imshow('Canny image', edges)
    # cv2.imwrite("./postProcessImages/Canny.jpg", edges)
    image_string = cv2.imencode('.jpg', edges)[1].tobytes()
    imageName = flask.request.get_json()["filename"] + '_sobelX.jpg'
    # cv2.imshow('Gray image', gray)
    try:

        s3.upload_fileobj(
            io.BytesIO(image_string),
            os.environ.get("S3_BUCKET_NAME"),
            imageName,
            ExtraArgs={
                "ACL": "public-read",
                "ContentType": 'image/jpeg'
            }
        )

    except Exception as e:
        # This is a catch all exception, edit this part to fit your needs.
        print("Something Happened: ", e)
        return e
    print(os.environ.get("CLOUDFRONT_URL")+imageName)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    print("Working")
    return {
        "url": os.environ.get("CLOUDFRONT_URL")+imageName
    }

@app.route('/sobely', methods=['GET', 'POST'])
def SobelY():
    # print(flask.request.get_json()["url"])
    req = urllib.request.urlopen(flask.request.get_json()["url"])
    arr = np.asarray(bytearray(req.read()), dtype=np.uint8)
    image = cv2.imdecode(arr, -1)
    # image = cv2.imread('./preProcessImages/test.png')
    scale_percent = 100 # percent of original size
    width = int(image.shape[1] * scale_percent / 100)
    height = int(image.shape[0] * scale_percent / 100)
    dim = (width, height)
    img = cv2.resize(image, dim, interpolation = cv2.INTER_AREA) 
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray,(3,3),0)
    edges = cv2.Sobel(blur,cv2.CV_64F,0,1,ksize=5)
    # cv2.imshow('Original image',img)
    # cv2.imshow('Canny image', edges)
    # cv2.imwrite("./postProcessImages/Canny.jpg", edges)
    image_string = cv2.imencode('.jpg', edges)[1].tobytes()
    imageName = flask.request.get_json()["filename"] + '_sobelY.jpg'
    # cv2.imshow('Gray image', gray)
    try:

        s3.upload_fileobj(
            io.BytesIO(image_string),
            os.environ.get("S3_BUCKET_NAME"),
            imageName,
            ExtraArgs={
                "ACL": "public-read",
                "ContentType": 'image/jpeg'
            }
        )

    except Exception as e:
        # This is a catch all exception, edit this part to fit your needs.
        print("Something Happened: ", e)
        return e
    print(os.environ.get("CLOUDFRONT_URL")+imageName)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    print("Working")
    return {
        "url": os.environ.get("CLOUDFRONT_URL")+imageName
    }



@app.route('/canny', methods=['GET', 'POST'])
def Canny():
    # print(flask.request.get_json()["url"])
    req = urllib.request.urlopen(flask.request.get_json()["url"])
    arr = np.asarray(bytearray(req.read()), dtype=np.uint8)
    image = cv2.imdecode(arr, -1)
    # image = cv2.imread('./preProcessImages/test.png')
    scale_percent = 100 # percent of original size
    width = int(image.shape[1] * scale_percent / 100)
    height = int(image.shape[0] * scale_percent / 100)
    dim = (width, height)
    img = cv2.resize(image, dim, interpolation = cv2.INTER_AREA) 
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray,100,200)
    # cv2.imshow('Original image',img)
    # cv2.imshow('Canny image', edges)
    # cv2.imwrite("./postProcessImages/Canny.jpg", edges)
    image_string = cv2.imencode('.jpg', edges)[1].tobytes()
    imageName = flask.request.get_json()["filename"] + '_canny.jpg'
    # cv2.imshow('Gray image', gray)
    try:

        s3.upload_fileobj(
            io.BytesIO(image_string),
            os.environ.get("S3_BUCKET_NAME"),
            imageName,
            ExtraArgs={
                "ACL": "public-read",
                "ContentType": 'image/jpeg'
            }
        )

    except Exception as e:
        # This is a catch all exception, edit this part to fit your needs.
        print("Something Happened: ", e)
        return e
    print(os.environ.get("CLOUDFRONT_URL")+imageName)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    print("Working")
    return {
        "url": os.environ.get("CLOUDFRONT_URL")+imageName
    }

@app.route('/laplacian', methods=['GET', 'POST'])
def Laplacian():
    # print(flask.request.get_json()["url"])
    req = urllib.request.urlopen(flask.request.get_json()["url"])
    arr = np.asarray(bytearray(req.read()), dtype=np.uint8)
    image = cv2.imdecode(arr, -1)
    # image = cv2.imread('./preProcessImages/test.png')
    scale_percent = 100 # percent of original size
    width = int(image.shape[1] * scale_percent / 100)
    height = int(image.shape[0] * scale_percent / 100)
    dim = (width, height)
    img = cv2.resize(image, dim, interpolation = cv2.INTER_AREA) 
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray,(3,3),0)
    edges = cv2.Laplacian(blur,cv2.CV_64F)
    # cv2.imshow('Original image',img)
    # cv2.imshow('Canny image', edges)
    # cv2.imwrite("./postProcessImages/Canny.jpg", edges)
    image_string = cv2.imencode('.jpg', edges)[1].tobytes()
    imageName = flask.request.get_json()["filename"] + '_laplacian.jpg'
    # cv2.imshow('Gray image', gray)
    try:

        s3.upload_fileobj(
            io.BytesIO(image_string),
            os.environ.get("S3_BUCKET_NAME"),
            imageName,
            ExtraArgs={
                "ACL": "public-read",
                "ContentType": 'image/jpeg'
            }
        )

    except Exception as e:
        # This is a catch all exception, edit this part to fit your needs.
        print("Something Happened: ", e)
        return e
    print(os.environ.get("CLOUDFRONT_URL")+imageName)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    print("Working")
    return {
        "url": os.environ.get("CLOUDFRONT_URL")+imageName
    }


app.run(port=5000, debug=True)