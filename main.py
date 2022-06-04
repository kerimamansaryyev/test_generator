from tkinter import *
from tkinter import filedialog
import os
from shutil import copyfile
from tkinter import messagebox

class Questions:
    def __init__(self, questions,name,path):
        self.questions = questions
        self.name = name
        self.path = path
        self.JSON()
        self.HTML()
        
    def jsonize(self,data):
        return '"' + data + '"'
    def HTML(self):
        content = "<!DOCTYPE html>\n<html>\n"
        content = content + "<head>\n\t<title>" + self.name + "</title>"
        content = content + "\n\t<script src='./Questions.js'></script>"
        content = content + '<link rel="stylesheet" href="./design.css">'
        content = content + "\n\t<script src='./Script.js'></script>"
        content = content + "\n</head>\n<body onload='render()'><section id='body'></section><progress id='prog' max='100' value='0'></progress></body></html>"
        newpath = self.path + "/Test.html"
        HTML = open(newpath, "w")
        HTML.write(content)
        HTML.close()
    def JSON(self):
        newpath = self.path + "/Questions.js"
        JSONFILE = open(newpath, "w")
        content = "const data=["
        number = 0
        for question in self.questions:
            content = content + "\n\t{\n\t\t" + self.jsonize('descr')+":" + self.jsonize(question['descr'])+","
            content = content + "\n\t\t" + self.jsonize('right')+":" + self.jsonize(question['right'])+","
            content = content + "\n\t\t" + self.jsonize('others')+":" + "["
            for i in range(len(question['others'])):
                if(i == len(question['others'])-1):
                    content = content + self.jsonize(question['others'][i])
                else:
                    content = content + self.jsonize(question['others'][i]) + ","
            content = content + "]"
            if (number == (len(self.questions)-1)):
                content = content + "\n\t}\n"
            else:
                content = content + "\n\t},\n"
            number = number + 1
        content = content + "]"
        JSONFILE.write(content)
        JSONFILE.close()



class Application:
    #Renders
    properties = {}
    slaves = []
    labels = []
    right = None
    rightLabel = None
    ready_questions = []
    end_of_grid = 6
    def WindowSet(self):
        self.Window = Tk()
        self.Window.configure(background="#292929")
        self.Window.title("SmartSheet     by Kerim Amansaryyev")
        self.Window.geometry('830x450')
        self.container = Frame(self.Window)
        self.container.configure(background="#292929")
        self.container.config(highlightthickness=0)
        self.canvas = Canvas(self.container, width=800,height=450)
        self.canvas.configure(background="#292929")
        self.scrollbar = Scrollbar(self.container,orient="vertical", command=self.canvas.yview)
        self.container.config(highlightthickness=0)
        self.scrollable = Frame(self.canvas)
        self.scrollable.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
            scrollregion=self.canvas.bbox("all")
        ))
        self.canvas.create_window((0, 0), window=self.scrollable, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.config(highlightthickness=0)
        self.Top_Label_Set()
        self.Add_Button_Render()
        self.Finish_Button_Render()
        self.Labels_render(2,0,'Name your Test')
        self.Entry_Render('name',2,1,1)
        self.Labels_render(3,0,'Description of the Question')
        self.Entry_Render('description',3,1,2)
        self.Labels_render(4,0,'How many answers do you want to add?')
        self.Entry_Render('Number_of_Answers',4,1,1)
        self.Increase_button()
        self.Remove_Button_Render()
        self.container.pack(fill="both",expand=True)
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")
        self.scrollable.configure(background="#292929")
        self.scrollable.config(highlightthickness=0)
        
    def Top_Label_Set(self):
        Top_Label = Label(self.scrollable, text="Welcome, here you can create your own app", font=("Righteous", 25),fg="#67cbbd",bg="#292929")
        Top_Label.grid(column=0, row=1, columnspan=3,padx=10,pady=20)
    def Add_Button_Render(self):
        def on_click():
            others = []
            if(len(self.slaves)>0):
                for slave in self.slaves:
                    others.append(slave.get())
                self.ready_questions.append({
                    "descr": self.properties['description'].get(),
                    "right": self.right.get(),
                    "others": others
                })
                messagebox.showinfo("Information",str( len(self.ready_questions) )+" questions added")
            else: messagebox.showinfo("Information","List is empty")
            
        self.Add = Button(self.scrollable, text="Add Question To List", command=on_click,width=20, font=("Raleway", 11),bg="#67cbbd",fg="#292929")
        self.Add.config(relief=FLAT)
        self.Add.grid(column=0, row=self.end_of_grid, columnspan=3,padx=5,pady=5)
        
    def Increase_button(self):
        def on_click():
            if(self.properties['Number_of_Answers'].get() != ''):
                if (self.right!=None):
                    self.right.destroy()
                    if (self.end_of_grid>5):
                        self.end_of_grid-=1
                
                for slave in self.slaves:
                    slave.destroy()
                    if (self.end_of_grid>5):
                        self.end_of_grid-=1
                self.slaves = []
                for label in self.labels:
                    label.destroy()
                self.labels = [] 
                self.Add.destroy()
                self.Finish.destroy()
                self.Remove.destroy()
                if( int(self.properties['Number_of_Answers'].get()) > 0 ):
                    self.rightLabel = Label(self.scrollable, text='Right Answer',font=("Raleway", 12),fg="#67cbbd",bg="#292929")
                    self.rightLabel.grid(column=0,row=self.end_of_grid)
                    self.right = Entry(self.scrollable, width=40,font=("Raleway", 12))
                    self.right.grid(column=1,row=self.end_of_grid,columnspan=2,padx=3,pady=10)
                    self.end_of_grid+=1
                    for i in range(int(self.properties['Number_of_Answers'].get())-1):
                        b = Entry(self.scrollable, width=40,font=("Raleway", 12))
                        b.grid(column=1,row=self.end_of_grid,columnspan=2,padx=3,pady=10)
                        self.slaves.append(b)
                        c = Label(self.scrollable, text='Answer '+str(i+2),font=("Raleway", 12),fg="#67cbbd",bg="#292929")
                        c.grid(column=0,row=self.end_of_grid)
                        self.labels.append(c)
                        self.end_of_grid+=1
                
                self.Add_Button_Render()
                self.Finish_Button_Render()
                self.Remove_Button_Render()
            
        btn = Button(self.scrollable, text="Add",width=10, command=on_click)
        btn.grid(column=2, row=4)

    def Finish_Button_Render(self):
        def on_click():
            self.directory = filedialog.askdirectory()
            newpath = self.directory + '/' +self.properties['name'].get() 
            if not os.path.exists(newpath):
                os.makedirs(newpath)
                self.directory = newpath
                script_dir = os.path.dirname(os.path.abspath(__file__))+"\\Script.js"
                dst = newpath+"/Script.js"
                copyfile(script_dir, dst)
                design_dir = os.path.dirname(os.path.abspath(__file__))+"\\design.css"
                dst = newpath+"/design.css"
                copyfile(design_dir,dst)
                design_dir = os.path.dirname(os.path.abspath(__file__))+"\\Righteous\\Righteous-Regular.ttf"
                dst = newpath+"/Righteous-Regular.ttf"
                copyfile(design_dir,dst)
                design_dir = os.path.dirname(os.path.abspath(__file__))+"\\Raleway\\Raleway-SemiBold.ttf"
                dst = newpath+"/Raleway-SemiBold.ttf"
                copyfile(design_dir,dst)
                design_dir = os.path.dirname(os.path.abspath(__file__))+"\\images\\cover.jpg"
                dst = newpath+"/cover.jpg"
                copyfile(design_dir,dst)
                Test = Questions(self.ready_questions,self.properties['name'].get(),self.directory)
            
        self.Finish = Button(self.scrollable, text="Create a file", command=on_click,width=20, font=("Raleway", 11),bg="#67cbbd",fg="#292929")
        self.Finish.config(relief=FLAT)
        self.Finish.grid(column=0, row=self.end_of_grid+2, columnspan=3,padx=5,pady=5)

    def Remove_Button_Render(self):
        def on_click():
            if (len(self.ready_questions)>0):
                self.ready_questions.pop()
                messagebox.showinfo("Information",str( len(self.ready_questions) )+" questions remained")
            else: messagebox.showinfo("Information","List is empty")
            
        self.Remove = Button(self.scrollable, text="Remove from list", command=on_click,width=20, font=("Raleway", 11),bg="#67cbbd",fg="#292929")
        self.Remove.config(relief=FLAT)
        self.Remove.grid(column=0, row=self.end_of_grid+3, columnspan=3,padx=5,pady=5)
            
    def Labels_render(self,ro,col,txt):
        label = Label(self.scrollable, text=txt, font=("Raleway", 14),fg="#67cbbd",bg="#292929")
        label.grid(column=col,row=ro,padx=5,pady=10)

    def Entry_Render(self,changing,ro,col,height):
        self.properties[changing] = Entry(self.scrollable, width=40,font=("Raleway", 12))
        self.properties[changing].grid(column=col,row=ro,padx=5,pady=5)
    #Events

            
    def __init__(self):
        self.WindowSet()
       
        self.Window.mainloop()

NewApp = Application()
