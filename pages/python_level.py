import customtkinter as ctk
import tkinter as tk
import subprocess
import sys
import os

# 난이도별 예제 코드:
# difficulty_codes 딕셔너리에 각 난이도별 Python 예제 코드 저장
# 초급: 기본 출력과 변수 사용
# 중급: 함수 정의와 리스트 활용
# 고급: 클래스와 메서드 구현

# 주요 함수
# center_window():
# 창을 화면 중앙에 위치시키는 기능

# show_error_message(error_msg):
# 오류 발생 시 모달 팝업 창으로 메시지 표시
# 빨간색 오류 제목과 상세 내용 표시
# 확인 버튼으로 창 닫기

# run_play_game(difficulty, code_lines):
# 선택된 난이도의 게임 실행
# play.py 파일 경로 찾기
# 환경변수로 게임 설정 전달
# 새 프로세스로 게임 실행

# on_difficulty_selected(level):
# 난이도 버튼 클릭 시 처리
# 해당 난이도의 코드 가져와서 게임 실행

# add_hover_effect(button):
# 버튼에 마우스 오버 효과 추가
# 배경색과 테두리 색상 변경

window = ctk.CTk()
window.title("PYTHON 난이도 선택")
window.geometry("1920x1080")
window.configure(fg_color="#FBE6A2")

def center_window():
    window.update_idletasks()
    width = window.winfo_width()
    height = window.winfo_height()
    x = (window.winfo_screenwidth() // 2) - (width // 2)
    y = (window.winfo_screenheight() // 2) - (height // 2)
    window.geometry(f'{width}x{height}+{x}+{y}')

center_window()


difficulty_codes = {
    "초급": [
        "print('Hello World')",
        "name = 'Python'",
        "print(f'Hello, {name}!')"
    ],
    "중급": [
        "def calculate_sum(a, b, c):",
        "    return a + b + c",
        "",
        "numbers = [10, 20, 30]",
        "result = calculate_sum(*numbers)",
        "print(f'Sum: {result}')"
    ],
    "고급": [
        "class Calculator:",
        "    def __init__(self):",
        "        self.result = 0.0",
        "    ",
        "    def add(self, a, b):",
        "        self.result = a + b",
        "        return self.result",
        "    ",
        "    def multiply(self, a, b):",
        "        self.result = a * b",
        "        return self.result",
        "",
        "calc = Calculator()",
        "print(calc.add(10.5, 20.3))",
        "print(calc.multiply(5.5, 4.2))"
    ]
}

# 오류 발생 시 팝업창으로 메시지를 띄우는 함수
def show_error_message(error_msg):
    error_window = ctk.CTkToplevel(window)  # 새로운 창 (모달)
    error_window.title("오류")
    error_window.geometry("500x250")
    error_window.configure(fg_color="white")
    error_window.resizable(False, False)    # 창 크기 변경 불가

    error_window.transient(window)          # 부모 창 위에 항상 위치
    error_window.grab_set()                 # 다른 창 클릭 방지 (모달)

    # 메시지 컨테이너 프레임
    message_container = ctk.CTkFrame(error_window, fg_color="white")
    message_container.pack(fill="both", expand=True, padx=30, pady=30)

    # 오류 제목
    error_label = ctk.CTkLabel(
        message_container,
        text="게임 실행 중 오류가 발생했습니다:",
        font=("Arial", 16, "bold"),
        text_color="red"
    )
    error_label.pack(pady=(10, 5))

    # 오류 상세 내용
    detail_label = ctk.CTkLabel(
        message_container,
        text=error_msg,
        font=("Arial", 12),
        text_color="black",
        wraplength=400                  # 너무 길면 줄바꿈
    )
    detail_label.pack(pady=(5, 20))

    # 확인 버튼 (창 닫기용)
    ok_button = ctk.CTkButton(
        message_container,
        text="확인",
        width=100,
        height=40,
        font=("Arial", 16, "bold"),
        fg_color="#FF6B6B",            # 빨간색
        text_color="white",
        hover_color="#FF5252",         # 호버 시 더 진한 빨간색
        corner_radius=10,
        command=error_window.destroy   # 버튼 클릭 시 창 닫기
    )
    ok_button.pack(pady=10)


# 난이도와 코드 목록을 받아 play.py 파일을 새 프로세스로 실행하는 함수
def run_play_game(difficulty, code_lines):
    try:
        base_dir = os.path.dirname(os.path.abspath(__file__))  # 현재 파일의 디렉토리 경로

        # 여러 위치에서 play.py 파일 탐색
        possible_paths = [
            os.path.join(base_dir, "play.py"),
            os.path.join(base_dir, "pages", "play.py")
        ]

        play_file_path = None
        for path in possible_paths:
            if os.path.exists(path):   # 파일이 존재하면
                play_file_path = path
                break

        if not play_file_path:
            raise FileNotFoundError("play.py 파일을 찾을 수 없습니다.")

        window.destroy()  # 현재 난이도 선택 창 닫기

        # 환경변수 구성
        env = os.environ.copy()
        env['GAME_DIFFICULTY'] = difficulty
        env['GAME_CODE'] = '|'.join(code_lines)  # 코드 여러 줄을 | 로 연결해서 문자열로 넘김
        env['GAME_LANGUAGE'] = 'PYTHON'

        # 외부 play.py 실행
        subprocess.Popen([sys.executable, play_file_path], env=env)

    except Exception as e:
        show_error_message(str(e))  # 오류 발생 시 팝업 표시


def on_difficulty_selected(level):
    print(f"선택된 PYTHON 난이도: {level}")
    selected_code = difficulty_codes.get(level, [])
    run_play_game(level, selected_code)

def add_hover_effect(button):
    def on_enter(event):
        button.configure(fg_color="#F5F5F5", border_color="#D0D0D0")

    def on_leave(event):
        button.configure(fg_color="white", border_color="#E0E0E0")

    button.bind("<Enter>", on_enter)
    button.bind("<Leave>", on_leave)


main_frame = ctk.CTkFrame(window, fg_color="#FBE6A2")
main_frame.pack(fill="both", expand=True, padx=50, pady=50)

title_label = ctk.CTkLabel(
    main_frame,
    text="PYTHON 난이도 선택",
    font=("Arial", 48, "bold"),
    text_color="black",
    fg_color="transparent"
)
title_label.pack(pady=(50, 80))

button_container = ctk.CTkFrame(main_frame, fg_color="#FBE6A2")
button_container.pack(expand=True, fill="both")

buttons_frame = ctk.CTkFrame(button_container, fg_color="#FBE6A2")
buttons_frame.pack(expand=True)

for level in ["초급", "중급", "고급"]:
    button_frame = ctk.CTkFrame(buttons_frame, fg_color="#FBE6A2")
    button_frame.pack(side="left", padx=40, pady=50)

    btn = ctk.CTkButton(
        button_frame,
        text=level,
        width=200,
        height=250,
        font=("Arial", 28, "bold"),
        fg_color="white",
        text_color="black",
        hover_color="#F0F0F0",
        corner_radius=20,
        border_width=2,
        border_color="#E0E0E0",
        command=lambda l=level: on_difficulty_selected(l)
    )
    btn.pack()

    add_hover_effect(btn)

# 앱 실행
window.mainloop()