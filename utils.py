def set_cookies(refresh, response):
    response.set_cookie(
                'admin_cify_access',
                str(refresh.access_token),
                max_age=refresh.payload['exp'],
                httponly=True,
                secure=True,
                samesite='None'
            )
    response.set_cookie(
        'admin_cify_refresh',
        str(refresh),
        max_age=refresh.payload['exp'],
        httponly=True,
        secure=True,
        samesite='None'
    )
    response.set_cookie(
        'admin_cify_exp',
        refresh.payload['exp'],
        max_age=refresh.payload['exp'],
        httponly=True,
        secure=True,
        samesite='None'
    )
    return response