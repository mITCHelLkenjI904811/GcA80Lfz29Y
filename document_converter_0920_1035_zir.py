# 代码生成时间: 2025-09-20 10:35:45
from pyramid.config import Configurator
from pyramid.response import Response
from pyramid.view import view_config
import json
from docx import Document
from docx.shared import Inches
import os

# 定义 logger
import logging
log = logging.getLogger(__name__)

# 配置 Pyramid 应用
def main(global_config, **settings):
    config = Configurator(settings=settings)
    config.include('.pyramid_routes')
    config.scan()
    return config.make_wsgi_app()

# 定义视图函数
@view_config(route_name='convert', renderer='json')
def convert(request):
    """
    将 DOCX 文档转换为 PDF
    """
    # 获取上传的文件
    file = request.params.get('file', None)
    if file is None:
        return {'error': 'No file provided.'}

    # 尝试保存上传的文件
    try:
        with file.open('rb') as uploaded_file:
            document = Document(uploaded_file)
            docx_file_path = 'temp.docx'
            with open(docx_file_path, 'wb') as docx_file:
                document.save(docx_file)
    except Exception as e:
        log.error(f'Error converting file: {e}')
        return {'error': 'Failed to convert file.'}

    # 将 DOCX 转换为 PDF
    try:
        os.system(f'libreoffice --headless --convert-to pdf --outdir . {docx_file_path}')
        pdf_file_path = 'temp.pdf'
        with open(pdf_file_path, 'rb') as pdf_file:
            pdf_content = pdf_file.read()
    except Exception as e:
        log.error(f'Error converting DOCX to PDF: {e}')
        return {'error': 'Failed to convert DOCX to PDF.'}
    finally:
        # 清理临时文件
        os.remove(docx_file_path)
        os.remove(pdf_file_path)

    # 返回 PDF 文件内容
    return {'pdf': pdf_content}

# 定义路由
def includeme(config):
    config.add_route('convert', '/convert')
    config.scan()
