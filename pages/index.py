import customtkinter as ctk
import subprocess
import os
import sys

def open_login_page():
    python = sys.executable
    subprocess.Popen(
        [python, "login.py"],
        cwd = os.getcwd(),  # 현재 작업 디렉토리
        stdout = subprocess.PIPE,
        stderr = subprocess.PIPE,
        start_new_session = True
    )
    root.destroy()

def open_signup_page():
    python = sys.executable
    subprocess.Popen(
        [python, "signup.py"],
        cwd = os.getcwd(),  # 현재 작업 디렉토리
        stdout = subprocess.PIPE,
        stderr = subprocess.PIPE,
        start_new_session = True
    )
    root.destroy()

# 기본 설정
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

root = ctk.CTk()
root.title("TACO")
root.geometry("1920x1080")
root.configure(fg_color = "#FBE6A2")

# 하얀 프레임
frame = ctk.CTkFrame(
    root,
    width = 400,
    height = 232,
    corner_radius = 20,
    fg_color = "white"
)
frame.place(
    relx = 0.5,
    rely = 0.5,
    anchor = "center"
)
frame.pack_propagate(False)

# 프레임 중앙 배치
container = ctk.CTkFrame(frame, fg_color = "transparent")
container.place(
    relx = 0.5,
    rely = 0.5,
    anchor = "center"
)

# 타이틀
title = ctk.CTkLabel(
    container,
    text = "TACO",
    font = ("pretendard", 32, "bold"),
    text_color="black")
title.pack(pady = (0, 20))

# 버튼 프레임
button_frame = ctk.CTkFrame(container, fg_color = "transparent")
button_frame.pack()

# 로그인 버튼
login_button = ctk.CTkButton(
    button_frame,
    text = "로그인",
    width = 130,
    height = 50,
    corner_radius = 15,
    fg_color = "white",
    text_color = "black",
    font = ("pretendard", 18),
    border_color = "gray",
    border_width = 1,
    hover_color = "#e0e0e0",
    command = open_login_page
)
login_button.grid(
    row = 0,
    column = 0,
    padx = 10,
    pady = 10,
    sticky = "ew"
)

# 회원 가입 버튼
signup_button = ctk.CTkButton(
    button_frame,
    text = "회원가입",
    width = 130,
    height = 50,
    corner_radius = 15,
    fg_color = "white",
    text_color = "black",
    font = ("pretendard", 18),
    border_color = "gray",
    border_width = 1,
    hover_color = "#e0e0e0",
    command = open_signup_page
    # master=tabview.tab("tab view")
)
signup_button.grid(
    row = 0,
    column = 1,
    padx = 10,
    pady = 10,
    sticky = "ew"
)

# 버튼 프레임 컬럼 설정
button_frame.grid_columnconfigure(0, weight=1)
button_frame.grid_columnconfigure(1, weight=1)

root.mainloop()