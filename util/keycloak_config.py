#!/usr/bin/env python3
# coding: utf8

from keycloak import KeycloakOpenID
from util.VarConfig import VarConfig


def get_keycloak_openid():
    # Create KeycloakOpenID instance
    if not hasattr(get_keycloak_openid, "openid"):
        config = VarConfig.get()
        get_keycloak_openid.openid = KeycloakOpenID(
            server_url=config["KC_SERVER_URL"],
            client_id=config["KC_CLIENT_ID"],
            realm_name=config["KC_REALM"],
            client_secret=config["KC_CLIENT_SECRET"],
        )

    return get_keycloak_openid.openid
