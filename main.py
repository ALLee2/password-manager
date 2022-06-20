import json
from tkinter import *
from tkinter import messagebox
from random import choice, randint, shuffle


# import pyperclip


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
# Password Generator Project
def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_entry.delete(0, END)
    if letter_entry.get().isnumeric():
        nr_letters = int(letter_entry.get())
    else:
        nr_letters = randint(8, 10)
    if symbol_entry.get().isnumeric():
        nr_symbols = int(symbol_entry.get())
    else:
        nr_symbols = randint(2, 4)
    if number_entry.get().isnumeric():
        nr_numbers = int(number_entry.get())
    else:
        nr_numbers = randint(2, 4)

    password_letters = [choice(letters) for _ in range(nr_letters)]
    password_symbols = [choice(symbols) for _ in range(nr_symbols)]
    password_numbers = [choice(numbers) for _ in range(nr_numbers)]

    password_list = password_letters + password_symbols + password_numbers
    shuffle(password_list)

    password = "".join(password_list)
    password_entry.insert(0, password)
    # pyperclip.copy(password)


# ---------------------------- SAVE PASSWORD ------------------------------- #
def save_data():
    website = website_entry.get()
    username = username_entry.get()
    password = password_entry.get()
    new_data = {
        website: {
            "username": username,
            "password": password,
        }
    }

    if len(website_entry.get()) == 0 or len(password_entry.get()) == 0:
        messagebox.showinfo(title="Oops", message="Please do not leave any fields empty.")
    else:
        is_ok = messagebox.askokcancel(title=website_entry.get(), message=f"These are the details entered:\nUsername: "
                                                                          f"{username_entry.get()}\nPassword: "
                                                                          f"{password_entry.get()}\nIs it ok to save?")
        if is_ok:
            mypass_data = open("mypass_data.txt", "a")
            mypass_data.write(f"{website} | {username} | {password}\n")
            mypass_data.close()

            try:
                with open("mypass.json", "r") as data_file:
                    # Reading old data
                    data = json.load(data_file)
                    # Updating old data with new data
                    data.update(new_data)

                with open("mypass.json", "w") as data_file:
                    # Saving updated data
                    json.dump(data, data_file, indent=4)

            except FileNotFoundError:
                with open("mypass.json", "w") as data_file:
                    # Saving new data
                    json.dump(new_data, data_file, indent=4)

            finally:
                website_entry.delete(0, END)
                password_entry.delete(0, END)
                username_entry.delete(0, END)
                username_entry.insert(0, "Username/ Email")
                letter_entry.delete(0, END)
                symbol_entry.delete(0, END)
                number_entry.delete(0, END)


# ---------------------------- SEARCH SETUP ------------------------------- #
def search():
    website = website_entry.get()
    try:
        with open("mypass.json") as data_file:
            data = json.load(data_file)
    except FileNotFoundError:
        messagebox.showinfo(title="Error", message="No Data File Found.")
    else:
        if website in data:
            username = data[website]["username"]
            password = data[website]["password"]
            messagebox.showinfo(title=website, message=f"These are the details saved: \nUsername: {username} "
                                                       f"\nPassword: {password}")
        else:
            messagebox.showinfo(title="Error", message=f"No details for {website} exists.")


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Password Manager")
window.config(padx=20, pady=20)

canvas = Canvas(width=200, height=200)
mypass_img = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=mypass_img)
canvas.grid(column=1, row=0)

# Labels
website_label = Label(text="Website/ App:")
website_label.grid(column=0, row=1)

username_label = Label(text="Username:")
username_label.grid(column=0, row=2)

letter_label = Label(text="No. of Letters for Password:")
letter_label.grid(column=0, row=3)

symbol_label = Label(text="No. of Symbols for Password:")
symbol_label.grid(column=1, row=3)

number_label = Label(text="No. of Numbers for Password:")
number_label.grid(column=2, row=3)

password_label = Label(text="Password:")
password_label.grid(column=0, row=5)

# Entries
website_entry = Entry(width=33)
website_entry.grid(column=1, row=1, sticky=W)

username_entry = Entry(width=52)
username_entry.grid(column=1, row=2, columnspan=2, sticky=W)
username_entry.insert(0, "Username/ Email")

letter_entry = Entry(width=5)
letter_entry.grid(column=0, row=4)

symbol_entry = Entry(width=5)
symbol_entry.grid(column=1, row=4)

number_entry = Entry(width=5)
number_entry.grid(column=2, row=4)

password_entry = Entry(width=33)
password_entry.grid(column=1, row=5, sticky=W)

# Buttons
search_button = Button(text="Search", command=search, width=14)
search_button.grid(column=2, row=1, sticky=W)

generate_button = Button(text="Generate Password", command=generate_password)
generate_button.grid(column=2, row=5, sticky=W)

add_button = Button(text="Add", width=44, command=save_data)
add_button.grid(column=1, row=6, columnspan=2, sticky=W)

window.mainloop()
