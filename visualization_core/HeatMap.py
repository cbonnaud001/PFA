from Visualization import *
from Datas import Datas

class HeatMap(Visualization):
    """
    This type of visualization calculates the heatmap on the test image from the output of the selected convolutional layer
    """
    def __init__(self, datas : Datas):
        super(HeatMap, self).__init__(datas)
        self.visu_name = "HeatMap"

    # Utility function that overlaps all images in DIR
    def __overlap(self, DIR, layer_name, o_name):
        """output_name = Datas.get_res_path() + o_name
        origin_image = Image.open(output_name)
        origin_image = origin_image.convert("RGBA")"""

        files = [f for f in listdir(DIR) if isfile(join(DIR, f))]
        old = Image.open(DIR + files[0])
        old = old.convert("RGBA")

        for fname in files[1:]:
            new = Image.open(DIR + fname)
            new = new.convert("RGBA")
            old = Image.blend(new, old, 0.5)

        old2 = Image.open(DIR + files[-1])
        old2 = old2.convert("RGBA")

        for i in range(1, len(files), -1):
            new = Image.open(DIR + files[i])
            new = new.convert("RGBA")
            old2 = Image.blend(new, old2, 0.5)


        res_name = self.get_basic_name()
        res = {res_name : res_name + ".png"}
        result = Image.blend(old, old2, 0.5)
        result.save(Datas.get_res_path() + self.get_basic_name() + ".png", "PNG")
        result.show()
        return res

    def clear_png_dir(self, DIR):
        for f in os.listdir(DIR):
            filename, file_ext = os.path.splitext(f)
            if file_ext == ".png":
                os.unlink(DIR + f)

    # heatmap core function
    def __display_heatmaps(self, activations, o_name):
        plot_dir = Datas.get_static_path() + "heat_plots/"

        self.clear_png_dir(plot_dir)
        for layer_name, acts in activations.items():
            if acts.shape[0] != 1:
                print('-> Skipped. First dimension is not 1.')
                continue
            if len(acts.shape) <= 2:
                print('-> Skipped. 2D Activations.')
                continue
            print('')

        img = self.datas.img
        layer_name = self.datas.get_layer_name()
        scaler = MinMaxScaler()
        scaler.fit(acts.reshape(-1, 1))
        for i  in range(len(activations)):
            img = acts[0, :, :, i]
            # scale the activations (which will form our heat map) to be in range 0-1
            img = scaler.transform(img)
            # resize heatmap to be same dimensions of image
            img = Image.fromarray(img)
            #img = img.resize((image.shape[0], image.shape[1]), Image.BILINEAR)
            img = np.array(img)
            plt.imshow(img)
            # overlay a 70% transparent heat map onto the image
            # Lowest activations are dark, highest are dark red, mid are yellow
            plt.imshow(img, alpha=0.3, cmap='jet', interpolation='bilinear')
            plt.savefig(plot_dir + layer_name.split('/')[0] + '_'  + str(i) + '.png', bbox_inches='tight')

        return self.__overlap(plot_dir, layer_name.split('/')[0], o_name)



    # The main method that runs the visualization
    def run(self):
        model = self.datas.model
        image = self.datas.img
        layer_name = self.datas.get_layer_name()
        activations = self.get_activations(model, image, l_name = layer_name)

        return self.__display_heatmaps(activations, self.datas.img_name)

