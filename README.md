### Use Github's OAuth/Account to Login Your Server -- Python/Flask Example

Same gist at: https://gist.github.com/xros/aba970d1098d916200d0acce8feb0251

Here I explain How-to

Before you write codes, you need to 

Create an app on Github
==================
<img width="1338" alt="iShot2022-01-20 21 59 43" src="https://user-images.githubusercontent.com/2342412/150412769-658f4544-05e2-49db-942a-b1f9ba7978eb.png">

Then Register a new OAuth Application
======================
<img width="1357" alt="iShot2022-01-20 22 13 12" src="https://user-images.githubusercontent.com/2342412/150412916-798193fc-0f51-4733-b2e1-c2b1820eea35.png">

Then Get your client ID and client Secret
====
<img width="1086" alt="iShot2022-01-20 21 58 53" src="https://user-images.githubusercontent.com/2342412/150413000-6a1d6600-5c8d-4ed1-a1c5-14715669559c.png">




In 5 steps,

1. On your server, create a URI to redirect to Github with your Client ID (Github thinks you as a client).
2. On the GitHub OAuth page, user type credentials and successfully login.
3. Github server knows the success login, then Github sends a HTTP request with `code` to your server -- **callback**
4. On your server, with the `code`, your server sends a HTTP request to Github to obtain a temp `access_token`.
5. On your server, with the `access_token`, your server sends a HTTP request to Github to get the github user's info.

Explain with the codes
---------------
1. On your server, create a URI to redirect to Github with your Client ID (Github thinks you as a client).

```python
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
```

2. On the GitHub OAuth page, user type credentials and successfully login.
<img width="1037" alt="iShot2022-01-20 22 49 09" src="https://user-images.githubusercontent.com/2342412/150411574-828defd9-a70c-4837-92d5-4c98fb78ddf3.png">


Step 3,4,5 are in the codes

```python
@app.route('/oauth2/<service>/callback')
def oauth2_callback(service):
    print(service)
# 3. Github server knows the success login, then Github sends a HTTP request with `code` to your server -- **callback**
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
# 4. On your server, with the `code`, your server sends a HTTP request to Github to obtain a temp `access_token`.
    r = requests.post(access_token_url, json=payload, headers={'Accept': 'application/json'})
    access_token = json.loads(r.text).get('access_token')
    print(access_token)
    # 拿到access token之后就可以去读取用户的信息了
    access_user_url = 'https://api.github.com/user'
# 5. On your server, with the `access_token`, your server sends a HTTP request to Github to get the github user's info.
    r = requests.get(access_user_url, headers={'Authorization': 'token ' + access_token})
    return jsonify({
        'status': 'success',
        'data': json.loads(r.text)
    })
```

Now run the app.py application (all in one)
===================

`pip install flask, furl, requests`
Run the app
`export FLASK_ENV=development && flask run`

What does User feel?
=========
User go to http://127.0.0.1:5000
He will be redirected to login, then login success , then your server will have these to finish the session.


<img width="1429" alt="iShot2022-01-20 23 07 25" src="https://user-images.githubusercontent.com/2342412/150414062-71a8118d-2fbc-4638-b5cf-0f219b3c65ac.png">

Inspired from [here](https://zhuanlan.zhihu.com/p/39500505)