import tkinter as tk
from tkinter import ttk
import ttkbootstrap as tb

class MultiPageApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Multi-Page App")
        
        # Create a style
        self.style = tb.Style(theme='litera')
        
        # Create a container
        container = ttk.Frame(self.root)
        container.pack(side="top", fill="both", expand=True)
        
        # Initialize an empty dictionary to hold the pages
        self.pages = {}
        
        # Add pages to the dictionary
        for F in (Page1, Page2, Page3):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.pages[page_name] = frame
            
            # Put all pages in the same location; the one on the top is the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")
        
        # Show the first page
        self.show_page("Page1")
    
    def show_page(self, page_name):
        '''Show a frame for the given page name'''
        page = self.pages[page_name]
        page.tkraise()

class Page1(ttk.Frame):
    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        self.controller = controller
        
        label = ttk.Label(self, text="This is Page 1")
        label.pack(side="top", fill="x", pady=10)
        
        button2 = ttk.Button(self, text="Go to Page 2",
                            command=lambda: controller.show_page("Page2"))
        button2.pack()
        
        button3 = ttk.Button(self, text="Go to Page 3",
                            command=lambda: controller.show_page("Page3"))
        button3.pack()

class Page2(ttk.Frame):
    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        self.controller = controller
        
        label = ttk.Label(self, text="This is Page 2")
        label.pack(side="top", fill="x", pady=10)
        
        button1 = ttk.Button(self, text="Go to Page 1",
                            command=lambda: controller.show_page("Page1"))
        button1.pack()
        
        button3 = ttk.Button(self, text="Go to Page 3",
                            command=lambda: controller.show_page("Page3"))
        button3.pack()

class Page3(ttk.Frame):
    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        self.controller = controller
        
        label = ttk.Label(self, text="This is Page 3")
        label.pack(side="top", fill="x", pady=10)
        
        button1 = ttk.Button(self, text="Go to Page 1",
                            command=lambda: controller.show_page("Page1"))
        button1.pack()
        
        button2 = ttk.Button(self, text="Go to Page 2",
                            command=lambda: controller.show_page("Page2"))
        button2.pack()

# Create the root window
root = tk.Tk()

# Create the app
app = MultiPageApp(root)

# Start the app
root.mainloop()
