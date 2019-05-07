import logging
import os
import traceback

from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.shortcuts import HttpResponse, render
from oauth2client.client import FlowExchangeError
from oauth2client.client import flow_from_clientsecrets

LOGIN_REDIRECT_URL = '/'
CLIENT_SECRETS = os.path.join(os.path.dirname(__file__), '..', 'client_secret.json')
xsrfutil = object()

logger = logging.getLogger("main")


def make_flow_from_request(request):
    if request.is_secure():
        protocol = 'https'
    else:
        protocol = 'http'
    next_url = request.session.get('next_url')
    if next_url is None:
        request.session['next_url'] = request.GET.get('next', LOGIN_REDIRECT_URL)
    oauth2_callback_url = '%s://%s/oauth2callback' % (protocol, request.get_host())
    logger.info(oauth2_callback_url)
    return flow_from_clientsecrets(
        CLIENT_SECRETS,
        scope='email',
        redirect_uri=oauth2_callback_url
    )


def oauth_login_view(request):
    flow = make_flow_from_request(request)
    flow.params['state'] = xsrfutil.generate_token(settings.SECRET_KEY, request.user)
    authorize_url = flow.step1_get_authorize_url()
    return HttpResponseRedirect(authorize_url)


def oauth_callback_view(request):
    flow = make_flow_from_request(request)
    try:
        credentials = flow.step2_exchange(request.REQUEST)
    except FlowExchangeError as e:
        logger.info(request.REQUEST, str(e))
        return HttpResponse(u'FlowExchangeError: %s' % (str(e),))

    email = credentials.id_token['email']
    next_url = request.session.get('next_url', LOGIN_REDIRECT_URL)
    try:
        user = authenticate(username=email, password='1')
        login(request, user)
    except Exception as e:
        logger.info('%s %s %s', email, str(e), traceback.format_exc())
        return HttpResponse('Failed to login: %s' % (str(e),))
    if not user.is_active:
        return HttpResponse('Failed to login: user has been suspended.')
    return HttpResponseRedirect(next_url)


def logout_view(request):
    if request.user:
        logout(request)
    return render(request, 'python_test/logged_out.html')
