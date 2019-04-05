from Visualization import *

class FilterMax(Visualization):


    def __init__(self,
                 datas : Datas,
                 plot_all = -1, #plotting all filters of all layers
                 plot_firstn = -1, # set to no as default
                 n = -1, # is plot_alln != 1 this one is ignored
                 plot_list = -1, # set to no as default
                 plotting_list = None, # if plot_list != 1 this one is ignored
                 upscaling_steps = 9,
                 upscaling_factor = 5.2,
                 output_dim = (412, 412)):
        """
        Initialize the visualisation
        Priority :
        if 
        #Arguments:
        datas : countain the model, the layer_id
        plot_all : if 1 then need to compute filterMax for all filters
        plot_firstn : if 1 then need to compute filterMax for only n first filters
        n : if plot_firstn = 1 then represents the number of filter the algorithm has to be computed on
        plot_list : if 1 then need to compute filterMax for a sublist of filters
        plotting_list : if plot_list = 1 then represents the sublist the algorithm has to be computed on
        #Return:
        The visualization initialized
        """
        
        super(FilterMax, self).__init__(datas)
        self.__plot_all = plot_all
        self.__plot_firstn = plot_firstn
        self.__n = n
        self.__plot_list = plot_list
        self.__plotting_list = plotting_list
        self.__upscaling_steps = upscaling_steps
        self.__upscaling_factor = upscaling_factor
        self.__output_dim = output_dim
                 
                 



    #Generates image for one particular filter.
    def __generate_filter_image(self,
                              input_img,
                              layer_output,
                              filter_index,
                              step=1.,
                              epochs=15,
                              upscaling_steps=9,
                              upscaling_factor=1.2,
                              output_dim=(412, 412),
                              filter_range=(0, None)):
        """
        # Arguments
        input_img: The input-image Tensor.
        layer_output: The output-image Tensor.
        filter_index: The to be processed filter number.
                        Assumed to be valid.
        #Returns
        Either None if no image could be generated.
        or a tuple of the image (array) itself and the last loss.
        """

        s_time = time.time()

        with self.datas.graph.as_default():
            # we build a loss function that maximizes the activation
            # of the nth filter of the layer considered
            if K.image_data_format() == 'channels_first':
                loss = K.mean(layer_output[:, filter_index, :, :])
            else:
                loss = K.mean(layer_output[:, :, :, filter_index])

            # we compute the gradient of the input picture wrt this loss
            grads = K.gradients(loss, input_img)[0]
        
            # normalization trick: we normalize the gradient
            grads = self.normalize(grads)

            # this function returns the loss and grads given the input picture
            iterate = K.function([input_img], [loss, grads])

            # we start from a gray image with some random noise
            intermediate_dim = tuple(
                int(x / (upscaling_factor ** upscaling_steps)) for x in output_dim)
            if K.image_data_format() == 'channels_first':
                input_img_data = np.random.random(
                    (1, 3, intermediate_dim[0], intermediate_dim[1]))
            else:
                input_img_data = np.random.random(
                    (1, intermediate_dim[0], intermediate_dim[1], 3))
            input_img_data = (input_img_data - 0.5) * 20 + 128

            # Slowly upscaling towards the original size prevents
            # a dominating high-frequency of the to visualized structure
            # as it would occur if we directly compute the 412d-image.
            # Behaves as a better starting point for each following dimension
            # and therefore avoids poor local minima
            for up in reversed(range(upscaling_steps)):
                # we run gradient ascent for e.g. 20 steps
                for _ in range(epochs):
                    loss_value, grads_value = iterate([input_img_data])
                    input_img_data += grads_value * step

                # some filters get stuck to 0, we can skip them
                if loss_value <= K.epsilon():
                    return None

            # Calulate upscaled dimension
            intermediate_dim = tuple(
                int(x / (upscaling_factor ** up)) for x in output_dim)
            # Upscale
            img = self.deprocess_image(input_img_data[0])
            img = np.array(pil_image.fromarray(img).resize(intermediate_dim,
                                                            pil_image.BICUBIC))
            input_img_data = [self.process_image(img, input_img_data[0])]

            # decode the resulting input image
            img = self.deprocess_image(input_img_data[0])
            e_time = time.time()
            print('Costs of filter {:3}: {:5.0f} ( {:4.2f}s )'.format(filter_index,
                                                                        loss_value,
                                                                        e_time - s_time))

            return img, loss_value, e_time - s_time






    def __draw_filters(self,
                     filters,
                     layer_name,
                     count,
                     n=None,
                     step=1.,
                     epochs=15,
                     upscaling_steps=9,
                     upscaling_factor=1.2,
                     output_dim=(412, 412),
                     filter_range=(0, None)):

        """
        Draw the best filters in a nxn grid.
        # Arguments
        filters: A List of generated images and their corresponding losses
                for each processed filter.
        n: dimension of the grid.
            If none, the largest possible square will be used
        layer_name: the name of the layer selected by the user 
        """

        if n is None:
            n = int(np.floor(np.sqrt(len(filters))))
        
        # the filters that have the highest loss are assumed to be better-looking.
        # we will only keep the top n*n filters.
    
        filters.sort(key=lambda x: x[1], reverse=True)
        filters = filters[:n * n]

        # build a black picture with enough space for
        # e.g. our 8 x 8 filters of size 412 x 412, with a 5px margin in between
        MARGIN = 5
        width = n * output_dim[0] + (n - 1) * MARGIN
        height = n * output_dim[1] + (n - 1) * MARGIN
        stitched_filters = np.zeros((width, height, 3), dtype='uint8')

        # fill the picture with our saved filters
        for i in range(n):
            for j in range(n):
                img, _ = filters[i * n + j]
                width_margin = (output_dim[0] + MARGIN) * i
                height_margin = (output_dim[1] + MARGIN) * j
                stitched_filters[
                    width_margin: width_margin + output_dim[0],
                    height_margin: height_margin + output_dim[1], :] = img

        plot_dir = Datas.get_static_path() + "plots/"

        # save the result to disk
        save_img(plot_dir + 'vgg_{0:}_{1:}x{1:}_Filter{2:}.png'.format(layer_name, n, count), stitched_filters)

    def process_layer(self):
        """
        Compute filterMax on filters of the layer_id-th actual model's layer
        #Return:
        A dictionnary `res' which values are filename registered in
        /mysite/mysite/static/mysite/Result
        and for each key x:
        res[x] = x + ".png"
        """
        model = self.datas.model
        l_index = self.datas.layer_id
        model = self.datas.model
        input_img = model.inputs[0]
        res = {}

        plot_dir = Datas.get_static_path() + "plots/"

        # the filter only exists in convolutional layers, so skip the rest
        if (not isinstance(model.layers[l_index], LAYERS.convolutional.Conv2D)):
            print(model.layers[l_index].name + "is not a convolutional layer")
            return

        # printing the current layer we're working on
        print("Working on layer : " + model.layers[l_index].name)

        # creating a directory having the layer's name
        layer_dir = plot_dir + model.layers[l_index].name + "/"
        if not os.path.exists(layer_dir):
            os.mkdir(layer_dir)

        # creating a log file for errors, filter's costs history and execution time
        with open(plot_dir + "fMax_" + model.layers[l_index].name + "_err_cost_history.txt", "a") as f: 

            # to store errors and filter's costs
            errors_index = []
            costs = []

            processed_filters = []

            if self.__plot_all == 1: # if we want to plot all filters of all convolutional layers           
                for f_index in range(len(model.layers[l_index].get_weights()[1])):
                    img_loss = self.__generate_filter_image(input_img, model.layers[l_index].output, f_index)
                    if (img_loss != None):
                        processed_filters.append((img_loss[0],img_loss[1]))
                        self.__draw_filters(processed_filters, model.layers[l_index].name, f_index)
                        costs.append("Costs of filter " + str(f_index) + " : " + str(img_loss[1]) + " (" + str(img_loss[2]) + "s )")
                    else:
                        errors_index.append(f_index)

            elif self.__plot_firstn == 1 and self.__n >= 1: # if we only want to plot the n first filters of each convolutional layer
                for f_index in range(len(model.layers[l_index].get_weights()[1])) :
                    if f_index > self.__n - 1 : break
                    img_loss = self.__generate_filter_image(input_img, model.layers[l_index].output, f_index)
                    if (img_loss != None):
                        processed_filters.append((img_loss[0],img_loss[1]))
                        self.__draw_filters(processed_filters, model.layers[l_index].name, f_index)
                        costs.append("Costs of filter " + str(f_index) + " : " + str(img_loss[1]) + " (" + str(img_loss[2]) + "s )")
                    else:
                        errors_index.append(f_index)
                        
            elif self.__plot_list == 1 and self.__plotting_list != None: # if we only want to plot specified filters of each convolutional layer
                for f_index in self.__plotting_list:
                    img_loss = self.__generate_filter_image(input_img, model.layers[l_index].output, f_index)
                    if (img_loss != None):
                        processed_filters.append((img_loss[0],img_loss[1]))
                        self.__draw_filters(processed_filters, model.layers[l_index].name, f_index)
                        costs.append("Costs of filter " + str(f_index) + " : " + str(img_loss[1]) + " (" + str(img_loss[2]) + "s )")
                    else:
                        errors_index.append(f_index)
                        
            # we move the generated images to there corresponded directories        
            if (len(processed_filters) != 0):
                tomove = [file for file in os.listdir(plot_dir) if os.path.splitext(file)[1] == '.png']
                dirdst = Datas.get_res_path()
                Visualization.clear_dir_ext(dirdst)
                for imgname in tomove:
                    name, ext = os.path.splitext(imgname)
                    shutil.move(plot_dir + imgname, dirdst)
                    res[name] = imgname
                """cmd = "mv plots/vgg* plots/" + model.layers[l_index].name
                os.system(cmd)"""

            # we save errors log
            if (len(errors_index) !=0):
                f.write("Error 102: \ncannot generate images for the following filters of the layer " + model.layers[l_index].name + ":\n")
                f.write(str(errors_index))

            # we save costs and execution time
            if (len(costs) != 0):
                f.write("\n\n##################################\n\nCosts history : \n")
                for i in range(len(costs)):
                    f.write(costs[i] + "\n")
        print (res)
        return res


    # The main method that runs the visualization
    def run(self):
        """
        Run the visualization.
        First clean plot directory.
        Then compute filterMax on appropriate filters. 
        #Return:
        A dictionnary `res' which values are filename registered in
        /mysite/mysite/static/mysite/Result
        and for each key x:
        res[x] = x + ".png"

        Same as 
        """
        plot_dir = Datas.get_static_path() + "plots/"
        if not os.path.exists(plot_dir):
            os.mkdir(plot_dir)
        Visualization.clear_dir_ext(plot_dir, [".png", ".txt"])
        
        return self.process_layer()
