## Git Repository 소개

안녕하세요.

보안상 기업명을 말씀드릴 순 없고, 기업과제전형을 위해 만들어진 Repository입니다.

제일 아래 Reference에도 적혀져 있지만, 기업과제전형을 위한 Repository기 때문에 이 코드를 이용한 이득 및 무단배포는 법적책임을 물을 수 있습니다.

읽어주셔서 감사합니다.


<br>

## Contents

1. Skill & Tools
2. ERD Diagram
3. EndPoint
4. Postman API Documentaion
5.  Unit Test 결과
6. Commit Message GuideLines
7. Reference

<br>

## Skill & Tools
* BackEnd : Python, django, django-environ
* DataBase : sqlite3
* ETC Tool : Git, GitHub, Postman

<br>

## ERD Diagram

![기업과제1 (1)](https://user-images.githubusercontent.com/88086271/146576137-57f0c197-f188-4e32-9128-b58e3f337424.png)


<br>

## EndPoint

1. 영화 리스트 조회

GET /movies

2. 영화 디테일 조회

GET /movies/{int:movie_id}

3. 영화 추가

POST /movies

4. 리뷰 디테일 조회

GET /movies/{int:movie_id}/reviews/{int:review_id}

5. 리뷰 추가

POST /movies/{int:movie_id}

6. 리뷰 수정

PUT /movies/{int:movie_id}/reviews/{int:review_id}

7. 리뷰 삭제

DELETE /movies/{int:movie_id}/reviews/{int:review_id}

8. 리뷰 추천

POST /movies/{int:movie_id}/reviews/{int:review_id}

9. 리뷰추천 삭제

DELETE /movies/{int:movie_id}/reviews/{int:review_id}/votes/{int:review_vote_id}


<br>

## Postman API Documentation

![Postman API Documentation 명세서](https://documenter.getpostman.com/view/17716434/UVRAH6TB)


<br>


## Unit Test 결과

![image](https://user-images.githubusercontent.com/88086271/146575560-cb39e2e9-ec0b-46bd-9133-f1060c38b850.png)


<br>

## Commit Message GuideLines

1. 분류는 Add / Remove / Modify / Fix / Refactor / Docs로 나뉜다.
2. ADD : 기능 추가할 시 기입
3. Remove : 폴더/파일 삭제할 시 기입
4. Modify : 수정 (JSON 데이터 포맷 등 코드가 아닌 사항을 변경할 시 기입)
5. Fix : 버그/오류 해결할 시 기입
6. Refactor : 코드 리팩토링 (ORM구문 변경, 불필요 코드 제거, 성능 개선 등 코드 관련된 내용 수정할 시 기입)
7. Docs : 문서에 관련된 수정작업(README 등)

<br>

## Reference
* 이 프로젝트는 기업과제전형을 목적으로 만들었습니다.
* 이 코드를 활용하여 이득을 취하거나 무단 배포할 경우, 법적으로 문제가 있을 수 있습니다.
