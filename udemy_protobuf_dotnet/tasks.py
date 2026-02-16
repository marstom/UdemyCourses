from invoke import task, Collection
import os



@task
def source(c):
    c.run("source .venv/bin/activate")
    c.run("export PYTHONPATH=$(pwd):$(pwd)/generated")

@task
def clean(c):
    try:
        c.run("find . -type f \\( -name '*_pb2.py' -o -name '*_pb2.pyi' -o -name '*_pb2_grpc.py' \\) -delete")
    except:
        print("Noting to revmove")

@task
def ppath(c):
    c.run("echo $PYTHONPATH")


@task
def _generate_grpc(c):
    # Generate pb2 + type hints + grpc stubs into proto_output/
    names = [os.path.join("protos", "groom.proto"), os.path.join("protos", "my.proto")]
    for protoc_name in names:
        
        c.run(
            f""" 
            python -m grpc_tools.protoc \
            -I ./protos \
            --python_out=generated \
            --grpc_python_out=generated \
            {protoc_name}
            """
        )


@task
def _generate_grpc_groomadmin(c):
    names = [os.path.join("protos", "groom.proto")]
    folder = os.path.join("groomadmin", "protos")
    folder_base = os.path.join("groomadmin")
    for protoc_name in names:
        c.run(
            f""" 
            cd groomadmin &&
            python -m grpc_tools.protoc \
            -I ./protos \
            --python_out=generated \
            --pyi_out=generated \
            --grpc_python_out=generated \
            {protoc_name}
            """
        )

@task(clean, _generate_grpc, _generate_grpc_groomadmin)
def generate_protos(c):
    """This generates all protos"""
    print("Protos generated")
    # c.run("invoke generate-grpc")
    # c.run("invoke generate-grpc-groomadmin")

############# Services

@task
def run_groom_server(c):
    """ First run a server"""
    c.run("python src/groom_server.py")

@task
def run_groom_admin(c):
    """ Second run this admin panel, it will monitor messages for you!"""
    c.run("cd groomadmin && python monitor_chat.py", echo=True, pty=True)


@task
def run_node_client(c):
    """
    Next run this client:
    It will push some messages to queue, so our client can display something!
    Node client which send news.
    """
    # pty - colors
    # c.run("node newsbot/client.js", pty=True, echo=True)
    c.run("node newsbot/client.js")

