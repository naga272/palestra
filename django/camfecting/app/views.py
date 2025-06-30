from django.shortcuts import render

# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import os
import time


def homepage(request):
    return render(request, "index.html", {})


@csrf_exempt
def upload_image(request):
    if request.method == 'POST':
        image_file = request.FILES.get('image')
        if not image_file:
            return JsonResponse({'status': 'error', 'message': 'Nessun file ricevuto'}, status=400)

        # Salva il file nel percorso voluto
        save_path = os.path.join('media', f'snapshot_{time.time()}.jpg')
        with open(save_path, 'wb+') as f:
            for chunk in image_file.chunks():
                f.write(chunk)

        return JsonResponse({'status': 'ok'})
    return JsonResponse({'status': 'error', 'message': 'Metodo non consentito'}, status=405)
