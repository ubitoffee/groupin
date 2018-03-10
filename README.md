# GroupIn

---

## 개발환경

 - Python : <a href="https://www.python.org/downloads/windows/" target="_blank">3.6.1</a> 버전 설치
 - IDE : <a href="https://www.jetbrains.com/pycharm/" target="_blank">Pycharm</a>
 - Build Tools : <a href="https://nodejs.org/ko/" target="_blank">Node.js</a>
    - bower와 grunt를 이용하기위해 설치
    
    ```commandline
       npm install -g bower
       npm install -g grunt
       
       bower install
    ```

 - DB : ~~<a href="http://www.enterprisedb.com/products-services-training/pgdownload#windows">PostgreSQL</a>~~ Azure MSSQL로 이전
    
    - ~~환경변수 설정~~
        ```
           setx PATH "%PATH%;C:\Program Files\PostgreSQL\{설치한 버전}\bin"
        ```
        
    - ~~psycopg2 설치~~
        ```
          pip install psycopg2
        ```
        
    - ~~command line 사용~~
        ```
           command line 로그인 시 psql -U postgres -W 명령 입력 후 비밀번호 입력 
        ```
    
    - ~~DB 및 유저 생성 쿼리~~
        ```sql
          CREATE USER {사용자};
          CREATE DATABASE groupin OWNER {사용자};
          
          ALTER ROLE {사용자} SET client_encoding to 'utf-8';
          ALTER ROLE {사용자} SET timezone to 'Asia/Seoul';
    
          GRANT ALL PRIVILEGES ON DATABASE groupin to ubitoffee;
        ```
        
    - ~~Django settings.py 설정~~
        ```python
      DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'groupin',
            'USER': 'ubitoffee',
            'PASSWORD': 'ubitoffee',
            'HOST': 'localhost',
            'PORT': '',
        }
      }
        ```

    - pyodbc 설치
        ```
          pip install django-pyodbc-azure
        ```

    - Django settings.py 설정
        ```python
            DATABASES = {
                'default': {
                    'ENGINE': 'sql_server.pyodbc',
                    'NAME': 'groupin',
                    'USER': 'ubitoffee',
                    'PASSWORD': '#####',
                    'HOST': 'groupin-server.database.windows.net',
                    'PORT': '',
                }
            }
        ```

    - MS SSMS 설치
    - python manage.py migrate

 - gettext 설치
    - Windiws
        ```
            https://mlocati.github.io/articles/gettext-iconv-windows.html
        ```
    - Linux
        ```

        ```

---