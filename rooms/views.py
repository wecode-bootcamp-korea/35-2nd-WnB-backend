import json

from django.views        import View
from django.http         import JsonResponse
from django.db.models    import Q

from rooms.models        import *
from reservations.models import *
from hosts.models        import Host

class RoomsView(View):
    def get(self, request): 
        category          = request.GET.get('category', None)
        check_in          = request.GET.get('check_in', None)
        check_out         = request.GET.get('check_out', None)
        maximum_occupancy = request.GET.get('maximum_occupancy', None)
        bed               = request.GET.get('bed', None)
        bathroom          = request.GET.get('bathroom', None)
        bedroom           = request.GET.get('bedroom', None)
        address           = request.GET.get('address',None)
        room_type_ids     = request.GET.getlist('room_type_id', None)
        facility_ids      = request.GET.getlist('facility_id', None)
        min_price         = request.GET.get('min_price', None)
        max_price         = request.GET.get('max_price', None)
        reservations      = []

        q                 = Q()
        
        if min_price and max_price:
            q &= Q(price__gte = min_price, price__lte = max_price)

        if address:
            q &= Q(address__icontains = address)

        if room_type_ids:
            q &= Q(room_type__id__in = room_type_ids)

        if bed:
            q &= Q(bed__gte = bed)

        if bedroom:
            q &= Q(bedroom__gte = bedroom)

        if bathroom:
            q &= Q(bathroom__gte = bathroom)

        if category :
            q &= Q(category_id = category)

        if facility_ids:
            q &= Q(roomfacility__room_facility_id__in = facility_ids)

        if maximum_occupancy:
            q &= Q(maximum_occupancy__gte = maximum_occupancy)

        if check_in and check_out:
            reservations = Reservation.objects.filter(
                Q(
                    check_in__lte=check_in, check_out__gte=check_out
                ) |
                Q(
                    check_in__lte=check_in, check_out__gt=check_in
                ) |
                Q(
                    check_in__lt=check_out, check_out__gte=check_out
                )
            )

        rooms = Room.objects.filter(q).distinct().exclude(reservation__in=reservations)

        result  = [{
            'room_id'     : room.id,
            'room_name'   : room.name,
            'room_price'  : room.price,
            'room_image'  : [image.url for image in room.image_set.all()],
            'room_address': room.address,
            'latitude'    : room.latitude,
            'longitude'   : room.longitude,
            'bed'         : room.bed,
            'description' : room.description
        } for room in rooms]

        return JsonResponse({'result' : result}, status=200)