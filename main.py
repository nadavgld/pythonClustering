from Tkinter import Tk, Label, Button, Entry, END, W, E
import tkMessageBox
from tkFileDialog import askopenfilename
import pandas as pd
import xlrd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import numpy as np


class Clustering:

    def __init__(self, master):

        self.filename = ""
        self.hasPre = False
        self.rawData = ""
        self.nClust = -1
        self.nRuns = -1
        self.master = master
        master.title("K Means Clustering")

        self.label = Label(master, text="")
        self.label.pack()

        self.entry = Entry(master)
        self.entry.pack()
        self.browseBtn = Button(master, text="Browse", command=self.browseFile)

        vcmd = master.register(self.validate)

        self.clustersNum = Entry(master, validate="key", validatecommand=(vcmd, '%P'))
        self.clusterNumLabel = Label(master, text="Num of clusters k")

        self.clustersRun = Entry(master, validate="key", validatecommand=(vcmd, '%P'))
        self.clustersRunLabel = Label(master, text="Num of runs")

        self.preProcessBtn = Button(master, text="Pre-Process", command=lambda: self.preProcessing())
        self.clusterBtn = Button(master, text="Cluster", command=lambda: self.clustering())

        # LAYOUT

        self.label.grid(row=0, column=0, sticky=W)
        self.label.grid(row=1, column=0, sticky=W)
        self.label.grid(row=2, column=0, sticky=W)
        self.label.grid(row=3, column=0, sticky=W)

        self.entry.grid(row=4, column=11, columnspan=5, sticky=W + E)
        self.browseBtn.grid(row=4, column=2, columnspan=3, sticky=W + E)

        self.clustersNum.grid(row=7, column=9, columnspan=3, sticky=W + E)
        self.clusterNumLabel.grid(row=7, column=2, columnspan=3, sticky=W)

        self.clustersRun.grid(row=10, column=9, columnspan=3, sticky=W + E)
        self.clustersRunLabel.grid(row=10, column=2, columnspan=3, sticky=W)

        self.preProcessBtn.grid(row=13, column=2, columnspan=3)
        self.clusterBtn.grid(row=13, column=11, columnspan=3)

    def browseFile(self):

        Tk().withdraw()
        self.filename = askopenfilename()
        self.entry.delete(0, END)
        self.entry.insert(0, self.filename)

    def validate(self, new_text):
        if not new_text:
            self.entered_number = 0
            return True

        try:
            self.entered_number = int(new_text)
            return True
        except ValueError:
            return False

    def preProcessing(self):
        if not self.filename:
            tkMessageBox.showerror("K Means Clustering", "Please choose file before..")
        else:
            self.rawData = pd.ExcelFile(self.filename)
            self.df = (self.rawData.parse("Data behind Table 2.1 WHR 2017", header=0))

            numeric_data = self.df.iloc[:, 2:]
            string_data = self.df.iloc[:, 0:1]

            fillNA = numeric_data.apply(lambda x: x.fillna(x.mean()), axis=0)
            standard = StandardScaler().fit(fillNA).transform(fillNA)
            standard = pd.DataFrame(standard, columns=numeric_data.columns)

            afterClean = pd.concat([string_data, standard], axis=1)

            self.complete_ready_data = afterClean.groupby(by=afterClean['country'], axis=0).mean()
            self.hasPre = True
            tkMessageBox.showinfo("K Means Clustering", "Preprocessing completed successfully!")

    def clustering(self):
        self.nClust = self.clustersNum.get()
        self.nRuns = self.clustersRun.get()
        if not self.hasPre:
            tkMessageBox.showerror("K Means Clustering", "Please preprocess data before..")
        elif self.nClust == "" or self.nClust <= 0:
            tkMessageBox.showerror("K Means Clustering", "Please fill positive number of clusters")
        elif self.nRuns == "" or self.nRuns <= 0:
            tkMessageBox.showerror("K Means Clustering", "Please fill positive number of runs")
        else:
            model = KMeans(n_clusters=int(self.nClust), n_init=int(self.nRuns)).fit(self.complete_ready_data)

            self.complete_ready_data['Clustering'] = model.labels_
            print self.complete_ready_data
            print "guy guy"

root = Tk()
root.geometry("900x580")
my_gui = Clustering(root)
root.mainloop()
