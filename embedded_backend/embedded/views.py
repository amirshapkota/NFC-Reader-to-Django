from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
def rfid_view(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
            scanner_id = data.get('scanner_id')
            uid = data.get('uid')
            if scanner_id and uid:
                print(f"Received Scanner ID: {scanner_id}, UID: {uid}")
                return JsonResponse({'status': 'success', 'scanner_id': scanner_id, 'uid': uid})
            else:
                print("Error: Missing scanner_id or uid")
                return JsonResponse({'status': 'error', 'message': 'Missing scanner_id or uid'}, status=400)
        except json.JSONDecodeError:
            print("Error: JSON decode error")
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)
