import json
import uuid

from django.http            import JsonResponse
from django.views           import View

from reservations.models    import Reservation
from rooms.models           import Room
from core.utils             import signin_decorator

class MainResevationsView(View):
    @signin_decorator
    def get(self, request): 
        reservations    = Reservation.objects.select_related("room") \
                                             .prefetch_related("room__image_set") \
                                             .filter(user = request.user)
        result = [{
            'reservation_number'        : reservation.number,
            'room'                      : reservation.room.name,
            'check_in'                  : reservation.check_in,
            'check_out'                 : reservation.check_out,
            'images'                    : reservation.room.image_set.all()[0].url,
            'address'                   : reservation.room.address,
            'detail_address'            : reservation.room.detail_address
        } for reservation in reservations]

        return JsonResponse({"RESULT": result}, status=200)

    @signin_decorator
    def post(self, request):
        try:
            data                    = json.loads(request.body)
            user                    = request.user
            room                    = Room.objects.get(id=data['room'])
            check_in                = data['check_in']
            check_out               = data['check_out']
            people                  = data['people']
            price                   = data['price']
            number                  = uuid.uuid1()

            Reservation.objects.create(
                check_in            = check_in,
                check_out           = check_out,
                people              = people,
                room                = room,
                user                = user,
                price               = price,
                number              = number
            )

            return JsonResponse({"MESSAGE": "SUCCESS"}, status=201)

        except KeyError:
            return JsonResponse({"MESSAGE": "KEY_ERROR"}, status=400)
        except Room.DoesNotExist:
            return JsonResponse({"MESSAGE": "DOESNOT_EXIST_ROOM"}, status=400)

class DetailReservationView(View):
    @signin_decorator
    def get(self, request, reservation_number):
        reservation          = Reservation.objects.select_related("room") \
                                                  .prefetch_related("room__image_set") \
                                                  .get(user = request.user, number = reservation_number)

        result = {
            'reservation_number'            : reservation.number,
            'user_name'                     : reservation.user.last_name + " " + reservation.user.first_name,
            'room'                          : reservation.room.name,
            'price'                         : reservation.price,
            'people'                        : reservation.people,
            'check_in'                      : reservation.check_in,
            'check_out'                     : reservation.check_out,
            'images'                        : [image.url for image in reservation.room.image_set.all()],
            'description'                   : reservation.room.description,
            'address'                       : reservation.room.address + " " + reservation.room.detail_address,
            'latitude'                      : reservation.room.latitude,
            'longitude'                     : reservation.room.longitude
        }
        return JsonResponse({"RESULT": result}, status=200)