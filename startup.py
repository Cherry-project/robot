from cherry import *
robot=Cherry.setup()
port=Cherry.connectssh()
Cherry.serve(port)

