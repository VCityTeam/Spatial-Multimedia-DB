#!/usr/bin/env python3
# coding: utf8

from time import time

from util.Exception import Unauthorized
from util.encryption import *
from util.log import info_logger
from entities.User import User
from entities.UserRole import UserRole
import persistence_unit.PersistenceUnit as pUnit


class UserController:
    """
    Class that allows communication with the DB
    No instance is needed because all its methods are static.
    This methods are used to make a CRUD operation,
    by making a query or a transaction with the DB by using
    the decorators '~persistence_unit.PersistenceUnit.make_a_query'
    and make_a_transaction
    """

    @staticmethod
    @pUnit.make_a_transaction
    def create_user(session, *args):
        attributes = args[0]
        user = User()
        user.set_role(session.query(UserRole).filter(
            UserRole.label == UserRole.get_clearance(0)).one())
        user.update(attributes)
        session.add(user)
        return user

    @staticmethod
    @pUnit.make_a_transaction
    def create_privileged_user(session, *args):
        attributes = args[0]
        payload = args[1]
        if User.is_admin(attributes):
            user = User()
            user.set_role(session.query(UserRole).filter(UserRole.label == attributes["role"]).one())
            user.update(attributes)
            session.add(user)
            return user
        else:
            raise AuthError

    @staticmethod
    @pUnit.make_a_transaction
    def create_admin_user(session, *args):
        attributes = args[0]
        user = User()
        user.update(attributes)
        user.set_role(session.query(UserRole).filter(UserRole.label == attributes["role"]).one())
        session.add(user)
        return user

    @staticmethod
    @pUnit.make_a_query
    def get_user_by_id(session, *args):
        attributes = args[0]
        user_id = attributes
        user = session.query(User).filter(User.id == user_id).one()
        return user

    @staticmethod
    @pUnit.make_a_transaction
    def login(session, *args):
        try:
            attributes = args[0]
            username = attributes['username']
            password = attributes['password']
            user = session.query(User).filter(
                User.username == username).one()
            if is_password_valid(user.password, password):
                exp = time() + 24 * 3600
                payload = {
                    'user_id': user.id,
                    'username': user.username,
                    'firstName': user.firstName,
                    'lastName': user.lastName,
                    'email': user.email,
                    'role': user.role.serialize(),
                    'exp': exp
                }
                return {
                    "token": jwt.encode(
                        payload, VarConfig.get()['SPATIAL_MULTIMEDIA_DB_PASSWORD'],
                        algorithm='HS256').decode('utf-8')
                }
            else:
                raise Unauthorized
        except Exception as e:
            info_logger.error(e)
            raise Unauthorized('Wrong credentials')

    @staticmethod
    @pUnit.make_a_transaction
    def create_admin(session):
        print('try to create admin')
        admin_exist = False
        for user in session.query(User).all():
            if user.username == VarConfig.get()['SPATIAL_MULTIMEDIA_DB_ADMIN_USERNAME'] or user.email == VarConfig.get()['SPATIAL_MULTIMEDIA_DB_ADMIN_EMAIL']:
                admin_exist = True
                print("An admin with the requested username or email already exists in database. New admin won't be added.")
        if not admin_exist:
            attributes = {
                "email": VarConfig.get()['SPATIAL_MULTIMEDIA_DB_ADMIN_EMAIL'],
                "firstName": VarConfig.get()['SPATIAL_MULTIMEDIA_DB_ADMIN_FIRST_NAME'],
                "lastName": VarConfig.get()['SPATIAL_MULTIMEDIA_DB_ADMIN_LAST_NAME'],
                "password": VarConfig.get()['SPATIAL_MULTIMEDIA_DB_ADMIN_PASSWORD'],
                "role": "admin",
                "username": VarConfig.get()['SPATIAL_MULTIMEDIA_DB_ADMIN_USERNAME'],
                "user_position": "admin"
            }
            UserController.create_admin_user(attributes)
