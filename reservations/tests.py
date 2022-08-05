import json
import jwt

from django.test            import TestCase, Client
from django.conf            import settings

from reservations.models    import Reservation
from rooms.models           import *
from users.models           import User
from hosts.models           import Host

class ReservationTest(TestCase):
    def setUp(self):
        User.objects.create(
                    id                  = 1,
                    first_name          = "doyeon",
                    last_name           = "kim",
                    kakao_id            = 12345,
                    kakao_profile_img   = "https://img.hankyung.com/photo/201903/AA.19067065.1.jpg",
                    phone_number        = "010-1234-1234",
                    birth_day           = "1992-10-15"
        )

        Host.objects.create(
                    id                  = 1,
                    user                = User.objects.get(id = 1),
                    profile_img         = "https://img.hankyung.com/photo/201903/AA.19067065.1.jpg"
        )

        Category.objects.bulk_create([
            Category(id = 1, name = "아파트",    img_url= "https://cdn-icons.flaticon.com/png/512/1311/premium/1311979.png?token=exp=1659507624~hmac=788b6e1f842695381fa984cfbcc8ec83"),
            Category(id = 2, name = "주택",     img_url="https://cdn-icons.flaticon.com/png/512/1018/premium/1018573.png?token=exp=1659507261~hmac=9d706053f8190cea635552f33355fef0"),
            Category(id = 3, name = "캠핑",     img_url="https://cdn-icons.flaticon.com/png/512/4469/premium/4469267.png?token=exp=1659507279~hmac=fe9ad89039cdb6b99b21f6efd58dc648"),
            Category(id = 4, name = "수영장",    img_url="https://cdn-icons-png.flaticon.com/512/3131/3131742.png"),
            Category(id = 5, name = "해변",     img_url="https://cdn-icons.flaticon.com/png/512/2664/premium/2664589.png?token=exp=1659507343~hmac=f98901f91a52ca6863fa0b48f529e83e"),
            Category(id = 6, name = "국립공원",  img_url="https://cdn-icons-png.flaticon.com/512/2509/2509907.png")
        ])

        RoomType.objects.bulk_create([
            RoomType(id = 1, name = "집전체"),
            RoomType(id = 2, name = "개인실"),
        ])

        Facility.objects.bulk_create([
            Facility(id = 1, name = "와이파이"),
            Facility(id = 2, name = "주방"),
            Facility(id = 3, name = "휴게실"),
            Facility(id = 4, name = "전자레인지"),
            Facility(id = 5, name = "세탁기"),
        ])

        Room.objects.create(
                    id                  = 1,
                    name                = "펜션1",
                    address             = "강원도",
                    detail_address      = "대관령면",
                    price               = 10000,
                    description         = "산속에서 즐기는 휴식같은 하루",
                    latitude            = 10.1010,
                    longitude           = 12.1221,
                    maximum_occupancy   = 10,
                    bedroom             = 10,
                    bathroom            = 10,
                    bed                 = 10,
                    host                = Host.objects.get(id = 1),
                    room_type           = RoomType.objects.get(id = 1),    
                    category            = Category.objects.get(id = 1)
        )

        Room.objects.create(
                    id                  = 2,
                    name                = "펜션2",
                    address             = "강원도",
                    detail_address      = "강릉",
                    price               = 10000,
                    description         = "바다에서 즐기는 서핑",
                    latitude            = 101.2010,
                    longitude           = 20.1221,
                    maximum_occupancy   = 10,
                    bedroom             = 10,
                    bathroom            = 10,
                    bed                 = 10,
                    host                = Host.objects.get(id = 1),
                    room_type           = RoomType.objects.get(id = 2),    
                    category            = Category.objects.get(id = 5)
        )

        Image.objects.bulk_create([
            Image(id = 1, room = Room.objects.get(id = 1), url = "https://images.unsplash.com/photo-1610641818989-c2051b5e2cfd?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1770&q=80"),
            Image(id = 2, room = Room.objects.get(id = 1), url = "https://images.unsplash.com/photo-1582719508461-905c673771fd?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1450&q=80"),
            Image(id = 3, room = Room.objects.get(id = 1), url = "https://images.unsplash.com/photo-1586611292717-f828b167408c?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1674&q=80"),
            Image(id = 4, room = Room.objects.get(id = 2), url = "https://images.unsplash.com/photo-1610641818989-c2051b5e2cfd?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1770&q=80"),
            Image(id = 5, room = Room.objects.get(id = 2), url = "https://images.unsplash.com/photo-1582719508461-905c673771fd?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1450&q=80"),
            Image(id = 6, room = Room.objects.get(id = 2), url = "https://images.unsplash.com/photo-1586611292717-f828b167408c?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1674&q=80")
        ])
        
        RoomFacility.objects.bulk_create([
            RoomFacility(id = 1, room = Room.objects.get(id = 1), room_facility = Facility.objects.get(id = 1) ),
            RoomFacility(id = 2, room = Room.objects.get(id = 1), room_facility = Facility.objects.get(id = 2) ),
            RoomFacility(id = 3, room = Room.objects.get(id = 1), room_facility = Facility.objects.get(id = 3) ),
            RoomFacility(id = 4, room = Room.objects.get(id = 1), room_facility = Facility.objects.get(id = 4) ),
            RoomFacility(id = 5, room = Room.objects.get(id = 1), room_facility = Facility.objects.get(id = 5) ),
            RoomFacility(id = 6, room = Room.objects.get(id = 2), room_facility = Facility.objects.get(id = 1) ),
            RoomFacility(id = 7, room = Room.objects.get(id = 2), room_facility = Facility.objects.get(id = 2) ),
            RoomFacility(id = 8, room = Room.objects.get(id = 2), room_facility = Facility.objects.get(id = 3) ),
            RoomFacility(id = 9, room = Room.objects.get(id = 2), room_facility = Facility.objects.get(id = 4) ),
            RoomFacility(id = 10, room = Room.objects.get(id = 2), room_facility = Facility.objects.get(id = 5) )
        ])

        Reservation.objects.create(
                    id                  = 1,
                    number              = "100",
                    check_in            = "2022-08-02",
                    check_out           = "2022-08-10",
                    people              = 10,
                    price               = 10000.00,
                    room                = Room.objects.get(id = 1),
                    user                = User.objects.get(id = 1)
        )

        Reservation.objects.create(
                    id                  = 2,
                    number              = "200",
                    check_in            = "2022-08-12",
                    check_out           = "2022-08-15",
                    people              = 10,
                    price               = 10000.00,
                    room                = Room.objects.get(id = 2),
                    user                = User.objects.get(id = 1),       
        )

    def tearDown(self):
        Reservation.objects.all().delete()
        User.objects.all().delete()
        Host.objects.all().delete()
        Room.objects.all().delete()
        Category.objects.all().delete()
        RoomFacility.objects.all().delete()
        Facility.objects.all().delete()
        Image.objects.all().delete()
        RoomType.objects.all().delete()

    def test_success_reservation_get(self):
        client      = Client()
        token       = jwt.encode({'id': User.objects.get(id=1).id}, settings.SECRET_KEY, settings.ALGORITHM)
        headers     = {'HTTP_Authorization' : token}
        response    = client.get('/reservations', **headers, content_type='application/json')

        body =  {
                "RESULT" : [{
                    'reservation_number'        : "100",
                    'user_name'                 : "kim doyeon",
                    'room'                      : "펜션1",
                    'price'                     : "10000.00",
                    'people'                    : 10,
                    'check_in'                  : "2022-08-02",
                    'check_out'                 : "2022-08-10",
                    'img'                       : "https://images.unsplash.com/photo-1610641818989-c2051b5e2cfd?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1770&q=80"
                },
                {   'reservation_number'        : "200",
                    'user_name'                 : "kim doyeon",
                    'room'                      : "펜션2",
                    'price'                     : "10000.00",
                    'people'                    : 10,
                    'check_in'                  : "2022-08-12",
                    'check_out'                 : "2022-08-15",
                    'img'                       : "https://images.unsplash.com/photo-1610641818989-c2051b5e2cfd?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1770&q=80"
                }
                ]
            }
        
        self.assertEqual(response.json(), body)
        self.assertEqual(response.status_code, 200)
    
    def test_Success_Reservation_post(self):
        client = Client()
                    
        data = {
                    "id"                  : 1,
                    "check_in"            : "2022-08-02",
                    "check_out"           : "2022-08-10",
                    "people"              : 10,
                    "price"               : 10000.00,
                    "room"                : 1
        }

        token    = jwt.encode({'id': User.objects.get(id=1).id}, settings.SECRET_KEY, settings.ALGORITHM)
        headers  = {"HTTP_AUTHORIZATION": token}
        response = client.post('/reservations', json.dumps(data), content_type='application/json', **headers)
        
        self.assertEqual(response.json(), {"MESSAGE": "SUCCESS"})
        self.assertEqual(response.status_code, 201)

    def test_Key_Error_Reservation_post(self):
        client = Client()

        data = {
                    "id"                  : 1,
                    "check_in"            : "2022-08-02",
                    "check_out"           : "2022-08-10",
                    "people"              : 10,
                    "price"               : 10000.00,
                    #"room"                : 1
        }

        token    = jwt.encode({'id': User.objects.get(id=1).id}, settings.SECRET_KEY, settings.ALGORITHM)
        headers  = {"HTTP_AUTHORIZATION": token}
        response = client.post('/reservations', json.dumps(data), content_type='application/json', **headers)

        self.assertEqual(response.json(), {"MESSAGE" : "KEY_ERROR"})
        self.assertEqual(response.status_code, 400)

    def test_DoesNot_Exist_Room_Error_Reservation_post(self):
        client = Client()

        data = {
                    "id"                  : 1,
                    "check_in"            : "2022-08-02",
                    "check_out"           : "2022-08-10",
                    "people"              : 10,
                    "price"               : 10000.00,
                    "room"                : 100
        }

        token    = jwt.encode({'id': User.objects.get(id=1).id}, settings.SECRET_KEY, settings.ALGORITHM)
        headers  = {"HTTP_AUTHORIZATION": token}
        response = client.post('/reservations', json.dumps(data), content_type='application/json', **headers)

        self.assertEqual(response.json(), {"MESSAGE" : "DOESNOT_EXIST_ROOM"})
        self.assertEqual(response.status_code, 400)