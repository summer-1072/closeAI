import pdfplumber
from pdf2docx import Converter

# 使用pdfplumber打开PDF文件
with pdfplumber.open('/Users/kaiwang/work/NERF.pdf') as pdf:
    text_content = ''

    # 遍历PDF中的每一页
    for page in pdf.pages:
        # 从当前页中提取文字
        text = page.extract_text()
        if text:  # 确保当前页确实包含文字
            text_content += text.replace('\n', ' ')  # 添加文字到总的文字内容中，每页后加换行符

# 打印提取的文字内容
print(text_content)