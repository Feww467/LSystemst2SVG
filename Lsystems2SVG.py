from tkinter import *
from tkinter import filedialog
import numpy as np


global filename
filename = ""
root = Tk()
def ChooseFile():
    root.update_idletasks()
    global filename
    filename = filedialog.askopenfilename(initialdir="/C", title="Select a file")
#TextSpace
TextSpaceFrame = Frame(root) 
TextSpaceFrame.grid(row=0, column=0, rowspan=12)
TextSpace = Text(TextSpaceFrame, width=30)
#ChooseFile
ChooseFileButton = Button(root, text="Choose file", padx=40, command=ChooseFile)
ChooseFileButton.grid(row=0,column=1)
#Color
ColorLabel = Label(root, text="Line color:")
ColorLabel.grid(row=2, column=1)
ColorInput = Entry(root, width=20)
ColorInput.grid(row=3, column=1)
#LineWidth
WidthLabel = Label(root, text="Line width:")
WidthLabel.grid(row=4, column=1)
WidthInput = Entry(root, width=20)
WidthInput.grid(row=5, column=1)
#Lenght
LenghtLabel = Label(root, text="Lenght:")
LenghtLabel.grid(row=6, column=1)
LenghtInput = Entry(root, width=20)
LenghtInput.grid(row=7, column=1)
#Angle
AngleLabel = Label(root, text="Angle:")
AngleLabel.grid(row=8, column=1)
AngleInput = Entry(root, width=20)
AngleInput.grid(row=9, column=1)
#Coeficient
CoeficientLabel = Label(root, text="Coeficient:")
CoeficientLabel.grid(row=10, column=1)
CoeficientInput = Entry(root, width=20)
CoeficientInput.grid(row=11, column=1)
#OutPutFileName
OutputLabel = Label(root, text="Output file name:")
OutputLabel.grid(row=12, column=1)
OutputInput = Entry(root, width=20)
OutputInput.grid(row=13, column=1)
#Formula
FormulaLabel = Label(root, text="Formula:")
FormulaLabel.grid(row=12,column=0)
FormulaInput = Entry(root, width=20)
FormulaInput.grid(row=13, column=0)
#Axiom
AxiomLabel = Label(root, text="Axiom:")
AxiomLabel.grid(row=14, column=0)
AxiomInput = Entry(root, width=20)
AxiomInput.grid(row=15, column=0)
#Iteration
IterationLabel = Label(root, text="Iterations")
IterationLabel.grid(row=14, column=1)
IterationInput = Entry(root, width=20)
IterationInput.grid(row=15,column=1)
TextSpace.grid()

def Convert2SVG(From_formula, axiom):
    if From_formula == True:
        string = axiom
    else:
        try:
            string = open(filename, "r").read()
        except:
            string = str(TextSpace.get("1.0",END))
    #Formulas
    output_string = """<svg width="100" height="100">"""
    stroke_width = WidthInput.get()
    color = str(ColorInput.get())
    lenght= float(LenghtInput.get())
    output_string = """<svg width="100" height="100">"""
    x_previous = 0
    y_previous = 0
    x_new = 0
    y_new=0
    angle = 180
    angle_difference = float(AngleInput.get())
    lenght_coeficient = float(CoeficientInput.get())
    #Push and Pop
    positions_x = []
    positions_y = []
    angles = []
    lenghts = []
    for i in string:
        if i == "f":
            x_previous = x_previous+round((np.sin(np.deg2rad(angle)))*lenght)
            y_previous = y_previous+round((np.cos(np.deg2rad(angle)))*lenght)
        if i == "F":
            x_new = x_previous+round((np.sin(np.deg2rad(angle)))*lenght)
            y_new = y_previous+round((np.cos(np.deg2rad(angle)))*lenght)

            output_string+='''\n<line x1="'''+str(x_previous)+'''" y1="'''+str(y_previous)+'''" x2="'''+str(x_new)+'''" y2="'''+str(y_new)+'''" style="stroke:'''+color+''';stroke-width:'''+str(stroke_width)+'''" />'''
            y_previous = y_new
            x_previous = x_new
        if i == "+":
            angle -= angle_difference
        if i == "-":
            angle += angle_difference
        if i == ">":
            lenght*=lenght_coeficient
        if i == "<":
            lenght/=lenght_coeficient
        if i == "[":
            positions_x.append(x_previous)
            positions_y.append(y_previous)
            angles.append(angle)
            lenghts.append(lenght)
        if i == "]":
            x_previous = positions_x.pop()
            y_previous = positions_y.pop()
            angle = angles.pop()
            lenght = lenghts.pop()

    output_string+="\n</svg>"
    with open((OutputInput.get()+".svg"), "w") as output:
        output.write(output_string)
def CalculateFromFormula():
    axiom = AxiomInput.get()
    variable = (((FormulaInput.get()).split("="))[0]).strip(" ")
    replacement = (((FormulaInput.get()).split("="))[1]).strip(" ")
    for i in range(0,int(IterationInput.get())):
        axiom = axiom.replace(variable, replacement,)
    Convert2SVG(True, axiom)

def clearToTextInput():
   TextSpace.delete("1.0","end")

def Convert2SVGFromString():
    Convert2SVG(False, "")



Convert2SVGButton = Button(root, text="Convert to SVG", padx=40, command=Convert2SVGFromString)
Convert2SVGButton.grid(row=16, column=1)
CalculateFromFormulaButton = Button(root, text="Calculate from formula", padx=40, command=CalculateFromFormula)
CalculateFromFormulaButton.grid(row=16,column=0)
ClearButton = Button(root, text="Clear textspace", padx=40, command=clearToTextInput)
ClearButton.grid(row=1, column=1)
root.mainloop()