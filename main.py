import subprocess
import tkinter as tk


def close_window():
    root.destroy()


def run_recognize_face():
    subprocess.Popen(["python", "recognize_face.py"])


def run_register_face():
    subprocess.Popen(["python", "register_face.py"])


root = tk.Tk()
root.title("Nhan dien khuon mat")
root.geometry("500x200")

frame = tk.Frame(root)
frame.pack(expand=True, fill='both')

labelTitle = tk.Label(frame, text="NHAN DIEN KHUON MAT", font=("Arial", 18))
labelTitle.pack(pady=(20, 0))

btnRecognizeFace = tk.Button(frame, text="Nhan dien", width=15, font=("Arial", 12), command=run_recognize_face)
btnRecognizeFace.pack(side='left', padx=10)

btnRegisterFace = tk.Button(frame, text="Dang ki", width=15, font=("Arial", 12), command=run_register_face)
btnRegisterFace.pack(side='left', padx=10)

btnClose = tk.Button(frame, text="Close", width=15, font=("Arial", 12), command=close_window)
btnClose.pack(side='left', padx=10)

root.mainloop()
