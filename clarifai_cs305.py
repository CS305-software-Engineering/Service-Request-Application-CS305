from clarifai.rest import ClarifaiApp
from PIL import Image
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from dotenv import load_dotenv
import os
# import validators
load_dotenv()
app = ClarifaiApp(api_key = os.environ.get('CLARIFAI_API_KEY'))

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

## this function to search for a word in a list of words in O(nlogn) complexity ###
# input: L (a list of words), target (word to be searched)
# output: None( if value is not found), target(if found)
def binary_search(L, target):
    i = 0
    j = len(L) - 1
    while i <= j:
        middle = (i + j)//2
        midpoint = L[middle]
        if midpoint > target:
            j = middle - 1
        elif midpoint < target:
            i = middle + 1
        else:
            return midpoint

path = 'F:/Pythons/resources/iron1.jpg'
faucet_url1 = 'https://www.aquantindia.com/wp-content/uploads/2020/04/Faucets-in-Chrome-Finish.jpg'
# file = Image.open('F:/Pythons/resources/iron1.jpg')
# file.show()

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

    plumber_set = ['faucet','pipes','pipe','shower','wash','basin','water','washcloset','bathroom','water closet','flush','bathtub','steel','plumber','plumbing','wet']
    electrical_set = ['electrical','electronics','power','appliance','computer','conditioner','technology','wire','connection','switch','electricity','lamp','ceiling','fan','heater']  
    score_plumber = 0
    score_electrical =0
    
    ##### has n^2 complexity
    # for tag in tags: 
    #     if(tag in plumber_set):
    #         score_plumber+=1
    #     if(tag in electrical_set):
    #         score_electrical+=1

    ##### has nlog(n) complexity
    for word in tags:
        if binary_search(plumber_set,word) is not None:
            score_plumber+=1
        if binary_search(electrical_set,word) is not None:
            score_electrical+=1

    print("score_plumber =",score_plumber)
    print("score_electrical =",score_electrical)
    
    if(max(score_electrical,score_plumber)==0):
        return "something went wrong, could not predict the department"
    else:
        if(score_plumber>=score_electrical):
            return "plumber"
        else:
            return "electrical"


dept = classification(faucet_url1)
print(dept)