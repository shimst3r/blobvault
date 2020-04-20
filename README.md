# Blob Vault

## A Secure Way of Sharing Almost Anything

Choose and upload almost any content you like, it will be automatically encrypted using the [Fernet algorithm](https://github.com/fernet/spec/).

## Description

The file will be stored on disk and the corresponding download URL will be shared via the provided email address, using the [SendGrid](https://sendgrid.com) service.

Make sure to copy the decryption key. It won't be stored on our servers. Once it's gone, it's gone. Apply the key by appending `?key=$keyvalue` to the download URL.

**One last thing:** Each blob can be downloaded once and only once. After the content is decrypted, it will be purged from our database.

## License

Copyright 2020 Nils Müller<shimst3r@gmail.com>

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
