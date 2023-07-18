#!/usr/bin/env python3
# coding: utf8
from util.Exception import *
from util.log import *
from util.VarConfig import *
from util.keycloak_config import get_keycloak_openid

from flask import jsonify, request, redirect
import sqlalchemy.exc
import sqlalchemy.orm
from functools import wraps


class Response:
    """
    Represents a response that can be handled y Flask. It contains a 'content',
    which should be a string, a dict or a list. If it is a dict or a list,
    the content will be formatted into a JSON format thanks to the 'jsonify'
    method from flask.
    """

    def __init__(self, content):
        if isinstance(content, (dict, list)):
            self.content = jsonify(content)
        else:
            self.content = content

    def format(self):
        """
        Format the response for Flask. Should not be called from the
        superclass. Should be overridden by subclasses to return the content
        and an error code.
        """
        raise NotImplementedError(
            "Cannot send an abstract Response. Please "
            "send a subclass instead."
        )


class ResponseOK(Response):
    """
    Represents a HTTP 200 OK response. See the `Response` superclass for more
    information.
    """

    def format(self):
        return self.content, 200


class ResponseCreated(Response):
    """
    Represents a HTTP 201 CREATED response. See the `Response` superclass for
    more information.
    """

    def format(self):
        return self.content, 201


class ResponseNoContent(Response):
    """
    Represents a HTTP 204 NO CONTENT response. As no content should be provided
    with this kind of response, the constructor does not take any argument.
    """

    def __init__(self):
        super().__init__("")

    def format(self):
        return "", 204


def format_response(
    old_function,
    authorization_function=None,
    authorization=None,
    resource_id=None,
):
    """
    Decorator used to format the response of `old_function` into a Flask
    response tuple. `old_function` should either return a `Response` object
    or raise an exception.
    :param old_function: The old function.
    :param authorization_function:
    :param authorization:
    :param resource_id:
    :return: A new function which returns a Flask response.
    """

    @wraps(old_function)
    def new_function(*args, **kwargs):
        try:
            if authorization_function:
                authorization_function(authorization, resource_id)
            response = old_function(*args, **kwargs)
            if isinstance(response, Response):
                return response.format()
            else:
                return response
        except BadRequest as e:
            return f"Bad request  \n{e}", 400
        except Unauthorized as e:
            return f"Unauthorized  \n{e}", 401
        except AuthError as e:
            return f"Forbidden  \n{e}", 403
        except (
            sqlalchemy.exc.IntegrityError,
            sqlalchemy.exc.DataError,
            UnprocessableEntity,
        ) as e:
            return f"Unprocessable entity  \n{e}", 422
        except (NotFound, sqlalchemy.orm.exc.NoResultFound) as e:
            return f"Not found\n{e}", 404
        except FormatError as e:
            return f"Unsupported file format  \n{e}", 415
        except Conflict as e:
            return f"Conflict  \n{e}"
        except Exception as e:
            info_logger.error(e)
            return f"Unexpected error  \n{e}", 500

    return new_function


def use_authentication(realm, server_url, client_id, client_secret):
    """
    Decorator used to specify that a route needs Keycloak authentication. This
    decorator should be placed after the `app.route` decorator of Flask.
    In case authentication fails (invalid or expired token), this decorator
    redirects to Keycloak login page.
    :param realm:
    :param server_url:
    :param client_id:
    :param client_secret
    """

    def decorator_protect(func):
        @wraps(func)
        def protected_view(*args, **kwargs):
            keycloak_openid = get_keycloak_openid()

            # Get the access token from the request headers
            access_token = request.headers.get("Authorization", "").split(
                "Bearer "
            )[-1]

            # Validate the access token
            token_info = keycloak_openid.introspect(access_token)

            if not token_info["active"]:
                # Redirect to the Keycloak login page if the token is invalid or expired
                return redirect(keycloak_openid.authorization_url())

            # Token is valid, proceed with the protected view
            return func(*args, **kwargs)

        return protected_view

    return decorator_protect
