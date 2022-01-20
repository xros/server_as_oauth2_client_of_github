# github生成的两把钥匙
client_id = 'e3a53e8921975c37fe3d'
client_secret = '739a252f5022855aadcc832a2facd86b1b836ef6'
from flask import Flask, \
        redirect, \
        jsonify
from furl import furl
import requests
import json
from flask import request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    url = 'https://github.com/login/oauth/authorize'
    params = {
        'client_id': client_id,
        # 如果不填写redirect_uri那么默认跳转到oauth中配置的callback url。
        # 'redirect_uri': 'http://dig404.com/oauth2/github/callback',
        'scope': 'read:user',
        # 随机字符串，防止csrf攻击
        'state': 'An unguessable random string.',
        'allow_signup': 'true'
    }
    url = furl(url).set(params)
    return redirect(str(url), 302)

@app.route('/oauth2/<service>/callback')
def oauth2_callback(service):
    print(service)

    code = request.args.get('code')
    # 根据返回的code获取access token
    access_token_url = 'https://github.com/login/oauth/access_token'
    payload = {
        'client_id': client_id,
        'client_secret': client_secret,
        'code': code,
        # 'redirect_uri':
        'state': 'An unguessable random string.'
    }
    r = requests.post(access_token_url, json=payload, headers={'Accept': 'application/json'})
    access_token = json.loads(r.text).get('access_token')
    print(access_token)
    # 拿到access token之后就可以去读取用户的信息了
    access_user_url = 'https://api.github.com/user'
    r = requests.get(access_user_url, headers={'Authorization': 'token ' + access_token})
    return jsonify({
        'status': 'success',
        'data': json.loads(r.text)
    })
