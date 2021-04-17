# Path annotation tool
#
#
# Helps to define the segments of the path, where the center of the package should pass.
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import collections  as mc
import numpy as np
import json
from absl import flags
from absl import app
########################

FLAGS = flags.FLAGS
flags.DEFINE_string('image_path', None, 'Path to image')
flags.DEFINE_string('output_path', None, 'Output path to json')

#####################

class LineBuilder:
    def __init__(self, path_to_img, output_path):
        self.path_to_img = path_to_img
        self.output_path = output_path
        self.fig, self.ax = plt.subplots()
        self.base_img = plt.imread(self.path_to_img)
        self.ax.imshow(self.base_img)
        self.line, = self.ax.plot([0], [0], 'o', picker=5)  # empty line
        self.xs = list(self.line.get_xdata())
        self.ys = list(self.line.get_ydata())
        self.cid = self.line.figure.canvas.mpl_connect('button_press_event', self.on_point)
        self.cm = self.line.figure.canvas.mpl_connect('key_press_event', self.change_mode)
        self.crm = self.line.figure.canvas.mpl_connect('pick_event', self.on_pick)
        self.add_point = True
        self.dict_title ={True:'Add points \n (remove press c; path mode press x)',
                         False: 'Remove points \n (add press c; path mode press x)'}
        
        self.ax.set_title(self.dict_title[self.add_point])
        self.n_points=0
        self.point_mode=True
        self.lines = []
        self.lines_ind = []
        self.temp_ini_point = None
        self.segment_collection = []
        plt.show()

    def on_point(self, event):
        if event.inaxes!=self.line.axes: return
        if self.add_point and self.point_mode:            
            if self.n_points == 0:
                self.xs=[event.xdata]
                self.ys=[event.ydata]
            else:
                self.xs.append(event.xdata)
                self.ys.append(event.ydata)
            self.n_points += 1
            self.line.set_data(self.xs, self.ys)
            self.line.figure.canvas.draw()


    def on_pick(self,event):
        line = event.artist
        inds = event.ind
        if not self.add_point and self.point_mode:
            for ind in inds:
                self.xs.pop(ind)
                self.ys.pop(ind)
            self.lines = []
            self.lines_ind = []
            self.temp_ini_point = None
            self.remove_collection()
            #self.segment_collection = self.ax.add_collection(self.segment_collection)    
        elif not self.point_mode:
            if self.temp_ini_point is None:
                self.temp_ini_point = int(inds[0])
            else:
                self.lines += [[(self.xs[self.temp_ini_point], self.ys[self.temp_ini_point ]),
                                (self.xs[inds[0]], self.ys[inds[0]])]]
                self.lines_ind += [(self.temp_ini_point, int(inds[0]))]
                self.temp_ini_point = None
                if len(self.segment_collection)>0:
                    self.remove_collection()
                self.segment_collection += [self.ax.add_collection(mc.LineCollection(self.lines, linewidths=2))]
        self.line.set_data(self.xs, self.ys)
        self.line.figure.canvas.draw()
                
    def remove_collection(self):
        #for i in range(len(self.lines)):
        self.ax.collections = [] 
        self.segment_collection = []
        self.line.set_data(self.xs, self.ys)
        self.line.figure.canvas.draw()
    def change_mode(self, event):
        ###Danger zone: some keys are also quick controls for the plot in jupyter and they can interact in a non desirable way...
        if event.key == 'c':
            self.add_point = not self.add_point
            self.ax.set_title(self.dict_title[self.add_point])
        elif event.key == 'x':
            self.point_mode = not self.point_mode
            if not self.point_mode:
                self.ax.set_title('path mode (point mode press x)')
            else:
                self.add_point = True
                self.ax.set_title(self.dict_title[self.add_point])
        elif event.key == 'g':
            json_data = json.dumps({'x':self.xs,
                "y":self.ys,
                "segments": self.lines_ind,
                "height": int(self.base_img.shape[0]),
                "width": int(self.base_img.shape[1])})
            with open(self.output_path, 'w') as file:
                file.write(json_data)
            plt.close()

        self.line.figure.canvas.draw()





def main(argv):
    flags.mark_flag_as_required('image_path')
    flags.mark_flag_as_required('output_path')
    LineBuilder(FLAGS.image_path, FLAGS.output_path)


if __name__ == '__main__':
    app.run(main)
       
