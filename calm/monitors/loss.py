'''
    calm.mon.loss.py
    jason corso

    MMonitors the loss during a caffe training and plots it incrementally

    Expects caffe to be maintaining a .INFO file in /tmp

    Starts up by loading what is in /tmp/caffe.INFO

    Requires watchdog and wxpython
'''

import sys
import os.path
import time
import argparse
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


            self.app.update(event.src_path)


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
        if self.app.monitortest:
            self.axes.plot(self.app.testiter,self.app.testloss,color="green")
        self.canvas.draw()
        self.canvas.Refresh()


class LossMonitor(wx.App):
    def __init__(self, redirect=False, filename=None, monitortest=False):
        wx.App.__init__(self, redirect, filename)
        #self.kSize = 480
        self.iter = np.zeros([10,1]) #np.asarray(range(10))
        self.loss = np.zeros([10,1]) #np.random.randint(0,100,[10,1])
        self.testiter = np.zeros([10,1]) #np.asarray(range(10))
        self.testloss = np.zeros([10,1]) #np.random.randint(0,100,[10,1])
        self.monitortest = monitortest

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
        wx.App.__del__(self)
        self.observer.stop()
        self.observer.join()

    def update(self,path):

        f = open(path,'r')
        s = f.read()
        f.close()
        pattern = re.compile(r'Iteration (\d+), loss = (\d+.\d+)')
        grou = np.asarray(pattern.findall(s)).astype(np.float32)

        self.iter = grou[:,0]
        self.loss = grou[:,1]

        print "min loss is %f"%(np.min(self.loss))
        print "max loss is %f"%(np.max(self.loss))
        print "mean loss is %f"%(np.mean(self.loss))
        print "median loss is %f"%(np.median(self.loss))

        if self.monitortest:
            t1pat = re.compile(r'Iteration (\d+), Testing net')
            t1gro = np.asarray(t1pat.findall(s)).astype(np.float32)

            t2pat = re.compile(r'Test loss: (\d+.\d+)')
            t2gro = np.asarray(t2pat.findall(s)).astype(np.float32)

            self.testiter = t1gro
            self.testloss = t2gro
            if (self.testloss.size == 0) or (self.testiter.size == 0):
                print "no test loss present in the log even though you said to monitor it\n Turning off test loss monitoring"
                self.monitortest = False

        if self.monitortest:
            print "test min loss is %f"%(np.min(self.testloss))
            print "test max loss is %f"%(np.max(self.testloss))
            print "test mean loss is %f"%(np.mean(self.testloss))
            print "test median loss is %f"%(np.median(self.testloss))

        self.panel.draw()
        self.panel.Refresh()

def main():
    parser = argparse.ArgumentParser(description='Short sample app')
    parser.add_argument('--monitor-test', dest='monitortest', action='store_true', help='Monitor Test Loss')
    parser.add_argument('--no-monitor-test', dest='monitortest', action='store_false')
    parser.set_defaults(monitortest=False)
    args = parser.parse_args()

    app = LossMonitor(monitortest = args.monitortest)
    app.update('/tmp/caffe.INFO')
    app.MainLoop()


if __name__ == '__main__':
    main()


