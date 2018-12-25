from Crypto.Util.asn1 import DerSequence
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA
from Crypto.Cipher import PKCS1_v1_5 as Cipher_pkcs1_v1_5
from Crypto.Signature import PKCS1_v1_5 as Signature_pkcs1_v1_5
from binascii import a2b_base64
import base64
import json
import os
import time

cur_file_path = os.path.dirname(os.path.realpath(__file__))

COUPON_PUB_KEY_PATH = os.path.join(os.path.dirname(cur_file_path), "resource/aibili/aibili_coupon_public.crt")
COUPON_PRI_KEY_PATH = os.path.join(os.path.dirname(cur_file_path), "resource/aibili/aibili_coupon_pri.pem")

COUPON_PUBLIC_KEY_PATH = os.path.join(os.path.dirname(cur_file_path), "resource/aibili/aibili_coupon_pub.crt")
COUPON_PRIVATE_KEY_PATH = os.path.join(os.path.dirname(cur_file_path), "resource/aibili/aibili_coupon_private.pem")

AIBILI_PUBLIC_KEY_PATH = os.path.join(os.path.dirname(cur_file_path), "resource/aibili/aibili_public.crt")
AIBILI_PRIVATE_KEY_PATH = os.path.join(os.path.dirname(cur_file_path), "resource/aibili/aibili_private.pem")

LOGIN_PUBLIC_KEY_PATH = os.path.join(os.path.dirname(cur_file_path), "resource/aibili/login_public.crt")
LOGIN_PRIVATE_KEY_PATH = os.path.join(os.path.dirname(cur_file_path), "resource/aibili/login_private.pem")

key_path = {"AIBILI_PUBLIC_KEY_PATH": AIBILI_PUBLIC_KEY_PATH, "AIBILI_PRIVATE_KEY_PATH": AIBILI_PRIVATE_KEY_PATH,
            "COUPON_PUB_KEY_PATH": COUPON_PUB_KEY_PATH, "COUPON_PRI_KEY_PATH": COUPON_PRI_KEY_PATH,
            "COUPON_PUBLIC_KEY_PATH": COUPON_PUBLIC_KEY_PATH, "COUPON_PRIVATE_KEY_PATH": COUPON_PRIVATE_KEY_PATH,
            "LOGIN_PUBLIC_KEY_PATH": LOGIN_PUBLIC_KEY_PATH, "LOGIN_PRIVATE_KEY_PATH": LOGIN_PRIVATE_KEY_PATH}

# 加密
def encrypt(data, pub_key_path='AIBILI_PUBLIC_KEY_PATH', default_length=117):
    """
    单次加密串的长度最大为 (key_size/8)-11
    1024bit的证书用100， 2048bit的证书用 200
    """

    with open(key_path.get(pub_key_path), "r") as f:
        key = f.read()
        # Convert from PEM to DER
        lines = key.replace(" ", '').split()
        der = a2b_base64(''.join(lines[1:-1]))

        # Extract subjectPublicKeyInfo field from X.509 certificate (see RFC3280)
        cert = DerSequence()
        cert.decode(der)
        tbsCertificate = DerSequence()
        tbsCertificate.decode(cert[0])
        subjectPublicKeyInfo = tbsCertificate[6]

        # Initialize RSA key
        rsa_key = RSA.importKey(subjectPublicKeyInfo)
        cipher = Cipher_pkcs1_v1_5.new(rsa_key)
        data = data.encode()
        length = len(data)
        if length < default_length:
            cipher_text = base64.b64encode(cipher.encrypt(data)).decode()
            return cipher_text

        res = []
        offset = 0
        while length - offset > 0:
            if length - offset > default_length:
                # res.append(base64.b64encode(cipher.encrypt(data[offset:offset + default_length])).decode())
                res.append(cipher.encrypt(data[offset:offset + default_length]))
            else:
                # res.append(base64.b64encode(cipher.encrypt(data[offset:])).decode())
                res.append(cipher.encrypt(data[offset:]))
            offset += default_length
        cipher_text = b""
        for r in res:
            cipher_text += r
        cipher_text = base64.b64encode(cipher_text).decode()
        return cipher_text


# 解密
def decrypt(data, pri_key_path='AIBILI_PRIVATE_KEY_PATH', default_length=128):
    """
    1024bit的证书用128，2048bit证书用256位
    """

    with open(key_path.get(pri_key_path)) as f:
        key = f.read()
        rsa_key = RSA.importKey(key)
        cipher = Cipher_pkcs1_v1_5.new(rsa_key)
        data = base64.b64decode(data.encode())
        length = len(data)
        if length < default_length:
            decrypt_text = cipher.decrypt(data, 'ERROR')
            return decrypt_text
        res = []
        offset = 0
        while length - offset > 0:
            if length - offset > default_length:
                res.append(cipher.decrypt(data[offset:offset + default_length], "ERROR"))

            else:
                res.append(cipher.decrypt(data[offset:], "ERROR"))
            offset += default_length
        cipher_text = b""
        for r in res:
            cipher_text += r
        try:
            decrypt_text = json.loads(cipher_text.decode())
        except Exception as e:
            decrypt_text = cipher_text.decode()
        return str(decrypt_text) if type(decrypt_text) == int else decrypt_text


# 签名
def generate_signature(data, pri_key_path='AIBILI_PRIVATE_KEY_PATH'):
    with open(key_path.get(pri_key_path)) as f:
        key = f.read()
        rsa_key = RSA.importKey(key)
        signer = Signature_pkcs1_v1_5.new(rsa_key)
        digest = SHA.new()
        digest.update(base64.b64decode(data))
        sign = signer.sign(digest)
        signature = base64.b64encode(sign).decode()
        return signature

def sign(data, pri_key_path='AIBILI_PRIVATE_KEY_PATH'):
    with open(key_path.get(pri_key_path)) as f:
        key = f.read()
        rsa_key = RSA.importKey(key)
        signer = Signature_pkcs1_v1_5.new(rsa_key)
        digest = SHA.new(data.encode())
        sign = signer.sign(digest)
        signature = base64.b64encode(sign).decode()
        return signature

# 验签
def verify_signature(result, pub_key_path='AIBILI_PUBLIC_KEY_PATH'):
    sign = result.get("sign").encode()
    data = result.get("data").encode()
    with open(key_path.get(pub_key_path)) as f:
        key = f.read()
        # Convert from PEM to DER
        lines = key.replace(" ", '').split()
        der = a2b_base64(''.join(lines[1:-1]))

        # Extract subjectPublicKeyInfo field from X.509 certificate (see RFC3280)
        cert = DerSequence()
        cert.decode(der)
        tbsCertificate = DerSequence()
        tbsCertificate.decode(cert[0])
        subjectPublicKeyInfo = tbsCertificate[6]

        rsa_key = RSA.importKey(subjectPublicKeyInfo)
        verifier = Signature_pkcs1_v1_5.new(rsa_key)
        digest = SHA.new()
        # Assumes the data is base64 encoded to begin with
        digest.update(base64.b64decode(data))
        is_verify = verifier.verify(digest, base64.b64decode(sign))
        return is_verify


def verify_sign(result, pub_key_path='AIBILI_PUBLIC_KEY_PATH'):
    sign = result.get("sign").encode()
    data = str(result.get("data")).encode()
    with open(key_path.get(pub_key_path)) as f:
        key = f.read()
        # Convert from PEM to DER
        lines = key.replace(" ", '').split()
        der = a2b_base64(''.join(lines[1:-1]))

        # Extract subjectPublicKeyInfo field from X.509 certificate (see RFC3280)
        cert = DerSequence()
        cert.decode(der)
        tbsCertificate = DerSequence()
        tbsCertificate.decode(cert[0])
        subjectPublicKeyInfo = tbsCertificate[6]

        rsa_key = RSA.importKey(subjectPublicKeyInfo)
        signer = Signature_pkcs1_v1_5.new(rsa_key)
        digest = SHA.new(data)
        is_verify = signer.verify(digest, base64.b64decode(sign))
        return is_verify


if __name__ == '__main__':
    # data = '''NPUkyWNhTRDq7Q573/ASwJs9jE/JoOmiSTH5mAa68npU6H5FeBvnbUNlCsYwZ8nD7yS9E/L1il/TWFlKOvvB+pWQ+z1sfzunAACONt3wViT6+RvOWEw8W6Ghb00Xif/AY98x4lVo+CoPmtHNPzOlikQJaYwwArXH9VqT4lcleEA='''
    # with open("../resource/aibili/aibili_private.pem") as f:
    #     key = f.read()
    #     rsa_key = RSA.importKey(key)
    #     cipher = Cipher_pkcs1_v1_5.new(rsa_key)
    #     p = base64.b64decode(data.encode())
    #     result = ''
    #     while True:
    #         x = p[0:128]
    #         p = p[128:]
    #         if x:
    #             result += cipher.decrypt(x, "ERROR").decode('utf-8')
    #         else:
    #             break
    #     print(result)

    data = {"timestamp": str(int(round(time.time() * 1000)))}
    data = {"mblNo": "18152149829", "bonId":"1000000000000200", "expireDate":"2018-12-09 07:20:33",
            "createDate":"2018-12-09 07:20:33", "name":"RTF测试财富券", "prizeDesc":"RTF测试用", "useDesc":"随便用",
            "type":"4", "rate":"0.5", "bonSts":"D", "timestamp": str(int(round(time.time() * 1000)))}
    data = {"mobile":"18152149829",  "timestamp": str(int(round(time.time() * 1000)))}
    if type(data) == list:
        data = {"list": data}
    curr_ency = encrypt(str(data), 'COUPON_PUBLIC_KEY_PATH')
    curr_sign = generate_signature(curr_ency, 'COUPON_PRIVATE_KEY_PATH')
    print(f'"sign": "{curr_sign}", "data": "{curr_ency}"')

    data = {
    "sign": "IL9WGCgcLT25M+yn51gaJS5/SfvLcFHyabZtlQozoSRLtFPNOzkuiRKoN+ZL8V+R57kuCEhkJYiHixw9bk4FE+eAgGUktM4zrh08pjKlTtvhZTpUJpfJ/pSoU32QWhraT/x5cvIgKolX1gpK7EkjBdMGHafVnJSaVjwnQCAa2oM=",
    "data": "xHfai9vEqg6O6rc91Xn9DAgpGIClGZ4q5wgzAwqbD5019k4SlLLSeYb0DaMdni4apQgrC/sVxSgRKA6e6Nzk45yjwbohrT+/iXv7xUIuBgMfgStg7PYFG2G4OFKhLCE5FLbqPUqaiEWXhW5sgfzA8IINur4CC1LfXzBLICPrCd8="
}
    result = verify_sign(data, 'COUPON_PUBLIC_KEY_PATH')
    result_decrypt = decrypt(str(data.get("data")), 'COUPON_PRIVATE_KEY_PATH')
    print(f'result:{result}, result_decrypt:{result_decrypt}')
