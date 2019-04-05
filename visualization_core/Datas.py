from libs import *

class Datas(object):
    """
    Store useful datas like the current model and its graph,
    the class, the layer and the image the user could have selected
    """
    model = None # The model currently used
    img = None # The image currently selected by the user
    img_name = "" # The image name
    layer_id = 0 # The layer identifier selected by the user
    class_name = ""  # The class selected by the user
    graph = None # The default graph of the current model

    #Default applications that the user could use (now only VGG16 and VGG19 are available)
    _DEFAULT_GRAPHS = ["VGG16", "VGG19"]
    #Directory where to find other models (.h5 extension)
    _GRAPHS_DIR = os.getcwd() + "/graphs/"
    #Directory where to find classes in which images could be selected
    _IMGS_DIR = os.getcwd() + "/mysite/static/mysite/Images/"
    
    @staticmethod
    def get_static_path():
        """
        #Return:
        return the path to static files.
        This is for client which can only access datas from
        cwd/mysite/static/mysite/
        """
        return os.getcwd() + "/mysite/static/mysite/"

    @staticmethod
    def get_res_path():
        """
        #Return:
        return the path to result files.
        This is the directory where images and files are stored
        """
        return os.getcwd() + "/mysite/static/mysite/Result/"

    def get_layer_name(self):
        """
        #Return the name of the current layer
        """
        return self.model.layers[self.layer_id].get_config()["name"]

    def __load_default_models(self, model_name):
        """
        If model_name belongs to keras' applications
        load the model with this application
        #Arguments:
        model_name : The name of a keras' application
        """
        if model_name in dir(applications):
            self.model = getattr(applications, model_name)(include_top=False,
                weights='imagenet')

    def __init__(self, model_name = "VGG16"):
        """
        Initialize all datas needed for visualization
        like models, layer ids, the image selected by the user
        #Arguments
        model_name : the name of the model we need to create
        """
        if model_name in self._DEFAULT_GRAPHS:
            self.__load_default_models(model_name)
        else :
            self.model = load_model(self._GRAPHS_DIR + model_name)
        self.graph = tf.get_default_graph()

    def reset(self):
        """
        Clear all variables and reset tensorflow backend
        """
        backend.clear_session()
        self.model = None # The model currently used
        self.img = None # The image currently selected by the user
        self.img_name = "" # The image name
        self.layer_id = 0 # The layer identifier selected by the user
        self.class_name = ""  # The class selected by the user
        self.graph = None # The default graph of the current model

    def set_class(self, class_name):
        """
        Set the class name
        #Argument:
        class_name : the name of the class selected by the user
        """
        self.class_name = class_name

    def set_layer(self, lid):
        """
        Set the layer id
        #Argument:
        layer_id : the id of the layer selected by the user
        """
        self.layer_id = lid

    def set_img(self, img_name):
        """
        Open the image selected by the user
        and format it to be passed to keras subrootins
        like Model.predict that require a special format
        for the image
        #Argument:
        img_name : the name of an image situated in _IMGS_DIR
        """
        img_name = img_name.split('/')[-1]
        location = self._IMGS_DIR + self.class_name + "/" + img_name
        self.img_name = img_name
        self.img = np.array(cv2.imread(location))
        self.img = np.expand_dims(self.img, axis = 0)
