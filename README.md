# FastAPI CSRF Protect

[![Build Status](https://travis-ci.com/aekasitt/fastapi-csrf-protect.svg?branch=master)](https://app.travis-ci.com/github/aekasitt/fastapi-csrf-protect)
[![Package Vesion](https://img.shields.io/pypi/v/fastapi-csrf-protect)](https://pypi.org/project/fastapi-csrf-protect)
[![Format](https://img.shields.io/pypi/format/fastapi-csrf-protect)](https://pypi.org/project/fastapi-csrf-protect)
[![Python Version](https://img.shields.io/pypi/pyversions/fastapi-csrf-protect)](https://pypi.org/project/fastapi-csrf-protect)
[![License](https://img.shields.io/pypi/l/fastapi-csrf-protect)](https://pypi.org/project/fastapi-csrf-protect)

## Features

FastAPI extension that provides stateless Cross-Site Request Forgery (XSRF) Protection support.
Aimed to be easy to use and lightweight, we adopt [Double Submit Cookie](https://cheatsheetseries.owasp.org/cheatsheets/Cross-Site_Request_Forgery_Prevention_Cheat_Sheet.html#double-submit-cookie) mitigation pattern.
If you were familiar with `flask-wtf` library this extension suitable for you.
This extension inspired by `fastapi-jwt-auth` 😀

- Storing `fastapi-csrf-token` in cookies or serve it in template's context

## 🚧 Breaking Changes (0.3.0 -> 0.3.1)

* The `generate_csrf` method has now been marked for deprecation
* The recommended method is now `generate_csrf_tokens` which returns a tuple of tokens, first unsigned
  and the latter signed
* Recommended pattern is for the first token is aimed for returning as part of context
* Recommended pattern is for the signed token to be set in client's cookie completing [Double Submit Cookie](https://cheatsheetseries.owasp.org/cheatsheets/Cross-Site_Request_Forgery_Prevention_Cheat_Sheet.html#double-submit-cookie)
* To prevent token reuse, protected endpoint can unset the signed CSRF Token in client's cookies as
  per example code and recommended pattern.

## Installation

The easiest way to start working with this extension with pip

```bash
pip install fastapi-csrf-protect
# or
poetry add fastapi-csrf-protect
```

## Getting Started

The following examples show you how to integrate this extension to a FastAPI App

### Example Login Form

```python
from fastapi import FastAPI, Request, Depends
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi_csrf_protect import CsrfProtect
from fastapi_csrf_protect.exceptions import CsrfProtectError
from pydantic import BaseModel

app = FastAPI()
templates = Jinja2Templates(directory="templates")

class CsrfSettings(BaseModel):
  secret_key: str = "asecrettoeverybody"
  cookie_samesite: str = "none"

@CsrfProtect.load_config
def get_csrf_config():
  return CsrfSettings()

@app.get("/login")
def form(request: Request, csrf_protect: CsrfProtect = Depends()):
  """
  Returns form template.
  """
  csrf_token, signed_token = csrf_protect.generate_csrf_tokens()
  response = templates.TemplateResponse(
    "form.html", {"request": request, "csrf_token": csrf_token}
  )
  csrf_protect.set_csrf_cookie(signed_token, response)
  return response

@app.post("/login", response_class=JSONResponse)
def create_post(request: Request, csrf_protect: CsrfProtect = Depends()):
  """
  Creates a new Post
  """
  csrf_protect.validate_csrf(request)
  response: JSONResponse = JSONResponse(status_code=200, content={"detail": "OK"})
  csrf_protect.unset_csrf_cookie(response)  # prevent token reuse
  return response

@app.exception_handler(CsrfProtectError)
def csrf_protect_exception_handler(request: Request, exc: CsrfProtectError):
  return JSONResponse(status_code=exc.status_code, content={"detail": exc.message})

```

## Contributions

To contribute to the project, fork the repository and clone to your local device and install preferred testing dependency [pytest](https://github.com/pytest-dev/pytest)
Alternatively, run the following command on your terminal to do so:

```bash
pip install -U poetry
poetry install
```

Testing can be done by the following command post-installation:

```bash
poetry install --with test
pytest
```

### Run Examples

To run the provided examples, first you must install extra dependencies [uvicorn](https://github.com/encode/uvicorn) and [jinja2](https://github.com/pallets/jinja/)
Alternatively, run the following command on your terminal to do so

```bash
poetry install --with examples
```

Running the example utilizing Context and Headers

```bash
uvicorn examples.login:app
```

## License

This project is licensed under the terms of the MIT license.
