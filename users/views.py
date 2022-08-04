import requests
import json
import jwt

from django.shortcuts   import redirect
from django.http        import JsonResponse
from django.views       import View

from users.models import User
from wnb          import settings

REST_API_KEY = 'b75ac57d41bd4ab6442b150d79e36bee'
REDIRECT_URI = 'http://127.0.0.1:8000/users/signup'
    
class KakaoSignUpView(View):
    def get(self, request):
        
        ###### 인가코드 요청하기 (나혼자)
        KAKAO_URL =f'https://kauth.kakao.com/oauth/authorize?response_type=code&client_id=${REST_API_KEY}&redirect_uri=${REDIRECT_URI}'

        code_data = {
            'grant_type' : 'authorization_code',
            'client_id' : REST_API_KEY,
            'redirect_uri' : REDIRECT_URI,
            'response_type' : 'code'
        }
        
        code_response = requests.get(KAKAO_URL, data=code_data)  # 요청에 대한 응답이 access_code에 담김
        
        code = request.GET.get('code')   # url에 /~~?code=1235로부터 code값 뽑아오기
        # print('코드', code)               # code뽑아오기 성공
        
        ###### 인가코드로 토큰 요청하기 (나혼자)
        KAKAO_URL_TOKEN = 'https://kauth.kakao.com/oauth/token' # 요청보낼 카카오 주소

        token_data = {
            'grant_type' : 'authorization_code',
            'client_id' : REST_API_KEY,
            'redirect_uri' : REDIRECT_URI,
            'code' : code
        }
        
        token_response = requests.post(KAKAO_URL_TOKEN, data=token_data).json()   # post로 보내라고 되어있음
        
        # print(token_response)                     # {}안에 필요한 값들이 담겨옴
        token = token_response.get('access_token')  # get을 사용하면 딕셔너리에서 벨류값 추출 가능
        # print('토큰', token)                         # 토큰 뽑아오기 성공

        ###### 토큰으로 유저정보 요청하기 (나혼자)
        KAKAO_USER_INFO = 'https://kapi.kakao.com/v2/user/me'
        HEADER          = {'Authorization' : f'Bearer {token}'}
        
        user_info_response = requests.get(KAKAO_USER_INFO, headers=HEADER).json()  
        
        kakao_id          = user_info_response['id']    # {} 딕셔너리에서 필요한 데이터값들 추출하기
        kakao_profile_img = user_info_response['kakao_account']['profile']['profile_image_url']
        email             = user_info_response['kakao_account']['email']
        # print(kakao_id, kakao_profile_img, email)       # 유저 데이터 뽑기 성공
        
        print('여기서에러')
        
        ###### kakao_id가 우리 DB에 있는 사람이라면 메인창으로 이동하기
        ## 에러발생 : 애초에 if문 안으로 못들어갈텐데 에러가 발생하고있음
        # if User.objects.get(kakao_id = kakao_id).exists():
        #     print('들어감')
        #     return redirect('https://www.naver.com')    # 이동시킬 메인화면 URL 적기
        
        # print('안들어감')
        
        ###### 우리 DB에 없는 사람이라면 추가정보 입력하는 창으로 이동하기
        return redirect(f'/users/info?kakao_id={kakao_id}')
    
class ExtraUserInfoView(View):
    # def get(self, request):
    
        # a = request.GET.get('kakao_id')   # def get, get하면 받을 수 있음.
        # print(a)
        
    ###### get -> post는 안되는데.. 이게 되나?? ㅠㅠㅠㅠㅠ    
    def post(self, request):
        a = request.POST['kakao_id']
        print(a)
        
        # 사용자 정보를 추가 입력 받고
        # User 객체를 생성한다
        # User.objects.create(
#             first_name = first_name,          
#             last_name = last_name,      
#             email = email,         
#             kakao_id = kakao_id,      
#             kakao_profile_img = kakao_profile_img,
#             phone_number = phone_number,        
#             birth_day = birth_day
#         )

        # JWT토큰을 생성한다.
        # user_token = jwt.encode({'kakao_id' : a}, settings.SECRET_KEY, settings.ALGORITHM)
                
        # return JsonResponse({'result':'test'}, status=200)
    
        
        
        
        
        # 인가코드 받기 (예빈님)
        
        # code = request.META.get('HTTP_AUTHORIZATION')   # 인가 코드. 
        
        # token_response = requests.post("https://kauth.kakao.com/oauth/token", data=data).json()
        # print(token_response)
    
        # token = request.META.get('HTTP_AUTHORIZATION')         # 예빈님이 보내준 요청의 헤더에 있는 AUTHORIZATION 값을 뽑는다.
        # # print(token)
        # url    = 'https://kapi.kakao.com/v2/user/me'
        # header = {"Authorization" : f'Bearer ${token}'}

        # response = requests.get(url, headers=header)
        # response = response.json()    # 카카오 서버로 헤더에 토큰을 담아서 '요청'을 보낸다
        # print(response)
        
        # # kakao_id = 'hello'
        # kakao_id          = response['id']
        # print(kakao_id)
        # email             = response['kakao_account']['email']
        # kakao_profile_img = response['kakao_account']['profile_image_url']
        
        # if User.objects.get(kakao_id=kakao_id).exist():
            # 유저가 이미 존재한다면
            # return redirect('https://www.google.com')  # 메인 화면으로 이동
        
        # 존재하지 않을 때 여기로 온다
        # 프론트단에서 사용자가 이름/성/생일을 입력해야하니까 새창으로 이동 => 
        # 그 입력한 값을 내가 또 받아올 수가 있나?
        # return redirect('/users/test', kakao_id=kakao_id)
        # return redirect("/users/test")
        # return JsonResponse({'result':'test'},status=200)
        # print(kakao_id)
        # return redirect('/users/test', kakao_id)
        
        # 최초가입자 카카오 로그인 => 우리회원 최초 로그인이네? db에 없어
        # 판단 후 
        # 회원정보를 입력하는 창으로 이동하고.
        # 저장 => create
        
        # null, default로 가입하고
        # 개인정보 페이지가 필요하네
        # 마이페이지에서 수정하도록