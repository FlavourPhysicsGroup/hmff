from functools import partial
from typing import Callable

from .src import pole_dominance as pole
from .src import z_parameterization as zp


class FormFactor:
    """FormFactor 通用信息类"""

    def __init__(self, name: str, impl_configs: dict, **kwargs):
        self.IS, self.FS = name.split("->")  # 初末态强子名称, e.g. "B", "K"
        self.name = name
        self.kwargs = kwargs
        self.description = kwargs.get("description")  # 作学术方面介绍
        self.impl_configs = impl_configs

        # 形状因子名称的列表,e.g. ['f+', 'f0', 'A1', 'A2', 'A3', ...]
        self.ff_names = kwargs.get("ff_names")

        # e.g. {'one-pole': impl_obj}, 其中 impl_obj 是一个 Impl 类的对象 (object)
        self._impls = {key: Impl(key, value) for key, value in impl_configs.items()}

    def set_description(self, des):
        self.description = des  # 设置形状因子的描述

    @property
    def impl_names(self):
        """返回所有Impl名称的列表"""
        return list(self._impls.keys())

    def add_impl(self, impl_obj):
        if impl_obj.name in self.impl_names:
            raise KeyError(f"Impl '{impl_obj.name}' already exists in FormFactor '{self.name}'")
        self._impls[impl_obj.name] = impl_obj

    def get_impl(self, impl_name):
        """一个实现指: 特定一篇文章中给出的具体数值信息"""
        if impl_name not in self._impls:
            raise KeyError(f"Impl '{impl_name}' not found in FormFactor '{self.name}'")
        return self._impls.get(impl_name)


class Impl:
    """实现: 指特定一篇文章中给出的具体数值信息"""

    def __init__(self, name, config, **kwargs):
        self.name = name
        self.config = config  # 从YAML读入的原始字典数据
        self.kwargs = kwargs

        # self.ff_tex_names = kwargs.get('ff_tex_names')  # 存储形状因子的TeX名称的列表
        # self.ff_obj = kwargs.get("ff_obj")  # 形状因子对象
        # self._internal_params = {}  # 内部参数

    @property
    def ref(self):
        """参考文献"""
        return self.config.get("ref")

    @property
    def comment(self):
        return self.config.get("comment")

    @property
    def citation(self):
        cite = self.config.get("citation key") or self.ref
        return cite

    @property
    def method(self):
        """方法说明, e.g. 'LQCD', 'LCSR' or 'HQEFT'"""
        res = self.config.get("method") or self.name.split("-")[0]
        return res

    @property
    def form_factor_names(self):
        """包含的形状因子名称的列表, e.g. ['f+', 'f0']"""
        return list(self.config.get("form factors").keys())

    def form_factor_function(self, ff_name) -> Callable[[float], float]:
        """获取形状因子对应的拟合函数: f(qsq)"""
        if ff_name not in self.form_factor_names:
            raise KeyError(f"'{ff_name}' not found in Impl '{self.name}'")

        ff_config = self.config.get("form factors").get(ff_name)
        ff_data = ff_config.get("parameter")

        # 如果形状因子f_0需要f_+的信息, 则需要更新f_0中的pars
        if ff_config.get("a0_last") is not None:
            ff_fp_config = self.config.get("form factors").get("f+")
            cond2 = ff_fp_config.get("parameterization")
            cond3 = ff_config.get("parameterization") in ["BCL 3", "BCL 4"]
            if cond2 and cond3:
                ff_data = zp.add_a0_N_minus_1_from_ap(ff_fp_config.get("parameter"), ff_data)

        match ff_config.get("parameterization"):
            case "one pole":
                ff_data = pole.format_parameters_one_pole(ff_data)
                return partial(pole.f_one_pole, pars=ff_data)
            case "double pole 1":
                ff_data = pole.format_parameters_double_pole_1(ff_data)
                return partial(pole.f_double_pole_1, pars=ff_data)
            case "double pole 2":
                ff_data = pole.format_parameters_double_pole_2(ff_data)
                return partial(pole.f_double_pole_2, pars=ff_data)
            case "BCL 1":
                ff_data = zp.format_parameter_BCL_1(ff_data)
                return partial(zp.f_BCL_1, pars=ff_data)
            case "BCL 2":
                ff_data = zp.format_parameter_BCL_2(ff_data)
                return partial(zp.f_BCL_2, pars=ff_data)
            case "BCL 3":
                ff_data = zp.format_parameter_BCL_3(ff_data)
                return partial(zp.f_BCL_3, pars=ff_data)
            case "BCL 4":
                ff_data = zp.format_parameter_BCL_4(ff_data)
                return partial(zp.f_BCL_4, pars=ff_data)
            case "z-expansions 1":
                # TODO: 格式化参数
                return partial(zp.f_z_expansions_1, pars=ff_data)
            case "z-expansions 2":
                # TODO: 格式化参数
                return partial(zp.f_z_expansions_2, pars=ff_data)
            case "z-expansions 3":
                # TODO: 格式化参数
                return partial(zp.f_z_expansions_3, pars=ff_data)
            case _:
                raise ValueError(
                    f"{self.name} has no such parameterization: {self.parameterization}"
                )

    def get_central_values(self, qsq):
        """返回此文章中包含的所有形状因子在特定qsq时的中心值"""
        infos = []
        for ff in self.form_factor_names:
            ff_func = self.form_factor_function(ff)
            infos.append(ff_func(qsq))
        return infos
