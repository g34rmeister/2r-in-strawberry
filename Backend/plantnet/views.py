from django.shortcuts import render
import requests
from django.http import JsonResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST, require_GET
import json
import re
import base64
from .models import Plant, UserChallenge
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.
plantnet_api = "https://my-api.plantnet.org/v2/"
    
dificulties = {
    'easy': 1,
    'mid': 2,
    'hard': 3
}

# --- NEW GetRandomPlantView ---
class GetRandomPlantView(APIView):
    permission_classes = [IsAuthenticated] # This will check for the Bearer token

    def post(self, request, *args, **kwargs):
        user = request.user
        data = request.data # DRF parses the JSON for you

        difficulty = data.get('difficulty', None)
        if not difficulty:
            # Note: You probably meant "Missing 'difficulty' field"
            return Response({"error": "Missing 'difficulty' field"}, status=status.HTTP_400_BAD_REQUEST)
        
        level_id = dificulties.get(difficulty)
        if not level_id:
            return Response({'error': "Invalid level"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            plants_in_level = Plant.objects.filter(dificulty=level_id)
            if not plants_in_level.exists():
                return Response({"error": f"No plants for difficulty"}, status=status.HTTP_404_NOT_FOUND)
            
            random_plant = plants_in_level.order_by('?').first()
            
        except Exception as e:
            print(f"Error finding plant: {e}")
            return Response({"error": "Internal database error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        # --- Update the user's challenge ---
        try:
            UserChallenge.objects.update_or_create(
                user=user, 
                defaults={'current_challange': random_plant}
            )
        except Exception as e:
            print(f"Error updating challenge: {e}")
            return Response({"error": "Could not update user challenge"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        # --- Return the new plant details ---
        result = {
            'scientific-name': random_plant.scientific_name,
            'description': random_plant.description,
            'common-name': random_plant.common_name,
            'dificulty': random_plant.dificulty,
            'image-url': random_plant.image.url if random_plant.image else None
        }
        return Response(result, status=status.HTTP_200_OK)


# --- NEW GetChallengeView ---
class GetChallengeView(APIView):
    permission_classes = [IsAuthenticated] # This will check for the Bearer token

    def get(self, request, *args, **kwargs):
        user = request.user

        empty_challenge_response = {
            'scientific-name': None,
            'description': None,
            'common-name': None,
            'dificulty': None,
            'image-url': None
        }

        try:
            user_challenge_record = user.current_challenge_record
            current_plant = user_challenge_record.current_challange
            
            if current_plant is None:
                return Response(empty_challenge_response, status=status.HTTP_200_OK)

            result = {
                'scientific-name': current_plant.scientific_name,
                'description': current_plant.description,
                'common-name': current_plant.common_name,
                'dificulty': current_plant.dificulty,
                'image-url': current_plant.image.url if current_plant.image else None
            }
            return Response(result, status=status.HTTP_200_OK)

        except ObjectDoesNotExist:
            return Response(empty_challenge_response, status=status.HTTP_200_OK)
            
        except Exception as e:
            print(f"An unexpected error occurred: {e}") 
            return Response({"error": "An internal error occurred."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
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