# SNS 서비스 API 개발

### ✅ <b>DRF</b>를 활용하여 SNS 서비스 서버의 <b>REST API</b>를 개발한 프로젝트 입니다.
### <b>JWT</b>를 이용하여 유저 인증을 하고, 기능에 따라 권한을 제한합니다.

`❗️ 1차 개발 기간 : 2022.07.20~2022.07.26`

<br>

## 🛠 사용 기술
<img src="https://img.shields.io/badge/Python-3776AB?style=flat&logo=Python&logoColor=white">
<img src="https://img.shields.io/badge/Django-092E20?style=flat&logo=Django&logoColor=white">
<img src="https://img.shields.io/badge/SQLite-003B57?style=flat&logo=SQLite&logoColor=white">
<img src="https://img.shields.io/badge/Git-F05032?style=flat&logo=Git&logoColor=white">

<br>

## 📙 API 명세서

<img width="896" alt="스크린샷 2022-07-26 오후 6 26 16" src="https://user-images.githubusercontent.com/76423946/180973178-e37cb793-9a93-4b87-8911-4db86609689a.png">

<details>
<summary>API의 Request & Response</summary> 
<div markdown="1">

- signup
```
➡️ Request
{
  "email": "user1@gmail.com",
  "username": "user1",
  "password": "user1
}

➡️ Response 
(201 created)
{
  "message": "회원가입이 성공적으로 되었습니다."
}

(400 bad request)
{
  "message": "회원가입에 실패했습니다."
}
```
- login
```
➡️ Request
{
  "email": "user1@gmail.com",
  "password": "user1
}

➡️ Response 
(200 ok)
{
    "message": "로그인 되었습니다.",
    "access_token":  "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjU4ODA3NzI4LCJpYXQiOjE2NTg4MDc0MjgsImp0aSI6IjJiZThiNzU3NjBlNTRjMzg4ZTVmNDE2NjE5MGE5NDAyIiwidXNlcl9pZCI6MiwiZW1haWwiOiJ1c2VyMUBnbWFpbC5jb20iLCJ1c2VybmFtZSI6InVzZXIxIn0.3Fi_2tEBcwl1o8c15PAhKPhFKsboEGra6J3zg15mgvY",
    "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTY2MDAxNzAyOCwiaWF0IjoxNjU4ODA3NDI4LCJqdGkiOiJhYWE5NDQyMzhiMjA0MTc4OGE1NjNiOWEyNWYzYWExNiIsInVzZXJfaWQiOjIsImVtYWlsIjoidXNlcjFAZ21haWwuY29tIiwidXNlcm5hbWUiOiJ1c2VyMSJ9.42icshZ_1nCdUvXXHXtoCqNL4rLLxzVkCicJmsGhlMU"
}

(401 unauthorized)
{
    "error": "존재하지 않는 계정이거나 비밀번호가 맞지 않습니다."
}
```
- token_refresh
```
➡️ Request
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTY2MDAxNzAyOCwiaWF0IjoxNjU4ODA3NDI4LCJqdGkiOiJhYWE5NDQyMzhiMjA0MTc4OGE1NjNiOWEyNWYzYWExNiIsInVzZXJfaWQiOjIsImVtYWlsIjoidXNlcjFAZ21haWwuY29tIiwidXNlcm5hbWUiOiJ1c2VyMSJ9.42icshZ_1nCdUvXXHXtoCqNL4rLLxzVkCicJmsGhlMU"
}

➡️ Response 
(200 ok)
{
    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjU4ODA3OTAwLCJpYXQiOjE2NTg4MDc1ODgsImp0aSI6IjE1MmE3ZTk3MTRhMDRjNzBiNTQyMTgzYTM4NWM4MmU5IiwidXNlcl9pZCI6MiwiZW1haWwiOiJ1c2VyMUBnbWFpbC5jb20iLCJ1c2VybmFtZSI6InVzZXIxIn0.TYa5H3BKzmYsc4gErDufX7AofU8oAOhSPEgu6H0x2GQ"
}

(401 unauthorized : refresh 토큰이 잘못된 경우)
{
    "detail": "유효하지 않거나 만료된 토큰",
    "code": "token_not_valid"
}
or
(400 bad request : request에 refresh 토큰이 없는 경우)
{
    "refresh": [
        "이 필드는 필수 항목입니다."
    ]
}
```
- post_list_create(list)
```
➡️ Request
{}

➡️ Response 
(200 ok)
[
    {
        "id": 1,
        "writer": "mindi",
        "tags": [
            "#sns",
            "#blue"
        ],
        "like_count": 3,
        "like_users": [
            {
                "id": 1,
                "username": "mindi"
            },
            {
                "id": 2,
                "username": "user1"
            },
            {
                "id": 3,
                "username": "user2"
            }
        ],
        "title": "my feeling",
        "content": "badbad, actually not bad",
        "created_at": "2022-07-21T12:44:49.884216",
        "updated_at": "2022-07-25T12:42:57.999361",
        "view_counts": 18
    },
    ...
]
```
- post_list_create(list, is_deleted=true)
```
➡️ Request
<Headers>
Authorization : Bearer {access token}
{}

➡️ Response 
(200 ok)
[
    {
        "id": 27,
        "writer": "user1",
        "tags": [
            "#sns",
            "#orange"
        ],
        "like_count": 0,
        "like_users": [],
        "title": "user1의 첫 번째 게시글",
        "content": "user1의 첫 번째 게시글 입니다. 오예",
        "created_at": "2022-07-22T20:19:59.435413",
        "updated_at": "2022-07-23T00:40:19.888611",
        "is_deleted": true,
        "view_counts": 0
    }
]

(401 unauthorized : access 토큰이 잘못된 경우)
{
    "detail": "이 토큰은 모든 타입의 토큰에 대해 유효하지 않습니다",
    "code": "token_not_valid",
    "messages": [
        {
            "token_class": "AccessToken",
            "token_type": "access",
            "message": "유효하지 않거나 만료된 토큰"
        }
    ]
}
or
(401 unauthorized : header에 access 토큰이 없는 경우)
{
    "error": "접근권한이 없습니다."
}
```
- post_list_create(create)
```
➡️ Request
<Headers>
Authorization : Bearer {access token}

{
    "title": "덕몽어스",
    "content": "오늘은 덕몽어스 하는날~",
    "tags": [
        {"name":"#덕몽어스"},
        {"name":"#GooseGooseDuck"}
        ]
}

➡️ Response 
(201 created)
{
    "id": 31,
    "title": "덕몽어스",
    "content": "오늘은 덕몽어스 하는날~",
    "tags": [
        {
            "name": "#덕몽어스"
        },
        {
            "name": "#GooseGooseDuck"
        }
    ]
}

(401 unauthorized : access 토큰이 잘못된 경우)
{
    "detail": "이 토큰은 모든 타입의 토큰에 대해 유효하지 않습니다",
    "code": "token_not_valid",
    "messages": [
        {
            "token_class": "AccessToken",
            "token_type": "access",
            "message": "유효하지 않거나 만료된 토큰"
        }
    ]
}
or
(401 unauthorized : header에 access 토큰이 없는 경우)
{
    "detail": "자격 인증데이터(authentication credentials)가 제공되지 않았습니다."
}
```
- post_retrieve_update_delete(retrieve)
```
➡️ Request
{}

➡️ Response 
(200 ok)
{
    "id": 28,
    "writer": "mindi",
    "tags": [
        "#Monday",
        "#월요일"
    ],
    "like_count": 3,
    "like_users": [
        {
            "id": 3,
            "username": "user2"
        },
        {
            "id": 4,
            "username": "user3"
        },
        {
            "id": 5,
            "username": "user4"
        }
    ],
    "title": "월요일",
    "content": "오늘은 월요일 입니다.",
    "created_at": "2022-07-25T14:12:40.586701",
    "updated_at": "2022-07-26T18:40:11.692086",
    "view_counts": 7
}

(404 not found : 없는 게시글인 경우)
{
    "detail": "찾을 수 없습니다."
}
```
- post_retrieve_update_delete(update)
```
➡️ Request
<Headers>
Authorization : Bearer {access token}

{
    "tags": [
        {
            "name": "#Monday"
        },
                {
            "name": "#월요일싫다"
        }
    ]
}

➡️ Response 
(200 ok)
{
    "id": 28,
    "title": "월요일",
    "content": "오늘은 월요일 입니다.",
    "tags": [
        {
            "name": "#Monday"
        },
        {
            "name": "#월요일싫다"
        }
    ]
}

(401 unauthorized : header에 access 토큰이 없는 경우)
{
    "detail": "자격 인증데이터(authentication credentials)가 제공되지 않았습니다."
}
or
(401 unauthorized : access 토큰이 잘못된 경우)
{
    "detail": "이 토큰은 모든 타입의 토큰에 대해 유효하지 않습니다",
    "code": "token_not_valid",
    "messages": [
        {
            "token_class": "AccessToken",
            "token_type": "access",
            "message": "유효하지 않거나 만료된 토큰"
        }
    ]
}
or
(403 forbidden : 게시글 작성 본인 또는 관리자가 아닌 경우)
{
    "detail": "이 작업을 수행할 권한(permission)이 없습니다."
}
```
- post_retrieve_update_delete(delete)
```
➡️ Request
<Headers>
Authorization : Bearer {access token}

{}

➡️ Response 
(200 ok)
{
    "id": 28,
    "writer": "mindi",
    "tags": [
        {
            "name": "#Monday"
        },
        {
            "name": "#월요일싫다"
        }
    ],
    "like_count": 3,
    "like_users": [
        {
            "id": 3,
            "username": "user2"
        },
        {
            "id": 4,
            "username": "user3"
        },
        {
            "id": 5,
            "username": "user4"
        }
    ],
    "title": "월요일",
    "content": "오늘은 월요일 입니다.",
    "created_at": "2022-07-25T14:12:40.586701",
    "updated_at": "2022-07-26T19:45:16.470693",
    "is_deleted": true,
    "view_counts": 9
}

(401 unauthorized : header에 access 토큰이 없는 경우)
{
    "detail": "자격 인증데이터(authentication credentials)가 제공되지 않았습니다."
}
or
(401 unauthorized : access 토큰이 잘못된 경우)
{
    "detail": "이 토큰은 모든 타입의 토큰에 대해 유효하지 않습니다",
    "code": "token_not_valid",
    "messages": [
        {
            "token_class": "AccessToken",
            "token_type": "access",
            "message": "유효하지 않거나 만료된 토큰"
        }
    ]
}
or
(403 forbidden : 게시글 작성자 본인 또는 관리자가 아닌 경우)
{
    "detail": "이 작업을 수행할 권한(permission)이 없습니다."
}
or
(404 not found : 이미 삭제된 게시글인 경우)
{
    "detail": "찾을 수 없습니다."
}
```
- post_restore
```
➡️ Request
<Headers>
Authorization : Bearer {access token}

{}

➡️ Response 
(200 ok)
{
    "id": 28,
    "writer": "mindi",
    "tags": [
        {
            "name": "#Monday"
        },
        {
            "name": "#월요일싫다"
        }
    ],
    "like_count": 3,
    "like_users": [
        {
            "id": 3,
            "username": "user2"
        },
        {
            "id": 4,
            "username": "user3"
        },
        {
            "id": 5,
            "username": "user4"
        }
    ],
    "title": "월요일",
    "content": "오늘은 월요일 입니다.",
    "created_at": "2022-07-25T14:12:40.586701",
    "updated_at": "2022-07-26T19:59:30.293161",
    "is_deleted": false,
    "view_counts": 9
}

(401 unauthorized : header에 access 토큰이 없는 경우)
{
    "detail": "자격 인증데이터(authentication credentials)가 제공되지 않았습니다."
}
or
(401 unauthorized : access 토큰이 잘못된 경우)
{
    "detail": "이 토큰은 모든 타입의 토큰에 대해 유효하지 않습니다",
    "code": "token_not_valid",
    "messages": [
        {
            "token_class": "AccessToken",
            "token_type": "access",
            "message": "유효하지 않거나 만료된 토큰"
        }
    ]
}
or
(403 forbidden : 게시글 작성자 본인 또는 관리자가 아닌 경우)
{
    "detail": "이 작업을 수행할 권한(permission)이 없습니다."
}
or
(404 not found : 삭제되지 않았거나 이미 복구된 게시글인 경우)
{
    "detail": "찾을 수 없습니다."
}
```
- post_like
```
➡️ Request
<Headers>
Authorization : Bearer {access token}

{}

➡️ Response 
(200 ok)
{
    "message": "이 포스트에 좋아요를 눌렀습니다."
}

(401 unauthorized : header에 access 토큰이 없는 경우)
{
    "detail": "자격 인증데이터(authentication credentials)가 제공되지 않았습니다."
}
or
(401 unauthorized : access 토큰이 잘못된 경우)
{
    "detail": "이 토큰은 모든 타입의 토큰에 대해 유효하지 않습니다",
    "code": "token_not_valid",
    "messages": [
        {
            "token_class": "AccessToken",
            "token_type": "access",
            "message": "유효하지 않거나 만료된 토큰"
        }
    ]
}
or
(400 bad request : 이미 좋아요를 누른 경우)
[
    "이미 좋아요를 했습니다."
]
```
- post_unlike
```
➡️ Request
<Headers>
Authorization : Bearer {access token}

{}

➡️ Response 
(200 ok)
{
    "message": "이 포스트에 대한 좋아요를 취소했습니다."
}

(401 unauthorized : header에 access 토큰이 없는 경우)
{
    "detail": "자격 인증데이터(authentication credentials)가 제공되지 않았습니다."
}
or
(401 unauthorized : access 토큰이 잘못된 경우)
{
    "detail": "이 토큰은 모든 타입의 토큰에 대해 유효하지 않습니다",
    "code": "token_not_valid",
    "messages": [
        {
            "token_class": "AccessToken",
            "token_type": "access",
            "message": "유효하지 않거나 만료된 토큰"
        }
    ]
}
or
(400 bad request : 이미 좋아요를 취소했거나 좋아요를 하지 경우)
[
    "좋아요를 하지 않은 게시글로 좋아요를 취소할 수 없습니다."
]
```
</div>
</details>

<br>

## 📋 ERD
<img width="700" alt="스크린샷 2022-07-26 오후 9 15 59" src="https://user-images.githubusercontent.com/76423946/181003574-6ecec573-97e3-443b-9471-a2b1eb8427dd.png">

- 장고의 기본 User 모델이 아닌, 커스텀 User 모델을 사용합니다.
- Post 모델의 writer는 User 모델과 N:1관계 입니다.
- Post 모델의 like_users는 User 모델과 N:M 관계 입니다.
- Post모델과 Tags모델은 N:M 관계입니다.

<br>

## ✨ Git 컨벤션, 코드 컨벤션
- git commit message template
```
# --- 제목(title) - 50자 이내로 ---
# <타입(type)> <제목(title)>
# 예시(ex) : Docs : #1 README.md 수정
# --- 본문(content) - 72자마다 줄바꾸기  ---
# 예시(ex) :
# - Workflow
# 1. 커밋 메시지에 대한 문서 제작 추가.
# 2. commit message docs add.
# --- 꼬리말(footer) ---
# <타입(type)> <이슈 번호(issue number)>
# 예시(ex) : Fix #122
# --- COMMIT END ---
# <타입> 리스트
#   Init    : 초기화
#   Feat    : 기능추가
#   Add     : 내용추가
#   Update  : 기능 보완 (업그레이드)
#   Fix     : 버그 수정
#   Refactor: 리팩토링
#   Style   : 스타일 (코드 형식, 세미콜론 추가: 비즈니스 로직에 변경 없음)
#   Docs    : 문서 (README.md, ignore파일 추가(Add), 수정, 삭제)
#   Test    : 테스트 (테스트 코드 추가, 수정, 삭제: 비즈니스 로직에 변경 없음)
#   Chore   : 기타 변경사항 (빌드 스크립트 수정 등)
#   Rename  : 이름(파일명, 폴더명, 변수명 등)을 수정하거나 옮기는 작업만인 경우
#   Remove  : 파일을 삭제하는 작업만 수행한 경우    
# ------------------
#     제목 첫 글자를 대문자로
#     제목은 명령문으로
#     제목 끝에 마침표(.) 금지
#     제목과 본문을 한 줄 띄워 분리하기
#     본문은 "어떻게" 보다 "무엇을", "왜"를 설명한다.
#     본문에 여러 줄의 메시지를 작성할 땐 "-" 혹은 "번호"로 구분
# ------------------
```
- git branch
```
main-feature의 flow로 진행합니다.

feature 브랜치 네이밍: feature/#{이슈번호}
```
- Code convention
```
- Class
    - Pascal case
- Model
    - snake case
- Function
    - snake case
- Variables
    - snake case
```

<br>

## 🖇 Lint, Formatter
<img width="723" alt="스크린샷 2022-07-26 오후 9 42 37" src="https://user-images.githubusercontent.com/76423946/181008499-a05933c7-c471-43a3-be6d-915a584724ad.png">

- isort, black, flake8을 이용하여 린트와 포메터를 설정했습니다.
- pre-commit 라이브러리를 이용하여 commit 전에 위 세 가지 라이브러리들을 실행시켜 코드를 일관화 합니다.

<br>

## 📌 태스크 관리
<img width="1123" alt="스크린샷 2022-07-26 오후 9 29 03" src="https://user-images.githubusercontent.com/76423946/181005905-b6a60938-743c-4dae-af71-412acfdfc84b.png">

- 태스크를 깃허브의 issue로 생성하고 칸반보드로 관리하였습니다.
       
