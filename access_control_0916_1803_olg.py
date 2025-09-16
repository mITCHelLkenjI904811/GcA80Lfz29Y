# 代码生成时间: 2025-09-16 18:03:45
# access_control.py

"""
A Pyramid application that demonstrates access control.
"""

from pyramid.config import Configurator
from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.interfaces import IAuthenticationPolicy, IAuthorizationPolicy
from pyramid.renderers import JSON
from pyramid.response import Response
from pyramid.security import Allow, Authenticated, Everyone, ALL_PERMISSIONS, Deny
from pyramid.settings import aslist, asbool
from pyramid.threadlocal import get_current_registry

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .models import DBSession, Base

def main(global_config, **settings):
    """
    This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings)

    # Configure the authentication policy
    authn_policy = AuthTktAuthenticationPolicy('secret', callback=groupfinder)
    config.set_authentication_policy(authn_policy)

    # Configure the authorization policy
    authz_policy = ACLAuthorizationPolicy()
    config.set_authorization_policy(authz_policy)

    # Add a route to handle a protected endpoint
    config.add_route('protected_view', '/protected')

    # Add a view to handle the protected endpoint
    def protected_view(request):
        # Check if the user is authenticated
        if not request.authenticated_userid:
            return Response('You are not authenticated', status=401)

        # Check if the user has the necessary permission
        if not request.has_permission('view'):
            return Response('You do not have permission to view this', status=403)

        # If the user is authenticated and has the necessary permission,
        # return a success message
        return Response('Welcome to the protected area!')

    # Scan for models and setup the database
    engine = create_engine('sqlite:///access_control.db')
    Base.metadata.create_all(engine)
    DBSession.configure(bind=engine)

    # Add the view to the configuration
    config.add_view(protected_view, route_name='protected_view', renderer=JSON)

    # Scan for other views and register them
    config.scan()

    return config.make_wsgi_app()

# This function is called by the authentication policy callback
def groupfinder(userid, request):
    """
    This function is used to find the group memberships of a user.
    """
    # In a real application, you would query the database to find the user's groups
    # For demonstration purposes, we'll just return a hardcoded list
    return [Everyone, Authenticated]
