import os
import hashlib
from utils.logger_handler import logger
from langchain_community.document_loaders import PyPDFLoader,TextLoader
from langchain_core.documents import Document

def get_file_md5_hex(file_path:str):    #获取文件的md5的十六进制
    if not os.path.exists(file_path):
        logger.error(f'[md5计算]文件{file_path}不存在')
        return
    if not os.path.isfile(file_path):
        logger.error(f'[md5计算]路径{file_path}不是文件')
        return
    md5_obj = hashlib.md5()
    try:
        chunk_size = 4096   #避免文件过大占用内存
        with open(file_path,'rb') as f:    #必须二进制读取
            while chunk := f.read(chunk_size):
                md5_obj.update(chunk)
                """
                python新语法    :=
                chunk = f.read(chunk_size)
                while chunk:
                    md5_obj.update(chunk)
                    chunk = f.read(chunk_size)
                """
            md5_hex = md5_obj.hexdigest()
            return md5_hex
    except Exception as e:
        logger.error(f'计算文件{file_path}md5失败，{str(e)}')
        return None

def listdir_with_allow_type(path:str,allow_types:tuple[str]):    #返回文件夹内的文件列表(允许的文件后缀)
    files = []
    if not os.path.isdir(path):
        logger.error(f'[listdir_with_allow_type]{path}不是文件夹')
        return allow_types
    for f in os.listdir(path):
        if f.endswith(allow_types):
            files.append(os.path.join(path,f))
    return tuple(files)

def pdf_loader(file_path:str,passwd:str)->list[Document]:
    return PyPDFLoader(file_path,passwd).load()

def text_loader(file_path:str)->list[Document]:
    return TextLoader(file_path,encoding="utf-8").load()