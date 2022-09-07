##  🏨 위앤비 [We&B] _ wecode 35기 2차 프로젝트
- 위앤비는 에어비앤비를 모티브로 한 프로젝트입니다.
- 기획과 디자인은 참고하고 기능은 직접 구현하였습니다.

<br>

## 🏨 선정 이유
- 숙소 예약 서비스로 카카오 API를 사용한 소셜 로그인 기능과 함께 유저와 관련된 다양한 기능을 구현해 볼 수 있기 때문입니다.
- 상단 Nav바 검색과 오른쪽 상단 필터 기능을 활용해 다양한 필터링 시스템을 경험할 수 있기 때문입니다.
- 예약 서비스와 함께 예약 취소 시 해당 데이터를 삭제하는 로직을 구현해 볼 수 있기 때문입니다.

<br>

## 🏨 개발 인원
- Back-end  : 김도연, 전은형, 조민지
- Front-end : 류승연, 정억화, 정예빈, 최원익

<br>

## 🏨 개발 기간
- 2022.08.01 ~ 2022.08.12 (2주)

<br>

## 🏨 DB 모델링
- 모델링
<img width="943" alt="Screenshot 2022-08-12 at 12 39 38 PM" src="https://user-images.githubusercontent.com/106012542/184280866-ae2388b5-9ff7-43ad-9adb-269e3829a23c.png">

<br>

## 🏨 Directory 구조
```
.
├── __pycache__
├── core
├── hosts
├── reservations
├── reviews
├── rooms
├── users
└── wnb
```
<br>

## 🏨 백엔드 역할
- 김도연
  - AWS 배포
  - 예약 CRD API
- 전은형
  - 카카오톡 소셜 회원가입, 로그인 API
  - 회원 정보 수정 API
- 조민지
  - 룸 리스트 API
  - 룸 상세 API
  
<br>

## 🏨 백엔드 기술 스택
  - Back-end : Python, Django, JWT, Miniconda, 외부 API
  - Database : dbdiagram.io, MySQL
  - HTTP     : Postman
  - Common   : Trello, Slack, Git & Github
    
<br>

## 🏨 시연 영상
- 영상 주소 : https://www.youtube.com/watch?v=btDS154C5yg
![로그인 추가정보 입력](https://user-images.githubusercontent.com/106012542/184283204-7b1984e8-30a3-49fe-9862-ca3eb501aa8c.gif)
![카테고리 이동](https://user-images.githubusercontent.com/106012542/184288880-ba8540ee-b015-4b19-a583-7753f8dd67cb.gif)
![예약취소 후 달력, 로그아웃](https://user-images.githubusercontent.com/106012542/184288918-aa2fec98-d109-4320-a4e6-dbc3b39ccdf4.gif)
  
<br>

## 🏨 API명세서
- 주소 : https://www.notion.so/API-473f57d4911847eabe0b6828baa56961
![Aug-12-2022 12-52-28](https://user-images.githubusercontent.com/106012542/184282089-9bc4d9fb-76fc-4df8-8213-c7aa9b75b352.gif)

<br>

## 🏨 Trello
![Aug-12-2022 12-54-59](https://user-images.githubusercontent.com/106012542/184282292-fc5a06f6-600e-4140-b665-00d5381e7628.gif)
