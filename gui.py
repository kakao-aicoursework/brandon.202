import tkinter as tk
from tkinter import scrolledtext

import ai_model

def initialize(messages):
  def show_popup_message(window, message):
    popup = tk.Toplevel(window)
    popup.title("")

    # 팝업 창의 내용
    label = tk.Label(popup, text=message, font=("맑은 고딕", 12))
    label.pack(expand=True, fill=tk.BOTH)

    # 팝업 창의 크기 조절하기
    window.update_idletasks()
    popup_width = label.winfo_reqwidth() + 20
    popup_height = label.winfo_reqheight() + 20
    popup.geometry(f"{popup_width}x{popup_height}")

    # 팝업 창의 중앙에 위치하기
    window_x = window.winfo_x()
    window_y = window.winfo_y()
    window_width = window.winfo_width()
    window_height = window.winfo_height()

    popup_x = window_x + window_width // 2 - popup_width // 2
    popup_y = window_y + window_height // 2 - popup_height // 2
    popup.geometry(f"+{popup_x}+{popup_y}")

    popup.transient(window)
    popup.attributes('-topmost', True)

    popup.update()
    return popup

  def on_send():
    user_input = user_entry.get()
    user_entry.delete(0, tk.END)

    if user_input.lower() == "quit":
      window.destroy()
      return

    messages.append({"role": "user", "content": user_input})
    conversation.config(state=tk.NORMAL)  # 이동
    conversation.insert(tk.END, f"You: {user_input}\n", "user")  # 이동
    thinking_popup = show_popup_message(window, "처리중...")
    window.update_idletasks()
    # '생각 중...' 팝업 창이 반드시 화면에 나타나도록 강제로 설정하기
    response = ai_model.send_message(messages)
    thinking_popup.destroy()

    messages.append({"role": "assistant", "content": response})

    # 태그를 추가한 부분(1)
    conversation.insert(tk.END, f"gpt assistant: {response}\n", "assistant")
    conversation.config(state=tk.DISABLED)
    # conversation을 수정하지 못하게 설정하기
    conversation.see(tk.END)

  window = tk.Tk()
  window.title("GPT AI")

  font = ("맑은 고딕", 10)

  conversation = scrolledtext.ScrolledText(window, wrap=tk.WORD, bg='green',
                                           font=font)
  # width, height를 없애고 배경색 지정하기(2)
  conversation.tag_configure("user", background="red")
  # 태그별로 다르게 배경색 지정하기(3)
  conversation.tag_configure("assistant", background="blue")
  # 태그별로 다르게 배경색 지정하기(3)
  conversation.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
  # 창의 폭에 맞추어 크기 조정하기(4)

  input_frame = tk.Frame(window)  # user_entry와 send_button을 담는 frame(5)
  input_frame.pack(fill=tk.X, padx=10, pady=10)  # 창의 크기에 맞추어 조절하기(5)

  user_entry = tk.Entry(input_frame)
  user_entry.pack(fill=tk.X, side=tk.LEFT, expand=True)

  send_button = tk.Button(input_frame, text="Send", command=on_send)
  send_button.pack(side=tk.RIGHT)

  window.bind('<Return>', lambda event: on_send())
  window.mainloop()
