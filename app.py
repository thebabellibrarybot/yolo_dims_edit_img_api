#e = {
#    "body": {
#    "key":"msm854_fol. 47(v,r) expell_fol1L.jpg",
#    "bucket": "msm854",
#    "coords": [{2.0: [191, 150, 462, 484]}, {1.0: [457, 213, 524, 440]}],
#    "class": 2.0,
#    "action": "crop"
#    }
#}
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
def mask_img():
    return

def lambda_hanlder(event, context):
    coord_class = event['body']['class']
    coords = event['body']['coords']
    img = event['body']['key']
    buk = event['body']['bucket']
    action = event['body']['action']

    if action == 'crop':
        for dims in coords:
            if coord_class in dims:
                print(dims, 'dims sent to edit_img')
                s3url = crop_image(img, buk, dims)
                return s3url
            
    if action == 'mask':
        for dims in coords:
            if coord_class in dims:
                s3url = mask_img(img, buk, dims)
                return s3url
    

#i = lambda_hanlder(e,context=None)
#print(i)