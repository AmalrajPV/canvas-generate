from tkinter import *
from PIL import Image
import numpy as np
from tkinter.filedialog import askopenfilename
from tkinter import messagebox

import pyperclip


image = None
height = width = 0
pixel_arr = []
quality = 1


def add():
    global image, height, width, pixel_arr
    path = askopenfilename(
        filetypes=[('Image Files', ['*.jpeg', '*.png', '*jpg'])])
    if path:
        path_name.set(path)
        image = Image.open(path)
        if image.size[1] > 350:
            fh = 350
            hp = (fh/float(image.size[1]))
            ws = int((float(image.size[0])*float(hp)))
            image = image.resize((ws, fh), Image.NEAREST)
        width, height = image.size
        pixel_arr = list(image.getdata())
        generate_btn.grid(row=0, column=2, pady=10, ipady=5, sticky=EW, padx=5)
        quality_in.grid(row=0, column=1, pady=10, ipady=2, sticky=EW, padx=5)
        qlty.grid(row=0, column=0, pady=10, ipady=2, sticky=EW)


def clear():
    f = open('source.py', 'w')
    f.write('')
    f.close()


def generate():
    global image, height, width, pixel_arr, quality
    clear()
    quality = 11 - selection.get()
    funstg = '\'#{r:02x}{g:02x}{b:02x}\''
    funcallstg = '{rgb_to_hex(data[i][j][0], data[i][j][1], data[i][j][2])}'
    try:
        data = np.array(pixel_arr).reshape((height, width, 3))
    except:
        data = np.array(pixel_arr).reshape((height, width, 4))
    f = open('source.py', 'a')
    f.write(
        f'from tkinter import *\nroot = Tk()\nc = Canvas(root, height={height}, width={width}, background="black")\nc.pack()\ndata={data.tolist()}\ndef rgb_to_hex(r,g,b):\n return f{funstg}\nfor i in range(0, {height}, {quality}):\n for j in range(0, {width}, {quality}):\n  c.create_rectangle(j, i, j+{quality}, i+{quality}, outline="", fill=f"{funcallstg}")\nroot.mainloop()'
        )
    f.close()
    cbtn.grid(row=4, column=0)
    messagebox.showinfo(
        "Success", "Code generate. You can copy it from source.py")


def copy_text():
    global image, height, width, pixel_arr, quality
    f = open('source.py', 'r')
    code_line = f.read()
    f.close()
    pyperclip.copy(code_line)
    messagebox.showinfo('Copied', "Code Copied")
    image = None
    height = width = 0
    pixel_arr = []
    path_name.set('')


root = Tk()
root.geometry('500x250')
root.title('code generate')
root.grid_columnconfigure(0, weight=1)

path_name = StringVar()


head = Label(root, text="Generate Tkinter Canvas",
             font=('bold', 20), background="#56CD63")
head.grid(row=0, column=0, pady=5, sticky=EW)

info = Label(
    root, text="Add image to generate the source code and copy it from source.py", font=('italic', 10))
info.grid(row=1, column=0, pady=10, sticky=EW)

fr1 = Frame(root, pady=10)
fr1.grid(row=2, column=0, pady=10, padx=5, sticky=EW)
fr1.grid_columnconfigure(0, weight=1)
fr1.grid_columnconfigure(1, weight=1)

path_in = Entry(fr1, relief="flat", state="disabled", textvariable=path_name)
path_in.grid(row=0, column=0, sticky=EW, ipady=5, padx=2)

add_btn = Button(fr1, text="Add Image", command=add)
add_btn.grid(row=0, column=1, sticky=EW, ipady=2, padx=2)

fr2 = Frame(root)
fr2.grid(row=3, column=0, sticky=EW)
fr2.grid_columnconfigure(0, weight=1)
fr2.grid_columnconfigure(1, weight=2)
fr2.grid_columnconfigure(2, weight=2)

values = [10, 9, 8, 7, 6, 5, 4, 3, 2, 1]
selection = IntVar()
selection.set(values[0])
quality_in = OptionMenu(fr2, selection, *values)

qlty = Label(fr2, text="Quality (10-1)", font=("bold", 13))

generate_btn = Button(fr2, text="Generate", bg="grey", command=generate)

cbtn = Button(root, text="Copy Code", command=copy_text)

root.mainloop()
