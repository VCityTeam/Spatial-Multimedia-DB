#!/usr/bin/env python3
# coding: utf8

import os


class VarConfig:
    @staticmethod
    def get():
        config = {}
        with open(".env", 'r') as file:
            for line in file.readlines():
                # Allow empty line or comment line (starting with '#')
                if '=' in line and line[0] != '#':
                    var, value = line.replace('\n', '').split('=')
                    config[var] = value

            for var in config:
                print(var)
                if os.environ.get(var):
                    config[var] = os.environ.get(var)
    
            return config


if __name__ == '__main__':
    print(VarConfig.get())
