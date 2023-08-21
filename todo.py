n = 35
cur_i = 1
giffilepath = '1j64.gif'

from tkinter import StringVar, Tk, Entry, Label
from itertools import count, cycle
from PIL import ImageTk, Image
import tempfile

class EditableLabel(Label):
    def __init__(self, parent, rely, var, i, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.var = var
        self.i = i
        self.rely = rely
        self.configure(text=var.get())
        
        self.entry = Entry(self, insertbackground='white', bg=self['bg'], fg= self['fg'], font=self['font'], justify=self['justify'], textvariable=var)
        self.bind("<Double-1>", self.edit_start)
        self.entry.bind("<Return>", self.edit_stop)
        self.entry.bind("<FocusOut>", self.edit_stop)
        self.entry.bind("<Escape>", self.edit_cancel)

    def edit_start(self, event=None):
        self.entry.place(relx=0.5, rely=self.rely, relwidth=1.0, relheight=1.0, anchor="center")
        self.entry.focus_set()

    def edit_stop(self, event=None):
        self.configure(text=self.var.get())
        todos[self.i] = self.var.get()
        open('todos.txt','w').write('\n'.join(todos))
        self.entry.place_forget()

    def edit_cancel(self, event=None):
        self.entry.delete(0, "end")
        self.entry.place_forget()

class ImageLabel(Label):
    """
    A Label that displays images, and plays them if they are gifs
    :im: A PIL Image instance or a string filename
    """
    def load(self, im):
        if isinstance(im, str):
            im = Image.open(im)
        frames = []
 
        try:
            for i in count(1):
                frames.append(ImageTk.PhotoImage(im.copy()))
                im.seek(i)
        except EOFError:
            pass
        self.frames = cycle(frames)
 
        try:
            self.delay = im.info['duration']
        except:
            self.delay = 100
 
        if len(frames) == 1:
            self.configure(image=next(self.frames))
        else:
            self.next_frame()
 
    def unload(self):
        self.cronfigure(image=None)
        self.frames = None
 
    def next_frame(self):
        if self.frames:
            self.configure(image=next(self.frames))
            self.after(self.delay, self.next_frame)

ICON = (b'\x00\x00\x01\x00\x01\x00\x10\x10\x00\x00\x01\x00\x08\x00h\x05\x00\x00'
        b'\x16\x00\x00\x00(\x00\x00\x00\x10\x00\x00\x00 \x00\x00\x00\x01\x00'
        b'\x08\x00\x00\x00\x00\x00@\x05\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
        b'\x00\x01\x00\x00\x00\x01') + b'\x00'*1282 + b'\xff'*64

_, ICON_PATH = tempfile.mkstemp()
with open(ICON_PATH, 'wb') as icon_file:
    icon_file.write(ICON)

app = Tk()
app.title('')
w=app.winfo_screenwidth()
h=app.winfo_screenheight()
app.geometry("{0}x{1}+0+0".format(500*w//1536, 500*h//864))
# app.state('zoomed')
app.configure(background='black')
app.iconbitmap(ICON_PATH)
mainbg = ImageLabel(app)
mainbg.load(giffilepath)
mainbg.place(relx=0.5, rely=0.5, anchor='center')

maintextvar = StringVar()
try:
    textlines = open('todos.txt').read().splitlines()
    n = max(len(textlines)-1, n)
    todos = ['']*(n+1)
    for t in range(len(textlines)):
        try:
            todos[t]=textlines[t]
        except IndexError:
            todos.append(textlines[t])
except:
    todos = ['']*(n+1)
    

open('todos.txt','w').write('\n'.join(todos))
maintextvar.set(todos[0])
lines_dict = {}
def addline(x):
    lines_dict[x] = [StringVar(value=todos[x]), 0]
    lines_dict[x][1] = EditableLabel(app, rely=0.6, var=lines_dict[x][0], i=x, bg='black', fg='white', justify='center', width=32*w//1536, font=('Century Gothic',  16*h//864))

for x in range(1, len(todos)):
    addline(x)
textbox = EditableLabel(app, rely=0.5, var= maintextvar, i= 0, bg='black', fg='white', justify='center', width=16*w//1536, font=('Century Gothic',  32*h//864, 'bold'))
textbox.place(relx=0.5, rely=0.5, anchor='center')
lines_dict[cur_i][1].place(relx=0.5, rely=0.6, anchor='center')

def nextline(D):
    global cur_i
    lines_dict[cur_i][1].place_forget()
    cur_i+=D
    if cur_i==0:
        cur_i=n
    elif cur_i==n+1:
        cur_i=1
    lines_dict[cur_i][1].place(relx=0.5, rely=0.6, anchor='center')
    lines_dict[cur_i][1].focus()

def newline(e):
    global cur_i
    global n
    n+=1
    todos.append('')
    addline(n)
    lines_dict[cur_i][1].place_forget()
    cur_i = n
    lines_dict[cur_i][1].place(relx=0.5, rely=0.6, anchor='center')
    lines_dict[cur_i][1].focus()

app.bind_all('<Shift-Return>', newline) 
app.bind_all('<Up>', lambda e: nextline(-1))
app.bind_all('<Down>', lambda e: nextline(1))

app.attributes('-topmost', True)
app.update()
app.mainloop()