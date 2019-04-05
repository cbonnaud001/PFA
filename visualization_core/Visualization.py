from libs import *
from Datas import *

class Visualization(object):
    """
    The parent class of all visualization classes, it contains all commun methods like load_model, load_image..

    attr :
    model_name ; the current model's name
    test_img_name ; the current test image name
    layer_name ; the current layer's name
    """
    datas = None
    visu_name = ""

    def __init__(self, datas : Datas):
        self.datas = datas

    @staticmethod  
    def clear_dir_ext(dir_path, lext=[".png"]):
        if not os.path.exists(dir_path):
            print("Le repertoire {} est introuvable.".format(dir_path))
            return
        elif not os.path.isdir(dir_path):
            print("{} n'est pas un repertoire.".format(dir_path))
            return
        for f in os.listdir(dir_path):
            _, fext = os.path.splitext(f)
            if fext in lext:
                os.unlink(dir_path + f)

    #utility function to normalize a tensor.
    def normalize(self, x):
        """
        # Arguments
        x: An input tensor.
        # Returns
        The normalized input tensor.
        """
        return x / (K.sqrt(K.mean(K.square(x))) + K.epsilon())

    # Return a name useful to save images relatively to a visualization
    def get_basic_name(self, id=-1):
        model = self.datas.model
        img_name = self.datas.img_name
        cl_name = self.datas.class_name
        model_name = model.get_config()["name"]
        if id > 0:
            return self.visu_name + "_" + model_name + "_" + cl_name + "_" + img_name.split(".")[0] + "_l" + str(self.datas.layer_id) + "_" + str(id)
        else:
            return self.visu_name + "_" + model_name + "_" + cl_name + "_" + img_name.split(".")[0] + "_l" + str(self.datas.layer_id)

    #utility function to convert a float array into a valid uint8 image.
    def deprocess_image(self, x):
        """
        # Arguments
        x: A numpy-array representing the generated image.
        # Returns
        A processed numpy-array, which could be used in e.g. imshow.
        """
        # normalize tensor: center on 0., ensure std is 0.25
        x -= x.mean()
        x /= (x.std() + K.epsilon())
        x *= 0.25
        
        # clip to [0, 1]
        x += 0.5
        x = np.clip(x, 0, 1)

        # convert to RGB array
        x *= 255
        if K.image_data_format() == 'channels_first':
            x = x.transpose((1, 2, 0))
        x = np.clip(x, 0, 255).astype('uint8')
        return x


    #utility function to convert a valid uint8 image back into a float array.
    def process_image(self, x, former):
        """
        Reverses `deprocess_image`.
        # Arguments
        x: A numpy-array, which could be used in e.g. imshow.
        former: The former numpy-array.
        Need to determine the former mean and variance.
        # Returns
        A processed numpy-array representing the generated image.
        """
        if K.image_data_format() == 'channels_first':
            x = x.transpose((2, 0, 1))
        return (x / 255 - 0.5) * 4 * former.std() + former.mean()


    
    
    # Utility function that evaluates a model for a given input x
    def evaluate(self, model, nodes_to_evaluate, x, y=None):
        with self.datas.graph.as_default():
            if not model._is_compiled:
                if model.name in ['vgg16', 'vgg19', 'inception_v3', 'inception_resnet_v2', 'mobilenet_v2', 'mobilenetv2']:
                    model.compile(loss='categorical_crossentropy', optimizer='adam')
                else:
                    raise Exception('Compilation of the model required.')
            symb_inputs = (model._feed_inputs + model._feed_targets + model._feed_sample_weights)
            f = K.function(symb_inputs, nodes_to_evaluate)
            x_, y_, sample_weight_ = model._standardize_user_data(x, y)
            return f(x_ + y_ + sample_weight_)

    # Utility function that returns the gradient of all trainable weights of the model
    def get_gradients_of_trainable_weights(self, model, x, y):
        nodes = model.trainable_weights
        nodes_names = [w.name for w in nodes]
        return self.get_gradients(model, x, y, nodes, nodes_names)


    # Utility function that returns the gradient of the model activations
    def get_gradients_of_activations(self, model, x, y, layer_name=None):
        nodes = [layer.output for layer in model.layers if layer.name == layer_name or layer_name is None]
        nodes_names = [n.name for n in nodes]
        return self.get_gradients(model, x, y, nodes, nodes_names)

    # Utility function that returns all model gradients (weights, activations..)
    def get_gradients(self, model, x, y, nodes, nodes_names):
        if model.optimizer is None:
            raise Exception('Please compile the model first. The loss function is required to compute the gradients.')
        grads = model.optimizer.get_gradients(model.total_loss, nodes)
        gradients_values = self.evaluate(model, grads, x, y)
        result = dict(zip(nodes_names, gradients_values))
        return result


    # Utility function that returns the layer_name's activations
    def get_activations(self, model, x, l_name=None):
        nodes = [layer.output for layer in model.layers if layer.name == l_name or l_name is None]
        # we process the placeholders later (Inputs node in Keras). Because there's a bug in Tensorflow.
        input_layer_outputs, layer_outputs = [], []
        [input_layer_outputs.append(node) if 'input_' in node.name else layer_outputs.append(node) for node in nodes]
        activations = self.evaluate(model, layer_outputs, x, y=None)
        activations_dict = dict(zip([output.name for output in layer_outputs], activations))
        activations_inputs_dict = dict(zip([output.name for output in input_layer_outputs], x))
        result = activations_inputs_dict.copy()
        result.update(activations_dict)
        return result
