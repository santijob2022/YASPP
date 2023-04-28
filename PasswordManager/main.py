from tkinter import *
from tkinter import messagebox
import random
import pyperclip
import json

FONT_NAME = "Courier"

# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    nr_letters = random.randint(8, 10)
    nr_symbols = random.randint(2, 4)
    nr_numbers = random.randint(2, 4)

    password_list = []

    [password_list.append(random.choice(letters)) for _ in range(nr_letters)]
    [password_list.append(random.choice(symbols)) for _ in range(nr_symbols)]
    [password_list.append(random.choice(numbers)) for _ in range(nr_numbers)]

    random.shuffle(password_list)

    password = "".join(password_list)

    password_entry.insert(0, password)
    pyperclip.copy(password)

# ---------------------------- SAVE PASSWORD ------------------------------- #
def open_file(file_name, mode,data=None):        
    with open(file_name,mode) as f:
        if mode == "r":
            data = json.load(f) 
            print("\n\n", type(data))
            return data
        if mode == "w":
            json.dump(data,f,indent=4)

def save():
    website = website_entry.get()
    email = email_entry.get()
    password = password_entry.get()
    new_data = {
        website: {
            "email":email,
            "password" : password
        }
    }

    if website == "":
        messagebox.showinfo(title="Warning:",message="Website entry is empty.")
    elif password == "":
        messagebox.showinfo(title="Warning:",message="Password entry is empty.")
    else:
        is_ok = messagebox.askokcancel(title="Confirmation",
                                    message=(f"Website: {website}\nEmail\\username: {email}\n"
                                                f"Password: {password}\n"
                                                f"is it ok to save?\n"))
        if is_ok:
            try:
                old_data = open_file("data.json","r")                                                               
            except FileNotFoundError:
                open_file("data.json","w",new_data)
            else:
                old_data.update(new_data)
                open_file("data.json","w",old_data)     
            finally: 
                website_entry.delete(0, END)
                password_entry.delete(0, END)   

# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Password Manager")
#window.minsize(width=500, height=600)
window.config(padx=30, pady=30)# bg

canvas = Canvas(width=200, height=200, highlightthickness=0)
img = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=img) # The coordinate is the center of the image
# timer_text = canvas.create_text(
#     103, 130, text="00:00", fill="white", font=(FONT_NAME, 25, "bold"))
#canvas.grid(column=2, row=2)
canvas.grid(row=0,column=1)

########### Labels ###########
website_Label = Label(text="Website:", font=(
    "Arial"))#, width=10, height=1)
website_Label.grid(column=0, row=1)

email_Label = Label(text="Email/Username:", font=(
    "Arial"))  # , width=10, height=1)
email_Label.grid(column=0, row=2,pady=10)

password_Label = Label(text="Password:", font=(
    "Arial"))  # , width=10, height=1)
password_Label.grid(column=0, row=3)

########### Buttons ###########
generate_button = Button(text="Generate password",
                      highlightthickness=0,width=16,command=generate_password)
generate_button.grid(column=2, row=3)

add_button = Button(text="Add",
                      highlightthickness=0, width=45,command=save)
add_button.grid(column=1, row=4, columnspan=2, pady=10)

########### Entries ###########
website_entry = Entry(width=52)
website_entry.grid(row=1, column=1, columnspan=2)
website_entry.focus()
email_entry = Entry(width=52)
email_entry.grid(row=2, column=1, columnspan=2)
email_entry.insert(0,"santi.job.2022@gmail.com")
password_entry = Entry(width=32)
password_entry.grid(row=3, column=1)

window.mainloop()
