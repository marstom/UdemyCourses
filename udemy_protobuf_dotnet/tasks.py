from invoke import task


@task
def gen(c):
    c.run("protoc --python_out=./proto_output my.proto")