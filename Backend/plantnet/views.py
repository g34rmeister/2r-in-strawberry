from django.shortcuts import render
import requests
from django.http import JsonResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import json
import re
import base64
from .models import Plant
from django.shortcuts import render, get_object_or_404

# Create your views here.
plantnet_api = "https://my-api.plantnet.org/v2/"
    

@csrf_exempt
@require_POST
def get_random_plant(request):
    #define parameters for the request
    #Get users current latitudre and longitude
    usersLat=None
    usersLon=None
    boxSize=None

    try:
        data = json.loads(request.body.decode('utf-8'))

        #get args
        usersLat=data.get('lat')
        usersLon=data.get('lon')
        boxSize=data.get('size')

        if not (usersLat is not None and usersLon is not None and boxSize is not None):
            #arguemtns not correct
            return JsonResponse({'status': 'error', 'message': 'incorrect fields provided'}, status=400)
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': f'Error translating inputed json: {str(e)}'
        })

    
    #define the arguments for our api request
    params = {
        'topLeftLat': usersLat+boxSize,
        'topLeftLon': usersLon-boxSize,
        'bottomRightLat': usersLat-boxSize,
        'bottomRightLon': usersLon+boxSize,
        'api-key': settings.PLANTNET_API_KEY,
        'lang': 'en'
    }

    endpoint=f"{plantnet_api}/prediction/geo/species"

    #make the request
    try:
        response = requests.get(endpoint, params=params)

        #check for success
        if response.status_code == 200:
            #success
            data = response.json()
            print(data['results'])
            return JsonResponse({'status': 'success', 'results': data['results']}, status=response.status_code)
        else:
            #failed
            print(f"Error: {response.status_code}")
            print(response.text)
            return JsonResponse({
                'status': 'error',
                'message': 'Plantnet API returned error',
                'api_status': response.status_code,
                'api_details': response.text
            }, status=response.status_code)
    
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return JsonResponse({
            'status': 'error',
            'message': f'Error using Plantnet API: {str(e)}'
        }, status=503)
    
def getimageresults(request):
    organ = request.POST.get('organs', 'auto')#tell plantnet to detect what we are sending
    
    if 'images' not in request.FILES:
        return JsonResponse({'error': 'Missing required image field: '}, status=400)
    
    image_file = request.FILES['images']

    rawImage = image_file.read()
    filename=image_file.name
    imagetype=image_file.content_type

    #now that we have uncoded the image send request to plantnet
    indentify_params = {
        'api-key': settings.PLANTNET_API_KEY,
        'include-related-images': 'true',
        'lang': 'en'
    }

    form_data = {
        'organs': organ
    }

    files_payload = [
        ('images', (filename, rawImage, imagetype))
    ]

    id_url=f"{plantnet_api}identify/all"

    #make the request
    try:
        response = requests.post(
            id_url,
            params=indentify_params,
            data=form_data,
            files=files_payload,
        )

        response.raise_for_status()


        return response.json()
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': f'Error identifying from plantnet: {str(e)}'
        }, status=500)

@csrf_exempt
@require_POST
def identifyplant(request):
    results = getimageresults(request)
    if isinstance(results, JsonResponse):
        return results
    return JsonResponse(results)

def get_top_species(imageResults):
    plantResults=imageResults.get('results', [])#get all plant results or default to [] if non found
    top3= plantResults[:3]

    filterdResults = []
    for i,  result in enumerate(top3):
        #get name
        speciesInfo=result.get('species', {})

        #get the image url for the species
        image = result.get('images', [{}])[0]
        imageURL= image.get('url', {}).get('m') if image.get('url') else None

        filterdResults.append({
            'rank': i + 1,
            'likelihood': round(result.get('score', 0) * 100, 2),
            'scientific-name': speciesInfo.get('scientificNameWithoutAuthor'),
            'common-names': speciesInfo.get('commonNames', []),
            'example-image-url': imageURL
        })

    return filterdResults

#checks to see if the given plant picture matches the prompted species
@csrf_exempt
@require_POST
def validate_plant(request):
    correctSpec=request.POST.get('correct-species', None)
    if not correctSpec:
        return JsonResponse({'status': 'error', 'message': 'incorrect fields provided'}, status=400)
    results = getimageresults(request)
    if isinstance(results, JsonResponse):
        return results

    top3=get_top_species(results)
    
    #check if correct species is listed in top 3
    for result in top3:
        name=result.get('scientific-name')
        print("Scientific name is:")
        print(name)
        print("correct name is:")
        print(correctSpec)
        if name==correctSpec:
            response = {
                'correct': True,
            }
            return JsonResponse(response, status=200, safe=False)

    #wasnt in top 3 so failed
    response = {
        'correct': False
    }
    return JsonResponse(response, status=200, safe=False)

@csrf_exempt
@require_POST
def get_species_info(request):
    try:
        body = request.body

        data = json.loads(body)

        scientific_name = data.get('scientific-name', None)

        if not scientific_name:
            return JsonResponse({"error": "Missing 'scientific-name' field"}, status=400)
        
    except json.JSONDecodeError:
        return JsonResponse({"error": "invalid JSON"}, status=400)
    print("retrieving plant data")
    print(scientific_name)
    plant = get_object_or_404(
        Plant,
        scientific_name__iexact=scientific_name
    )

    print("got plant")
    print(plant.description)

    result = {
        'scientific-name': scientific_name,
        'description': plant.description,
        'common-name': plant.common_name,
        'dificulty': plant.dificulty,
        'image-url': plant.image.url
    }

    print(result)

    return JsonResponse(result, status=200, safe=False)