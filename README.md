### django command 에서 async로 httpx 요청 하는 데모 코드

### python env

```angular2html
python 3.12.2
```

### packages

```angular2html
requirementx.txt
```

### command crawling

```angular2html
python manage.py crawling
```

### crawling command path
```
django-httpx/
    manage.py
    core/
        management/
            commands/
                crawling.py
```


### 코드 설명

1. `python manage.py crawling` 실행 시 코드경로
    - `core/management/commands/crawling.py` 내 커멘드 클래스의 `crawling` 함수 실행
2. 프로젝트 내 루트 경로의 `url_list.txt` 파일에 들어있는 URL 수집
3. 이후 일괄 비동기 처리
