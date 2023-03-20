e = {
    "body": {
    "key":"msm854_fol. 47(v,r) expell_fol1L.jpg",
    "bucket": "msm854",
    "coords": [{2.0: [191, 150, 462, 484]}, {1.0: [457, 213, 524, 440]}],
    "class": 2.0,
    "action": "crop"
    }
}

from edit_img import crop_image
from edit_img import mask_image

def lambda_hanlder(event, context):
    coord_class = event['body']['class']
    coords = event['body']['coords']
    img = event['body']['key']
    buk = event['body']['bucket']
    action = event['body']['action']

    if action == 'crop':
        for dims in coords:
            if coord_class in dims:
                s3url = crop_image(img, buk, dims)
                return s3url
    if action == 'mask':
        for dims in coords:
            if coord_class in dims:
                s3url = mask_image(img, buk, dims)
                return s3url
    

i = lambda_hanlder(e,context=None)