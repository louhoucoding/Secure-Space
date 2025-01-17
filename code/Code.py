from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
import os
import subprocess
import time

direction = os.getcwd()
name = input("Enter your name: ")
password = input("Enter your password: ")
with open(r"C:\Programing\Projects\Projects_Python\Secure_space\Code\Name.txt", "r") as name_file:
    nm = name_file.read()

with open(r"C:\Programing\Projects\Projects_Python\Secure_space\Code\Password.txt", "r") as password_file:
    pwd = password_file.read()

if name == nm and pwd == password:
    print(name + ", Welcome in your Secure Space!")
elif name != nm or pwd != password:
    raise OSError("Invalid name or password.")

PATH = r"C:\Programing\Projects\Projects_Python\Secure_space\SS"
KEY_PATH = r"C:\Programing\Projects\Projects_Python\Secure_space\Keys"

# Keys Folder
try:
    os.mkdir(KEY_PATH)
except OSError:
    pass


def show_files():
    files = os.listdir(PATH)
    if files:
        print("Files in the directory:")
        for i, file in enumerate(files, 1):
            print(f"{i}. {file}")
    else:
        print("No files found in the directory.")


# Check the files from the direction
def check_files():
    return os.listdir(PATH)


# Encrypt file
def encrypt_file(file_name):
    key = get_random_bytes(16)  # Generate a 128-bit key for AES
    with open(fr"{PATH}\{file_name}", "rb") as file:
        file_data = file.read()

    # Generate cipher object and encrypt data
    cipher = AES.new(key, AES.MODE_CBC)
    encrypted_data = cipher.encrypt(pad(file_data, AES.block_size))

    # Write IV and encrypted data to file
    with open(fr"{PATH}\{file_name}", "wb") as file:
        file.write(cipher.iv)  # Prepend IV for decryption
        file.write(encrypted_data)

    # Save the key
    with open(fr"{KEY_PATH}\{file_name}_key", "wb") as key_file:
        key_file.write(key)

    time.sleep(1)
    print(f"The file '{file_name}' has been encrypted.")


def create_file():
    files = check_files()
    print("-" * 100)
    print("Files in the current directory:")
    for i, file in enumerate(files, 1):
        print(f"{i}. {file}")
    print("-" * 100)

    file_name = input("File name: \n    $ ").lower().strip()
    if file_name in check_files():
        print("The name already exists!")
        time.sleep(1)
    else:
        # Create file and open it in Notepad
        with open(fr"{PATH}\{file_name}", "w") as file:
            pass  # Just to create an empty file
        process = subprocess.Popen(["notepad.exe", fr"{PATH}\{file_name}"])
        process.wait()  # Wait until Notepad is closed

        # Encrypt the file
        encrypt_file(file_name)


def delete_file():
    # List existing files in the directory
    files = check_files()

    if not files:
        print("There are no files in this folder.")
        return  # Exit the function early if no files are found

    print("-" * 100)
    print("Files in the current directory:")
    for i, file in enumerate(files, 1):
        print(f"{i}. {file}")
    print("-" * 100)

    # Prompt the user for the file name
    file_name = input("\nEnter the name of the file you want to delete: \n    $ ").lower().strip()

    # Check if the file exists in the main directory
    if file_name in files:
        # Confirm deletion
        confirm = input(f"Are you sure you want to delete '{file_name}'? (yes/no): \n    $ ").strip().lower()
        if confirm == "yes":
            # Remove the file from the main directory
            os.remove(fr"{PATH}\{file_name}")
            print(f"File '{file_name}' has been deleted from the main directory.")

            # Check and remove the key file from the Keys directory
            key_file_path = fr"{KEY_PATH}\{file_name}_key"
            if os.path.exists(key_file_path):
                os.remove(key_file_path)
                print(f"Key file for '{file_name}' has been deleted from the Keys directory.")
            else:
                print(f"No key file found for '{file_name}' in the Keys directory.")
        else:
            print("File deletion canceled.")
    else:
        print(f"The file '{file_name}' does not exist in the current directory.")


# Decrypt file
def decrypt_file():
    files = check_files()
    print("-" * 100)
    print("Files in the current directory:")
    for i, file in enumerate(files, 1):
        print(f"{i}. {file}")
    print("-" * 100)

    # Check if the file exists
    file_name = input("File name: ").strip()
    if not os.path.exists(fr"{PATH}\{file_name}"):
        print(f"The file '{file_name}' does not exist in the directory.")
        return

    # Check if the key exists
    key_path = fr"{KEY_PATH}\{file_name}_key"
    if not os.path.exists(key_path):
        print(f"The key for '{file_name}' does not exist in the Keys directory.")
        return

    # Load the encryption key
    with open(key_path, "rb") as key_file:
        key = key_file.read()  # Assign key

    # Read the encrypted file
    with open(fr"{PATH}\{file_name}", "rb") as file:
        iv = file.read(16)  # The first 16 bytes are the IV
        encrypted_data = file.read()

    # Decrypt the file
    try:
        cipher = AES.new(key, AES.MODE_CBC, iv)
        decrypted_data = unpad(cipher.decrypt(encrypted_data), AES.block_size)
    except Exception as e:
        print(f"Error during decryption: {e}")
        return

    # Print the decrypted data
    print(f"Decrypted data from '{file_name}':")
    print("_" * 100)
    print(decrypted_data.decode())  # Assuming the data is text-based
    print("_" * 100)


def clear_all_files():
    # List all files in the main directory
    files = os.listdir(PATH)
    if not files:
        print("The main directory is already empty.")
    else:
        for file in files:
            file_path = os.path.join(PATH, file)
            if os.path.isfile(file_path):  # Ensure it's a file
                os.remove(file_path)
        print("All files in the main directory have been deleted.")

    # List all files in the Keys directory
    key_files = os.listdir(KEY_PATH)
    if not key_files:
        print("The Keys directory is already empty.")
    else:
        for key_file in key_files:
            key_file_path = os.path.join(KEY_PATH, key_file)
            if os.path.isfile(key_file_path):  # Ensure it's a file
                os.remove(key_file_path)
        print("All files in the Keys directory have been deleted.")


# Main program loop
while True:
    print("\nOptions:")
    print("1. Create a file.")
    print("2. Delete a file.")
    print("3. Show a file Decrypted")
    print("4. Clear all files.")
    print("5. Exit")

    choice = input("Select an option (1/2/3/4): \n    $ ").strip()
    if choice == "1":
        create_file()
    elif choice == "2":
        delete_file()
    elif choice == "3":
        decrypt_file()
    elif choice == "4":
        clear_all_files()
    elif choice == "5":
        print("Goodbye!")
        break
    else:
        print("Invalid option. Please try again.")
