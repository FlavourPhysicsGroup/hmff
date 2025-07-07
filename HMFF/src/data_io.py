"""读入YAML数据文件, 将结构化数据返回"""

import yaml
import importlib.resources as pkg_resources

def read_yaml(file_name):
    """读取data/*.yaml文件, file_name: 文件名(带后缀)"""
    with pkg_resources.open_text("HMFF.src.data", file_name) as file:
        data = yaml.load(file, Loader=yaml.SafeLoader)
    return data
