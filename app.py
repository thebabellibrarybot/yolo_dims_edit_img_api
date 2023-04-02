#e = {
#    "body": {
#    "key":"msm854_fol. 47(v,r) expell_fol1L.jpg",
#    "bucket": "msm854",
#    "coords": [{2.0: [191, 150, 462, 484]}, {1.0: [457, 213, 524, 440]}],
#    "class": 2.0,
#    "action": "crop"
#    }
#}
import boto3
from PIL import Image, ImageDraw
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

        # mask to 640x640 sz
        # Create a mask to keep everything inside the bounding box
        mask = Image.new('L', img_pil.size, color=0)
        draw = ImageDraw.Draw(mask)
        draw.rectangle(dim, fill=255)

        # Apply the mask to the image to set everything outside of the bounding box to white
        masked_image = Image.new('RGBA', img_pil.size, color=(255, 255, 255, 255))
        masked_image.paste(img_pil, mask=mask)
        
        # save and upload actions
        cl = str(dims.keys()).replace('dict_keys', '').replace('([', '').replace('])', '')
        cropped_key = 'cropped_' + cl + '_' + s3_img_key
        img_bytes = BytesIO()
        masked_image = masked_image.convert('RGB')
        masked_image.save(img_bytes, format='JPEG')
        img_bytes.seek(0)
        cropped_key = cropped_key.replace(' ', '_').replace('+', '%2B').replace(',','_')
        s3.put_object(Bucket=s3_bucket, Key=cropped_key, Body=img_bytes)
        out[cropped_key] = {s3_bucket: f'https://{s3_bucket}.s3.amazonaws.com/{cropped_key}'}
    return out

def mask_img(img, buk, dims):
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