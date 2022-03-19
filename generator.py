from tkinter import *
from PIL import Image
import numpy as np
from tkinter.filedialog import askopenfilename
from tkinter import messagebox


image = None
height = width = 0
pixel_arr = []


def rgb_to_hex(r, g, b):
        return f'#{r:02x}{g:02x}{b:02x}'


def add():
    global image, height, width, pixel_arr
    path = askopenfilename(filetypes=[('Image Files', ['*.jpeg', '*.png'])])
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
        generate_btn.grid(row=0, column=0, pady=10, ipady=5, sticky=EW, padx=5)


def clear():
    f = open('source.py', 'w')
    f.write('')
    f.close()


def generate():
    global image, height, width, pixel_arr
    clear()
    try:
        data = np.array(pixel_arr).reshape((height, width, 3))
    except:
        data = np.array(pixel_arr).reshape((height, width, 4))
    f = open('source.py', 'a')
    f.write(f'from tkinter import *\nroot = Tk()\nc = Canvas(root, height={height}, width={width})\nc.pack()\n')
    for i in range(height):
        for j in range(width):
                    f.write(f'c.create_rectangle({j}, {i}, {j+1}, {i+1}, fill="{rgb_to_hex(data[i][j][0], data[i][j][1], data[i][j][2])}", outline="")\n')
    f.write('root.mainloop()')
    f.close()
    messagebox.showinfo("Success", "Code generate. You can copy it from source.py")
    image = None
    height = width = 0
    pixel_arr = []
    path_name.set('')

root = Tk()
root.geometry('500x250')
root.title('code generate')
root.grid_columnconfigure(0, weight=1)

path_name = StringVar()


head = Label(root, text="Generate Tkinter Canvas", font=('bold', 20), background="#56CD63")
head.grid(row=0, column=0, pady=5, sticky=EW)

info = Label(root, text="Add image to generate the source code and copy it from source.py", font=('italic', 10))
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

generate_btn = Button(fr2, text="Generate", bg="grey", command=generate)

root.mainloop()
