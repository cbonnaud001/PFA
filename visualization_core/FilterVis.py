from Visualization import *
#from Datas import *

class FilterVis(Visualization):
    """
    Computes some filters of the layer selected by the user.
    """

    def __init__(self, datas : Datas):
        super(FilterVis, self).__init__(datas)
        self.visu_name = "FilterVis"


    #This method visualizes CNN layers activations
    def __display_activation(self, activations, col_size, row_size, act_index):

        """
        activations : a table of the activation matrix of each layer, layers are differentieted by their index which is the same as the layer's position in the model
        col_size : output image weidth
        row_size : output image height
        act_index : the layer's index
        """

        activation = activations[act_index]
        activation_index=0
        fig, ax = plt.subplots(row_size, col_size, figsize=(row_size*2.5,col_size*1.5))
        for row in range(0,row_size):
            for col in range(0,col_size):
                ax[row][col].imshow(activation[0, :, :, activation_index], cmap='gray')
                activation_index += 1
        plt.savefig("res.png")


    def run(self):
        """
        Run the visualization. Computes some filters of the layer selected by the user.
        """
        activation_model = Model(inputs=self.datas.model.input,
                    outputs=[self.datas.model.layers[self.datas.layer_id].output])
        with self.datas.graph.as_default():
            activation = activation_model.predict(self.datas.img)
            return self.save_images(activation)

    def _save_single_image(self, activation_index, img_names, activation):
        """
        Save one particular image related to one particular filter of the current layer
        """
        res_name = self.get_basic_name(activation_index)
        img_names[res_name] = res_name + ".png"
        Image.fromarray(activation[0, :, :, activation_index]).convert('L').save(Datas.get_res_path() + res_name + ".png")
        

    def save_images(self, activation):
        """
        Save all image using parallelism to save each image
        #Arguments:
        activation : a model which input is the input of the current model and outpout is the output of the current layer
        #Return:
        A dictionnary `res' which values match images generated for each filters
        For each key x :
        res[x] = x + ".png"
        """
        img_names = {}
        fig = plt.figure(frameon=False)
        ax = plt.Axes(fig, [0., 0., 1., 1.])
        ax.set_axis_off()
        fig.add_axes(ax)
        Parallel(n_jobs=24, backend="threading")(delayed(self._save_single_image)(row, img_names, activation) for row in range(10))
        return img_names
