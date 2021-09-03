#!/usr/bin/env python3
# Copyright (C) 2019-2020 All rights reserved.
# FILENAME:  load_config.py
# VERSION: 	 0.1.9
# CREATED: 	 2020-11-26 16:14
# AUTHOR: 	 Aekasitt Guruvanich <aekazitt@gmail.com>
# DESCRIPTION:
#
# HISTORY:
#*************************************************************
### Standard Packages ###
from typing import Any
### Third-Party Packages ###
import pytest
from fastapi.testclient import TestClient
from pydantic import ValidationError
### Local Modules ###
from . import *
from fastapi_csrf_protect import CsrfProtect

def test_missing_secret_key(setup, route: str='/protected'):
  client: TestClient = setup
  error_called: bool = False
  try:
    @CsrfProtect.load_config
    def load_secret_key():
      return [('secret_key', None)]
    client.get(route)
  except Exception as err:
    error_called = True
    assert isinstance(err, RuntimeError)
    assert err.args[0] == 'A secret key is required to use CSRF.'
  assert error_called == True

@pytest.mark.parametrize('config_key, config_value, valid', [
  ('secret_key', 2, False), \
    ('secret_key', 1.0, False), \
      ('secret_key', True, False), \
        ('secret_key', b'secret', False), \
          ('secret_key', 'secret', True), \
            ('secret_key', [], False), \
              ('secret_key', {}, False), \
  ('csrf_header_name', 2, False), \
    ('csrf_header_name', 1.0, False), \
      ('csrf_header_name', True, False), \
        ('csrf_header_name', b'header_name', False) ,\
          ('csrf_header_name', 'header_name', True), \
            ('csrf_header_name', [], False), \
              ('csrf_header_name', {}, False), \
  ('csrf_header_type', 2, False), \
    ('csrf_header_type', 1.0, False), \
      ('csrf_header_type', True, False), \
        ('csrf_header_type', b'header_type', False) ,\
          ('csrf_header_type', 'header_type', True), \
            ('csrf_header_type', [], False), \
              ('csrf_header_type', {}, False), \
  ('csrf_in_cookies', 2, False), \
    ('csrf_in_cookies', 1.0, False), \
      ('csrf_in_cookies', True, True), \
        ('csrf_in_cookies', b'in_cookies', False) ,\
          ('csrf_in_cookies', 'in_cookies', False), \
            ('csrf_in_cookies', [], False), \
              ('csrf_in_cookies', {}, False), \
  ('csrf_methods', 2, False), \
    ('csrf_methods', 1.0, False), \
      ('csrf_methods', True, False), \
        ('csrf_methods', b'GET, POST', False) ,\
          ('csrf_methods', 'GET, POST', False), \
            ('csrf_methods', [], True), \
              ('csrf_methods', {}, False), \
                ('csrf_methods', [1, 2, 3], False), \
                  ('csrf_methods', (1, 2, 3), False), \
                    ('csrf_methods', {1, 2, 3}, False), \
                      ('csrf_methods', ['1', '2', '3'], False), \
                        ('csrf_methods', ('1', '2', '3'), False), \
                          ('csrf_methods', {'1', '2', '3'}, False), \
                            ('csrf_methods', ['GET', 'POST', 'DELETE'], True), \
                              ('csrf_methods', ('GET', 'POST', 'DELETE'), True), \
                                ('csrf_methods', {'GET', 'POST', 'DELETE'}, True), \
                                  ('csrf_methods', {'key': 'value'}, False), \
        ])
def test_load_config(config_key:str, config_value: Any, valid: bool):
  error_raised: bool = False
  try:
    @CsrfProtect.load_config
    def load_csrf_configs():
      return [(config_key, config_value)]
  except Exception as err:
    error_raised = True
    assert isinstance(err, ValidationError)
  assert error_raised is (True, False)[valid]
