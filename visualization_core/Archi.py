from Visualization import *
#from Datas import Datas

class Archi(Visualization):
    """


    """
    def __init__(self, datas : Datas):
        super(Archi, self).__init__(datas)
        self.visu_name = "Archi"


    # Get simple architecture of the network
    def __get_architecture(self, model):
        # Return one letter to say what kind of layer is the parameter
        def name_type(name):
            if "conv" in name: return "c"
            elif "pool" in name: return "p"
            elif "input" in name: return "i"
            elif "flatten" in name: return "f"
            elif "dense" in name: return "d"
            else : return " "
        names = [layer.get_config()["name"] for layer in model.layers]
        return "".join([name_type(name) for name in names])

    # The main function that runs the visualization
    def run(self):
        model = self.datas.model
        return self.__get_architecture(model)
