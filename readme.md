# edit_image: via yolo dims

action function built to utalize data extracted from user page data

# crop_img:
## classes: 
- text: 2.0
- margin: 1.0
- image: 3.0

## actions:
- crop to class
- maintains original image size
- everything outside of class bounding box gets transformed into background color
TODO: impliment alternative crop-to function that alters page size
- resizes image to around the size of cropped area with 10px padding
* outputs image that can be used for mask or text-line extraction

# mask_img:
## classes: 
- text: 2.0
- margin: 1.0
- image: 3.0

## actions: 
- masks class
- makes everything inside the selected class background color
- cleaning image to make text-line extraction work easiser
- maintains original image size
- can be applied to cropped or original image
* outputs image that can be used for cropping or text-line extraction