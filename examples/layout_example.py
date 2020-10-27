# A simple example of a GUI focussing mostly on layout.

# Look carefully at the differences between one frame and the next frame.
# Also resize the window and see how the layout changes

# This example is not really in an OO style - if it was then I probably
# would have made the different components (i.e. each frame) inherit from
# Frame and contain the required buttons


import tkinter as tk 
#A standard message box

from tkinter import messagebox


class DemoApp(object):
    """Layout demo."""

    def __init__(self, master=None):
        self._master = master
        self._master.title("Layout Demo")
        self._master.protocol("WM_DELETE_WINDOW", self.quit)
        # Create a frame and put some buttons in it
        self._frame1 = tk.Frame(self._master,bg='black')
        self._frame1.pack()
        self._button1 = tk.Button(self._frame1, text="Button 01",bg='green',
                              width=len("Button 01"))
        self._button1.pack(side=tk.LEFT)
        self._button2 = tk.Button(self._frame1, text="Button 02", bg='green')
        self._button2.pack(side=tk.LEFT)
        self._button3 = tk.Button(self._frame1, text="Button 03",bg='green')
        self._button3.pack(side=tk.LEFT)
        # Create another frame and put some buttons in it
        self._frame2 = tk.Frame(self._master, bg='black')
        self._frame2.pack(fill=tk.X)
        self._button4 = tk.Button(self._frame2, text="Button 04",bg='green')
        self._button4.pack(side=tk.LEFT,expand=1)
        self._button5 = tk.Button(self._frame2, text="Button 05",bg='green')
        self._button5.pack(side=tk.LEFT,expand=1)
        self._button6 = tk.Button(self._frame2, text="Button 06",bg='green')
        self._button6.pack(side=tk.LEFT)
        # Yet another one
        self._frame3 = tk.Frame(self._master,bg = 'blue')
        self._frame3.pack(fill=tk.X, expand = 1)
        self._button7 = tk.Button(self._frame3, text="Button 07",bg='green')
        self._button7.pack(side=tk.LEFT)
        self._button8 = tk.Button(self._frame3, text="Button 08",bg='green')
        self._button8.pack(side=tk.LEFT)
        self._button9 = tk.Button(self._frame3, text="Button 09",bg='green')
        self._button9.pack(side=tk.LEFT)
        # Yet another one
        self._frame4 = tk.Frame(self._master,bg='yellow')
        self._frame4.pack(fill=tk.BOTH,expand=1,padx=40)
        self._button10 = tk.Button(self._frame4, text="Button 10",bg='green')
        self._button10.pack(side=tk.LEFT,ipadx=30)
        self._button11 = tk.Button(self._frame4, text="Button 11",bg='green')
        self._button11.pack(side=tk.LEFT, padx=20)
        self._button12 = tk.Button(self._frame4, text="Button 12",bg='green')
        self._button12.pack(side=tk.LEFT)
        
        # Yet another one
        self._frame5 = tk.Frame(self._master)
        self._frame5.pack(fill=tk.BOTH)
        self._quitbutton = tk.Button(self._frame5, text="QUIT", command = self.quit)
        self._quitbutton.pack(side=tk.LEFT,expand=1)
        self._dont = tk.Button(self._frame5, text="DON'T PRESS ME", command = self.dontdoit)
        self._dont.pack(side=tk.LEFT, expand=1)
        self._shout = 'I TOLD YOU NOT TO DO THAT'.split(' ')
        self._shoutbuttons = [(self._button1, 'Button 01'),
                             (self._button3, 'Button 03'),
                             (self._button4, 'Button 04'),
                             (self._button5, 'Button 05'),
                             (self._button9, 'Button 09'),
                             (self._button10, 'Button 10'),
                             (self._button11, 'Button 11')]
        self._shout_index = 0

    def quit(self):
        ans = messagebox.askokcancel('Verify exit', 'Really quit?')
        if ans:
            self._master.destroy()
            
    def dontdoit(self):
        """An example using timer events - after 500 milliseconds this
        function is called.
        """

        i = self._shout_index
        if i == 7:
            # got to the end - reset the last button and index
            button,text = self._shoutbuttons[i-1]
            button.configure(bg='green',fg='black',text=text)
            self._shout_index = 0
        elif i == 0:
            # just started - change the first button
            button,text = self._shoutbuttons[i]
            button.configure(bg='red',fg='yellow',text=self._shout[i])
            self._shout_index += 1
            # after 500ms call self.dontdoit
            self._master.after(500, self.dontdoit)
        else:
            # reset the previous button and change the next button
            previousbutton,previoustext = self._shoutbuttons[i-1]
            previousbutton.configure(bg='green',fg='black',text=previoustext)
            button,text = self._shoutbuttons[i]
            button.configure(bg='red',fg='yellow',text=self._shout[i])
            self._shout_index += 1
            self._master.after(500, self.dontdoit)
        



root = tk.Tk()
app = DemoApp(root)
root.mainloop()
