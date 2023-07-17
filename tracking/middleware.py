from .models import Tracker, Visit


class TrackerMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        user_agent = request.META.get('HTTP_USER_AGENT')
        trackID = request.META.get('HTTP_X_COMERCIFY_VISITOR')
        ip_address = request.META.get('HTTP_X_FORWARDED_FOR', '') or request.META.get(
            'HTTP_CLIENT_IP', '') or request.META.get('REMOTE_ADDR', '')
        logged_in = False
        if request.META.get('HTTP_AUTHORIZATION'):
            logged_in = True
        client_url = request.META.get('HTTP_ORIGIN')
        api_path = request.META.get('PATH_INFO')

        if trackID:
            Visit.objects.create(
                tracker_id=trackID,
                client_url=client_url,
                client_path="blob",
                api_path=api_path,
                browser=user_agent,
                ip_address=ip_address,
                logged_in=logged_in,
            )

        response = self.get_response(request)

        return response


"""
{'PATH': '/usr/local/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin', 'HOSTNAME': '28759cf1149e', 'POSTGRES_DB': 'postgres', 'POSTGRES_USER': 'root', 'POSTGRES_PASSWORD': 'root', 'SECRET_KEY': 'django-insecure-jfalh_%+a9ub@h*vrc*ws^et6*8-7*e56yzqj8g(pno-(iu^47', 'ENV': 'DEV', 'LANG': 'C.UTF-8', 'GPG_KEY': 'A035C8C19219BA821ECEA86B64E628F8D684696D', 'PYTHON_VERSION': '3.11.3', 'PYTHON_PIP_VERSION': '22.3.1', 'PYTHON_SETUPTOOLS_VERSION': '65.5.1', 'PYTHON_GET_PIP_URL': 'https://github.com/pypa/get-pip/raw/0d8570dc44796f4369b652222cf176b3db6ac70e/public/get-pip.py', 'PYTHON_GET_PIP_SHA256': '96461deced5c2a487ddc65207ec5a9cffeca0d34e7af7ea1afc470ff0d746207', 'PYTHONDONTWRITEBYTECODE': '1', 'PYTHONUNBUFFERED': '1', 'DJANGO_MANAGEPY_COLLECTSTATIC_NO_INPUT': '1', 'HOME': '/root', 'DOMAIN': '*', 'ADMIN_REACT_SITE': 'http://localhost:3000', 'STORE_NEXT_SITE': 'http://localhost:3005', 'DB_USER': 'postgres', 'DB_HOST': 'containers-us-west-90.railway.app', 'DB_PASSWORD': '1A6OZ867dYGB3VvDfkfG', 'DB_NAME': 'railway', 'DB_PORT': '7511', 'EMAIL_USERNAME': 'salahsaadaoui8@gmail.com', 'EMAIL_PASSWORD': 'wsizziubbceovhjj', 'EMAIL_SERVER': 'smtp.gmail.com', 'EMAIL_PORT': '2525', 'GOOGLE_CLIENT_ID': '626908472574-pkrn39o1ded5r8gi2guckphcnpimn4f1.apps.googleusercontent.com', 'GOOGLE_SECRET_KEY': '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', 'ENCRYPTION_KEY': 'PrWha5A9SwvsRxNgrkM8vOY0vB3px0Aik23yeBtPO8Q', 'DJANGO_SETTINGS_MODULE': 'core.settings', 'TZ': 'UTC', 'RUN_MAIN': 'true', 'SERVER_NAME': '28759cf1149e', 'GATEWAY_INTERFACE': 'CGI/1.1', 'SERVER_PORT': '8000', 'REMOTE_HOST': '', 'CONTENT_LENGTH': '', 'SCRIPT_NAME': '', 'SERVER_PROTOCOL': 'HTTP/1.1', 'SERVER_SOFTWARE': 'WSGIServer/0.2', 'REQUEST_METHOD': 'GET', 'PATH_INFO': '/vendor/orders/', 'QUERY_STRING': '', 'REMOTE_ADDR': '172.24.0.1', 'CONTENT_TYPE': 'application/json', 'HTTP_HOST': '127.0.0.1:8000', 'HTTP_USER_AGENT': 'Mozilla/5.0 (X11; Linux x86_64; rv:91.0) Gecko/20100101 Firefox/91.0', 'HTTP_ACCEPT': '*/*', 'HTTP_ACCEPT_LANGUAGE': 'en-US,en;q=0.5', 'HTTP_ACCEPT_ENCODING': 'gzip, deflate', 'HTTP_REFERER': 'http://localhost:3005/', 'HTTP_AUTHORIZATION': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjg5NjI1ODY0LCJpYXQiOjE2ODk2MTc5NzksImp0aSI6ImIwOTA3M2Q0MmM1OTRmMmZiOWEwMDllZDJkODk2YzU2IiwidXNlcl9pZCI6MzQwfQ.zdTL8RDN2-xoAVUqheItMsvaUHZ3es0dulmZyaqakcE', 'HTTP_X_COMERCIFY_VISITOR': '79800468-af97-4496-a238-8dc751279a9b', 'HTTP_ORIGIN': 'http://localhost:3005', 'HTTP_CONNECTION': 'keep-alive', 'HTTP_SEC_FETCH_DEST': 'empty', 'HTTP_SEC_FETCH_MODE': 'cors', 'HTTP_SEC_FETCH_SITE': 'cross-site', 'wsgi.input': <django.core.handlers.wsgi.LimitedStream object at 0x7f6bd518d390>, 'wsgi.errors': <_io.TextIOWrapper name='<stderr>' mode='w' encoding='utf-8'>, 'wsgi.version': (1, 0), 'wsgi.run_once': False, 'wsgi.url_scheme': 'http', 'wsgi.multithread': True, 'wsgi.multiprocess': False, 'wsgi.file_wrapper': <class 'wsgiref.util.FileWrapper'>}
"""
