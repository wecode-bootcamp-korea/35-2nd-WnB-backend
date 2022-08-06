import json

from django.http        import JsonResponse
from django.views       import View
from django.forms       import ValidationError

from users.models       import User
from core.utils         import check_first_name, check_last_name, check_phone_number, signin_decorator

class UserAdditionalInfoView(View):
    @signin_decorator
    def patch(self, request):
        try: 
            user = request.user
            data = json.loads(request.body)
            
            first_name   = data['first_name']
            last_name    = data['last_name']
            phone_number = data['phone_number']
            birth_day    = data['birth_day']
                      
            check_first_name(first_name)
            check_last_name(last_name)
            check_phone_number(phone_number)
            
            if User.objects.filter(phone_number = phone_number):
                return JsonResponse({'message':'PHONE_NUMBER_ALREADY_EXIST'}, status=400)
            
            user.first_name   = first_name
            user.last_name    = last_name
            user.phone_number = phone_number
            user.birth_day    = birth_day
            user.save()

            return JsonResponse({'message':'USER_INFO_UPDATED'}, status=201)
            
        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'}, status=400)
        
        except ValidationError as e:
            return JsonResponse({'message':f'{e}'}, status=400)