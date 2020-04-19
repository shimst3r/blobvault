# Blob Vault

## A Secure Way of Sharing Almost Anything

Choose and upload almost any content you like, it will be automatically encrypted using the [Fernet algorithm](https://github.com/fernet/spec/).

The file will be stored on disk and the corresponding download URL will be shared via the provided email address.

Make sure to copy the encryption key. It won't be stored on our servers. Once it's gone, it's gone. Apply the key by appending `?key=$keyvalue` to the download URL.
