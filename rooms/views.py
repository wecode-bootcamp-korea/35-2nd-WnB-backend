from django.http        import JsonResponse
from django.views       import View

class RoomView(View):
    def get(self, request):
        
        return JsonResponse({'result':'화면이동 성공'}, status=200)