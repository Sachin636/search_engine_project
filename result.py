from tkinter import *
from vector_space_model import vector_model
import webbrowser

def gui_search():
    root = Tk()
    chromedir= 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s'
    # Enter Query Message
    search_message = Label(root,text = "Enter Query")
    search_message.pack()
    search_query = Entry(root,width = 100,borderwidth=7)
    search_query.pack()
    search_query.insert(0,"Enter Your Query")
    frame = LabelFrame(root,padx=5,pady=5)
    frame.pack(padx=10,pady=10)
    # Button click action for search Button
    def myClick():
        for widget in frame.winfo_children():
            widget.destroy()
        text = vector_model(str(search_query.get()))
        for i in text:
            def openBrowser():
                webbrowser.get(chromedir).open(i)
            result = Button(frame,text = i,command=openBrowser)
            result.pack()
    search_button = Button(root,text = "Search",padx=100,command=myClick,bg='green')
    search_button.pack()
    root.mainloop()

def main():
    gui_search()

if __name__ == "__main__":
    main()


