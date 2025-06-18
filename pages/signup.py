import customtkinter as ctk  # GUI 생성을 위한 라이브러리
import subprocess  # 외부 프로세스 실행용
import sys  # 시스템 기능 사용
import os  # 파일 경로 관리
import db  # 데이터베이스 관리
db.create_tables()
# 함수 정의:
# back_login(): 로그인 페이지로 돌아가는 함수입니다. 현재 창을 닫고 login.py를 실행
# register_user(): 회원가입 처리를 담당
# 입력값 검증 (빈 값, 비밀번호 일치)
# 데이터베이스 연결 및 ID 중복 검사
# 새 사용자 등록

def back_login():
    subprocess.Popen([sys.executable, os.path.abspath("login.py")])
    window.withdraw()

def register_user():
    name = name_entry.get()
    user_id = id_entry.get()
    password = pw_entry.get()
    confirm_pw = confirm_pw_entry.get()

    if not name or not user_id or not password or not confirm_pw:
        print("모든 항목을 입력해주세요.")
        return

    if password != confirm_pw:
        print("비밀번호가 일치하지 않습니다.")
        return

    try:
        with db.get_connection() as conn:
            cursor = conn.cursor()

            # ID 중복 검사
            cursor.execute("SELECT id FROM users WHERE id = ?", (user_id,))
            if cursor.fetchone():
                print("이미 존재하는 ID입니다.")
                return

            # 회원가입
            cursor.execute(
                "INSERT INTO users (id, name, password) VALUES (?, ?, ?)",
                (user_id, name, password)
            )
            conn.commit()
            print("회원가입 완료!")
            back_login()
    except Exception as e:
        print(f"회원가입 실패: {e}")

window = ctk.CTk()
window.title("회원가입 페이지")
window.geometry("1920x1080")
window.configure(fg_color="#FBE6A2")

frame = ctk.CTkFrame(window, width=400, height=400, corner_radius=20, fg_color="white")
frame.place(relx=0.5, rely=0.5, anchor="center")

# 이름
name_label = ctk.CTkLabel(frame, text="이름", text_color="black", anchor="w")
name_label.place(x=30, y=30)
name_entry = ctk.CTkEntry(frame, width=300, height=40, fg_color="white", text_color="black")
name_entry.place(x=80, y=30)

# ID
id_label = ctk.CTkLabel(frame, text="ID", text_color="black", anchor="w")
id_label.place(x=30, y=90)
id_entry = ctk.CTkEntry(frame, width=300, height=40, fg_color="white", text_color="black")
id_entry.place(x=80, y=90)

# 비밀번호
pw_label = ctk.CTkLabel(frame, text="비밀번호", text_color="black", anchor="w")
pw_label.place(x=30, y=150)
pw_entry = ctk.CTkEntry(frame, width=300, height=40, fg_color="white", text_color="black", show="*")
pw_entry.place(x=80, y=150)

# 비밀번호 확인
confirm_pw_label = ctk.CTkLabel(frame, text="비밀번호 확인", text_color="black", anchor="w")
confirm_pw_label.place(x=30, y=210)
confirm_pw_entry = ctk.CTkEntry(frame, width=300, height=40, fg_color="white", text_color="black", show="*")
confirm_pw_entry.place(x=80, y=210)

# 확인 버튼
confirm_button = ctk.CTkButton(
    frame,
    text="가입하기",
    width=100,
    height=32,
    fg_color="black",
    hover_color="#333333",
    text_color="white",
    corner_radius=20,
    command=register_user
)
confirm_button.place(relx=0.5, rely=1.0, anchor="s", y=-30)

window.mainloop()
