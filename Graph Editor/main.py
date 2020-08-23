from tkinter import *
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('TkAgg')
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

def SaveImage():
    global plt
    plt.savefig('Your_Graph.png')
def Destroy(Main_Window):
    Main_Window.quit()
    Main_Window.quit()

'''
def GetText(canvas, Graph, a, Figure, EdgeList, InputBox, Main_Window, DGraph):
    global Layout_Type, Graph_Type
    NewString = InputBox.get('1.0', END)
    NewList = SliceIntoNumbers(NewString)
    if Graph_Type == 'Undirected':
        if NewList != EdgeList:
            EdgeList = NewList
            canvas.get_tk_widget().forget()
            Graph.clear()
            a.clear()
            for FirstNode, SecondNode in EdgeList:
                Graph.add_edge(FirstNode, SecondNode)
            if Layout_Type == 'Random':
                nx.draw(Graph, ax = a, with_labels = True, font_color = '#ffffff', node_color = '#333333', node_size = 1000, pos = nx.random_layout(Graph))
            if Layout_Type == 'Circular':
                nx.draw(Graph, ax=a, with_labels=True, font_color='#ffffff', node_color='#333333', node_size=1000, pos=nx.circular_layout(Graph))
            if Layout_Type == 'Planar':
                nx.draw(Graph, ax=a, with_labels=True, font_color='#ffffff', node_color='#333333', node_size=1000, pos=nx.planar_layout(Graph))
            if Layout_Type == 'Spring':
                nx.draw(Graph, ax=a, with_labels=True, font_color='#ffffff', node_color='#333333', node_size=1000, pos=nx.spring_layout(Graph))
            Figure.patch.set_facecolor('#4e4e4e')
            canvas = FigureCanvasTkAgg(Figure, master = Main_Window)
            canvas.draw()
            canvas.get_tk_widget().place(x = 244, y = 0)
    else:
        if NewList != EdgeList:
            EdgeList = NewList
            canvas.get_tk_widget().forget()
            DGraph.clear()
            a.clear()
            for FirstNode, SecondNode in EdgeList:
                DGraph.add_edge(FirstNode, SecondNode)
            if Layout_Type == 'Random':
                nx.draw(DGraph, ax = a, with_labels = True, font_color = '#ffffff', node_color = '#333333', node_size = 1000, pos = nx.random_layout(DGraph))
            if Layout_Type == 'Circular':
                nx.draw(DGraph, ax=a, with_labels=True, font_color='#ffffff', node_color='#333333', node_size=1000, pos=nx.circular_layout(DGraph))
            if Layout_Type == 'Planar':
                nx.draw(DGraph, ax=a, with_labels=True, font_color='#ffffff', node_color='#333333', node_size=1000, pos=nx.planar_layout(DGraph))
            if Layout_Type == 'Spring':
                nx.draw(DGraph, ax=a, with_labels=True, font_color='#ffffff', node_color='#333333', node_size=1000, pos=nx.spring_layout(DGraph))
            Figure.patch.set_facecolor('#4e4e4e')
            canvas = FigureCanvasTkAgg(Figure, master = Main_Window)
            canvas.draw()
            canvas.get_tk_widget().place(x = 244, y = 0)'''

def GetText(canvas, Graph, a, Figure, InputBox, Main_Window):
    global Layout_Type, Graph_Type, Weight, EdgeList, Previous_Graph_Type, Previous_Weight, Previous_Layout_Type
    labels = {}
    NewList = []
    lines = InputBox.get('1.0', END).splitlines()

    if Weight == 0:
        for line in lines:
            x, y = line.split()
            NewList.append((x, y))
    else:
        for line in lines:
            x, y, w = line.split()
            NewList.append((x, y, w))

    if Graph_Type == 'Undirected':
        Graph = nx.Graph()
    if Graph_Type == 'Directed':
        Graph = nx.DiGraph()

    if NewList != EdgeList or Previous_Graph_Type != Graph_Type or Previous_Weight != Weight or Previous_Layout_Type != Layout_Type:
        Previous_Graph_Type = Graph_Type
        EdgeList = NewList
        Previous_Weight = Weight
        Layout_Type = Previous_Layout_Type
        canvas.get_tk_widget().place_forget()
        Graph.clear()
        a.clear()
        if Weight == 0:
            Graph.add_edges_from(EdgeList)
        else:
            for x, y, w in EdgeList:
                Graph.add_edge(x, y, weight = w)
            for x, y, data in Graph.edges(data= True):
                labels[(x, y)] = data['weight']

        type = nx.random_layout(Graph)
        if Layout_Type == 'Random':
            type = nx.random_layout(Graph)
        if Layout_Type == 'Circular':
            type = nx.circular_layout(Graph)
        if Layout_Type == 'Planar':
            type = nx.planar_layout(Graph)
        if Layout_Type == 'Spring':
            type = nx.spring_layout(Graph)

        nx.draw_networkx(Graph, ax=a, with_labels=True, font_color='#ffffff', node_color='#333333', node_size=1000, pos=type)
        if Weight == 1:
            nx.draw_networkx_edge_labels(Graph, type, edge_labels = labels, label_pos = 0.5, bbox = dict(facecolor = '#5c5c5c', edgecolor = '#5c5c5c'))

        #nx.draw_networkx_edges(Graph, pos = type)
        Figure.patch.set_facecolor('#4e4e4e')
        canvas = FigureCanvasTkAgg(Figure, master=Main_Window)
        canvas.draw()
        canvas.get_tk_widget().place(x=244, y=0)


def RandomLayout(RandomButton, CircularButton, PlanarButton, SpringButton):
    global Layout_Type
    Layout_Type = 'Random'
    RandomButton.config(bg = '#aeaeae', fg = 'black')
    CircularButton.config(bg = '#5c5c5c', fg = '#a9a9a9')
    PlanarButton.config(bg = '#5c5c5c', fg = '#a9a9a9')
    SpringButton.config(bg = '#5c5c5c', fg = '#a9a9a9')

def CircularLayout(RandomButton, CircularButton, PlanarButton, SpringButton):
    global Layout_Type
    Layout_Type = 'Circular'
    CircularButton.config(bg = '#aeaeae', fg = 'black')
    RandomButton.config(bg='#5c5c5c', fg='#a9a9a9')
    PlanarButton.config(bg='#5c5c5c', fg='#a9a9a9')
    SpringButton.config(bg='#5c5c5c', fg='#a9a9a9')

def PlanarLayout(RandomButton, CircularButton, PlanarButton, SpringButton):
    global Layout_Type
    Layout_Type = 'Planar'
    PlanarButton.config(bg = '#aeaeae', fg = 'black')
    RandomButton.config(bg='#5c5c5c', fg='#a9a9a9')
    CircularButton.config(bg='#5c5c5c', fg='#a9a9a9')
    SpringButton.config(bg='#5c5c5c', fg='#a9a9a9')

def SpringLayout(RandomButton, CircularButton, PlanarButton, SpringButton):
    global Layout_Type
    Layout_Type = 'Spring'
    SpringButton.config(bg = '#aeaeae', fg = 'black')
    RandomButton.config(bg='#5c5c5c', fg='#a9a9a9')
    CircularButton.config(bg='#5c5c5c', fg='#a9a9a9')
    PlanarButton.config(bg='#5c5c5c', fg='#a9a9a9')

def UndirectedGraph():
    global Graph_Type
    Graph_Type = 'Undirected'
def DirectedGraph():
    global Graph_Type
    Graph_Type = 'Directed'
def Weighted():
    global Weight
    Weight = 1
def Unweighted():
    global Weight
    Weight = 0

def Run():
    Window.destroy()
    Main_Window = Tk()
    Main_Window.geometry('1000x600')
    Main_Window.title('Graph')
    Main_Window.configure(bg='#5c5c5c')
    global InputData, PreviousData
    frame = Frame(Main_Window, width=244, height=600, bg='#4e4e4e', bd=0.2)
    frame.place(x=0, y=0)
    EdgeList = []

    Graph = nx.Graph()
    Figure = plt.figure(figsize=(7.57, 6))
    a = Figure.add_subplot(1, 1, 1)
    a.set_facecolor('#5c5c5c')
    Figure.patch.set_facecolor('#4e4e4e')
    plt.axis('off')
    nx.draw_networkx(Graph, pos=nx.spring_layout(Graph), ax=a)
    canvas = FigureCanvasTkAgg(Figure, master=Main_Window)
    canvas.draw()
    canvas.get_tk_widget().place(x=244, y=0)

    # ----------------- Menu Bar -----------------
    menubar = Menu(Main_Window)
    Main_Window.config(menu=menubar)

    SubMenu1 = Menu(menubar, tearoff=0)
    menubar.add_cascade(label='File', menu=SubMenu1)
    SubMenu1.add_command(label='New Project', activebackground = '#ababab', activeforeground = 'black')
    SubMenu1.add_command(label='Save Graph', command=SaveImage, activebackground = '#ababab', activeforeground = 'black')

    global Graph_Type, Weight
    SubMenu3 = Menu(menubar, tearoff=0)
    menubar.add_cascade(label='Graph Type', menu=SubMenu3)
    my_var1 = IntVar()
    my_var2 = IntVar()
    SubMenu3.add_radiobutton(label='Undirected Graph', command = UndirectedGraph, activebackground = '#ababab', activeforeground = 'black', variable = my_var1)
    SubMenu3.add_radiobutton(label='Directed Graph', command = DirectedGraph, activebackground = '#ababab', activeforeground = 'black', variable = my_var1)
    SubMenu3.add_separator()
    SubMenu3.add_radiobutton(label = 'Weighted Graph', activebackground = '#ababab', activeforeground = 'black', command = Weighted, variable = my_var2)
    SubMenu3.add_radiobutton(label = 'Unweighted Graph', activebackground = '#ababab', activeforeground = 'black', command = Unweighted, variable = my_var2)

    menubar.add_command(label='Exit', command=Main_Window.quit)
    
    # ----------------- Data Box -----------------
    InputBox = Text(Main_Window, width=30, height=26, border=1, bg='#5c5c5c', fg='#a9a9a9', font=('Calibri', 12))
    GetButton = Button(Main_Window, text="Draw Graph", fg='#a9a9a9', bg='#5c5c5c', border=0.5, activebackground='#5c5c5c', command = lambda : GetText(canvas, Graph, a, Figure, InputBox, Main_Window))

    RandomButton = Button(Main_Window, text='Random', bg = '#5c5c5c', fg = '#a9a9a9', activeforeground = 'black', activebackground = '#aeaeae', command = lambda : RandomLayout(RandomButton, CircularButton, PlanarButton, SpringButton))
    CircularButton = Button(Main_Window, text='Circular', bg = '#5c5c5c', fg = '#a9a9a9', activeforeground = 'black', activebackground = '#aeaeae', command = lambda : CircularLayout(RandomButton, CircularButton, PlanarButton, SpringButton))
    PlanarButton = Button(Main_Window, text='Planar', bg = '#aeaeae', fg = 'black', activeforeground = 'black', activebackground = '#aeaeae', command = lambda : PlanarLayout(RandomButton, CircularButton, PlanarButton, SpringButton))
    SpringButton = Button(Main_Window, text='Spring', bg = '#5c5c5c', fg = '#a9a9a9', activeforeground = 'black', activebackground = '#aeaeae', command = lambda : SpringLayout(RandomButton, CircularButton, PlanarButton, SpringButton))

    LayoutLabel = Label(Main_Window, text = 'Layout', bg = '#4e4e4e', fg = '#a9a9a9')

    # ----------------- Placing -----------------
    RandomButton.place(x = 12, y = 560)
    CircularButton.place(x = 75, y = 560)
    PlanarButton.place(x = 134, y = 560)
    SpringButton.place(x = 185, y = 560)
    GetButton.place(x = 85, y = 505)
    InputBox.place(x = 0, y = 0)
    LayoutLabel.place(x = 100, y = 532)


    Main_Window.mainloop()

if __name__ == '__main__':
    Window = Tk()
    Window.geometry("1000x600")
    Window.title("Graphs")
    Window.configure(bg='#535353')
    menubar = Menu(Window, background='#535353', foreground='white', bd=0)
    Window.config(menu=menubar, bg='#535353')

    SubMenu1 = Menu(menubar, tearoff=0, bd=0, activeborderwidth=0, activebackground = '#ababab', activeforeground = 'black')
    menubar.add_cascade(label="File", menu=SubMenu1)
    SubMenu1.add_command(label="New Project", activebackground = '#ababab', activeforeground = 'black')
    SubMenu1.add_separator()
    SubMenu1.add_command(label="Exit", command=Window.quit, activebackground = '#ababab', activeforeground = 'black')

    SubMenu2 = Menu(menubar, tearoff=0)
    menubar.add_cascade(label="Help", menu=SubMenu2)

    CreateButton = Button(text="Create New Project", command=Run, fg="#b9b9b9", bg='#535353', activebackground='#535353', borderwidth=0, font=('calibri', 12)).place(x = 440, y = 300)

    Layout_Type = 'Planar'
    Previous_Layout_Type = ''
    Graph_Type = StringVar()
    Previous_Graph_Type = ''
    Weight = IntVar()
    Weight = 0
    Previous_Weight = -1
    EdgeList = []

    Window.mainloop()
