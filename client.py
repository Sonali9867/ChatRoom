import socket
import threading
import tkinter as tk
from tkinter import scrolledtext
from tkinter import messagebox

HOST = '127.0.0.1'
PORT = 1234


DARK_GREY = '#000000'      
MEDIUM_GREY = "#4C6A6D"    
OCEAN_BLUE = "#124AA4"     
WHITE = '#CAD2C5'   
FONT = ('Helvetica',15)
SMALL_FONT = ('Helvetica',13)
BUTTON_FONT = ('Helvetica',12)

client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

def add_message(message):
    message_box.config(state=tk.NORMAL)
    message_box.insert(tk.END, message + '\n')
    message_box.config(state=tk.DISABLED)


def connect():
    try:
        client.connect((HOST,PORT))
        print("Successfully connected to server")
        add_message("[SERVER] Successfully connected to the server!")
    except:
        messagebox.showerror("Unable to connect",f"Unable to connect to server {HOST} {PORT}")
        exit(0)

    username = username_textbox.get()

    if username != '':
        client.sendall(username.encode())
    else:
        messagebox.showerror("Invalid Username","Username cannot be empty")
        exit(0)

    threading.Thread(target=listen_for_messages_from_server, args=(client, )).start()
    username_textbox.config(state=tk.DISABLED)
    username_button.pack_forget()
    leave_button.pack(side=tk.RIGHT, padx=10)



def send_message():
    message = message_textbox.get()

    if message != '':
        client.sendall(message.encode())
        message_box.delete(0,len(message))
        message_textbox.delete(0, tk.END)
    else:
        messagebox.showerror("Empty message","Message cannot be empty")

 

def leave_chat():
    username = username_textbox.get()
    try:
        # client.sendall(f"__left__:{username}".encode())  
        client.close()
    except:
        pass
    root.destroy()

def listen_for_messages_from_server(client):

    while 1:
        message = client.recv(2048).decode('utf-8')

        if message:
            if " : " in message:
                username, message_content = message.split(" : ", 1)
                add_message(f"{username} : {message_content}")
            else:
                add_message(message.center(97))
        else:
            messagebox.showerror("Error", "Message received from client is empty.")
            break


# --- GUI ---
root = tk.Tk()
root.geometry("600x600")
root.title("Welcome to ChatRoom by Sonali Kannojiya")
root.resizable(False, False)

# Configure rows and columns
root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=4)
root.grid_rowconfigure(2, weight=1)
root.grid_columnconfigure(0, weight=1)

# Create frames with fixed heights
top_frame = tk.Frame(root, width=600, height=100, bg=DARK_GREY)
top_frame.grid(row=0, column=0, sticky="nsew")
top_frame.grid_propagate(False)

middle_frame = tk.Frame(root, width=600, height=400, bg=MEDIUM_GREY)
middle_frame.grid(row=1, column=0, sticky="nsew")
middle_frame.grid_propagate(False)

bottom_frame = tk.Frame(root, width=600, height=100, bg=DARK_GREY)
bottom_frame.grid(row=2, column=0, sticky="nsew")
bottom_frame.grid_propagate(False)

# --- Top Frame Content ---
usename_label = tk.Label(top_frame, text="Enter Username:", font=FONT, bg=DARK_GREY, fg=WHITE)
usename_label.pack(side=tk.LEFT, padx=10, pady=10)

username_textbox = tk.Entry(top_frame, font=FONT, bg=WHITE, fg=DARK_GREY, width=20)
username_textbox.pack(side=tk.LEFT, padx=5, pady=5)

username_button = tk.Button(top_frame, text="Join", font=BUTTON_FONT, bg=OCEAN_BLUE, fg=WHITE, command=connect)
username_button.pack(side=tk.RIGHT, padx=10, pady=5)

leave_button = tk.Button(top_frame, text="Leave", font=BUTTON_FONT, bg="red", fg=WHITE, command=leave_chat)


# --- Middle Frame Content ---
message_box = scrolledtext.ScrolledText(middle_frame,font=SMALL_FONT,bg=MEDIUM_GREY,fg=WHITE,
insertbackground=WHITE,width=67,height=27.5,borderwidth=4,relief="solid",highlightcolor="#000000")
message_box.config(state=tk.DISABLED)
message_box.pack()


# --- Bottom Frame Content ---
message_textbox = tk.Entry(bottom_frame, font=FONT, bg=WHITE, fg=DARK_GREY, width=45)
message_textbox.pack(side=tk.LEFT, padx=20,pady=10)

message_button = tk.Button(bottom_frame, text="Send", font=BUTTON_FONT, bg=OCEAN_BLUE, fg=WHITE, command=send_message)
message_button.pack(side=tk.LEFT, padx=10,pady=10)



def main():
    root.mainloop()     
    

if __name__=='__main__':
    main()