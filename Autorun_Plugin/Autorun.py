import tkinter as tk

def show_message():
  
    root = tk.Tk()
    root.title("Message")


    root.geometry("300x100")

   
    label = tk.Label(root, text="Hi, this is my", font=("Arial", 14))
    label.pack(pady=20)

 
    root.mainloop()


show_message()