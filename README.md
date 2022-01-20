Here I explain How-to

Register a new OAuth application
----------------------------------
<img width="1338" alt="iShot2022-01-20 21 59 43" src="https://user-images.githubusercontent.com/2342412/150407926-0be804d9-808c-4823-ad3a-2915bf04c9e1.png">

Then
---------------------------
<img width="1357" alt="iShot2022-01-20 22 13 12" src="https://user-images.githubusercontent.com/2342412/150408088-841a4ffa-dbe9-4e31-bab9-307fcf1e1a59.png">

Create a Client Secret with your Client ID
---------------------------
<img width="1086" alt="iShot2022-01-20 21 58 53" src="https://user-images.githubusercontent.com/2342412/150408221-39a87756-ce9b-4051-9b4e-be5865d509e9.png">


Let me explain the codes
===================

Before this, you need
`pip install flask furl requests`

1. Redirect page to GitHub with your Client ID and Client Secret (Github thinks your server as a client)
2. Then User can see your App on Github, and login with his GitHub credentials.
3. After user successfully login github, Github will send a HTTP request with `code` in URI to your server
4. Your server pick up the `code` from Github, and your server send a HTTP request with the `code` to Github to obtain an `access_token` from Github.
5. With this `access_token`, your server ask Github what the User is like, what his profile is and etc..


