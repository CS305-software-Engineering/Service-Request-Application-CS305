from clarifai.rest import ClarifaiApp
from PIL import Image
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
# import validators

app = ClarifaiApp()
######## This function takes a public url of the image and sends the predictions ################
def get_tags_from_url(image_url):
    response_data = app.tag_urls([image_url])
    tags = []
    for concept in response_data['outputs'][0]['data']['concepts']:
        tags.append(concept['name'])
    return tags

#### this can take a path of a local image file as input, uses OS library and sends predictions ##########################
def get_tags_from_path(img):
    # print(type(img))
    response_data = app.tag_files([img])
    tags = []
    for concept in response_data['outputs'][0]['data']['concepts']:
        tags.append(concept['name'])
    return tags



path = 'F:/Pythons/resources/iron1.jpg'
faucet_url1 = 'https://www.aquantindia.com/wp-content/uploads/2020/04/Faucets-in-Chrome-Finish.jpg'
# print(get_tags('https://www.aquantindia.com/wp-content/uploads/2020/04/Faucets-in-Chrome-Finish.jpg'))
# file = Image.open('F:/Pythons/resources/iron1.jpg')
# file.show()
# print(get_tags_from_image(path))

def classification(image_path):
    ## Code for image classification
    validate = URLValidator()
    try: 
        validate(image_path)
        print("is a URL =>", image_path)
        try:
            tags = get_tags_from_url(image_path)
        
        except:
            return "invalid URL of the image file, kindly enter exact path of the image file or image url"
    except ValidationError as e:
        print("is not a url =>",image_path)
        try:
            tags = get_tags_from_path(image_path)
            
        except:
            return "invalid PATH of the image file, kindly enter exact path of the image file or image url"

    plumber_set = ['faucet','pipes','pipe','shower','water']
    electrical_set = ['electrical','electronics','power','appliance']  
    score_plumber = 0
    score_electrical =0
    for tag in tags:
        if(tag in plumber_set):
            score_plumber+=1
        if(tag in electrical_set):
            score_electrical+=1
    
    if(max(score_electrical,score_plumber)==0):
        return "something went wrong, could not predict the department"
    else:
        if(score_plumber>=score_electrical):
            return "plumber"
        else:
            return "electrical"


dept = classification(faucet_url1)
print(dept)