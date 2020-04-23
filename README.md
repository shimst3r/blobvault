# Blob Vault

## A Secure Way of Sharing Almost Anything

Choose and upload almost any content you like, it will be automatically encrypted using the [Fernet algorithm](https://github.com/fernet/spec/). Given that the encryption is server-side, the main usecase of `blobvault` is hosting it yourself in a trusted environment.

## Description

The file will be stored on disk and the corresponding download URL will be shared via the provided email address, using the [SendGrid](https://sendgrid.com) service. Inform the person you're sharing the file with, otherwise they might get confused about the onsolicited email.

Make sure to copy the decryption key. It won't be stored on the servers. Once it's gone, it's gone.

**One last thing:** Each blob can be downloaded once and only once. After the content is decrypted, it will be purged from the database.

## Tech Stack

The project is based on [Python](https://www.python.org) and [Django](https://www.djangoproject.com).

The following packages are used on top:

* [cryptography](https://cryptography.io/en/latest/) for file encryption.
* [django-crispy-forms](https://django-crispy-forms.readthedocs.io/en/latest/) for prettier forms.
* [django-extension](https://django-extensions.readthedocs.io/en/latest/) for a better debugging experience.
* [django-sendgrid](https://github.com/sklarsa/django-sendgrid-v5) for [SendGrid](http://sendgrid.com) API integration.
* [waitress](https://docs.pylonsproject.org/projects/waitress/en/latest/) as WSGI server.
* [whitenoise](http://whitenoise.evans.io) for static file serving.

## How to run

Because the app relies on [SendGrid](http://sendgrid.com), you have to get an account. You have to set up an email address for SendGrid and request an API token.

The project has a `docker-compose` friendly setup. Install the [Docker](https://www.docker.com) desktop app, which includes the binaries for `docker-compose`. Adjust the `sample.env` and rename it to `.env`, then all you have to do is

```shell
docker-compose build
docker-compose up
```

If you want to, you can run the application the old-fashioned way, using the `requirements.txt` file:

```shell
python3 -m venv venv --prompt blobvault
source venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

In addition, you have to export the following environment variables:

- `EMAIL_SENDER` (your SendGrid sender email address)
- `SECRET_KEY` (your Django application secret key, just generate one that's sufficiently secret)
- `SENDGRID_API_KEY`

If you have set up everything properly, run the app via

```shell
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

using Django's built-in development server. Don't use it in production though, use [gunicorn](https://gunicorn.org) or [waitress](https://docs.pylonsproject.org/projects/waitress/en/stable/) instead.

## How to test

The test suite is still quite patchy, but it uses [hypothesis](https://hypothesis.readthedocs.io/en/latest/) for property based testing and [model-bakery](https://model-bakery.readthedocs.io/en/latest/) for test fixtures.

You can run the test suite via

```shell
source venv/bin/activate
python -m pip install -r dev_requirements.txt
python manage.py test
```

## Code Quality and CI

I try to stick to [black](https://black.readthedocs.io/en/stable/), [Django check](https://docs.djangoproject.com/en/3.0/ref/django-admin/#check), [flake8](https://flake8.pycqa.org/en/latest/), and [mypy](https://mypy.readthedocs.io/en/stable/) where possible, with minimal configuration.

Code compliance is checked using GitHub Actions.

## License

> Copyright 2020 Nils Müller <shimst3r@gmail.com>
>
> Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
>
> The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
>
> THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
