# -*- coding: cp950 -*-
import Table
import tkinter
from tkinter import *
from tkinter.ttk import *
filename = 'Demodata.txt'
class Application(Frame):
    def executeSQL(self):
        origin = self.Text.get("1.0", END)

        insts = self.getInstruction(origin)
        result = '--------------------------------------\n'
        for i in insts:
            Querier = SQL.querier()
            self.NewSystem = DBMS.DataSet()
            self.NewSystem.readData(filename)
            result += Querier.execute(i,self.NewSystem).getResult()
            result += '--------------------------------------'
        self.Output.delete("1.0", END)
        self.Output.insert(INSERT, result)
    def getInstruction(self,Instruction):
        instructions = ''
        insts = []
        inst = SQL.instruction()
        for c in Instruction:
            inst.add(c)
            if inst.getCount() == 0 and inst.hasdata():
                insts.insert(len(insts),inst)
                inst = SQL.instruction()
        return insts
    def createWidgets(self):

        self.QUIT = Button(self)
        self.QUIT["text"] = "QUIT"
        self.QUIT["command"] =  self.quit
        
        self.QUIT.pack({"side": "right"})
        self.execute = Button(self)
        self.execute["text"] = "EXECUTE",
        self.execute["command"] = self.executeSQL

        self.execute.pack({"side": "left"})

    def __init__(self, master=None):
        Frame.__init__(self, master)
        master.title ("SQL input window")
        master.geometry("800x600")
        self.TextLabel = Label(self, text = "input SQL here").pack()
        self.Text = Text(self,{'width':80,'height':12})
        self.Text.pack()
        
        self.OutputLabel = Label(self, text = "Output Result").pack()
        self.Output = Text(self,{'width':80,'height':18})
        self.Output.pack()

        self.pack()
        self.createWidgets()
        self.NewSystem = DBMS.DataSet()
        self.NewSystem.readData(filename)
        t = self.NewSystem.getTables()
        for table in t:
            print(table)

if __name__ == "__main__":
    import SQL,DBMS

    root = Tk()
    app = Application(master=root)
    app.mainloop()
    root.destroy()
    '''
    for i in insts:
        Querier = SQL.querier()
        NewSystem = DBMS.DataSet()
        NewSystem.readData("data3.txt")
        print i
        print Querier.execute(i,NewSystem)
        print '-----------------------------------'
    '''
