
# Info

.zellij/dev.kdl to jest zestaw pane dla zellij

najpierw stwórz sesję z zellij

```sh
zellij --session groom_dev
```

# Application architecture

[Rysunek](./Arci.drawio)




# How to 


Postam, import .proto


```sh
source init

python ./src/groom_server.py
python ./src/groom_client.py


# invoke completeion script

eval "$(invoke --print-completion-script zsh)"
```

FE ,streamuje newsy

```sh


./newsbot
node client.js

```


# TODO:

- [ ] Learn how to write unittests to GrpC
- [ ] Connect simple DB
- [ ] Minimal FE