# from clarifai.rest import ClarifaiApp
from PIL import Image
# from django.core.validators import URLValidator
# from django.core.exceptions import ValidationError
from dotenv import load_dotenv
import os

from clarifai_grpc.channel.clarifai_channel import ClarifaiChannel
from clarifai_grpc.grpc.api import service_pb2_grpc
stub = service_pb2_grpc.V2Stub(ClarifaiChannel.get_grpc_channel())

from clarifai_grpc.grpc.api import service_pb2, resources_pb2
from clarifai_grpc.grpc.api.status import status_code_pb2

# This is how you authenticate.
metadata = (('authorization', 'Key 02aad03316c148aab10375c462ae4f68'),)




######## This function takes a public url of the image and sends the predictions ################
def get_tags_from_url(image_url):
    tags = []
    request = service_pb2.PostModelOutputsRequest(
    model_id='aaa03c23b3724a16a56b629203edc62c',
    inputs=[
      resources_pb2.Input(data=resources_pb2.Data(image=resources_pb2.Image(url=image_url)))
    ])
    response = stub.PostModelOutputs(request, metadata=metadata)

    if response.status.code != status_code_pb2.SUCCESS:
        raise Exception("Request failed, status code: " + str(response.status.code))

    for concept in response.outputs[0].data.concepts:
        tags.append(concept.name)
    return tags

def get_tags_from_path(image_path):
    print("image path => ",image_path)
    with open(image_path,"rb") as f:
        file_bytes = f.read()
    tags = []
    request = service_pb2.PostModelOutputsRequest(
    model_id='aaa03c23b3724a16a56b629203edc62c',
    inputs=[
      resources_pb2.Input(data=resources_pb2.Data(image=resources_pb2.Image(base64=file_bytes)))
    ])
    response = stub.PostModelOutputs(request, metadata=metadata)

    if response.status.code != status_code_pb2.SUCCESS:
        raise Exception("Request failed, status code: " + str(response.status.code))

    for concept in response.outputs[0].data.concepts:
        tags.append(concept.name)
    return tags


img_url = 'https://www.havells.com/content/dam/havells/consumer/appliances-new/garment-care/dry-iron/adore-peach/cover.png'
# print(get_tags_from_url(img_url))
img_path = "F:/tryingStuff/Service-Request-Application-CS305/service/media/heater1.jpg"
# print(help(resources_pb2.Image))
print(get_tags_from_path(img_path))


"""app = ClarifaiApp(api_key = keykey)


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
print(dept)"""