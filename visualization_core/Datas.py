from libs import *

class Datas(object):
    model = None # The model currently used
    img = None # The image currently selected by the user
    img_name = "" # The image name
    layer_id = 0 # The layer identifier selected by the user
    class_name = ""  # The class selected by the user
    graph = None # The default graph of the current model

    _DEFAULT_GRAPHS = ["VGG16", "VGG19"]
    _GRAPHS_DIR = os.getcwd() + "/graphs/"
    _IMGS_DIR = os.getcwd() + "/mysite/static/mysite/Images/"
    
    @staticmethod
    def get_static_path():
        return os.getcwd() + "/mysite/static/mysite/"

    @staticmethod
    def get_res_path():
        return os.getcwd() + "/mysite/static/mysite/Result/"

    def get_layer_name(self):
        return self.model.layers[self.layer_id].get_config()["name"]

    def __load_default_models(self, model_name):
        if model_name in dir(applications):
            self.model = getattr(applications, model_name)(include_top=False,
                weights='imagenet')

    def __init__(self, model_name = "VGG16"):
        """
        model_name : the name of the model we need to create
        """
        if model_name in self._DEFAULT_GRAPHS:
            self.__load_default_models(model_name)
        else :
            self.model = load_model(self._GRAPHS_DIR + model_name)
        self.graph = tf.get_default_graph()

    def reset(self):
        backend.clear_session()
        self.model = None # The model currently used
        self.img = None # The image currently selected by the user
        self.img_name = "" # The image name
        self.layer_id = 0 # The layer identifier selected by the user
        self.class_name = ""  # The class selected by the user
        self.graph = None # The default graph of the current model

    def set_class(self, class_name):
        self.class_name = class_name

    def set_layer(self, lid):
        self.layer_id = lid

    def set_img(self, img_name):
        img_name = img_name.split('/')[-1]
        location = self._IMGS_DIR + self.class_name + "/" + img_name
        self.img_name = img_name
        self.img = np.array(cv2.imread(location))
        self.img = np.expand_dims(self.img, axis = 0)
