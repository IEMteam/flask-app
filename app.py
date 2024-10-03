from flask import Flask, request, jsonify, render_template
from PyPDF2 import PdfReader
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize

# 確保下載必要的 NLTK 資源
nltk.download('punkt')

app = Flask(__name__)

# 全局變數來保存 PDF 解析後的文本
pdf_text = ""

# 解析 PDF 文件
def extract_text_from_pdf(pdf_file_path):
    reader = PdfReader(pdf_file_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

# 查找與問題相關的句子
def find_answer(question, pdf_text):
    sentences = sent_tokenize(pdf_text)
    question_tokens = word_tokenize(question.lower())

    # 簡單關鍵字匹配來找相關的句子
    best_match = ""
    best_match_score = 0

    for sentence in sentences:
        sentence_tokens = word_tokenize(sentence.lower())
        common_words = set(question_tokens).intersection(sentence_tokens)
        match_score = len(common_words)

        if match_score > best_match_score:
            best_match_score = match_score
            best_match = sentence

    return best_match if best_match_score > 0 else "無法找到與此問題相關的答案。"

# 加載 PDF 檔案並儲存文本（在應用啟動時）
def load_pdf_file():
    global pdf_text
    pdf_text = extract_text_from_pdf('your_pdf_file.pdf')  # 替換為你的 PDF 文件路徑

# 接收問題並根據上傳的 PDF 查找答案
@app.route('/ask', methods=['POST'])
def ask_question():
    global pdf_text

    if not pdf_text:
        return jsonify({"error": "尚未加載任何 PDF 文件"}), 400

    data = request.json
    question = data.get('question', '')

    if not question:
        return jsonify({"error": "問題不可為空"}), 400

    answer = find_answer(question, pdf_text)
    return jsonify({"answer": answer})

# 新增根路由
@app.route('/')
def home():
    return render_template('index.html')  # 使用 render_template 加載 HTML 模板

if __name__ == '__main__':
    load_pdf_file()  # 在啟動時加載 PDF 文件
    app.run(host='0.0.0.0', port=5000, debug=True)  # 允許從任何 IP 訪問

