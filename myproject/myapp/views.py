from django.http import JsonResponse
from .cdc import output

def my_api_view(request):
    data = output
    return JsonResponse(data)
