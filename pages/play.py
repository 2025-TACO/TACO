import customtkinter as ctk
import tkinter as tk
from tkinter import ttk
import time
import subprocess
import sys


class CodingTypingGame:
    def __init__(self):
        # 커스텀TK 인터페이스의 테마 설정
        ctk.set_appearance_mode("light")  # 라이트 모드 설정
        ctk.set_default_color_theme("blue")  # 기본 색상 테마를 파란색으로 지정

        # 메인 윈도우 설정
        self.root = ctk.CTk()
        self.root.title("코딩 타자 게임")  # 창 제목 설정
        self.root.geometry("1920x1080")  # 창 크기 설정
        self.root.configure(fg_color="#FBE6A2")  # 배경색 설정 (노란색 계열)

        # 타자 게임 단계별 문장 리스트
        self.typing_stages = [
            "public class Main{",
            "    public static void main(String[] args){",
            "        int a = 1; int b = 2; int c = 3;",
            "        System.out.println(a + b + c);",
            "    }",
            "}"
        ]

        # 현재 게임 상태 관련 변수들
        self.current_stage = 0  # 현재 단계 (index)
        self.current_position = 0  # 현재 타이핑 위치
        self.typed_text = ""  # 현재까지 입력한 문자열
        self.start_time = None  # 타자 시작 시간
        self.errors = 0  # 오타 횟수
        self.total_chars = 0  # 입력한 총 문자 수

        self.error_positions = set()  # 오타가 발생한 위치들을 저장

        self.completed_inputs = []  # 각 단계에서 입력한 최종 문자열 저장

        # 통계 변수들
        self.typing_speed = 0  # 타자 속도 (타자수/분)
        self.accuracy = 100.0  # 정확도 %
        self.elapsed_time = "0:00"  # 경과 시간 문자열
        self.game_completed = False  # 게임이 완료되었는지 여부

        # UI 설정 및 이벤트 바인딩, 타이머 시작
        self.setup_ui()  # 사용자 인터페이스 구성
        self.bind_keyboard_events()  # 키보드 입력 이벤트 등록
        self.start_timer()  # 타이머 시작

    def setup_ui(self):
        # 메인 프레임 생성
        main_frame = ctk.CTkFrame(self.root, fg_color="#FBE6A2")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # 상단 헤더 구성
        self.create_header(main_frame)

        # 콘텐츠 영역 프레임 (좌우 레이아웃)
        content_frame = ctk.CTkFrame(main_frame, fg_color="#FBE6A2")
        content_frame.pack(fill="both", expand=True, pady=(20, 0))

        # 왼쪽 사이드바 구성
        self.create_sidebar(content_frame)

        # 오른쪽 메인 콘텐츠 구성
        self.create_main_content(content_frame)

    def create_header(self, parent):
        # 상단 헤더 프레임 생성
        header_frame = ctk.CTkFrame(parent, fg_color="#FBE6A2", height=60)
        header_frame.pack(fill="x", pady=(0, 10))
        header_frame.pack_propagate(False)

        # 돌아가기 버튼 생성
        back_btn = ctk.CTkButton(
            header_frame,
            text="< 돌아가기",  # 버튼 텍스트
            fg_color="white",  # 배경색
            text_color="black",  # 글자색
            hover_color="#E6D68A",  # 마우스 오버 시 색상
            width=100,
            height=40,
            border_width=1,
            border_color="black",
            command=self.go_back  # 버튼 클릭 시 실행할 함수
        )
        back_btn.pack(side="left", padx=10, pady=10)

    def create_sidebar(self, parent):
        # 사이드바 프레임 (왼쪽)
        sidebar_frame = ctk.CTkFrame(parent, width=280, fg_color="white")
        sidebar_frame.pack(side="left", fill="y", padx=(0, 20))
        sidebar_frame.pack_propagate(False)

        # 프로필 사진 프레임 (원형으로 표시)
        profile_frame = ctk.CTkFrame(sidebar_frame, width=100, height=100, fg_color="#D3D3D3", corner_radius=50)
        profile_frame.pack(pady=(30, 30))
        profile_frame.pack_propagate(False)

        # 통계 라벨 구성 (시간, 속도, 정확도)
        self.time_label = self.create_stat_row(sidebar_frame, "진행시간", "0:00")
        self.speed_label = self.create_stat_row(sidebar_frame, "타수(타/분)", "0")
        self.accuracy_label = self.create_stat_row(sidebar_frame, "정확도(%)", "100.00")

        # 사이드바 진행도 바
        self.progress_bar = ctk.CTkProgressBar(sidebar_frame, width=220, height=15, progress_color="#FF6B6B")
        self.progress_bar.pack(pady=(20, 10), padx=20)
        self.progress_bar.set(0.0)

        # 오타 수 라벨
        self.error_label = ctk.CTkLabel(sidebar_frame, text="오답 0", text_color="red", font=("Arial", 12, "bold"))
        self.error_label.pack(pady=(5, 20))

    def create_stat_row(self, parent, label, value):
        # 통계 항목 하나 구성 (이름 + 값)
        stat_frame = ctk.CTkFrame(parent, fg_color="white")
        stat_frame.pack(fill="x", padx=20, pady=8)

        stat_label = ctk.CTkLabel(stat_frame, text=label, text_color="black", font=("Arial", 12))
        stat_label.pack(side="left")

        value_label = ctk.CTkLabel(stat_frame, text=value, text_color="black", font=("Arial", 12, "bold"))
        value_label.pack(side="right")

        return value_label  # 나중에 업데이트 가능하도록 반환

    def create_main_content(self, parent):
        # 메인 콘텐츠 프레임 (오른쪽 영역)
        main_content_frame = ctk.CTkFrame(parent, fg_color="#FBE6A2")
        main_content_frame.pack(side="right", fill="both", expand=True)

        # 코드 타이핑 표시 영역 구성
        self.create_code_section(main_content_frame)

        # 키보드 시각화 영역 구성
        self.create_keyboard_section(main_content_frame)

    def create_code_section(self, parent):
        # 코드 표시 컨테이너
        code_container = ctk.CTkFrame(parent, fg_color="#FBE6A2")
        code_container.pack(fill="x", pady=(0, 20), padx=20)

        # 현재 입력 중인 코드 블록
        self.class_frame = ctk.CTkFrame(code_container, fg_color="white", corner_radius=15)
        self.class_frame.pack(fill="x", pady=(0, 10))

        self.class_text_display = tk.Text(
            self.class_frame,
            height=3,
            font=("Consolas", 16),  # 고정폭 글꼴
            wrap="word",
            bg="white",
            relief="flat",
            bd=0,
            padx=20,
            pady=20,
            state="disabled"
        )
        self.class_text_display.pack(fill="x", padx=20, pady=20)

        # 코드 텍스트의 스타일링 태그 정의
        self.class_text_display.tag_configure("correct", foreground="green", background="#E8F5E8")
        self.class_text_display.tag_configure("incorrect", foreground="red", background="#FFE8E8")
        self.class_text_display.tag_configure("current", background="#FFFFCC")
        self.class_text_display.tag_configure("remaining", foreground="gray")

        # 전체 코드 표시용 (완료된 단계 포함)
        self.main_code_frame = ctk.CTkFrame(code_container, fg_color="white", corner_radius=15)
        self.main_code_frame.pack(fill="x")

        self.main_text_display = tk.Text(
            self.main_code_frame,
            height=6,
            font=("Consolas", 16),
            wrap="word",
            bg="white",
            relief="flat",
            bd=0,
            padx=20,
            pady=20,
            state="disabled"
        )
        self.main_text_display.pack(fill="x", padx=20, pady=20)

        self.main_text_display.tag_configure("correct", foreground="green", background="#E8F5E8")
        self.main_text_display.tag_configure("incorrect", foreground="red", background="#FFE8E8")
        self.main_text_display.tag_configure("current", background="#FFFFCC")
        self.main_text_display.tag_configure("remaining", foreground="gray")
        self.main_text_display.tag_configure("completed", foreground="blue")

        # 처음에 텍스트 표시 업데이트
        self.update_text_display()

    def create_keyboard_section(self, parent):
        keyboard_frame = ctk.CTkFrame(parent, fg_color="white", corner_radius=15)
        keyboard_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        # 진행도 바
        progress_container = ctk.CTkFrame(keyboard_frame, fg_color="white")
        progress_container.pack(fill="x", padx=20, pady=15)

        self.main_progress = ctk.CTkProgressBar(progress_container, width=900, height=20, progress_color="#FF6B6B")
        self.main_progress.pack()
        self.main_progress.set(0.0)

        # 키보드 레이아웃 컨테이너
        keyboard_container = ctk.CTkFrame(keyboard_frame, fg_color="white")
        keyboard_container.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        # 키보드를 가운데 정렬하기 위한 프레임
        keyboard_center_frame = ctk.CTkFrame(keyboard_container, fg_color="white")
        keyboard_center_frame.pack(expand=True)

        # 키보드 행 정의
        keyboard_rows = [
            ["`", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "-", "=", "Backspace"],
            ["Tab", "q", "w", "e", "r", "t", "y", "u", "i", "o", "p", "[", "]", "\\"],
            ["Caps", "a", "s", "d", "f", "g", "h", "j", "k", "l", ";", "'", "Enter"],
            ["Shift", "z", "x", "c", "v", "b", "n", "m", ",", ".", "/", "Shift"],
            ["Ctrl", "Alt", "Space", "Alt", "Ctrl"]
        ]

        self.key_buttons = {}

        for row_idx, row in enumerate(keyboard_rows):
            row_frame = ctk.CTkFrame(keyboard_center_frame, fg_color="white")
            row_frame.pack(pady=3)

            for key in row:
                # 키 크기 조정
                key_width = 70
                if key in ["Backspace"]:
                    key_width = 200
                elif key == "Enter":
                    key_width = 160
                elif key == "Space":
                    key_width = 500
                elif key in ["Tab", "Caps", "Shift"]:
                    key_width = 140

                key_btn = ctk.CTkButton(
                    row_frame,
                    text=key if key != "Space" else "Space",
                    width=key_width,
                    height=70,
                    fg_color="#F0F0F0",
                    text_color="black",
                    hover_color="#E0E0E0",
                    corner_radius=8,
                    font=("Arial", 11)
                )
                key_btn.pack(side="left", padx=2)

                # 키 버튼 저장
                self.key_buttons[key.lower()] = key_btn
                if key == "Space":
                    self.key_buttons[" "] = key_btn

    def bind_keyboard_events(self):
        self.root.bind('<Key>', self.on_key_press)
        self.root.bind('<KeyPress>', self.on_key_press)
        self.root.focus_set()

    def start_timer(self):
        # 타이머 시작 (게임 시작과 동시에)
        self.start_time = time.time()
        self.update_timer()

    def update_timer(self):
        # 진행시간 업데이트
        if self.start_time:
            elapsed = time.time() - self.start_time
            minutes = int(elapsed // 60)
            seconds = int(elapsed % 60)
            self.elapsed_time = f"{minutes}:{seconds:02d}"
            self.time_label.configure(text=self.elapsed_time)

        # 1초마다 업데이트
        self.root.after(1000, self.update_timer)

    def on_key_press(self, event):
        char = event.char
        key = event.keysym.lower()

        # 특수키 처리
        if key == "backspace":
            self.handle_backspace()
            return
        elif key == "return" or key == "enter":
            self.handle_enter()
            return
        elif key == "tab":
            self.handle_tab()
            return
        elif key in ["shift_l", "shift_r", "control_l", "control_r", "alt_l", "alt_r"]:
            return
        elif not char or ord(char) < 32:  # 제어문자 무시
            return

        self.handle_character_input(char)   

    def handle_tab(self):
        # Tab 키를 공백 4개로 처리
        tab_spaces = "    "  # 4개의 공백

        if self.current_stage >= len(self.typing_stages):
            return

        target_text = self.typing_stages[self.current_stage]

        # Tab 키 하이라이트
        if "tab" in self.key_buttons:
            self.key_buttons["tab"].configure(fg_color="#FBE6A2")
            self.root.after(300, self.reset_key_colors)

        # Tab을 공백 4개로 처리
        for space in tab_spaces:
            if self.current_position >= len(target_text):
                break

            target_char = target_text[self.current_position]
            self.total_chars += 1

            if space == target_char:
                self.typed_text += space
                self.current_position += 1
            else:
                # 틀린 경우 오류 처리
                self.errors += 1
                self.error_positions.add(self.current_position)  # 오타 위치 기록
                self.typed_text += space
                self.current_position += 1

        self.update_display()

    def handle_character_input(self, char):
        if self.current_stage >= len(self.typing_stages):
            return

        target_text = self.typing_stages[self.current_stage]

        if self.current_position >= len(target_text):
            return

        target_char = target_text[self.current_position]
        self.total_chars += 1

        # 키보드 하이라이트
        self.highlight_key(char)

        if char == target_char:
            # 이전에 이 위치에서 오타가 있었는지 확인
            if self.current_position in self.error_positions:
                self.error_positions.remove(self.current_position)

            self.typed_text += char
            self.current_position += 1
        else:
            # 틀린 경우 오류 처리
            if self.current_position not in self.error_positions:
                self.errors += 1
                self.error_positions.add(self.current_position)  # 오타 위치 기록

            self.typed_text += char
            self.current_position += 1

        self.update_display()

    def handle_enter(self):
        # 현재 단계의 입력 내용을 저장
        if self.current_stage < len(self.typing_stages):
            self.completed_inputs.append(self.typed_text)

        # 현재 단계가 완료되었는지 확인하지 않고 무조건 다음 단계로
        if self.current_stage < len(self.typing_stages) - 1:
            # 다음 단계로 이동
            self.current_stage += 1
            self.current_position = 0
            self.typed_text = ""
            self.error_positions.clear()  # 새 단계에서는 오타 위치 초기화
            self.update_display()
        elif self.current_stage == len(self.typing_stages) - 1:
            # 마지막 단계에서 엔터를 누르면 완료
            self.current_stage += 1
            self.current_position = 0
            self.typed_text = ""
            self.game_completed = True
            self.update_display()
            self.show_completion_message()

        # Enter 키 하이라이트
        if "enter" in self.key_buttons:
            self.key_buttons["enter"].configure(fg_color="#FBE6A2")
            self.root.after(300, self.reset_key_colors)

        def handle_backspace(self):
            if self.current_position > 0:
                # 현재 커서보다 한 칸 앞의 위치를 삭제 대상 위치로 지정
                delete_position = self.current_position - 1

                # 커서 위치를 한 칸 뒤로 이동
                self.current_position -= 1

                # typed_text 문자열에서 마지막 문자 제거
                self.typed_text = self.typed_text[:-1]

                # 삭제한 위치가 오타였는지 확인하여 에러 정보 갱신
                if delete_position in self.error_positions:
                    self.error_positions.remove(delete_position)
                    if self.errors > 0:
                        self.errors -= 1  # 오타 수 감소

                # 디스플레이 갱신 (텍스트/진행률/통계)
                self.update_display()

            # 백스페이스 키 하이라이트 효과 적용
            if "backspace" in self.key_buttons:
                self.key_buttons["backspace"].configure(fg_color="#FBE6A2")
                self.root.after(300, self.reset_key_colors)  # 0.3초 후 색상 리셋

    def highlight_key(self, char):
        # 모든 키 버튼의 색상을 기본값으로 되돌림
        for key_btn in self.key_buttons.values():
            key_btn.configure(fg_color="#F0F0F0")

        # 눌린 키의 색상을 강조 색으로 설정
        key = char.lower()
        if key in self.key_buttons:
            self.key_buttons[key].configure(fg_color="#FBE6A2")
        elif char == ' ' and ' ' in self.key_buttons:
            self.key_buttons[' '].configure(fg_color="#FBE6A2")

        # 0.3초 후 원래 색상으로 복원
        self.root.after(300, self.reset_key_colors)

    def reset_key_colors(self):
        # 모든 키의 색상을 기본값으로 초기화
        for key_btn in self.key_buttons.values():
            key_btn.configure(fg_color="#F0F0F0")

    def update_display(self):
        # 텍스트 영역, 통계, 진행도 업데이트
        self.update_text_display()
        self.update_stats()
        self.update_progress()

    def update_text_display(self):
        # 현재 단계의 타이핑 영역 업데이트
        self.class_text_display.config(state="normal")
        self.class_text_display.delete(1.0, tk.END)

        if self.current_stage < len(self.typing_stages):
            # 현재 타이핑할 텍스트 가져오기
            target_text = self.typing_stages[self.current_stage]
            self.class_text_display.insert(tk.END, target_text + "\n", "remaining")

            # 사용자가 입력한 텍스트와 비교하여 색상 표시
            for i, char in enumerate(self.typed_text):
                if i < len(target_text) and char == target_text[i]:
                    self.class_text_display.insert(tk.END, char, "correct")  # 정답
                else:
                    self.class_text_display.insert(tk.END, char, "incorrect")  # 오답

            # 커서 위치 표시 (| 기호로)
            if self.current_position < len(target_text):
                self.class_text_display.insert(tk.END, "|", "current")
        else:
            # 모든 단계 완료 시 메시지 출력
            self.class_text_display.insert(tk.END, "모든 단계 완료!", "completed")

        self.class_text_display.config(state="disabled")

        # 아래쪽 메인 텍스트 창에 다음 단계들 미리보기 표시
        self.main_text_display.config(state="normal")
        self.main_text_display.delete(1.0, tk.END)

        if self.current_stage < len(self.typing_stages):
            remaining_stages = len(self.typing_stages) - self.current_stage - 1
            if remaining_stages > 0:
                for stage_idx in range(self.current_stage + 1, len(self.typing_stages)):
                    self.main_text_display.insert(tk.END, f"{self.typing_stages[stage_idx]}\n", "remaining")

        self.main_text_display.config(state="disabled")

    def update_stats(self):
        # 타수 계산: 현재까지 타이핑한 글자 수 / 경과 시간 * 60
        if self.start_time:
            elapsed = time.time() - self.start_time
            if elapsed > 0:
                total_typed_chars = sum(
                    len(self.typing_stages[i]) for i in range(self.current_stage)) + self.current_position
                self.typing_speed = int((total_typed_chars / elapsed) * 60)

        # 정확도 계산: 전체 글자 수 대비 오타 비율
        if self.total_chars > 0:
            self.accuracy = max(0, 100 - (self.errors / self.total_chars * 100))
        else:
            self.accuracy = 100.0

        # 화면에 통계 수치 표시
        self.speed_label.configure(text=str(self.typing_speed))
        self.accuracy_label.configure(text=f"{self.accuracy:.2f}")
        self.error_label.configure(text=f"오답 {self.errors}")

    def update_progress(self):
        # 전체 진행도 계산 (타이핑한 글자 수 / 전체 글자 수)
        total_chars = sum(len(stage) for stage in self.typing_stages)
        completed_chars = sum(len(self.typing_stages[i]) for i in range(self.current_stage))
        completed_chars += self.current_position

        progress = completed_chars / total_chars if total_chars > 0 else 0
        self.main_progress.set(progress)
        self.progress_bar.set(progress)

        # 완료 메시지는 여기서 호출하지 않음

    def show_completion_message(self):
        # 이미 메시지를 표시한 경우 재표시 방지
        if hasattr(self, 'completion_shown') and self.completion_shown:
            return
        self.completion_shown = True

        # 결과창 팝업 생성
        completion_window = ctk.CTkToplevel(self.root)
        completion_window.title("타이핑 완료")
        completion_window.geometry("450x650")
        completion_window.configure(fg_color="white")
        completion_window.resizable(False, False)
        completion_window.transient(self.root)
        completion_window.grab_set()

        # 스크롤 가능한 메인 컨테이너
        main_container = ctk.CTkScrollableFrame(completion_window, fg_color="white")
        main_container.pack(fill="both", expand=True, padx=20, pady=20)

        # 프로필 표시 영역 (원형 프로필 이미지)
        profile_container = ctk.CTkFrame(main_container, fg_color="white")
        profile_container.pack(pady=(0, 30))

        profile_frame = ctk.CTkFrame(profile_container, width=120, height=120, fg_color="#D3D3D3", corner_radius=60)
        profile_frame.pack()
        profile_frame.pack_propagate(False)

        # 사람 아이콘을 표현한 내부 프레임
        icon_frame = ctk.CTkFrame(profile_frame, width=60, height=60, fg_color="#A8A8A8", corner_radius=30)
        icon_frame.place(relx=0.5, rely=0.3, anchor="center")
        body_frame = ctk.CTkFrame(profile_frame, width=80, height=40, fg_color="#A8A8A8", corner_radius=20)
        body_frame.place(relx=0.5, rely=0.75, anchor="center")

        # 사용자 이름 표시
        name_label = ctk.CTkLabel(main_container, text="김미림", font=("Arial", 20, "bold"), text_color="black")
        name_label.pack(pady=(15, 25))

        # 통계 정보를 보여줄 컨테이너
        stats_container = ctk.CTkFrame(main_container, fg_color="#F8F8F8", corner_radius=10)
        stats_container.pack(fill="x", pady=(0, 25), padx=10)

        # 각 항목별 라벨과 값 표시
        stats_data = [
            ("진행시간", self.elapsed_time),
            ("타수(타/분)", str(self.typing_speed)),
            ("정확도(%)", f"{self.accuracy:.2f}")
        ]
        for i, (label, value) in enumerate(stats_data):
            stat_row = ctk.CTkFrame(stats_container, fg_color="transparent")
            stat_row.pack(fill="x", pady=10, padx=15)
            stat_label = ctk.CTkLabel(stat_row, text=label, font=("Arial", 14), text_color="black")
            stat_label.pack(side="left")
            stat_value = ctk.CTkLabel(stat_row, text=value, font=("Arial", 14, "bold"), text_color="black")
            stat_value.pack(side="right")

        # 하단 진행도 바 (100% 완료 표시)
        progress_container = ctk.CTkFrame(main_container, fg_color="white")
        progress_container.pack(fill="x", pady=(0, 15))
        result_progress = ctk.CTkProgressBar(progress_container, width=300, height=12, progress_color="#FF6B6B")
        result_progress.pack(pady=10)
        result_progress.set(1.0)

        # 오답 수 표시
        error_label = ctk.CTkLabel(main_container, text=f"오답 {self.errors}", font=("Arial", 12), text_color="red")
        error_label.pack(pady=(5, 25))

        # 버튼 컨테이너
        button_container = ctk.CTkFrame(main_container, fg_color="white", height=80)
        button_container.pack(fill="x", side="bottom")
        button_container.pack_propagate(False)

        button_inner_frame = ctk.CTkFrame(button_container, fg_color="white")
        button_inner_frame.pack(expand=True, fill="both", padx=20, pady=15)

        # 그만하기 버튼 (창 닫음)
        quit_btn = ctk.CTkButton(
            button_inner_frame, text="그만하기", width=120, height=45, fg_color="#D3D3D3",
            text_color="black", hover_color="#C0C0C0", corner_radius=22, font=("Arial", 13, "bold"),
            command=completion_window.destroy
        )
        quit_btn.pack(side="left", fill="x", expand=True, padx=(0, 10))

        # 계속하기 버튼 (게임 재시작)
        continue_btn = ctk.CTkButton(
            button_inner_frame, text="계속하기", width=120, height=45, fg_color="#FBE6A2",
            text_color="black", hover_color="#E6D68A", corner_radius=22, font=("Arial", 13, "bold"),
            command=lambda: self.restart_game(completion_window)
        )
        continue_btn.pack(side="right", fill="x", expand=True, padx=(10, 0))

    def restart_game(self, completion_window):
        # 결과창 닫기
        completion_window.destroy()

        # 게임 상태 초기화
        self.current_stage = 0
        self.current_position = 0
        self.typed_text = ""
        self.errors = 0
        self.total_chars = 0
        self.error_positions.clear()
        self.completed_inputs.clear()
        self.game_completed = False
        self.completion_shown = False
        self.typing_speed = 0
        self.accuracy = 100.0
        self.elapsed_time = "0:00"
        self.start_time = time.time()  # 시간 초기화
        self.update_display()  # 화면 갱신
        self.root.focus_set()  # 포커스 재설정

    def go_back(self):
        # 사용자가 나가려고 할 때 확인
        if self.current_stage > 0 or self.current_position > 0:
            if self.confirm_exit():
                self.exit_to_rank_select()
        else:
            self.exit_to_rank_select()

    def exit_to_rank_select(self):
        # rank.py를 실행하고 현재 창 닫기
        try:
            import os
            if os.path.exists("rank.py"):
                subprocess.Popen([sys.executable, "rank.py"])
                self.root.after(100, self.root.destroy)
            else:
                print("rank.py 파일을 찾을 수 없습니다.")
                self.root.destroy()
        except Exception as e:
            print(f"rank.py 실행 중 오류 발생: {e}")
            self.root.destroy()

    def confirm_exit(self):
        # 게임 종료 확인용 팝업창
        confirm_window = ctk.CTkToplevel(self.root)
        confirm_window.title("게임 종료")
        confirm_window.geometry("300x150")
        confirm_window.configure(fg_color="white")
        confirm_window.resizable(False, False)
        confirm_window.transient(self.root)
        confirm_window.grab_set()

        message_label = ctk.CTkLabel(
            confirm_window, text="정말로 게임을 종료하시겠습니까?", font=("Arial", 14), text_color="black"
        )
        message_label.pack(pady=30)

        button_frame = ctk.CTkFrame(confirm_window, fg_color="white")
        button_frame.pack(fill="x", padx=20, pady=10)

        result = [False]  # 결과를 리스트로 담아서 내부 함수에서 수정 가능하게 함

        def on_yes():
            result[0] = True
            confirm_window.destroy()

        def on_no():
            result[0] = False
            confirm_window.destroy()

        no_btn = ctk.CTkButton(button_frame, text="아니오", width=80, height=35, fg_color="#D3D3D3",
                               text_color="black", hover_color="#C0C0C0", command=on_no)
        no_btn.pack(side="left", padx=(0, 10))

        yes_btn = ctk.CTkButton(button_frame, text="예", width=80, height=35, fg_color="#FF6B6B",
                                text_color="white", hover_color="#FF5252", command=on_yes)
        yes_btn.pack(side="right")

        confirm_window.wait_window()  # 사용자가 선택할 때까지 대기
        return result[0]

    def run(self):
        # 메인 이벤트 루프 시작 (게임 실행)
        self.root.mainloop()


# 직접 실행할 경우 게임 실행
if __name__ == "__main__":
    game = CodingTypingGame()
    game.run()
