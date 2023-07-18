#!/usr/bin/env python3
# coding: utf8

import os
import sys


class VarConfig:
    # KC prefix stands for KeyCloak
    _mandatory_keys = [
        "KC_REALM",
        "KC_SERVER_URL",
        "KC_CLIENT_ID",
        "KC_CLIENT_SECRET",
    ]

    @staticmethod
    def get():
        config = {}
        with open(".env", "r") as file:
            for line in file.readlines():
                # Allow empty line or comment line (starting with '#')
                if "=" in line and line[0] != "#":
                    var, value = line.replace("\n", "").split("=")
                    config[var] = value

        # Overwrite with environment values when available
        for var in config:
            if os.environ.get(var):
                config[var] = os.environ.get(var)

        # Assert mandatory configuration values are present
        for key in VarConfig._mandatory_keys:
            if key not in config:
                print("Mandatory configuration value ", key, " is missing.")
                print("Exiting")
                sys.exit(1)

        return config


if __name__ == "__main__":
    print(VarConfig.get())
