from django.shortcuts import render

import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def process_image(request):
    if request.method == 'POST':
        # Get the image data from the request
        image_data = request.FILES.get('image')

        if not image_data:
            return JsonResponse({'error': 'No image provided'}, status=400)

        # Prepare the payload for the external service
        files = {'image': (image_data.name, image_data.read(), image_data.content_type)}

        # Send the POST request to the external service
        response = requests.post('http://127.0.0.1:5000/process_image', files=files)

        # Return the JSON response from the external service
        return JsonResponse(response.json(), status=response.status_code)

    return JsonResponse({'error': 'Invalid request method'}, status=405)