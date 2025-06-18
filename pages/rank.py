# 필요한 라이브러리 임포트
import customtkinter as ctk  # 사용자 지정 스타일이 가능한 tkinter 확장 GUI 라이브러리
from PIL import Image, ImageTk  # 이미지 처리 라이브러리 (logo 이미지 불러올 때 사용)
import os, subprocess, sys    # 시스템 경로, 외부 프로세스 실행, 파이썬 실행환경 정보 등 처리

# 창 기본 설정
window = ctk.CTk()  # CTk 윈도우 객체 생성
window.title("랭킹 페이지")  # 창 제목 설정
window.geometry("1920x1080")  # 창 크기 설정
window.configure(fg_color="#FBE6A2")  # 배경색 설정 (밝은 노랑색)

# 현재 선택된 메뉴 (초기값: JAVA)
selected_menu = ctk.StringVar(value="JAVA")

# 메뉴 버튼 리스트 (버튼 객체와 메뉴명 저장용)
menu_buttons = []

# 페이지 전환 함수: 선택된 언어 메뉴에 따라 해당 레벨 선택 화면 실행
def switch_page(menu_name):
    selected_menu.set(menu_name)  # 선택된 메뉴 상태 업데이트
    update_menu_styles()  # 스타일 업데이트
    print(f"'{menu_name}' 페이지로 전환")  # 디버깅용 출력

    # 메뉴 이름에 따라 실행할 파일 매핑
    file_mapping = {
        "JAVA": "java_level.py",
        "PYTHON": "python_level.py",
        "HTML": "html_level.py"
    }

    # 선택된 언어에 맞는 타겟 파일 가져오기
    target_file = file_mapping.get(menu_name, "level.py")

    # 파일 경로를 절대경로로 변환
    script_path = os.path.join(os.path.dirname(__file__), target_file)
    script_path = os.path.abspath(script_path)
    script_dir = os.path.dirname(script_path)

    # 해당 언어의 파일을 별도 프로세스로 실행
    subprocess.Popen(
        [sys.executable, script_path, menu_name],  # 인자: python 인터프리터, 파일 경로, 메뉴명
        cwd=script_dir  # 작업 디렉토리를 해당 스크립트 위치로 설정
    )

    # 현재 창은 일시적으로 숨김 (완전히 종료하진 않음)
    window.withdraw()

# 선택된 메뉴 버튼만 파란색으로 강조하는 함수
def update_menu_styles():
    for btn, name in menu_buttons:
        if selected_menu.get() == name:
            btn.configure(text_color="#2962FF", font=("Arial", 16, "bold"))  # 선택된 메뉴
        else:
            btn.configure(text_color="black", font=("Arial", 16))  # 비선택 메뉴

# 마이페이지로 이동하는 함수 (마이페이지는 별도 파일 실행)
def open_mypage():
    script_path = os.path.join(os.path.dirname(__file__), "mypage.py")
    script_path = os.path.abspath(script_path)
    script_dir = os.path.dirname(script_path)

    subprocess.Popen(
        [sys.executable, script_path],
        cwd=script_dir
    )
    window.withdraw()

# 상단 바 프레임 생성 (로고 + 메뉴 + 마이페이지)
top_frame = ctk.CTkFrame(window, height=80, fg_color="white", corner_radius=0)
top_frame.pack(fill="x", side="top")  # 상단 고정

# 로고 프레임 (좌측)
logo_frame = ctk.CTkFrame(top_frame, fg_color="transparent")
logo_frame.pack(side="left", padx=30, pady=20)

# 로고 이미지 불러오기
logo_path = os.path.join(os.path.dirname(__file__), "..", "assets", "logo.png")
logo_path = os.path.abspath(logo_path)
logo_image = ctk.CTkImage(Image.open(logo_path), size=(60, 60))

# 로고 이미지 라벨 생성
logo_label = ctk.CTkLabel(logo_frame, image=logo_image, text="")
logo_label.pack(side="left", padx=5)

# 로고 텍스트 라벨 (TACO)
logo_text = ctk.CTkLabel(logo_frame, text="TACO", font=("Arial", 22, "bold"), text_color="black")
logo_text.pack(side="left")

# 로고 아래 강조 밑줄
underline = ctk.CTkFrame(logo_frame, width=50, height=6, fg_color="#FFF59D", corner_radius=3)
underline.place(relx=0.5, rely=1, anchor="s", x=12, y=8)

# 가운데 메뉴 프레임 (JAVA / PYTHON / HTML 버튼)
menu_frame = ctk.CTkFrame(top_frame, fg_color="transparent")
menu_frame.pack(side="left", padx=80)

menus = ["JAVA", "PYTHON", "HTML"]
for menu in menus:
    btn = ctk.CTkButton(
        menu_frame,
        text=menu,
        command=lambda m=menu: switch_page(m),  # 버튼 클릭 시 페이지 전환
        fg_color="transparent",
        hover_color="#f1f1f1",
        text_color="black",
        font=("Arial", 16),
        width=60,
        height=30,
    )
    btn.pack(side="left", padx=20)
    menu_buttons.append((btn, menu))  # 버튼 저장 (스타일 변경용)

# 버튼 초기 스타일 적용
update_menu_styles()

# 오른쪽: 마이페이지 아이콘 (이모지 사용)
user_icon = ctk.CTkLabel(top_frame, text="◡̈", font=("Arial", 26), text_color="black", cursor="hand2")
user_icon.pack(side="right", padx=30)
user_icon.bind("<Button-1>", lambda e: open_mypage())  # 클릭 시 마이페이지로 이동

# 메인 화면 - 제목과 드롭다운
title_frame = ctk.CTkFrame(window, fg_color="#FBE6A2")
title_frame.pack(pady=30)

# 언어 선택 드롭다운
dropdown = ctk.CTkOptionMenu(
    title_frame,
    values=menus,
    fg_color="#ffffff",
    text_color="black",
    button_color="#ffffff",
    button_hover_color="#f1f1f1",
    width=120
)
dropdown.set("JAVA")  # 기본 선택값
dropdown.pack(side="left", padx=10)

# "실시간 랭킹" 제목 라벨
title_label = ctk.CTkLabel(title_frame, text="실시간 랭킹", font=("Arial", 20, "bold"), text_color="black")
title_label.pack(side="left", padx=10)

# 메인 루프 실행 (GUI 시작)
window.mainloop()
