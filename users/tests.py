import json
import jwt

from django.test    import TestCase, Client

from users.models   import User
from django.conf    import settings

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
        
        self.assertEqual(response.json(), {'message':'USER_INFO_UPDATED', 'user_name':f'{User.objects.get(id=1).last_name + User.objects.get(id=1).first_name}'})
        self.assertEqual(response.status_code, 201)

