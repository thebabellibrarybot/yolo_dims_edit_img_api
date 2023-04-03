import numpy as np
import cv2
import boto3
from io import BytesIO

def crop_image(img, buk, dims):
    print('edit_img started')
    s3_img_key = img
    s3_bucket = buk
    crop_to_dims = []
    for classes, dim in dims.items():
        crop_to_dims.append(dim)
   
    out = {}
    for dim in crop_to_dims:
        # download image to bytes from s3
        s3 = boto3.client('s3')
        img_object = s3.get_object(Bucket=s3_bucket, Key=s3_img_key)
        img_data = img_object['Body'].read()
        img = cv2.imdecode(np.frombuffer(img_data, np.uint8), cv2.IMREAD_COLOR)
        img = cv2.resize(img, (640, 640))

        # mask to 640x640 sz
        mask = np.zeros((img.shape[0], img.shape[1]), dtype=np.uint8)
        cv2.rectangle(mask, tuple(dim[:2]), tuple(dim[2:]), color=255, thickness=-1)

        # Apply the mask to the image to set everything outside of the bounding box to white
        masked_image = cv2.bitwise_and(img, img, mask=mask)
        
        # save and upload actions
        cl = str(dims.keys()).replace('dict_keys', '').replace('([', '').replace('])', '')
        cropped_key = 'cropped_' + cl + '_' + s3_img_key
        success, img_bytes = cv2.imencode('.jpg', masked_image)
        if success:
            img_bytes = BytesIO(img_bytes)
            cropped_key = cropped_key.replace(' ', '_').replace('+', '%2B').replace(',','_')
            s3.put_object(Bucket=s3_bucket, Key=cropped_key, Body=img_bytes.getvalue())
            out[cropped_key] = {s3_bucket: f'https://{s3_bucket}.s3.amazonaws.com/{cropped_key}'}
    return out

def mask_img(img, buk, dims):
    s3_img_key = img
    s3_bucket = buk
    crop_to_dims = dims

    # download image to bytes from s3

    # get image original size

    # mask image to over dims but keep same size of original image with white background 

    # upload new image to s3 with name 'masked_dims.key_' + 's3_img_key'

    # return the buket and s3key and s3url of the newly cropped image



    print(img, buk, dims)