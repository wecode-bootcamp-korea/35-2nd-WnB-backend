from django.http            import JsonResponse
from django.views           import View

from reservations.models    import Reservation
from core.utils             import signin_decorator

class ResevationsView(View):
    @signin_decorator
    def get(self, request): 
        user            = request.user
        reservations    = Reservation.objects.select_related("room") \
                                             .prefetch_related("room__image_set") \
                                             .filter(user = user)
        result = [{
            'reservation_number'        : reservation.number,
            'user_name'                 : reservation.user.last_name + " " + reservation.user.first_name,
            'room'                      : reservation.room.name,
            'price'                     : reservation.price,
            'people'                    : reservation.people,
            'check_in'                  : reservation.check_in,
            'check_out'                 : reservation.check_out,
            'img'                       : reservation.room.image_set.all()[0].url
        } for reservation in reservations]

        return JsonResponse({"RESULT": result}, status=200)