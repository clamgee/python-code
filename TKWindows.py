import tkinter as tk
windows=tk.Tk()
windows.title('My Windows')
windows.geometry('200x200')
#------------Label & Button 測試------------
# textvar=tk.StringVar()
# l=tk.Label(windows,textvariable=textvar,bg='green',font=('Arial',12),width=15,height=2)
# l.pack()
# on_hit=False
# def hit_me():
#     global on_hit
#     if on_hit==False:
#         textvar.set('You had hit!')
#         on_hit=True
#     else:
#         textvar.set('')
#         on_hit=False

# b=tk.Button(windows,text='hit me',width=15,height=2,command=hit_me,)
# b.pack()
#
#------------Label & Button 測試------------end
#------------Insert point & Insert end 測試--------
e1=tk.Entry(windows,show='*')
e1.pack()
def insert_point():
    var=e1.get()
    t1.insert('insert',var)
def insert_end():
    var=e1.get()
    t1.insert('end',var)
b1=tk.Button(windows,text='insert point',width=15,height=2,command=insert_point)
b1.pack()
b2=tk.Button(windows,text='insert end',command=insert_end)
b2.pack()
t1=tk.Text(windows,height=2)
t1.pack()
#------------Insert point & Insert end 測試--------end

windows.mainloop()