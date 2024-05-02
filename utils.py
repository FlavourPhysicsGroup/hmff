import yaml
import codecs
from pathlib import Path

formfactors = {}  # 存储实现对象的字典, e.g. {name: obj_ff} 其中 obj_ff 是 FormFactor 类的对象 (object)


def all():  # 打印实现对象的字典
    for key, value in formfactors.items():
        print(f"{key}: {value}")


def read_yaml(file_name):
    file_path = "data/" + file_name
    with codecs.open(Path(__file__).parent / f'{file_path}', 'r', encoding='utf-8') as file:
        data = yaml.load(file, Loader=yaml.FullLoader)
    return data
