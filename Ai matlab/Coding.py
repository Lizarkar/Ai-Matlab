import matlab.engine
from google import genai
import re
import sys
import os

# 1. DÁN MÃ API KEY CỦA BẠN VÀO ĐÂY
API_KEY = "idk"

client = genai.Client(api_key=API_KEY)

print("⏳ Đang khởi động MATLAB ngầm...")
try:
    eng = matlab.engine.start_matlab()
    print("✅ MATLAB đã khởi động!\n")
except Exception as e:
    print(f"❌ Không thể khởi động MATLAB: {e}")
    sys.exit()

# TẠO THƯ MỤC DỰ ÁN CHUẨN GITHUB
# Mọi file AI tạo ra sẽ được nhét gọn gàng vào thư mục này
WORKSPACE_DIR = "My_Project_Workspace"
if not os.path.exists(WORKSPACE_DIR):
    os.makedirs(WORKSPACE_DIR)

# Lệnh cho MATLAB trỏ vào thư mục này để có thể chạy các file bên trong
eng.cd(WORKSPACE_DIR, nargout=0)

# DẠY AI CÁCH TRÌNH BÀY NHIỀU FILE
system_instruction = """
Bạn là Siêu trợ lý tạo dự án đa ngôn ngữ. 
Khi người dùng yêu cầu, bạn có thể tạo nhiều file (.m, .cpp, .py, .csv...).
BẮT BUỘC trả về nội dung theo cấu trúc sau cho MỖI file:
---FILE: ten_file.mo_rong---
[Nội dung code ở đây]
---END---
Tuyệt đối không dùng thẻ markdown. Chỉ xuất code.
Nếu cần chạy MATLAB, hãy tạo ít nhất một file .m đóng vai trò chạy chính.
"""

chat = client.chats.create(
    model="gemini-3.6-flash",
    config={"system_instruction": system_instruction}
)

def process_and_save_files(text):
    """Hàm này dùng thuật toán tìm kiếm để cắt các đoạn code AI sinh ra và lưu thành nhiều file riêng"""
    pattern = r"---FILE:\s*(.+?)---\n(.*?)(?:---END---|\Z)"
    matches = re.finditer(pattern, text, re.DOTALL)
    
    saved_files = []
    for match in matches:
        filename = match.group(1).strip()
        content = match.group(2).strip()
        
        # Lưu file vào trong thư mục dự án
        filepath = os.path.join(WORKSPACE_DIR, filename)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        saved_files.append(filename)
        
    return saved_files

def run_ai_matlab_agent(user_prompt):
    current_prompt = user_prompt
    for attempt in range(5):
        print(f"🔄 AI đang thiết kế dự án... (Lần {attempt + 1}/5)")
        response = chat.send_message(current_prompt)
        
        # Python đọc và tạo ra các file vật lý
        saved_files = process_and_save_files(response.text)
        
        if not saved_files:
            print("⚠️ Lỗi định dạng từ AI. Đang yêu cầu AI viết lại...")
            current_prompt = "Bạn phải dùng đúng định dạng ---FILE: ten_file--- rồi kết thúc bằng ---END---. Hãy viết lại."
            continue
            
        print(f"📁 Đã tạo thành công các file: {', '.join(saved_files)}")
        
        # Tìm xem trong các file vừa tạo có file MATLAB (.m) nào không để chạy
        m_files = [f for f in saved_files if f.endswith('.m')]
        
        if m_files:
            # Chọn file .m đầu tiên để chạy
            main_file = m_files[0].replace('.m', '')
            print(f"🚀 Đang đưa '{main_file}.m' vào MATLAB chạy thử...")
            try:
                eng.eval(main_file, nargout=0)
                print("✅ CHẠY THÀNH CÔNG! (Xem biểu đồ nếu có)\n")
                break
            except matlab.engine.MatlabExecutionError as e:
                error_msg = str(e)
                print(f"⚠️ Phát hiện lỗi khi chạy:\n{error_msg}")
                current_prompt = f"File {main_file}.m bị lỗi sau:\n{error_msg}\nHãy sửa lại toàn bộ các file."
        else:
            print("✅ Đã lưu file (Không có file MATLAB nên không cần chạy test).\n")
            break
    else:
        print("❌ AI đã thử 5 lần nhưng chưa hoàn thiện được.")

# ==========================================
# GIAO DIỆN CHAT TƯƠNG TÁC
# ==========================================
print("======================================================")
print("🤖 SIÊU TRỢ LÝ ĐA NGÔN NGỮ ĐÃ SẴN SÀNG!")
print("======================================================")

while True:
    yeu_cau = input("\n👉 Nhập yêu cầu: ")
    if yeu_cau.lower() in ['thoat', 'thoát', 'exit', 'quit']:
        break
    if yeu_cau.strip() == '':
        continue
    run_ai_matlab_agent(yeu_cau)

print("\n👋 Đang đóng MATLAB...")
eng.quit()