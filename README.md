# Blob Vault

## A Secure Way of Sharing Almost Anything

Choose and upload almost any content you like, it will be automatically encrypted using the [Fernet algorithm](https://github.com/fernet/spec/).

## Description

The file will be stored on disk and the corresponding download URL will be shared via the provided email address, using the [SendGrid](https://sendgrid.com) service.

Make sure to copy the decryption key. It won't be stored on our servers. Once it's gone, it's gone. Apply the key by appending `?key=$keyvalue` to the download URL.

**One last thing:** Each blob can be downloaded once and only once. After the content is decrypted, it will be purged from our database.

## How to run

I will add a Dockerfile soon™. Until then, you have to run the application the old-fashioned way, using the `dev_requirements.txt`:

```shell
python3 -m venv venv --prompt blobvault
source venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r dev_requirements.txt
```

Because the app relies on [SendGrid](http://sendgrid.com), you have to get an account. You have to set up an email address for SendGrid and request an API token.

In addition, you have to export the following environment variables:

- `EMAIL_SENDER` (your SendGrid sender email address)
- `SECRET_KEY` (your Django application secret key, just generate one that's sufficiently secret)
- `SENDGRID_API_KEY`

If you have set up everything properly, run the app via

```shell
python manage.py runserver
```

using Django's built-in development server. Don't use it in production though, use [gunicorn](https://gunicorn.org) or [waitress](https://docs.pylonsproject.org/projects/waitress/en/stable/) instead.

## How to test

The test suite is still quite patchy, but it uses [hypothesis](https://hypothesis.readthedocs.io/en/latest/) for property based testing and [model-bakery](https://model-bakery.readthedocs.io/en/latest/) for test fixtures.

You can run the test suite via

```shell
source venv/bin/activate
python manage.py test
```

## Code Quality and CI

I try to stick to [black](https://black.readthedocs.io/en/stable/), [flake8](https://flake8.pycqa.org/en/latest/), and [mypy](https://mypy.readthedocs.io/en/stable/) where possible.

At the moment, there is no CI set up (I'm sorry). Once I find the time, I will add GitHub Actions (I promise).

## License

Copyright 2020 Nils Müller<shimst3r@gmail.com>

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
