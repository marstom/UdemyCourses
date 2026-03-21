from invoke import task


@task
def ppath(c):
    c.run("echo $PYTHONPATH")


@task()
def generate_protos(c):
    """This generates all protos"""
    # admin
    c.run(
        """ 
        cd groom_admin &&
        python -m grpc_tools.protoc \
        -I ./protos \
        --python_out=. \
        --pyi_out=. \
        --grpc_python_out=. \
        protos/groom.proto
        """
    )
    print("ok")

    # server
    c.run(
        """ 
        cd groom_server &&
        python -m grpc_tools.protoc \
        -I ./protos \
        --python_out=. \
        --pyi_out=. \
        --grpc_python_out=. \
        protos/*.proto
        """
    )
    print("ok")

    # chat
    c.run(
        """ 
        cd chat_client &&
        python -m grpc_tools.protoc \
        -I ./protos \
        --python_out=. \
        --pyi_out=. \
        --grpc_python_out=. \
        protos/groom.proto
        """
    )
    print("ok")
    print("Protos generated!")


"""
   result = protoc.main(
        [
            "protoc",
            f"-I{base_proto_path}",
            f"-I{grpc_include}",
            "--python_out=.",
            "--grpc_python_out=.",
            "THE PATH",
        ]
"""

############# Services


@task
def run_1_groom_server(c):
    """First run a server"""
    c.run(
        "cd groom_server && PYTHONPATH=$(pwd) python ./src/groom_server.py",
        echo=True,
    )


@task
def run_2_groom_admin(c):
    """Second run this admin panel, it will monitor messages for you!"""
    c.run(
        "cd groom_admin && PYTHONPATH=$(pwd) python monitor_chat.py",
        echo=True,
        pty=True,
    )


@task
def run_3_node_client(c):
    """
    Next run this client:
    It will push some messages to queue, so our client can display something!
    Node client which send news.
    """
    # pty - colors
    # c.run("node newsbot/client.js", pty=True, echo=True)
    c.run("cd js_newsbot && node client.js")


@task
def run_4_chat(c):
    """
    Next run this client:
    It will push some messages to queue, so our client can display something!
    Node client which send news.
    """
    # pty - colors
    # c.run("node newsbot/client.js", pty=True, echo=True)
    c.run(
        "cd chat_client & PYTHONPATH=$(pwd) python chat_client.py", echo=True, pty=True
    )


# Experimental zellij layout, please change groom_dev to your session name if you have different
@task
def dev(c):
    c.run("zellij --session groom_dev --layout .zellij/dev.kdl", pty=True)

@task
def test(c):
    c.run("pytest -vvs .")