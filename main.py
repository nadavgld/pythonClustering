from Tkinter import Tk, Label, Button, Entry, END, W, E, Canvas
import tkMessageBox
from tkFileDialog import askopenfilename
from sklearn.cluster import KMeans
import cleanData
import numpy as np
import matplotlib
# from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

matplotlib.use("TkAgg")
import matplotlib.pyplot as plt


# GUI Class - Clustering
class Clustering:

    # Class initialize and function definition
    def __init__(self, master):

        # In-class variables
        self.window = master
        self.filename = ""
        self.hasPre = False
        self.rawData = ""
        self.nClust = -1
        self.nRuns = -1
        self.master = master
        master.title("K Means Clustering")

        # Buttons, Entries & Labels setup
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

        self.preProcessBtn = Button(master, text="Pre-Process", command=lambda: self.preprocessing())
        self.clusterBtn = Button(master, text="Cluster", command=lambda: self.clustering())

        # LAYOUT

        self.label.grid(row=0, column=0, sticky=W)
        self.label.grid(row=1, column=0, sticky=W)
        self.label.grid(row=2, column=0, sticky=W)
        self.label.grid(row=3, column=0, sticky=W)
        self.label.grid(row=14, column=0, sticky=W)
        self.label.grid(row=15, column=0, sticky=W)

        self.entry.grid(row=4, column=11, columnspan=5, sticky=W + E)
        self.browseBtn.grid(row=4, column=2, columnspan=3, sticky=W + E)

        self.clustersNum.grid(row=7, column=9, columnspan=3, sticky=W + E)
        self.clusterNumLabel.grid(row=7, column=2, columnspan=3, sticky=W)

        self.clustersRun.grid(row=10, column=9, columnspan=3, sticky=W + E)
        self.clustersRunLabel.grid(row=10, column=2, columnspan=3, sticky=W)

        self.preProcessBtn.grid(row=13, column=2, columnspan=3)
        self.clusterBtn.grid(row=13, column=11, columnspan=3)

    # Browse file function - saves filename to self.filename
    def browseFile(self):

        Tk().withdraw()
        self.filename = askopenfilename()
        self.entry.delete(0, END)
        self.entry.insert(0, self.filename)

    # Validate function - checks that the entries will get only numbers
    def validate(self, new_text):
        if not new_text:
            self.entered_number = 0
            return True

        try:
            self.entered_number = int(new_text)
            return True
        except ValueError:
            return False

    # Preprocessing the data using StandardScaler
    def preprocessing(self):
        if not self.filename:
            tkMessageBox.showerror("K Means Clustering", "Please choose file before..")
        else:
            self.complete_ready_data = cleanData.clean(self.filename)
            self.hasPre = True
            tkMessageBox.showinfo("K Means Clustering", "Preprocessing completed successfully!")

    # Clustering the data using KMeans clustering
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

            # Generate scatter plot
            fig = Figure(figsize=(6, 6),dpi=70)
            a = fig.add_subplot(111)
            a.scatter(x=self.complete_ready_data["Generosity"], y=self.complete_ready_data["Social support"],
                               c=self.complete_ready_data['Clustering'])
            a.set_xlabel('Generosity', fontsize=16)
            a.set_ylabel('Social support', fontsize=16)

            # Generate second plot
            fig2 = Figure(figsize=(6, 6),dpi=70)
            b = fig2.add_subplot(111)
            b.scatter(x=self.complete_ready_data["Social support"], y=self.complete_ready_data["Social support"],
                               c=self.complete_ready_data['Clustering'])
            b.set_xlabel('Social support', fontsize=16)
            b.set_ylabel('Social support', fontsize=16)

            canvas = matplotlib.backends.backend_tkagg.FigureCanvasTkAgg(fig, master=self.window)
            canvas.get_tk_widget().grid(row=17,column=70)
            canvas.draw()

            canvas2 = matplotlib.backends.backend_tkagg.FigureCanvasTkAgg(fig2, master=self.window)
            canvas2.get_tk_widget().grid(row=17,column=150)
            canvas2.draw()


# Placing window in the center of the screen
def center(win):
    win.update_idletasks()
    width = 1200
    height = 600
    x = (win.winfo_screenwidth() // 2) - (width // 2)
    y = (win.winfo_screenheight() // 2) - (height // 2)
    win.geometry('{}x{}+{}+{}'.format(width, height, x, y))


# Opens the GUI
root = Tk()
center(root)
Clustering(root)
root.mainloop()
