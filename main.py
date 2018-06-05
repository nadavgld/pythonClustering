from Tkinter import Tk, Label, Button, Entry, IntVar, END, W, E
import tkFileDialog

class Calculator:

    def __init__(self, master):
        self.master = master
        master.title("Python Clustering")

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

        self.entry.grid(row=4, column=11, columnspan=5, sticky=W+E)
        self.browseBtn.grid(row=4, column=2, columnspan=3, sticky=W+E)

        self.clustersNum.grid(row=7, column=9, columnspan=3, sticky=W+E)
        self.clusterNumLabel.grid(row=7, column=2, columnspan=3, sticky=W)

        self.clustersRun.grid(row=10, column=9, columnspan=3, sticky=W + E)
        self.clustersRunLabel.grid(row=10, column=2, columnspan=3, sticky=W)

        self.preProcessBtn.grid(row=13, column=2, columnspan=3)
        self.clusterBtn.grid(row=13, column=11, columnspan=3)

    def browseFile(self):
        from tkFileDialog import askopenfilename

        Tk().withdraw()
        self.filename = askopenfilename()
        self.entry.delete(0,END)
        self.entry.insert(0,self.filename)

    def validate(self, new_text):
        if not new_text: # the field is being cleared
            self.entered_number = 0
            return True

        try:
            self.entered_number = int(new_text)
            return True
        except ValueError:
            return False

    def preProcessing(self):
        print 1

    def clustering(self):
        print 2

    # def update(self, method):
    #     if method == "add":
    #         self.total += self.entered_number
    #     elif method == "subtract":
    #         self.total -= self.entered_number
    #     else: # reset
    #         self.total = 0
    #
    #     self.total_label_text.set(self.total)
    #     self.entry.delete(0, END)

root = Tk()
root.geometry("270x180")
my_gui = Calculator(root)
root.mainloop()