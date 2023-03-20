def crop_image(img, buk, dims):
    s3_img_key = img
    s3_bucket = buk
    crop_to_dims = dims

    # download image to bytes from s3

    # get image original size

    # crop image to dims but keep same size of original image with white background and cropped section in the same position on the page

    # upload new image to s3 with name 'cropped_dims.key_' + 's3_img_key'

    # return the buket and s3key and s3url of the newly cropped image



    print(img, buk, dims)

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