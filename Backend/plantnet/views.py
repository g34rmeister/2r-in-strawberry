from django.shortcuts import render
import requests
from django.http import JsonResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import json

# Create your views here.
plantnet_api = "https://my-api.plantnet.org/v2"

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