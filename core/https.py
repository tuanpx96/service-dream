from django.http import HttpResponseRedirect

SIXCENTS_PROTOCOL = 'ml'


class HttpSixcentResponseRedirect(HttpResponseRedirect):
    allowed_schemes = [SIXCENTS_PROTOCOL]
