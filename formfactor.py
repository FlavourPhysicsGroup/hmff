import one_pole
import yaml
import codecs
import z_param
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path


class FormFactor:

    def __init__(self, IS, FS,**extra):
        self.name = f"{IS}->{FS} form factors"
        self.obj_name = f"f{IS}{FS}"  # 形状因子对象的名称，使用'f'、初始状态和最终状态构建
        self.extra = extra
        self.IS = IS  # 初始状态名称, e.g. "B"
        self.FS = FS  # 最终状态名称, e.g. "K"
        self.description = extra.get('description')  # 作学术方面介绍
        self.ff_names = extra.get('ff_names')  # 存储形状因子名称的列表,e.g. ['f+', 'f0', 'A1', 'A2', 'A3', 'T1', ...]
        self.impl_names = []  # 存储实现名称的列表,e.g."one-pole"
        self.impls = {}  # 存储实现对象的字典, e.g. {'one-pole': impl_obj}, 其中 impl_obj (Impl): Impl 类的对象 (object)

    def set_description(self, des):
        self.description = des  # 设置形状因子的描述

    def add_impl(self, impl_obj):
        self.impl_names.append(impl_obj.param_form)  # 添加实现名称到列表中
        self.impls[impl_obj.param_form] = impl_obj.name  # 将参数形式存储到字典中，使用实现对象作为键

    def get_impl(self, impl_name):
        if impl_name in self.impl_names:
            return self.impls[impl_name]  # 返回指定名称的实现对象
        else:
            print(f"警告：未找到 '{impl_name}' 实现. ")
            quit


class Impl:

    def __init__(self, name,**extra):
        self.name = name  # 实现的名称
        self.extra = extra
        self.description = extra.get('description')  # e.g. "只实现了标量形状因子: f+, f0. 参考了 XX 文章. 存在 XX 问题"
        self.ff_names = extra.get ('ff_names') # 存储形状因子名称的列表，e.g. ['f+', 'f0']
        self.ff_tex_names = extra.get('ff_tex_names')  # 存储形状因子的TeX名称的列表
        self.param_form = extra.get('param_form')  # 参数形式，e.g. 'z-param', 'BGL' or 'one-pole'
        self.methods = extra.get('methods')  # 方法说明，e.g. 'LQCD', 'LCSR' or 'HQEFT'
        self.ref = extra.get('ref')  # 参考资料
        self.ff_obj = None  # 形状因子对象
        self._internal_params = {}  # 内部参数

    def get_ref(self):
        print(self.ref)  # 返回参考资料

    def set_description(self, des):
        self.description = des  

    def get_central_values(self, qsq):
        IS = self.ff_obj.IS
        FS = self.ff_obj.FS
        if self.param_form == 'one-pole':
            ff = one_pole.ff(IS, FS, qsq)  # 调用外部函数计算中心值（使用one-pole参数形式）
        elif self.param_form == 'z-param':
            ff = z_param.ff(IS, FS, qsq)  # 调用外部函数计算中心值（使用z-param参数形式）
        return ff

    def draw(self, x,y):  # 绘制形状因子图像，x，y为横纵坐标最大值。
        length = len(self.ff_names)
        qs = np.linspace(0, x, 100)
        if length == 3:
            ffs = {'f+': [], 'f0': [], 'fT': []}
            for q in qs:
                ffdict = self.get_central_values(q)
                for key, values in ffdict.items():
                    ffs[key].append(values)
        elif length == 2:
            ffs = {'f+': [], 'f0': []}
            for q in qs:
                ffdict = self.get_central_values(q)
                for key, values in ffdict.items():
                    ffs[key].append(values)
        elif length == 7:
            ffs = {'V': [], 'A0': [], 'A1': [], 'A2': [], 'T1': [], 'T2': [], 'T3': []}
            for q in qs:
                ffdict = self.get_central_values(q)
                for key, values in ffdict.items():
                    ffs[key].append(values)
        colors = ['red', 'green', 'blue', 'cyan', 'magenta', 'yellow', 'black', 'white']
        for i, (key, values) in enumerate(ffs.items()):
            plt.plot(qs, values, label=key, color=colors[i])

        plt.xlim(0, x)
        plt.ylim(0, y)
        plt.xlabel('q^2[GeV]')
        plt.ylabel('f(q^2)')
        plt.legend()
        plt.grid(True)
        plt.show()

success = {} # 存储实现对象的字典, e.g. {name: obj_ff} 其中 obj_ff 是 FormFactor 类的对象 (object)
def all(): # 打印实现对象的字典
    for key, value in success.items():
        print(f"{key}: {value}")

def read_yaml(file_name):
    file_path = "data/" + file_name
    with codecs.open(Path(__file__).parent / f'{file_path}', 'r', encoding='utf-8') as file:
        data = yaml.load(file, Loader=yaml.FullLoader)
    return data

# 实际操作应在input.py进行