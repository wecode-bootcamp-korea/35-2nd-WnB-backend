import json
import jwt

from django.test    import TestCase, Client
from django.conf    import settings
from unittest.mock  import patch, MagicMock

from users.models   import User

class KakaoOauthViewTest(TestCase):
    def setUp(self):
        User.objects.create(
              id                = 1,
              email             = 'test@gmail.com',
              kakao_id          = 44444,
              kakao_profile_img = 'https://i.pinimg.com/564x/5c/a1/42/5ca142d34fd1903773b4f4e6f43d9045.jpg',
        )
        
    def tearDown(self):
        User.objects.all().delete()
    
    @patch("users.views.requests")
    def test_success_kakao_signup(self, mocked_requests):
        client = Client()
        
        class MockedResponse:
            def json(self):
                return {
                    "id": 2022080735,
                    "connected_at": "2022-08-04T06:27:33Z",
                    "properties": {
                        "profile_image": "프로필이미지 url",
                        "thumbnail_image": "카카오 배경화면 이미지 url"
                    },
                    "kakao_account": {
                        "profile_image_needs_agreement": 'false',
                        "profile": {
                            "thumbnail_image_url": "카카오 thumb nail img",
                            "profile_image_url": "카카오 프로필 이미지",
                            "is_default_image": 'false'
                        },
                        "has_email": 'true',
                        "email_needs_agreement": 'false',
                        "is_email_valid": 'true',
                        "is_email_verified": 'true',
                        "email": "fake-email@test.com",
                        "has_birthday": 'true',
                        "birthday_needs_agreement": 'false',
                        "birthday": "0809",
                        "birthday_type": "SOLAR"
                    }
                }
            
        mocked_requests.get = MagicMock(return_value = MockedResponse())
        
        headers  = {'HTTP_Authorization' : '가짜 access_token'}
        response = client.get("/users/kakao/oauth", **headers)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), {
            'message': 'SUCCESS',
            'token'  : jwt.encode({'id':User.objects.latest('id').id}, settings.SECRET_KEY, settings.ALGORITHM)
        })  
           
    @patch("users.views.requests")
    def test_success_kakao_signin(self, mocked_requests):
        client = Client()
        
        class MockedResponse:
            def json(self):
                return {
                    "id": 44444,
                    "connected_at": "2022-08-04T06:27:33Z",
                    "properties": {
                        "profile_image": "프로필이미지 url",
                        "thumbnail_image": "카카오 배경화면 이미지 url"
                    },
                    "kakao_account": {
                        "profile_image_needs_agreement": 'false',
                        "profile": {
                            "thumbnail_image_url": "카카오 thumb nail img",
                            "profile_image_url": "카카오 프로필 이미지",
                            "is_default_image": 'false'
                        },
                        "has_email": 'true',
                        "email_needs_agreement": 'false',
                        "is_email_valid": 'true',
                        "is_email_verified": 'true',
                        "email": "fake-email@test.com",
                        "has_birthday": 'true',
                        "birthday_needs_agreement": 'false',
                        "birthday": "0909",
                        "birthday_type": "SOLAR"
                    }
                }
                 
        mocked_requests.get = MagicMock(return_value = MockedResponse())
        
        headers  = {'HTTP_Authorization' : '가짜 access_token'}
        response = client.get("/users/kakao/oauth", **headers)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
            'message': 'SUCCESS',
            'token'  : jwt.encode({'id':User.objects.latest('id').id}, settings.SECRET_KEY, settings.ALGORITHM)
        })           

class UserAdditionalInfoViewTest(TestCase):
    def setUp(self):
        User.objects.create(
            id                = 1,
            kakao_id          = '12345667',
            email             = 'test1@test.com',
            kakao_profile_img = 'http://test1.com'
        )
    
        User.objects.create(
            id                = 2,
            kakao_id          = '4444444',
            email             = 'test2@test.com',
            kakao_profile_img = 'http://test2.com'
        )
        
        User.objects.create(
            id                = 3,
            kakao_id          = '7777777',
            email             = 'test3@test.com',
            kakao_profile_img = 'http://test3.com',
            phone_number      = '010-4444-4444'
        )
    
    def tearDown(self):
        User.objects.all().delete()
    
    def test_fail_user_patch_additional_info_because_no_token(self):
        client = Client()
        
        data = {
            'first_name'  : '은형',
            'last_name'   : '전',
            'phone_number': '010-1223-1234',
            'birth_day'   : '2022-08-08'
        }
        
        response = client.patch('/users/additional-info', json.dumps(data), content_type='application/json')
        
        self.assertEqual(response.json(), {'message':'INVALID_TOKEN'})
        self.assertEqual(response.status_code, 400)
        
    def test_fail_user_patch_additional_info_because_wrong_token(self):
        client = Client()
        
        data = {
            'first_name'  : '은형',
            'last_name'   : '전',
            'phone_number': '010-1223-1234',
            'birth_day'   : '2022-08-08'
        }

        headers  = {"HTTP_AUTHORIZATION": 'fake_token'}
        response = client.patch('/users/additional-info', json.dumps(data), content_type='application/json', **headers)
        
        self.assertEqual(response.json(), {'message':'INVALID_TOKEN'})
        self.assertEqual(response.status_code, 400)
        
    def test_fail_user_patch_additional_info_because_already_exist_number(self):
        client = Client()
        
        data = {
            'first_name'  : '은형',
            'last_name'   : '전',
            'phone_number': '010-4444-4444',
            'birth_day'   : '2022-08-08'
        }

        token    = jwt.encode({'id': User.objects.get(id=2).id}, settings.SECRET_KEY, settings.ALGORITHM)
        headers  = {"HTTP_AUTHORIZATION": token}
        response = client.patch('/users/additional-info', json.dumps(data), content_type='application/json', **headers)
        
        self.assertEqual(response.json(), {'message':'PHONE_NUMBER_ALREADY_EXIST'})
        self.assertEqual(response.status_code, 400)
                
    def test_fail_user_patch_additional_info_because_key_error_no_birth_day(self):
        client = Client()
        
        data = {
            'first_name'  : '은형',
            'last_name'   : '전',
            'phone_number': '010-4444-4444'
        }

        token    = jwt.encode({'id': User.objects.get(id=2).id}, settings.SECRET_KEY, settings.ALGORITHM)
        headers  = {"HTTP_AUTHORIZATION": token}
        response = client.patch('/users/additional-info', json.dumps(data), content_type='application/json', **headers)
        
        self.assertEqual(response.json(), {'message':'KEY_ERROR'})
        self.assertEqual(response.status_code, 400)
        
    def test_fail_user_patch_additional_info_because_first_name_validation(self):
        client = Client()
        
        data = {
            'first_name'  : 'eunhyung',
            'last_name'   : '전',
            'phone_number': '010-4444-4444',
            'birth_day'   : '2022-08-08'
        }

        token    = jwt.encode({'id': User.objects.get(id=2).id}, settings.SECRET_KEY, settings.ALGORITHM)
        headers  = {"HTTP_AUTHORIZATION": token}
        response = client.patch('/users/additional-info', json.dumps(data), content_type='application/json', **headers)
        
        self.assertEqual(response.json(), {'message':"['FIRST_NAME_ERROR']"})
        self.assertEqual(response.status_code, 400)
        
    def test_fail_user_patch_additional_info_because_last_name_validation(self):
        client = Client()
        
        data = {
            'first_name'  : '은형',
            'last_name'   : 'jeon',
            'phone_number': '010-8787-1203',
            'birth_day'   : '2022-08-08'
        }

        token    = jwt.encode({'id': User.objects.get(id=2).id}, settings.SECRET_KEY, settings.ALGORITHM)
        headers  = {"HTTP_AUTHORIZATION": token}
        response = client.patch('/users/additional-info', json.dumps(data), content_type='application/json', **headers)
        
        self.assertEqual(response.json(), {'message':"['LAST_NAME_ERROR']"})
        self.assertEqual(response.status_code, 400)
        
    def test_fail_user_patch_additional_info_because_phone_number_validation(self):
        client = Client()
        
        data = {
            'first_name'  : '은형',
            'last_name'   : '전',
            'phone_number': '01012341234',
            'birth_day'   : '2022-08-08'
        }

        token    = jwt.encode({'id': User.objects.get(id=2).id}, settings.SECRET_KEY, settings.ALGORITHM)
        headers  = {"HTTP_AUTHORIZATION": token}
        response = client.patch('/users/additional-info', json.dumps(data), content_type='application/json', **headers)
        
        self.assertEqual(response.json(), {'message':"['PHONE_NUMBER_ERROR']"})
        self.assertEqual(response.status_code, 400)
        
    def test_success_user_patch_additional_info(self):
        client = Client()
        
        data = {
            'first_name'  : '은형',
            'last_name'   : '전',
            'phone_number': '010-1223-1234',
            'birth_day'   : '2022-08-08'
        }

        token    = jwt.encode({'id': User.objects.get(id=1).id}, settings.SECRET_KEY, settings.ALGORITHM)
        headers  = {"HTTP_AUTHORIZATION": token}
        response = client.patch('/users/additional-info', json.dumps(data), content_type='application/json', **headers)
        
        self.assertEqual(response.json(), {'message':'USER_INFO_UPDATED'})
        self.assertEqual(response.status_code, 201)