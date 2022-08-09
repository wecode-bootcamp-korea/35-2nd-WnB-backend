from http.server import BaseHTTPRequestHandler
import json

from django.views        import View
from django.http         import JsonResponse
from django.db.models    import Q

from rooms.models        import *
from reservations.models import *
from hosts.models        import Host

class ReservationFilterView(View):
    def get(self, request):
        category          = request.GET.get('category', 3)
        check_in          = request.GET.get('check_in', None)
        check_out         = request.GET.get('check_out', None)
        maximum_occupancy = request.GET.get ('maximum_occupancy', None)
        bed               = request.GET.get('bed', None)
        bathroom          = request.GET.get('bathroom', None)
        bedroom           = request.GET.get('bedroom', None)
        address           = request.GET.get('address',None)
        room_type         = request.GET.get('room_type', None)

        print(bathroom)
        search_filter     = Q()
        q                 = Q()
        dateq             = Q()

        if address:
            q &= Q(address__name__icontains = address)

        if room_type:
            q &= Q(room_type = room_type)

        if bed:
            q &= Q(bed__gte = bed)

        if bedroom:
            q &= Q(bedroom__gte = bedroom)

        if bathroom:
            q &= Q(bathroom__gte = bathroom)

        if category :
            rooms = Room.objects.filter(category_id = category)

        if check_in and check_out:
            dateq |= Q(reservation__check_in__gt = check_in, reservation__check_out__lt=check_out)
            dateq |= Q(reservation__check_out__gt = check_in )
            dateq |= Q(reservation__check_in__lt = check_out)
            
            rooms  = Room.objects.filter(q)

        if maximum_occupancy:
            search_filter &= Q(maximum_occupancy__gte = maximum_occupancy)

            rooms = Room.objects.filter(search_filter)

        result  = [{
                    'room_id'               : room.id,
                    'room_name'             : room.name,
                    'room_price'            : room.price,
                    'room_image'            : [image.url for image in room.image_set.all()],
                    'room_address'          : room.address,
                    'room_category'         : room.category.id,
                    'room_checkin'          : [i.check_in for i in room.reservation_set.all()],
                    'room_checkout'         : [i.check_out for i in room.reservation_set.all()],
                    'room_type'             : room.room_type
                    }for room in rooms]

        return JsonResponse({'result' : result}, status=200)
               
class RoomDetailView(View):
    def get(self, request, room_id):
        try:
            room = Room.objects.get(id=room_id)

            result = {
                'id'               : room_id,
                'name'             : room.name,
                'address'          : room.address,
                'detail_address'   : room.detail_address,
                'price'            : room.price,
                'description'      : room.description,
                'latitude'         : room.latitude,
                'longitude'        : room.longitude,
                'maximum_occupancy': room.maximum_occupancy,
                'bedroom'          : room.bedroom,
                'bathroom'         : room.bathroom,
                'bed'              : room.bed,
                'host'             : {
                    'id'           : room.host_id,
                    'first_name'   : room.host.user.first_name,
                    'last_name'    : room.host.user.last_name,
                    'phone_number' : room.host.user.phone_number,
                    'profile_img'  : room.host.profile_img
                },
                'category'         : {
                    'id'     : room.category_id,
                    'name'   : room.category.name,
                    'img_url': room.category.img_url
                },
                'room_type'        : {
                    'id'  : room.room_type_id,
                    'name': room.room_type.name
                },
                'images'       : [image.url for image in room.image_set.all()],
                'detail_images': [image.url for image in room.detailimage_set.all()],
                'facilities'   : [facilities.room_facility.name for facilities in room.roomfacility_set.all()]
            }

            return JsonResponse({'result': result}, status = 200)

        except Room.DoesNotExist:
            return JsonResponse({'message' : 'INVALID_ROOM'}, status = 404)
        
        except Host.DoesNotExist:
            return JsonResponse({'message' : 'INVALID_HOST'}, status = 404)
