from FilterMax import *
from FilterVis import *
from HeatMap import *
from Archi import *
STRING = ''
class Manager:
    """
    Manager system for client requests, each change in the front end is interpretated as a new commande to execute, the communication is done through out a string wich contains all the updated informations as following :
    str = 'vt,mn,t_im,l_n,plot_a,plot_fn,n,plot_l,{1.5.6},act_indx,keep_g'
    where : 
        #         vt is an integer showing the vis type,
        #         mn is the model path
        #         t_im is the test image path
        #         l_n is the layer name
        #         plot_a is an integer indicating if we'll plot all filters
        #         plot_fn is an integer indicating if we'll plot only the first n filters
        #         n is an integer indicating the number of the first filters
        #         plot_l is an integer idicating if we'll plot a list of filters
        #         {x, y..} the list of the filters index
        #         act_indx is the layer's index for the FilterVis visualization
        #         keep_g (1 or 0) : for the Manager to know if the app is still runing

    attr : 
    __keep_goin ; 0 or 1, telling the Manager when to stop waiting for new commandes
    __change_model ; 0 or 1, telling the Manager when to clear the session for a new one
    """
    class Response:
        """
        a helpful class to divise the commande string
        ------------------------------------------------
        """
        def __init__(self, string):
            self.__feed_dict = {'vis_type': 0,
                                'model_name': 1,
                                'test_image': 2,
                                'layer_name': 3,
                                'plot_all': 4,
                                'plot_firstn': 5,
                                'n': 6,
                                'plot_list': 7,
                                'plotting_list': 8,
                                'act_index': 9}
            self.__string = string
            
            
        # Utility method that returns the corresponding information
        def get(self, string):
            return self.__string.split(';')[self.__feed_dict[string]]

        
        """
        -----------------------------------------------------
        """


    def __init__(self):
        self.__keep_going = 1
        self.__change_model = 0

    # this method gets the new commande from the server encoded in a string
    # TODO PROPERLY !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    def __get_coded_string(self, change_after = -1):
        string = STRING#"3;VGG16;test.jpg;block1_conv1;-1;1;2;-1;[1,2,3];2;1"
        if string.split(';')[-1] == 0:
            self.__keep_going = 0
        
        return string
        
    # check if the current commande 'string' is the same as the one sent by the server
    def __check_for_change(self, string):
        if (string == self.__get_coded_string()):
            return False
        else:
            if (string.split(";")[1] != self.__get_coded_string().split(";")[1]):
                self.__change_model = 1
            return True
         


        
    # runs a session with the proper visualization and parameters
    def __run_session(self, code_string):
        res = self.Response(code_string)
        if res.get('vis_type') == str(0) : # FilterVis
            core = FilterVis(model_n = res.get('model_name'),
                             layer_n = res.get('layer_name'),
                             act_index = res.get('act_index'),
                             test_im = res.get('test_image'))
            core.run()
            print('FilterVis executed successufely')
        if res.get('vis_type') == str(1) : # FilterMax
            core = FilterMax(plot_all = res.get('plot_all'),
                             plot_firstn = res.get('plot_firstn'),
                             n = res.get('n'),
                             plot_list = res.get('plot_list'),
                             plotting_list = res.get('plotting_list'),
                             model_n = res.get('model_name'))
            core.run()
            print('FilterMax executed successufely')
        print('res.get = {}'.format(res.get('vis_type')))
        c = res.get('vis_type')
        if res.get('vis_type') == str(2) :
            print('executing Heatmap on the model' + res.get('model_name') + '/' + res.get('layer_name') + 'with the test image : ' + res.get('test_image'))
            core = HeatMap(res.get('model_name'),
                           res.get('test_image'),
                           res.get('layer_name'))
            core.run()
            print('HeatMap executed successufely')
        if res.get('vis_type') == str(3) : # Archi
            print('executing Archi on the model' + res.get('model_name') + '/' + res.get('layer_name') + 'with the test image : ' + res.get('test_image'))
            core = Archi(res.get('model_name'))
            core.run()
    """
    # m = Manager(); m["net-name"] = "VGG16"
    def __setitem__(self, key, value):
        if key == "net-name":
            self.__change_model = 1"""


    def main(self):
        # ingoring Tensorflow warrnings
        os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

        # recovering the current commande to execute
        commande = self.__get_coded_string()

        # executing a session of visualization with the proper parameters
        self.__run_session(commande)
        
        # while the user is still using the application
        while (self.__keep_going == 1):
            # waiting for the current commande to change / for the app to shutdown
            while(not self.__check_for_change(commande) and self.__keep_going == 1):
                # updating the commande variable
                commande = self.__get_coded_string()
            # if the commande has changed
            if self.__keep_going == 1:
                # if the model needs to be changed, clear the session
                if self.__change_model == 1:
                    K.clear_session()
                # execute the new commande
                self.__run_session(self.__get_coded_string())
            


if __name__ == '__main__':
    class Foo:
        def __init__(self):
            self.bar = 0
        
        def truc(self, key, value):
            if key == "bar":
                self.bar = value

        def __setitem__(self, key, value):
            self.truc(key, value)

        def __repr__(self):
            return str(self.bar)

        __str__ = __repr__
    """manager = Manager()
    manager.main()"""
    foo = Foo()
    print(foo)
    foo.truc("bar", 50)
    print(foo)
    foo["bar"] = 53
    print(foo)
    
    exit(0)


