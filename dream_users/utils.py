from datetime import timedelta
import requests
from django.conf import settings
from django.utils import timezone

from dream_users.models import LoginHistory, User


# def get_user_type(user_id: int) -> int:
#     # TODO: Should implement scheduled task to update user_type
#     has_course = CourseBuy.objects.filter(
#         user_id=user_id,
#         created_at__date__gte=timezone.now().today() - timedelta(days=settings.EXPIRED_COURSE_TIME)
#     ).exists()
#     if has_course:
#         return User.TYPE_PREMIUM
#     else:
#         return User.TYPE_FREE


def get_expired_time(token):
    return token.created + timedelta(seconds=settings.EXPIRED_TOKEN_TIME)


def get_line_profile(line_access_token):
    ACCESS_TOKEN = 'Bearer ' + '{' + line_access_token + '}'
    headers = {'Authorization': ACCESS_TOKEN}
    response = requests.get(url=settings.URL_GET_PROFILE_LINE, headers=headers).json()
    return response


def check_expired_time_reset_token(reset_token):
    utc_now = timezone.now()
    expired_time = reset_token.created_at + timedelta(seconds=settings.EXPIRED_TOKEN_RESET_TIME)

    if utc_now > expired_time:
        return False
    return True


def check_expired_time_confirm_email_token(token):
    utc_now = timezone.now()
    expired_time = token.created_at + timedelta(seconds=settings.EXPIRED_TOKEN_CONFIRM_EMAIL_TIME)

    if utc_now > expired_time:
        return False
    return True


def get_facebook_profile(fb_access_token):
    reponse = requests.get(settings.URL_GET_ID_FACEBOOK + fb_access_token).json()
    data = {
        'id': reponse['id'],
        'name': reponse['name']
    }
    return data


def create_or_update_login_history(user_id):
    current_day = timezone.now()
    if LoginHistory.objects.filter(user_id=user_id).exists():
        user_login_day = LoginHistory.objects.filter(
            user_id=user_id
        ).order_by('-end_date').first()
        diff_date = current_day.date() - user_login_day.end_date
        if diff_date.days == 1:
            user_login_day.end_date = current_day.date()
            user_login_day.num_date = user_login_day.num_date + 1
            user_login_day.save()
        elif diff_date.days != 0:
            LoginHistory.objects.create(user_id=user_id)
    else:
        LoginHistory.objects.create(user_id=user_id)
