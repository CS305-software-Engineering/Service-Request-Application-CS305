from clarifai.rest import ClarifaiApp
import os
from PIL import Image

app = ClarifaiApp() 

######## This function takes a public url of the image and sends the predictions ################
# def get_tags(image_url):
#     response_data = app.tag_urls([image_url])
#     tags = []
#     for concept in response_data['outputs'][0]['data']['concepts']:
#         tags.append(concept['name'])
#     return tags

# print(get_tags('https://www.aquantindia.com/wp-content/uploads/2020/04/Faucets-in-Chrome-Finish.jpg'))



#### this can take a path of a local image file as input, uses OS library and sends predictions ##########################
def get_tags_from_image(img):
    response_data = app.tag_files([img])
    # response_d2 = app.tag_files([])
    # print(response_data)
    tags = []
    for concept in response_data['outputs'][0]['data']['concepts']:
        tags.append(concept['name'])
    return tags


#
path = 'resources/iron1.jpg'
# file = Image.open('resources/iron1.jpg')
# file.show()
print(get_tags_from_image(path))