from tkinter import *

from cryptography.fernet import Fernet

window = Tk()
window.geometry('1366x768')
window.title("Welcome to LikeGeeks app")

lblKey = Label(window, text="Key", width=20).grid(row=0)
txtKey = Entry(window, width=150)
txtKey.grid(row=0, column=1)

lblString = Label(window, text="String", width=20).grid(row=1)
txtString = Entry(window, width=150)
txtString.grid(row=1, column=1)

text = Text(window)
text.grid(columnspan=2, sticky="ew")


def encrypt():
    try:
        if txtString.get() is None or txtString.get() == '':
            text.replace(1.0, END, '')
            return
        key = bytes(txtKey.get(), "utf-8")
        b_str = bytes(txtString.get(), "utf-8")
        f = Fernet(key)
        text.replace(1.0, END, bytes.decode(f.encrypt(b_str), "utf-8"))
    except Exception as exc:
        print(f'Encryption is failed: {exc}')
        text.replace(1.0, END, '')


def decrypt():
    try:
        key = bytes(txtKey.get(), "utf-8")
        b_str = bytes(txtString.get(), "utf-8")
        f = Fernet(key)
        text.replace(1.0, END, bytes.decode(f.decrypt(b_str), "utf-8"))
    except Exception as exc:
        if exc.__class__.__name__ == 'InvalidToken':
            exc = 'Invalid input string!'
        print(f'Decryption is failed: {exc}')
        text.replace(1.0, END, '')


button_frame = Frame(window)
button_frame.grid(columnspan=2)
btnEncrypt = Button(button_frame, text="Encrypt", command=encrypt).grid(row=0, column=0)

btnDecrypt = Button(button_frame, text="Decrypt", command=decrypt).grid(row=0, column=1)

window.mainloop()
