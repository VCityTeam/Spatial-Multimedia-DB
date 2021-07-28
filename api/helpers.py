#!/usr/bin/env python3
# coding: utf8
from entities.User import User
from util.Exception import *
from util.log import *
from util.VarConfig import *

from flask import jsonify, request
import sqlalchemy.exc
import sqlalchemy.orm
import jwt
import re

from persistence_unit import PersistenceUnit as pUnit

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
        raise NotImplementedError("Cannot send an abstract Response. Please "
                                  "send a subclass instead.")


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
        super().__init__('')

    def format(self):
        return '', 204


def format_response(old_function, authorization_function=None,
                    authorization=None, resource_id=None):
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
            return f'Bad request  \n{e}', 400
        except Unauthorized as e:
            return f'Unauthorized  \n{e}', 401
        except AuthError as e:
            return f'Forbidden  \n{e}', 403
        except (sqlalchemy.exc.IntegrityError, sqlalchemy.exc.DataError, UnprocessableEntity) as e:
            return f'Unprocessable entity  \n{e}', 422
        except (NotFound, sqlalchemy.orm.exc.NoResultFound) as e:
            return f'Not found\n{e}', 404
        except FormatError as e:
            return f'Unsupported file format  \n{e}', 415
        except Conflict as e:
            return f'Conflict  \n{e}'
        except Exception as e:
            info_logger.error(e)
            return f"Unexpected error  \n{e}", 500

    return new_function


def use_authentication(required=True):
    """
    Decorator used to specify that a route needs authentication. To put after
    the `app.route` decorator from Flask. Will search in the request headers
    for an 'Authorization' field and decode it as JWT. If the field cannot be
    found, or the timeout is expired, or the field is not a valid JWT, returns
    a LoginError.
    :param required: Specify if the auth is required or not. If set to True,
    the decorator will raise an Unauthorized exception if no auth is provided.
    If set to false, it will pass None as auth_info.
    """
    def decorator(old_function):
        @wraps(old_function)
        def new_function(*args, **kwargs):
            try:
                # Can raise a KeyError if header is not found
                try:
                    bearer = request.headers["Authorization"]
                    encoded_jwt = re.search('Bearer (.*)', bearer).group(1)
                    decoded_jwt = jwt.decode(encoded_jwt, VarConfig.get()['SPATIAL_MULTIMEDIA_DB_ADMIN_PASSWORD'],
                                             algorithms=['HS256'])
                    if decoded_jwt is None:
                        raise Unauthorized

                    session = pUnit.Session()
                    user = session.query(User).filter(User.id == decoded_jwt['user_id']).one()
                    session.close()
                    if user is None:
                        raise UnprocessableEntity("User does not exist")
                except KeyError:
                    if required:
                        raise Unauthorized("Missing 'Authorization' header")
                    else:
                        decoded_jwt = None

                kwargs['auth_info'] = decoded_jwt
                return old_function(*args, **kwargs)
            except jwt.PyJWTError as e:
                raise Unauthorized(e)
            except AttributeError:
                raise Unauthorized("Missing 'Authorization' header")
            except Exception as e:
                raise e

        return new_function
    return decorator
