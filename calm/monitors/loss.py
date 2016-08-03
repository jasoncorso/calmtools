'''
    calm.mon.monloss.py
    jason corso

    MMonitors the loss during a caffe training and plots it incrementally

    Expects caffe to be maintaining a .INFO file in /tmp

    Requires watchdog and wxpython
'''

import sys
import os.path
import time
import re
import numpy as np
import wx
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, FileModifiedEvent

import matplotlib as mpl
mpl.use('WxAgg')
import matplotlib.backends.backend_wxagg
import matplotlib.figure

class UpdateEvent(FileSystemEventHandler):
    def __init__(self,lossmonitorapp):
        self.app = lossmonitorapp

    def on_modified(self, event):
        if isinstance(event,FileModifiedEvent) and event.src_path.startswith('/tmp/caffe') \
                                               and event.src_path.find('.INFO') != -1:
            print "log %s updated" %(event.src_path)

            f = open(event.src_path,'r')
            s = f.read()
            f.close()
            pattern = re.compile(r'Iteration (\d+), loss = (\d+.\d+)')
            grou = np.asarray(pattern.findall(s)).astype(np.float32)
            self.app.iter = grou[:,0]
            self.app.loss = grou[:,1]

            print "min loss is %f"%(np.min(self.app.loss))
            print "max loss is %f"%(np.max(self.app.loss))
            print "mean loss is %f"%(np.mean(self.app.loss))
            print "median loss is %f"%(np.median(self.app.loss))

            self.app.update()
            print self.app.jname


class MatplotlibPanel(wx.Panel):
    def __init__(self, parent, app):
        wx.Panel.__init__(self, parent)

        # assign app so we can access the data to plot
        self.app = app

        self.figure = mpl.figure.Figure()
        self.axes = self.figure.add_subplot(111)
        self.canvas = mpl.backends.backend_wxagg.FigureCanvasWxAgg(self, -1, self.figure)
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.canvas, 1, wx.LEFT | wx.TOP | wx.GROW)
        self.SetSizer(self.sizer)
        self.Fit()

    def draw(self):
        print "MatplotlibPanel draw"
        print "min loss is %f"%(np.min(self.app.loss))
        self.axes.clear()
        self.axes.plot(self.app.iter,self.app.loss)
        self.canvas.draw()
        self.canvas.Refresh()


class LossMonitor(wx.App):
    def __init__(self, redirect=False, filename=None):
        wx.App.__init__(self, redirect, filename)
        #self.kSize = 480
        self.iter = np.zeros([10,1]) #np.asarray(range(10))
        self.loss = np.zeros([10,1]) #np.random.randint(0,100,[10,1])

        self.jname = "Caffe Loss Monitor"
        self.frame = wx.Frame(None, title=self.jname)
        self.panel = MatplotlibPanel(self.frame,self)
        self.panel.draw()
        self.frame.Show()

        # create the file system watchdog
        self.event_handler = UpdateEvent(self)
        self.observer = Observer()
        self.observer.schedule(self.event_handler, "/tmp", recursive=False)
        self.observer.start()

    def __del__(self):
        self.observer.stop()
        self.observer.join()

    def update(self):
        self.panel.draw()
        self.panel.Refresh()

def main():
    app = LossMonitor()
    app.MainLoop()


if __name__ == '__main__':
    main()


