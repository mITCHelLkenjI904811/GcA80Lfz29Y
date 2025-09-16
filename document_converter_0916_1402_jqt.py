# 代码生成时间: 2025-09-16 14:02:16
import os
from pyramid.config import Configurator
from pyramid.response import Response
from pyramid.view import view_config
import requests
import zipfile
from docx import Document
from io import BytesIO


# 定义文档转换器类
class DocumentConverter:
    def __init__(self):
        self.base_url = 'http://localhost:6543'

    # 将docx转换为pdf
    def docx_to_pdf(self, docx_path):
        try:
            # 读取docx文件
            document = Document(docx_path)
            # 将docx文件转换为pdf
            pdf_bytes = self._convert_to_pdf(document)
            # 返回pdf文件
            return pdf_bytes
        except Exception as e:
            raise Exception(f"Failed to convert docx to pdf: {str(e)}")

    # 将pdf转换为docx
    def pdf_to_docx(self, pdf_path):
        try:
            # 读取pdf文件
            pdf_bytes = self._read_pdf(pdf_path)
            # 将pdf文件转换为docx
            docx = self._convert_to_docx(pdf_bytes)
            # 返回docx对象
            return docx
        except Exception as e:
            raise Exception(f"Failed to convert pdf to docx: {str(e)}")

    # 内部方法：将docx转换为pdf
    def _convert_to_pdf(self, document):
        # 将docx对象转换为pdf
        # 这里使用了一个假设的转换服务
        response = requests.post(f"{self.base_url}/convert/docx_to_pdf", json={'document': document})
        return response.content

    # 内部方法：将pdf转换为docx
    def _convert_to_docx(self, pdf_bytes):
        # 将pdf字节转换为docx对象
        # 这里使用了一个假设的转换服务
        response = requests.post(f"{self.base_url}/convert/pdf_to_docx", data=pdf_bytes)
        return response.json()

    # 内部方法：读取pdf文件
    def _read_pdf(self, pdf_path):
        # 读取pdf文件内容
        with open(pdf_path, 'rb') as file:
            return file.read()


# Pyramid视图函数
@view_config(route_name='convert', request_method='POST')
def convert(request):
    converter = DocumentConverter()
    doc_type = request.matchdict['type']
    file_path = request.matchdict['file']

    try:
        if doc_type == 'docx_to_pdf':
            return Response(converter.docx_to_pdf(file_path))
        elif doc_type == 'pdf_to_docx':
            return Response(converter.pdf_to_docx(file_path))
        else:
            raise Exception("Invalid document type")
    except Exception as e:
        return Response(str(e), status=400)


# Pyramid配置
def main(global_config, **settings):
    config = Configurator(settings=settings)
    config.include('pyramid_chameleon')
    config.add_route('convert', '/convert/:type/:file')
    config.scan()
    return config.make_wsgi_app()
