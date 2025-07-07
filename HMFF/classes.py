import matplotlib.pyplot as plt
import numpy as np


class FormFactor:

    def __init__(self, name: str, impl_configs: dict, **kwargs):
        self.IS, self.FS = name.split('->')  # 初末态强子名称, e.g. "B", "K"
        self.name = name
        self.kwargs = kwargs
        self.description = kwargs.get('description')  # 作学术方面介绍
        self.impl_configs = impl_configs

        # 形状因子名称的列表,e.g. ['f+', 'f0', 'A1', 'A2', 'A3', ...]
        self.ff_names = kwargs.get('ff_names')

        # 存储实现名称的列表
        self.impl_names = list(impl_configs.keys())

        # 存储实现对象的字典, 懒加载
        # e.g. {'one-pole': impl_obj}, 其中 impl_obj (Impl): Impl 类的对象 (object)
        self._impls = {}

    def set_description(self, des):
        self.description = des  # 设置形状因子的描述

    def add_impl(self, impl_obj):
        if impl_obj.name in self.impl_names:
            raise KeyError(f"Impl '{impl_obj.name}' already exists in formfactor '{self.name}'")
        self._impls[impl_obj.name] = impl_obj  # 将参数形式存储到字典中，使用实现对象作为键
        self.impl_names.append(impl_obj.name)  # 添加实现名称到列表中

    def get_impl(self, impl_name):
        """懒加载指定 impl"""
        if impl_name not in self._impls:
            config = self.impl_configs.get(impl_name)
            if not config:
                raise KeyError(f"Impl '{impl_name}' not found in formfactor '{self.name}'")

            self._impls[impl_name] = Impl(impl_name, config)
        return self._impls[impl_name]


class Impl:

    def __init__(self, name, config, **kwargs):
        self.name = name  # 实现的名称
        self.config = config
        self.kwargs = kwargs
        # self.description = kwargs.get(
        #     'description')  # e.g. "只实现了标量形状因子: f+, f0. 参考了 XX 文章. 存在 XX 问题"
        # self.ff_names = kwargs.get('ff_names')  # 存储形状因子名称的列表，e.g. ['f+', 'f0']
        # self.ff_tex_names = kwargs.get('ff_tex_names')  # 存储形状因子的TeX名称的列表
        # self.param_form = kwargs.get('param_form')  # 参数形式，e.g. 'z-param', 'BGL' or 'one-pole'
        # self.methods = kwargs.get('methods')  # 方法说明，e.g. 'LQCD', 'LCSR' or 'HQEFT'
        # self.ref = kwargs.get('ref')  # 参考资料
        # self.ff_obj = kwargs.get("ff_obj")  # 形状因子对象
        # self._internal_params = {}  # 内部参数

    @property
    def ref(self):
        return self.config.get('ref')

    @property
    def comment(self):
        return self.config.get('comment')

    @property
    def citation(self):
        cite = self.config.get('citation key') or self.ref
        return cite

    @property
    def method(self):
        res = self.config.get('method') or self.name.split('-')[0]
        return res

    # def set_func(self, func):
    #     """func(qsq) 应该是一个只关于qsq的函数"""
    #     self._func = func

    # def get_central_values(self, qsq):
    #     # IS = self.ff_obj.IS
    #     # FS = self.ff_obj.FS
    #     # if self.param_form == 'one-pole':
    #     #     ff = one_pole.ff(IS, FS, qsq)  # 调用外部函数计算中心值（使用one-pole参数形式）
    #     # elif self.param_form == 'z-param':
    #     #     ff = z_param.ff(IS, FS, qsq)  # 调用外部函数计算中心值（使用z-param参数形式）
    #     # return ff
    #     return self._func(qsq)

    # def draw(self, x, y):  # 绘制形状因子图像，x，y为横纵坐标最大值。
    #     length = len(self.ff_names)
    #     qs = np.linspace(0, x, 100)
    #     if length == 3:
    #         ffs = {'f+': [], 'f0': [], 'fT': []}
    #         for q in qs:
    #             ffdict = self.get_central_values(q)
    #             for key, values in ffdict.items():
    #                 ffs[key].append(values)
    #     elif length == 2:
    #         ffs = {'f+': [], 'f0': []}
    #         for q in qs:
    #             ffdict = self.get_central_values(q)
    #             for key, values in ffdict.items():
    #                 ffs[key].append(values)
    #     elif length == 7:
    #         ffs = {'V': [], 'A0': [], 'A1': [], 'A2': [], 'T1': [], 'T2': [], 'T3': []}
    #         for q in qs:
    #             ffdict = self.get_central_values(q)
    #             for key, values in ffdict.items():
    #                 ffs[key].append(values)
    #     colors = ['red', 'green', 'blue', 'cyan', 'magenta', 'yellow', 'black', 'white']
    #     for i, (key, values) in enumerate(ffs.items()):
    #         plt.plot(qs, values, label=key, color=colors[i])

    #     plt.xlim(0, x)
    #     plt.ylim(0, y)
    #     plt.xlabel(r'$q^2$ [GeV]')
    #     plt.ylabel(r'$f(q^2)$')
    #     plt.legend()
    #     plt.grid(True)
    #     plt.show()
