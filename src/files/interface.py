import json , time, csv
import tkinter as tk
from tkinter import font
from tkinter import ttk
from tkinter import messagebox
import tkinter.messagebox as tkmsg
from PIL import ImageTk, Image
from files.network import Network

PATHS = {   "logo" : "files/img/logo.png", "icon" : "img/kijiji.ico", "startBtn" : "files/img/startBtn.png", 
            "searchBtn" : "files/img/searchBtn.png", "clearBtn" : "files/img/clear.png", "lines" : "files/londonlines.csv",
            "stations" : "files/londonstations.csv", "connections" : "files/londonconnections.csv",
        }
global STATIONS
global GRAPH


class NetworkGraphApp(object):
    def __init__(self):
        # Initializing Application Window
        self.root = tk.Tk()
        self.windowWidth            = self.root.winfo_reqwidth()
        self.windowHeight           = self.root.winfo_reqheight()
        self.root['background']   = '#0D0C52'
        self.root.title("London station Network Graph")
        # self.root.iconbitmap(PATHS["icon"])
        self.root.resizable(False, False)
        self.root.show_frame = self.show_frame
        

    # Function to position the window at the center of your screen
    def position_window(self, geo):
        positionRight   = int(self.root.winfo_screenwidth()  * 0.3)
        positionDown    = int(self.root.winfo_screenheight() * 0.1)
       


        # Positions the window in the center of the page.
        self.root.geometry("+{}+{}".format(positionRight, positionDown))
        self.root.geometry(geo)


    # Function to position Frame
    def position_Frame(self):
        self.container = tk.Frame(
            self.root, 
            bg="#0D0C52",
            bd = 0,
            width=568,
            height=488
        )
        self.container.pack()


    #show frames
    def show_frame(self, frame_class, geo, data=None):
        """Destroys current frame and replaces it with a new one."""
        new_frame = frame_class(self.root, data)
        self.position_window(geo)
        if self.container is not None:
            self.container.destroy()
        self.container = new_frame
        self.container.pack(side = "top", fill = "both", expand = True)


    def window_loop(self):
        self.position_window('568x488')
        self.position_Frame()
        self.show_frame(WelcomePage, '568x488', None)
        return self.root




# welocmeWindow Frame
class WelcomePage(tk.Frame):
    def __init__(self, master, data):
        tk.Frame.__init__(
            self, 
            master, 
            bg="#0D0C52",
            bd = 0,
            width=568,
            height=488
        )
        self.st = []
        self.lines = []
        self.ID = []
        self.line_id = []
        self.graph = []
        self.position_headerText()
        self.position_logoImg()
        self.position_StartBtn(master)
        self.position_howToText()
        self.setGraph()

    # How to guide
    def howToPopup(self, event):
        with open ("files/howto.txt", "r") as f:
            help_msg = f.read()
        tkmsg.showinfo(title="How to Guide is here!", message=help_msg)


    # convert csv to json
    def csv_to_json(self, Path, name):
        jsonArray = []
        
        
        with open(Path, encoding='utf-8') as csvf: 
            csvReader = csv.DictReader(csvf) 
            
            for row in csvReader: 
                jsonArray.append(row)
                if name == "lines":
                    self.lines.append(row["name"].strip())
                    self.line_id.append(row["line_id"].strip())
                elif name == "stations":
                    self.st.append(row["name"].strip())
                    self.ID.append(row["id"].strip())

        STATIONS = tuple(self.st)
        return jsonArray


    # function to set graph from csv
    def setGraph(self):
        lines = self.csv_to_json(PATHS["lines"], "lines")
        stations = self.csv_to_json(PATHS["stations"], "stations")
        connections = self.csv_to_json(PATHS["connections"], "connections")
        


        for connection in connections:
            st1 = self.ID.index(connection["station1"])
            st2 = self.ID.index(connection["station2"])
            lid = self.line_id.index(connection["line_id"])
            tp = (self.st[st1], self.st[st2], self.lines[lid], connection["time"])
            self.graph.append(tp)
            
        GRAPH = Network(self.graph)
        print(GRAPH)


    # Function to position the text at the center of the window
    def position_headerText(self):
        x_axis = 568 - 470
        y_axis = 488 - 470
        self.headerTxt = ttk.Label(
            self, 
            background="#0D0C52",
            foreground = "#FFFFFF",
            text="London Station Network Graph", 
            font=("Roboto Condensed", 18, "bold")
        ).place(x=x_axis, y=y_axis)


    # Function to position logo
    def position_logoImg(self):
        x_axis = 0
        y_axis = 488 - 425
        self.c = tk.Canvas(
            self, 
            bg = '#0D0C52',
            bd = 0,
            highlightthickness=0,
            width = 563, 
            height = 280
        )
        self.img_1 = ImageTk.PhotoImage(Image.open(PATHS["logo"]).resize((265, 265), Image.ANTIALIAS)) 
        # print(img) 
        self.c.create_image(150, 20, anchor="nw", image=self.img_1)
        self.c.image = self.img_1
        self.c.place(x=x_axis, y=y_axis)
        self.c.image = self.img_1


    # Function to position button
    def position_StartBtn(self, master):
        # Placement axis
        x_axis = 568 - 368
        y_axis = 488 - 130
        # Add Image
        self.img_2 = ImageTk.PhotoImage(Image.open(PATHS["startBtn"]))
        # Create button and image
        self.startBtn = tk.Button(
            self, 
            image=self.img_2,
            bd = 0,
            command=lambda: master.show_frame(FormPage, '739x668', data=[tuple(self.st), self.graph])
        )
        self.startBtn.image = self.img_2
        self.startBtn.place(x=x_axis, y=y_axis)
        self.startBtn.image = self.img_2


    # Function to position the how to link
    def position_howToText(self):
        x_axis = 568 - 354
        y_axis = 488 - 60
        self.howtoTxt = ttk.Label(
            self, 
            background="#0D0C52",
            foreground = "#FFFFFF",
            text="How To Guide ?", 
            font=("Roboto Condensed", 12, "bold"),
            cursor= "hand2",
        )
        self.howtoTxt.bind("<Button-1>", self.howToPopup)
        self.howtoTxt.place(x=x_axis, y=y_axis)



# station form frame
class FormPage(tk.Frame):
    def __init__(self, master, data):
        tk.Frame.__init__(
            self, 
            master, 
            bg="#0D0C52",
            bd = 0,
            width=739,
            height=668
        )

        self.st = data[0]
        self.graph = data[1]
        self.position_clock()
        self.position_headerSection()
        self.position_Dropdowns()
        self.position_Table()
        self.position_searchBtn()
        self.position_allLocations()
        self.faultyStations = self.toJson(mode="r")
        print(self.faultyStations)
        self.setBadLocation(self.faultyStations)
        # self.position_processWindow()
        self.update_time()

    # def to json
    def toJson (self, mode="r", dicty=None):
        if mode == "w":
            json_object = json.dumps(dicty, indent = 4)
            with open("files/bad.json", "w+") as outfile:
                outfile.write(json_object)

        else:
            with open('files/bad.json', 'r') as openfile:
                json_object = json.load(openfile)

                
        return json_object


    def setBadLocation(self, js):
        count = 0
        for i in self.tbl.get_children():
            self.tbl.delete(i)
            
        for loc in js:
            count += 1
            loc = (count, loc, "In-active")   
            self.tbl.insert('', tk.END, values=loc)


    def removeBadLocation(self, event):
        item = self.tbl.selection()
        selected_item = item[0]

        for i in self.tbl.get_children():
            if i ==  selected_item :
                item = self.tbl.item(i)
                remove = item["values"][1]
                print(remove)
                self.faultyStations.remove(remove)
                print(self.faultyStations)
                self.toJson(mode="w", dicty=self.faultyStations)

        self.setBadLocation(self.faultyStations)


    # Function to show path
    def showPath(self):
        fr = self.provinceInput.get().strip()
        t0 = self.cityInput.get().strip()
        graph = Network(self.graph)
        # fr = "Snaresbrook"
        # t0 = "Leytonstone"

        if fr == "" or t0 == "":
            messagebox.showerror("Error", "From and to Locations cannot be empty fields")
        elif fr == t0 or t0 == fr:
            messagebox.showerror("Error", "Location and destination must be different")
        elif fr in self.faultyStations or t0 in self.faultyStations:
            if fr in self.faultyStations:
                tag = fr
            else :
                tag = t0
            messagebox.showerror("Error", tag + " is registered as a faulty station")
        else:

            self.path = tk.Toplevel(
                self,
                bg="#0D0C52",
                cursor="arrow",
                height="500",
                width="200"
            )
            self.path.maxsize(500, 200)
            self.path.minsize(500, 200)
            self.path.resizable(False, False)
            x = self.winfo_screenwidth()  * 0.4
            y = self.winfo_screenheight()  * 0.5
            w = self.path.winfo_width()
            h = self.path.winfo_height()
            self.path.geometry("%dx%d+%d+%d" % (w, h, x, y))
            print(fr)
            print(t0)
           
            raw_results = graph.dijkstra(str(fr),str(t0))
            # print(list(raw_results))
            results, curr_dist = raw_results
            results = list(results)

            if results and len(results) > 0:
                all_stops = "Starting Station : \n"
                for stop in results:
                    all_stops = all_stops + stop + " --> "

                all_stops = all_stops + "\n Reached destination"
                result = tk.Label(self.path, text = all_stops, font=("Roboto Condensed", 18), padx=20, bg="orange")
                result.pack()
                result_time = tk.Label(self.path, text = "Total time of travel : " + str(curr_dist) + " minutes", font=("Roboto Condensed", 18), padx=20, bg="orange")
                result_time.pack()
            else:
                result = tk.Label(self.path, text = "No connection exist between the two locations", font=("Roboto Condensed", 16), padx=20, bg="orange")
                result.pack()
        
    
    # Function to register bad stations
    def registerBadStation(self, event):
        station = self.badInput.get().strip()
        if station not in self.faultyStations:
            self.faultyStations.append(station)

        fs = self.toJson(mode="w", dicty=self.faultyStations)
        self.setBadLocation(self.faultyStations)
        messagebox.showinfo("showinfo", station + " has been successfully registered as a faulty station")
        self.bad.destroy()


    # Function to add faulty stations
    def addFaultyStations(self):
        self.bad = tk.Toplevel(
            self,
            bg="#0D0C52",
            cursor="arrow",
            height="400",
            width="170"
        )
        self.bad.maxsize(400, 170)
        self.bad.minsize(400, 170)
        self.bad.resizable(False, False)
        x = self.winfo_screenwidth()  * 0.4
        y = self.winfo_screenheight()  * 0.2
        w = self.bad.winfo_width()
        h = self.bad.winfo_height()
        self.bad.geometry("%dx%d+%d+%d" % (w, h, x, y))

        self.badLbl = ttk.Label(
            self.bad, 
            background="#0D0C52",
            foreground = "#FFFFFF",
            text=" Faulty Station :", 
            font=("Roboto Condensed", 16)
        ).pack()

        self.badInput = ttk.Combobox(
            self.bad, 
            background="#0D0C52",
            foreground = "#0D0C52",
            text=" Bad :", 
            font=("Roboto Condensed", 16),
            textvariable=tk.StringVar(), 
            state="readonly",
            values = self.st
        )
        self.badInput.bind("<<ComboboxSelected>>", self.registerBadStation)
        self.badInput.pack()


    # Function to create and position the text and logo at the center of the window
    def position_headerSection(self):
        x_axis = 739 - 540
        y_axis = 668 - 658
        self.headerTxt = ttk.Label(
            self, 
            background="#0D0C52",
            foreground = "#FFFFFF",
            text="London station Network Graph", 
            font=("Roboto Condensed", 20, "bold")
        ).place(x=x_axis, y=y_axis)

        self.c2 = tk.Canvas(
            self, 
            bg = '#0D0C52',
            bd = 0,
            highlightthickness=0,
            width = 70, 
            height = 50
        )
        x_axis = 739 - 640
        y_axis = 668 - 668
        self.img_3 = ImageTk.PhotoImage(Image.open(PATHS["logo"]).resize((42, 42), Image.ANTIALIAS)) 
        # print(img) 
        self.c2.create_image(20, 10, anchor="nw", image=self.img_3)
        self.c2.image = self.img_3
        self.c2.place(x=x_axis, y=y_axis)
        self.c2.image = self.img_3
    
 
    # function to position clock
    def position_clock(self):
        x_axis = 739 - 450
        y_axis = 668 - 618
        curr_time = time.strftime('%H:%M:%S %p')
        self.clock_label = tk.Label(self, padx=20, text=curr_time, pady=10, bg="orange", fg="black")
        self.clock_label.place(x=x_axis, y=y_axis)


    def update_time(self):
        curr_time = time.strftime('%H:%M:%S %p')
        self.clock_label.config(text="Time Now: " + str(curr_time))
        self.clock_label.after(1000, self.update_time)


    #Function to create and position from and to station
    def position_Dropdowns(self): 
        x_axis = 739 - 620
        y_axis = 668 - 570
        self.provinceLbl = ttk.Label(
            self, 
            background="#0D0C52",
            foreground = "#FFFFFF",
            text=" From Station :", 
            font=("Roboto Condensed", 16)
        ).place(x=x_axis, y=y_axis)

        x_axis = 739 - 699
        y_axis = 668 - 544
        self.provinceInput = ttk.Combobox(
            self, 
            background="#0D0C52",
            foreground = "#0D0C52",
            text=" Province :", 
            font=("Roboto Condensed", 16),
            textvariable=tk.StringVar(), 
            state="readonly",
            values = self.st
        )
        self.provinceInput.place(x=x_axis, y=y_axis)
        

        x_axis = 739 - 200
        y_axis = 668 - 570
        self.cityLbl = ttk.Label(
            self, 
            background="#0D0C52",
            foreground = "#FFFFFF",
            text=" To Station :", 
            font=("Roboto Condensed", 16),
        ).place(x=x_axis, y=y_axis)

        x_axis = 739 - 310
        y_axis = 668 - 544
        self.cityInput = ttk.Combobox(
            self, 
            background="#0D0C52",
            foreground = "#0D0C52",
            text=" Province :",
            textvariable=tk.StringVar(), 
            state="readonly", 
            values = self.st,
            font=("Roboto Condensed", 16),
        )
        self.cityInput.place(x=x_axis, y=y_axis)


    # Function to position location tables
    def position_Table(self):
        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure(
            "Treeview",
            background = "#C4C4C4",
            foreground = "black",
            rowheight = 20,
            fieldbackground = "#C4C4C4",
        )

        self.style.map (
            "Treeview",
            background= [('selected' , '#0D0C52')]
        )
        x_axis = 739 - 699
        y_axis = 668 - 490

        self.tbl = ttk.Treeview(
            self, 
            show='headings', 
            height="10",
           
        )

        self.tbl['columns']=('s/n', 'Station/Line', 'Status')
        self.tbl.column('s/n',  width=80, anchor=tk.CENTER)
        self.tbl.column('Station/Line',  width=272, anchor=tk.CENTER)
        self.tbl.column('Status',  width=272, anchor=tk.CENTER)

        # define headings
        self.tbl.heading('s/n', text='s/n')
        self.tbl.heading('Station/Line', text='Station/Line')
        self.tbl.heading('Status', text='Status')

        self.tbl.bind("<Double-1>", self.removeBadLocation)

        self.tbl.place(x=x_axis, y=y_axis)

        x_axis = 739 - 70
        y_axis = 668 - 490
        self.scrollbar = tk.Scrollbar(
            self, 
            bg="#0D0C52",
            activebackground="#0D0C52",
            orient=tk.VERTICAL, 
            command=self.tbl.yview,
           
            # height="10",
        )
        self.tbl.configure(yscroll=self.scrollbar.set)
        self.scrollbar.place(x=x_axis, y=y_axis, height="228")


    #Funtion to create and position add all locations
    def position_allLocations(self):
        #Placements axi
        x__axis = 939 - 500
        y_axis = 668 - 180
        self.allLocations = tk.Button(
            text="Register Bad Stations", 
            activebackground="white",bg="darkblue", 
            activeforeground="black", 
            overrelief="flat", foreground="white", 
            font=("Roboto", 14), relief="flat",
            cursor= "hand2",
            command=self.addFaultyStations
        )
        self.allLocations.place(x=x__axis, y=y_axis)


    #Function to create and position search btn
    def position_searchBtn(self):
        # Placement axis
        x_axis = 539 - 400
        y_axis = 668 - 180
        # Add Image
        self.img_5 = ImageTk.PhotoImage(Image.open(PATHS["searchBtn"]))
        # Create button and image
        self.searchBtn = tk.Button(
            self, 
            image=self.img_5,
            bd = 0,
            cursor= "hand2",
            command=self.showPath
        )
        self.searchBtn.image = self.img_5
        self.searchBtn.place(x=x_axis, y=y_axis)
        self.searchBtn.image = self.img_5