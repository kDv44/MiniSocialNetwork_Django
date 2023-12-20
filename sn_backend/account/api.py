from django.http import JsonResponse

from rest_framework.decorators import api_view, authentication_classes, permission_classes


@api_view(['POST'])
def signup(request):
    data = request.data
    message = 'success'

    return JsonResponse({'status': message})
