import sys
from Tkinter import Tk, Label, Button, Entry, END, W, E, Canvas, PhotoImage
import tkMessageBox
from tkFileDialog import askopenfilename
from sklearn.cluster import KMeans
import cleanData
import numpy as np
import matplotlib
# from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from PIL import ImageTk, Image
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
import plotly.plotly as py

py.sign_in('zaksg', 'n3lh0HSHhO2wjFtFsA9Y')


# GUI Class - Clustering
class Clustering:

    def selectAll(self, event):
        event.widget.delete(0, END)

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

        self.entry = Entry(master, state='disabled')
        self.entry.pack()
        self.browseBtn = Button(master, text="Browse", command=self.browseFile)

        vcmd = master.register(self.validate)

        self.clustersNum = Entry(master, validate="key", validatecommand=(vcmd, '%P'))
        self.clusterNumLabel = Label(master, text="Num of clusters k")
        self.clustersNum.bind('<Button-1>', self.selectAll)
        self.clustersNum.bind('<FocusIn>', self.selectAll)
        self.clustersNum.pack()

        self.clustersRun = Entry(master, validate="key", validatecommand=(vcmd, '%P'))
        self.clustersRunLabel = Label(master, text="Num of runs")
        self.clustersRun.bind('<Button-1>', self.selectAll)
        self.clustersRun.bind('<FocusIn>', self.selectAll)
        self.clustersRun.pack()

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
        self.entry.config(state='normal')
        self.entry.delete(0, END)
        self.entry.insert(0, self.filename)
        self.entry.config(state='disabled')

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
            donePre, self.complete_ready_data = cleanData.clean(self.filename)

            if not donePre:
                tkMessageBox.showerror("K Means Clustering", "Could not preprocess selected file")
            else:
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

            model = KMeans(n_clusters=int(self.nClust), n_init=int(self.nRuns)).fit(
                self.complete_ready_data.iloc[:, 1:])
            self.complete_ready_data['Clustering'] = model.labels_

            # Generate scatter plot & show on GUI
            fig = Figure(figsize=(6, 6), dpi=70)
            a = fig.add_subplot(111)
            a.scatter(x=self.complete_ready_data["Generosity"], y=self.complete_ready_data["Social support"],
                      c=self.complete_ready_data['Clustering'])
            a.set_title("Scatter plot for Generosity and Social support by cluster")
            a.set_xlabel('Generosity', fontsize=12)
            a.set_ylabel('Social support', fontsize=12)

            canvas = matplotlib.backends.backend_tkagg.FigureCanvasTkAgg(fig, master=self.window)
            canvas.get_tk_widget().grid(row=17, column=18)
            canvas.draw()

            # Generate second plot - Horopleth map & save to disk & show on GUI
            self.complete_ready_data.reset_index(inplace=True)
            # scl = [[0.0, 'rgb(242,240,247)'], [0.2, 'rgb(218,218,235)'], [0.4, 'rgb(188,189,220)'], \
            #        [0.6, 'rgb(158,154,200)'], [0.8, 'rgb(117,107,177)'], [1.0, 'rgb(84,39,143)']]
            scl = [[0.0, 'rgb(242,240,247)'], [0.4, 'rgb(188,189,220)'], [0.8, 'rgb(117,107,177)']]
            data = [dict(
                type='choropleth',
                colorscale=scl,
                autocolorscale=False,
                locations=self.complete_ready_data['country'],
                z=self.complete_ready_data['Clustering'].astype(float),
                locationmode='country names',
                text=self.complete_ready_data['country'],
                marker=dict(
                    line=dict(
                        color='rgb(255,255,255)',
                        width=2
                    )),
                colorbar=dict(
                    title="Cluster",
                    dtick = 1)
            )]

            layout = dict(
                title='Cluster by country on world map',
                geo=dict(
                    scope='world',
                    projection=dict(type='Mercator'),
                    showlakes=True,
                    lakecolor='rgb(255, 255, 255)'),
            )

            fig2 = dict(data=data, layout=layout)
            py.plot(fig2, filename='d3-cloropleth-map', auto_open=False)
            py.image.save_as(fig2, filename="world.png")

            im = Image.open('world.png')
            im = im.resize((520, 420), Image.ANTIALIAS)
            im = im.convert('RGB').convert('P', palette=Image.ADAPTIVE)
            im.save('world.gif')

            photo = PhotoImage(file='world.gif')
            photo.zoom(2)
            self.worldImg = Label(master=self.window, image=photo)
            self.worldImg.image = photo
            self.worldImg.grid(row=17, column=19)

            if tkMessageBox.askokcancel("K Means Clustering", "Clustering completed successfully!"):
                root.destroy()
                sys.exit()


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
