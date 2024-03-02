```javascript
//npm install crypto-js
import CryptoJS from 'crypto-js';

const key = CryptoJS.enc.Utf8.parse("1234123412ABCDEF");  // A sixteen-digit hexadecimal number as the key, key and iv use the same

// Decryption method
export function Decrypt(word) {
    let decrypt = CryptoJS.AES.decrypt(word, key, { iv: key, mode: CryptoJS.mode.CBC, padding: CryptoJS.pad.Pkcs7 });
    let decryptedStr = decrypt.toString(CryptoJS.enc.Utf8);
    return decryptedStr.toString();
}

// Encryption method
export function Encrypt(word) {
    let src = CryptoJS.enc.Utf8.parse(word)
    let encrypted = CryptoJS.AES.encrypt(src, key, { iv: key, mode: CryptoJS.mode.CBC, padding: CryptoJS.pad.Pkcs7 });
    return encrypted.toString();
}
```

```python
# -*- coding: utf-8 -*-
# @Time    : 2020/9/3 15:03
# @Author  : weidengyi

import base64
from Crypto.Cipher import AES


def pkcs7padding(text):
    """
    Plaintext uses PKCS7 padding
    Ultimately, when calling the AES encryption method, a byte array is passed in, which is required to be a multiple of 16, so the plaintext needs to be processed
    :param text: Content to be encrypted (plaintext)
    :return:
    """
    bs = AES.block_size  # 16
    length = len(text)
    bytes_length = len(bytes(text, encoding='utf-8'))
    # tips: In utf-8 encoding, English occupies 1 byte, while Chinese occupies 3 bytes
    padding_size = length if(bytes_length == length) else bytes_length
    padding = bs - padding_size % bs
    # tips: chr(padding) see the convention with other languages, some will use '\0'
    padding_text = chr(padding) * padding
    return text + padding_text


def pkcs7unpadding(text):
    """
    Process data that has been padded with PKCS7
    :param text: The decrypted string
    :return:
    """
    try:
        length = len(text)
        unpadding = ord(text[length-1])
        return text[0:length-unpadding]
    except Exception as e:
        pass


def aes_encode(key, content):
    """
    AES encryption
    key, iv use the same
    mode cbc
    padding pkcs7
    :param key: Key
    :param content: Content to encrypt
    :return:
    """
    key_bytes = bytes(key, encoding='utf-8')
    iv = key
    cipher = AES.new(key_bytes, AES.MODE_CBC, iv)
    # Process plaintext
    content_padding = pkcs7padding(content)
    # Encrypt
    aes_encode_bytes = cipher.encrypt(bytes(content_padding, encoding='utf-8'))
    # Re-encode
    result = str(base64.b64encode(aes_encode_bytes), encoding='utf-8')
    return result


def aes_decode(key, content):
    """
    AES decryption
     key, iv use the same
    mode cbc
    remove padding pkcs7
    :param key:
    :param content:
    :return:
    """
    key_bytes = bytes(key, encoding='utf-8')
    iv = key
    cipher = AES.new(key_bytes, AES.MODE_CBC, iv)
    # base64 decode
    aes_encode_bytes = base64.b64decode(content)
    # Decrypt
    aes_decode_bytes = cipher.decrypt(aes_encode_bytes)
    # Re-encode
    result = str(aes_decode_bytes, encoding='utf-8')
    # Remove padding content
    result = pkcs7unpadding(result)
    return result


if __name__ == "__main__":
    key = "1234123412ABCDEF"
    myStr = "testor"
    secret = aes_encode(key, myStr)
    print(secret)
    print(aes_decode(key, secret))
```

```
//JS validation
const secret = Encrypt("testor") 
console.log("secret:", secret) //secret: bCvq7vZd/DcQVlbZaK2d+g==
console.log(Decrypt(secret)) //testor

#Python validation
if __name__ == "__main__":
    key = "1234123412ABCDEF"
    myStr = "testor"
    secret = aes_encode(key, myStr) #  bCvq7vZd/DcQVlbZaK2d+g==
    print(secret)
    print(aes_decode(key, secret)) # testor
```