
# GRPC Chat

Zellij terminal, it starts server and clients
```sh
.zellij/dev.kdl
```


```sh
zellij --session groom_dev
```

# Application architecture

[Drawio diagram](./Arci.drawio)

# Running 

### Starting client and server
```sh
source init # initialize venv and set PYTHONPATH
./run_server # chat server
./run_client # chat client
```
Connands are also availabe via invoke

If you have zellij terminal then:
`inv run` will render 4panes with services!

If you prefer, docker compose is also available. (Make it later AWS deployable)

to enable invoke completion run:
```sh
eval "$(invoke --print-completion-script zsh)"
```


Testing:
`inv test`


### Postman/Bruno
To load methods user server-reflection.


### Frontend

```sh
cd ./newsbot
node client.js
```
Url is:
http://localhost:8081


But currently browsers does not handle bi-dir streams.

# Project services

- `groom_server/` - chat server
- `groom_client/` - chat client in terminal, run multiple instances and chat with each other
- `grpcweb_browser/` - grpc web browser client, shows how to user GRPC with browser,not all comm modes are available for browser
- `groom_admin/` - admin console, receives news
- `js_newsbot` - sent news to admin.
# TODO:

- [ ] Learn how to write unittests to GrpC
- [ ] Connect simple DB
- [x] Minimal FE