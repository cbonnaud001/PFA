import os
"""
if not os.path.exists("../../mysite/graphs"):
    print("There is no graphs/ dir where to find graphs")
    exit(1)
if not os.path.exists("../../mysite/Images"):
    print("There is no graphs/ dir where to find images")
    exit(1)
"""
"""
if not os.path.exists("./graphs"):
    print("There is no graphs/ dir where to find graphs")
    exit(1)
if not os.path.exists("./Images"):
    print("There is no graphs/ dir where to find images")
    exit(1)
"""
# Global constant
MODEL_NAME = None
TEST_IMAGE_PATH = None
GRAPHS_DIR = os.getcwd() + "/graphs/"
IMGS_DIR = os.getcwd() + "/mysite/static/mysite/Images/"
STATIC_SITE_DIR = os.getcwd() + "/mysite/static/mysite/"
RES_DIR = STATIC_SITE_DIR + "Result/"
DEFAULT_GRAPHS = ["VGG16"]

# Useful constant
model = None # Contains the name of the model selected by the user
model_name = None # Contain the name of the model opened
layer_outputs = None # Recovering the model's layers outputs
activations = None
cl_name = None # Class name where to find the image
img = None # Countain an image selected by the user
img_name = None # Contain the name of the image
layer_id = None # Contain the id of the layer we are studying
layer = None # The layer we are working on
activation_models = None
graph = None 