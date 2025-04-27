import customtkinter as ctk
import subprocess
import sys
import os

def back_login():
    subprocess.Popen([sys.executable, os.path.abspath("login.py")])
    window.destroy()

window = ctk.CTk()
window.title("회원가입 페이지")
window.geometry("1920x1080")
window.configure(fg_color="#FBE6A2")

# 하얀색 프레임
frame = ctk.CTkFrame(
    window,
    width = 400,
    height = 332,
    corner_radius = 20,
    fg_color = "white"
)
frame.place(relx = 0.5, rely = 0.5, anchor = "center")  # 화면 가운데 정렬

# 이름 라벨
id_label = ctk.CTkLabel(
    frame,
    text = "이름",
    text_color = "black",
    anchor = "w"
)
id_label.place(x = 30, y = 50)

# 이름 입력창
id_entry = ctk.CTkEntry(
    frame,
    width = 300,
    height = 40,
    fg_color = "white",
    text_color = "black"
)
id_entry.place(x = 80, y = 50)

# ID 라벨
id_label = ctk.CTkLabel(
    frame,
    text = "ID",
    text_color = "black",
    anchor = "w"
)
id_label.place(x = 30, y = 130)

# ID 입력창
id_entry = ctk.CTkEntry(
    frame,
    width = 300,
    height = 40,
    fg_color = "white",
    text_color = "black"
)
id_entry.place(x = 80, y = 130)

# PW 라벨
pw_label = ctk.CTkLabel(
    frame,
    text = "PW",
    text_color = "black",
    anchor = "w"
)
pw_label.place(x = 30, y = 210)

# PW 입력창
pw_entry = ctk.CTkEntry(
    frame,
    width = 300,
    height = 40,
    fg_color = "white",
    text_color = "black",
    show = "*"
)
pw_entry.place(x = 80, y = 210)

# 확인 버튼
confirm_button = ctk.CTkButton(
    frame,
    text = "확인",
    width = 100,
    height = 32,
    fg_color = "black",
    hover_color = "#333333",
    text_color = "white",
    corner_radius = 20,
    command = back_login
)
confirm_button.place(relx = 0.5, rely = 1.0, anchor = "s", y = -30)  # 박스 아래쪽에 배치

window.mainloop()
