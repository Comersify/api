def set_cookies(refresh, response, user_type):
    response.set_cookie(
                f'{user_type.lower()}_cify_access',
                str(refresh.access_token),
                max_age=refresh.payload['exp'],
                httponly=True,
                secure=True,
                samesite='None'
            )
    response.set_cookie(
        f'{user_type.lower()}_cify_refresh',
        str(refresh),
        max_age=refresh.payload['exp'],
        httponly=True,
        secure=True,
        samesite='None'
    )
    response.set_cookie(
        f'{user_type.lower()}_cify_exp',
        refresh.payload['exp'],
        max_age=refresh.payload['exp'],
        httponly=True,
        secure=True,
        samesite='None'
    )
    return response