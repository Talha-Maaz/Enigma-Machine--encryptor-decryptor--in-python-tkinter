import tkinter as tk
import random


def caesar_cipher(text, key, decrypt=False):
    result = ""
    for char in text:
        if char.isalpha():
            shift = key % 26 if not decrypt else (-key) % 26
            if char.islower():
                shifted = ord('a') + ((ord(char) - ord('a') + shift) % 26)
            else:
                shifted = ord('A') + ((ord(char) - ord('A') + shift) % 26)
            result += chr(shifted)
        else:
            result += char
    return result

# Playfair Cipher
def generate_playfair_key(key):
    key = key.replace(" ", "").upper()
    key_without_duplicates = "".join(dict.fromkeys(key))
    alphabet = "ABCDEFGHIKLMNOPQRSTUVWXYZ"
    playfair_key = key_without_duplicates
    for char in alphabet:
        if char not in playfair_key:
            playfair_key += char
    return playfair_key

def create_playfair_matrix(key):
    matrix = [[0] * 5 for _ in range(5)]
    key = generate_playfair_key(key)
    k = 0
    for i in range(5):
        for j in range(5):
            matrix[i][j] = key[k]
            k += 1
    return matrix

def playfair_cipher(text, key, decrypt=False):
    matrix = create_playfair_matrix(key)
    text = text.replace(" ", "").upper()
    result = ""
    for i in range(0, len(text), 2):
        a, b = text[i], text[i + 1]
        if a == b:
            b = 'X'
        a_row, a_col, b_row, b_col = 0, 0, 0, 0
        for row in range(5):
            if a in matrix[row]:
                a_row = row
                a_col = matrix[row].index(a)
            if b in matrix[row]:
                b_row = row
                b_col = matrix[row].index(b)
        if a_row == b_row:
            if decrypt:
                result += matrix[a_row][(a_col - 1) % 5]
                result += matrix[b_row][(b_col - 1) % 5]
            else:
                result += matrix[a_row][(a_col + 1) % 5]
                result += matrix[b_row][(b_col + 1) % 5]
        elif a_col == b_col:
            if decrypt:
                result += matrix[(a_row - 1) % 5][a_col]
                result += matrix[(b_row - 1) % 5][b_col]
            else:
                result += matrix[(a_row + 1) % 5][a_col]
                result += matrix[(b_row + 1) % 5][b_col]
        else:
            if decrypt:
                result += matrix[a_row][b_col]
                result += matrix[b_row][a_col]
            else:
                result += matrix[b_row][a_col]
                result += matrix[a_row][b_col]
    return result

# Vigenère Cipher
def vigenere_cipher(text, key, decrypt=False):
    key = key.upper()
    key_length = len(key)
    result = ""
    for i in range(len(text)):
        shift = ord(key[i % key_length]) - ord('A')
        if text[i].isalpha():
            if text[i].islower():
                shifted = ord('a') + ((ord(text[i]) - ord('a') + (-shift if decrypt else shift)) % 26)
            else:
                shifted = ord('A') + ((ord(text[i]) - ord('A') + (-shift if decrypt else shift)) % 26)
            result += chr(shifted)
        else:
            result += text[i]
    return result



history = []

# Function to display history in a separate window
def show_history():
    history_window = tk.Toplevel(root)
    history_window.title("Encryption/Decryption History")

    history_text = tk.Text(history_window, height=10, width=40, fg="chartreuse1", bg="black")
    history_text.pack()

    # Display history in the history dialog box
    for entry in history:
        history_text.insert(tk.END, entry + "\n")

#russian headline
def update_russian_letters():
  russian_alphabet = 'а12354бвгдеёжaзийклмbнmnоgadsdaawgsпрdfh!@#$%^&*(jhсcawтуфхцчшщъыьэюя'
  random_russian_text = ''.join(random.choices(russian_alphabet, k=70))
  russian_label.config(text=random_russian_text)
  russian_label.after(200, update_russian_letters)



# Function to perform cipher operation
def perform_cipher():
    text = text_entry.get()
    cipher_type = cipher_type_var.get().lower()
    key = key_entry.get()

    output_text.delete(1.0, tk.END)  # Clear previous output

    if cipher_type == 'caesar' or cipher_type == 'playfair' or cipher_type == 'vigenere':
        if cipher_type == 'caesar':
            key = int(key) if key.isdigit() else 0  # Ensure key is a number for Caesar cipher

        operation = operation_var.get().lower()  # Get encryption or decryption operation

        if operation == 'encrypt' or operation == 'decrypt':
            if cipher_type == 'caesar':
                result = caesar_cipher(text, key, operation == 'decrypt')
                history.append(f"**{operation.capitalize()}ion** \n\tcipher : caeser \n\tkey : {key}")
            elif cipher_type == 'playfair':
                result = playfair_cipher(text, key, operation == 'decrypt')
                history.append(f"**{operation.capitalize()}ion** \n\tcipher : playfair \n\tkey : {key}")
            else:
                result = vigenere_cipher(text, key, operation == 'decrypt')
                history.append(f"**{operation.capitalize()}ion** \n\tcipher : vigenere \n\tkey : {key}")

            output_text.insert(tk.END, f"Result: {result}")
        else:
            output_text.insert(tk.END, "Invalid choice")
    else:
        output_text.insert(tk.END, "Invalid Cipher Type")

#GUI setup
root = tk.Tk()
root.geometry("800x800")
root.title("Enigma Machine")
root.configure(bg="black")

frame = tk.Frame(root, bg="black")
frame.pack(padx=20, pady=20)

tk.Label(frame, text="Enigma Machine", fg="black", bg="chartreuse1", font=("times new roman", 28,  "bold")).grid(row=0, columnspan=2, pady=(40, 80))




tk.Label(frame, text="Enter text:", fg="chartreuse1", bg="black", font=("Arial", 12)).grid(row=1, column=0, sticky=tk.W, pady=5)
text_entry = tk.Entry(frame, bg="black", fg="chartreuse1")
text_entry.grid(row=1, column=1, padx=5, pady=5)

tk.Label(frame, text="Select Cipher:", fg="chartreuse1", bg="black", font=("Arial", 12)).grid(row=2, column=0, sticky=tk.W, pady=5)
cipher_type_var = tk.StringVar(value="Caesar")
cipher_type_dropdown = tk.OptionMenu(frame, cipher_type_var, "Caesar", "Playfair", "Vigenere")
cipher_type_dropdown.config(bg="black", fg="chartreuse1")
cipher_type_dropdown.grid(row=2, column=1, padx=5, pady=5)

tk.Label(frame, text="Enter Key:", fg="chartreuse1", bg="black", font=("Arial", 12)).grid(row=3, column=0, sticky=tk.W, pady=5)
key_entry = tk.Entry(frame, bg="black", fg="chartreuse1")
key_entry.grid(row=3, column=1, padx=5, pady=5)

tk.Label(frame, text="Operation:", fg="chartreuse1", bg="black", font=("Arial", 12)).grid(row=4, column=0, sticky=tk.W, pady=5)
operation_var = tk.StringVar(value="Encrypt")
operation_dropdown = tk.OptionMenu(frame, operation_var, "Encrypt", "Decrypt")
operation_dropdown.config(bg="black", fg="chartreuse1")
operation_dropdown.grid(row=4, column=1, padx=5, pady=5)

perform_button = tk.Button(frame, text="OK", command=perform_cipher, fg="chartreuse1", bg="black", font=("Arial", 12))
perform_button.grid(row=5, columnspan=2, pady=10)

output_text = tk.Text(frame, height=5, width=40, fg="chartreuse1", bg="black", font=("Arial", 12))
output_text.grid(row=6, columnspan=2)

history_button = tk.Button(frame, text="Show History", command=show_history, fg="chartreuse1", bg="black", font=("Arial", 12))
history_button.grid(row=7, columnspan=2, pady=10)



russian_label = tk.Label(root, text="", fg="chartreuse1", bg="black", font=("Arial", 12))
russian_label.pack(anchor=tk.S, pady=10)
update_russian_letters()




root.mainloop()