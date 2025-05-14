import customtkinter as ctk
import subprocess
import sys
import os

def go_back_signup():
    subprocess.Popen([sys.executable, os.path.abspath("signup.py")])
    window.destroy()

# 비밀번호 표시 토글용 변수
pw_visible = False

def toggle_password():
    global pw_visible
    if pw_visible:
        pw_entry.configure(show = "*")  # 비밀번호 가리기
        password_toggle_button.configure(text = "비밀번호 확인하기")
        pw_visible = False
    else:
        pw_entry.configure(show = "")  # 비밀번호 보이기
        password_toggle_button.configure(text = "비밀번호 숨기기")
        pw_visible = True

window = ctk.CTk()
window.title("로그인 페이지")
window.geometry("1920x1080")
window.configure(fg_color = "#FBE6A2")

# 하얀색 프레임
frame = ctk.CTkFrame(
    window,
    width = 400,
    height = 232,
    corner_radius = 20,
    fg_color = "white"
)
frame.place(relx = 0.5, rely = 0.5, anchor = "center")

# ID 라벨
id_label = ctk.CTkLabel(
    frame,
    text = "ID",
    text_color = "black",
    anchor = "w"
)
id_label.place(x = 30, y = 30)

# ID 입력창
id_entry = ctk.CTkEntry(
    frame,
    width = 300,
    height = 40,
    fg_color = "white",
    text_color = "black"
)
id_entry.place(x = 80, y = 30)

# PW 라벨
pw_label = ctk.CTkLabel(
    frame,
    text = "PW",
    text_color = "black",
    anchor = "w"
)
pw_label.place(x = 30, y = 100)

# PW 입력창
pw_entry = ctk.CTkEntry(
    frame,
    width = 300,
    height = 40,
    fg_color = "white",
    text_color = "black",
    show = "*"
)
pw_entry.place(x = 80, y = 105)

# 회원 가입 버튼 (회색)
signup_button = ctk.CTkButton(
    frame,
    text = "회원가입 하러 가기",
    command = go_back_signup,
    width = 120,
    height = 24,
    fg_color = "#CCCCCC",
    hover_color = "#AAAAAA",
    text_color = "black"
)
signup_button.place(x = 260, y = 75)

# 비밀번호 확인 버튼
password_toggle_button = ctk.CTkButton(
    frame,
    text = "비밀번호 확인하기",
    command = toggle_password,
    width = 120,
    height = 24,
    fg_color = "#CCCCCC",
    hover_color = "#AAAAAA",
    text_color = "black"
)
password_toggle_button.place(x = 260, y = 150)

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
    # command = go_back_login
)
confirm_button.place(relx = 0.5, rely = 1.0, anchor = "s", y = -10)

window.mainloop()
