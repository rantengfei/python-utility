# encoding: utf-8
from collections import OrderedDict
import rsa
import os
from sanic.response import json
import time
import base64
import json as jsonbase
from urllib.parse import quote, unquote

cur_file_path = os.path.dirname(os.path.realpath(__file__))
# --- for test
# WBF_PUBLIC_KEY_PATH = os.path.join(os.path.dirname(cur_file_path), "h5/resource/wbf/wbf_public.crt")
# WBF_PRIVATE_KEY_PATH = os.path.join(os.path.dirname(cur_file_path), "h5/resource/wbf/wbf_private.pem")

# ---- for hq  use
WBF_PRIVATE_KEY_PATH = os.path.join(os.path.dirname(cur_file_path), "resource/wbf/hq_private_encrypt.pem")
WBF_PUBLIC_KEY_PATH = os.path.join(os.path.dirname(cur_file_path), "resource/wbf/wbf_public_decrypt.pem")

# ----- for wbf use
# WBF_PRIVATE_KEY_PATH = os.path.join(os.path.dirname(cur_file_path), "h5/resource/wbf/wbf_private_encrypt.pem")
# WBF_PUBLIC_KEY_PATH = os.path.join(os.path.dirname(cur_file_path), "h5/resource/wbf/hq_public_decrypt.pem")

class SignTools:
    def __init__(self,
                 private_file=WBF_PRIVATE_KEY_PATH,
                 public_file=WBF_PUBLIC_KEY_PATH,
                 req_expired=30):
        self.private_file = private_file
        self.public_file = public_file
        self.req_expired = req_expired

    def generate_rsa_keys(self):
        # 生成密钥
        (pubkey, privkey) = rsa.newkeys(1024)
        # =================================
        # 场景〇：密钥保存导入
        # =================================
        # 保存密钥
        with open('public.pem','w+') as f:
            f.write(pubkey.save_pkcs1().decode())

        with open('private.pem','w+') as f:
            f.write(privkey.save_pkcs1().decode())

    # 公钥加密
    def encrypt(self, message):
        with open(self.public_file, 'r') as f:
            keyfile = f.read().encode()
            public_key = rsa.PublicKey.load_pkcs1(keyfile)
            block = rsa.encrypt(message.encode(), public_key)
            return base64.b64encode(block).decode()

    # 私钥解密
    def decrypt(self, message):
        with open(self.private_file, 'r') as f:
            keyfile = f.read().encode()
            private_key = rsa.PrivateKey.load_pkcs1(keyfile)
            return rsa.decrypt(base64.b64decode(message), private_key).decode()

    # 签名
    def generate_signature(self, params):
        data = self.sort_params(params)
        with open(self.private_file, 'r') as f:
            keyfile = f.read().encode()
            private_key = rsa.PrivateKey.load_pkcs1(keyfile)
            signature = rsa.sign(data.encode(), private_key, 'SHA-1')
            return base64.b64encode(signature).decode()


    # 验签
    def verify_signature(self, params, sign):
        timestamp_in = int(params.get("timestamp"))/1000
        timestamp_cur = int(self.get_timestamp())/1000
        diff = abs(int(timestamp_in) - int(timestamp_cur))
        if diff > self.req_expired:
            return False
        data = self.sort_params(params)
        with open(self.public_file) as f:
            keyfile = f.read().encode()
            public_key = rsa.PublicKey.load_pkcs1(keyfile)
            try:
                rsa.verify(data.encode(), base64.b64decode(sign), public_key)
                return True
            except Exception as e:
                return False

    # 按照ASCII码排序
    def sort_params(self, params):
        params.pop("sign", True)
        params = OrderedDict(sorted(params.items()))
        result = ""
        for key, value in params.items():
            if value:
                #result += f'&{key}={unquote(value) if value else ""}'
                result += f'&{key}={value if value else ""}'
        if result.find("&") == 0:
            result = result[1:]
        return result

    def get_timestamp(self):
        return str(int(round(time.time() * 1000)))

    def success(self, data={}):
        if type(data) == list:
            data = {"list": data}
        data["timestamp"] = self.get_timestamp()
        sign = self.generate_signature(data)
        result = json({"sign": sign, "data": data, "return_code": "0000", "return_msg": "成功"})
        return result

    def aborted(self, data={}, return_code="1111", return_msg="失败"):
        data["timestamp"] = self.get_timestamp()
        sign = self.generate_signature(data)
        result = json({"sign": sign, "data": data, "return_code": return_code, "return_msg": return_msg})
        return result

if __name__ == '__main__':

    signtools = SignTools()
    #signtools.generate_rsa_keys()
    print("-----加密-------------------------------------")
    message = "hello"
    message_encrypt = signtools.encrypt(message)
    print(f"message_encrypt={message_encrypt}")
    message_decrypt = signtools.decrypt(message_encrypt)
    print(f"message_decrypt={message_decrypt}")
    print("-----验签-------------------------------------")
    #params = {"mobile": "18919889828", "timestamp": signtools.get_timestamp(), "sign":"aaa"}
    params = {"mobile": "15343210969", "timestamp": signtools.get_timestamp(), "sign":"aaa"}
    # params = {
    #   "mobile":"18919889828",
    #   "name": "%E7%8E%8B%E9%94%A1%E5%8B%873",
    #   "id_card": "620102198106206515",
    #   "timestamp":signtools.get_timestamp(),
    #   "sign":""
    # }
    #params = {'mobile': '13574856074', 'name': '%E5%94%90%E9%9B%84%E9%B9%8F', 'id_card': '432524198911045813', 'timestamp': '1531555045726', 'sign': 'SiymtmQVEKg9l0XX+r4HQ9v+jFz933YtBNgsWjs1s9O+WQxH/KBI68C9oC+ahvfv5tqNnvszEeMC1IdnE/fqnBTsfQaL9bPDM47niEmQJJYOGfAPUmWJN8V9S6R3Ziwx43Wp2Dz4JImOtc2MF7m2CNLsblhO+5A+LmfieWO8+9k='}
    sign = signtools.generate_signature(params)
    print(f"sign={sign}")
    params["sign"] = sign
    print(f"{jsonbase.dumps(params)}")
    result = signtools.verify_signature(params, sign)
