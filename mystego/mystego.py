import cv2
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
import numpy as np
from PIL import Image, ImageTk

# Mapping characters to numbers and vice versa
char_to_int = {chr(i): i for i in range(256)}
int_to_char = {i: chr(i) for i in range(256)}

# Global password variable
password = ""

# Function to encrypt the message into an image
def encrypt_message():
    global password

    file_path = filedialog.askopenfilename(title="Select Image",
                                           filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
    if not file_path:
        return

    img = cv2.imread(file_path)
    if img is None:
        messagebox.showerror("Error", "Invalid image! Please select a valid image.")
        return

    msg = simpledialog.askstring("Input", "Enter secret message:")
    password = simpledialog.askstring("Input", "Enter a passcode:", show="*")

    if not msg or not password:
        messagebox.showerror("Error", "Message or passcode cannot be empty!")
        return

    msg_length = len(msg)
    if msg_length > img.shape[0] * img.shape[1]:
        messagebox.showerror("Error", "Message is too long for the selected image.")
        return

    # Encode message length in the first 3 pixels
    img[0, 0, 0] = msg_length // 256
    img[0, 0, 1] = msg_length % 256

    n, m, z = 0, 1, 0  # Start storing after the first pixel

    for i in range(msg_length):
        img[n, m, z] = char_to_int[msg[i]]
        n = (n + 1) % img.shape[0]
        m = (m + 1) % img.shape[1]
        z = (z + 1) % 3

    save_path = filedialog.asksaveasfilename(defaultextension=".png",
                                             filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg")])
    if save_path:
        cv2.imwrite(save_path, img)
        messagebox.showinfo("Success", "Message encrypted and saved successfully!")

# Function to decrypt the message from an image
def decrypt_message():
    global password

    file_path = filedialog.askopenfilename(title="Select Encrypted Image",
                                           filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
    if not file_path:
        return

    img = cv2.imread(file_path)
    if img is None:
        messagebox.showerror("Error", "Invalid image! Please select the correct encrypted image.")
        return

    pas = simpledialog.askstring("Input", "Enter passcode to decrypt:", show="*")

    if pas != password:
        messagebox.showerror("Error", "Incorrect passcode!")
        return

    # Retrieve the stored message length
    msg_length = int(img[0, 0, 0]) * 256 + int(img[0, 0, 1])

    decrypted_msg = ""
    n, m, z = 0, 1, 0  # Start retrieving after the first pixel

    try:
        for _ in range(msg_length):
            decrypted_msg += int_to_char[img[n, m, z]]
            n = (n + 1) % img.shape[0]
            m = (m + 1) % img.shape[1]
            z = (z + 1) % 3
    except KeyError:
        messagebox.showerror("Error", "Decryption failed! Image might be altered.")
        return

    messagebox.showinfo("Decrypted Message", f"Message: {decrypted_msg}")

# Function to close the application
def close_app():
    root.destroy()

# Create GUI window
root = tk.Tk()
root.title("🔒 Secure Image Steganography")
root.geometry("500x400")
root.configure(bg="#2c3e50")


# Title label
title_label = tk.Label(root, text="🔐 Image Steganography", font=("Arial", 16, "bold"), fg="white", bg="#2c3e50")
title_label.pack()

# Encrypt button
btn_encrypt = tk.Button(root, text="Encrypt Message", command=encrypt_message, font=("Arial", 12),
                        padx=20, pady=10, fg="white", bg="#3498db", activebackground="#2980b9", relief="raised")
btn_encrypt.pack(pady=15)

# Decrypt button
btn_decrypt = tk.Button(root, text="Decrypt Message", command=decrypt_message, font=("Arial", 12),
                        padx=20, pady=10, fg="white", bg="#2ecc71", activebackground="#27ae60", relief="raised")
btn_decrypt.pack(pady=15)

# Close button
btn_close = tk.Button(root, text="Exit", command=close_app, font=("Arial", 12),
                      padx=20, pady=10, fg="white", bg="#e74c3c", activebackground="#c0392b", relief="raised")
btn_close.pack(pady=15)

# Run GUI
root.mainloop()



