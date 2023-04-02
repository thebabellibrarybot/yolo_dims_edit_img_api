import boto3
from PIL import Image, ImageOps
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
        img_pil = Image.open(BytesIO(img_data))
        img_pil = img_pil.resize((640, 640))
        
        # crop image to dims but keep same size of original image with white background and cropped section in the same position on the page
        img_crop = img_pil.crop((dim[0], dim[1], dim[2], dim[3]))
        padded_image = ImageOps.expand(img_crop, border=10, fill=(255))
        cl = str(dims.keys()).replace('dict_keys', '').replace('([', '').replace('])', '')
        cropped_key = 'cropped_' + cl + '_' + s3_img_key
        img_bytes = BytesIO()
        padded_image.save(img_bytes, format='JPEG')
        img_bytes.seek(0)
        cropped_key = cropped_key.replace(' ', '_').replace('+', '%2B').replace(',','_')
        s3.put_object(Bucket=s3_bucket, Key=cropped_key, Body=img_bytes)
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