from functools import partial
from typing import Callable
from copy import deepcopy

from . import pole_dominance as pole
from . import z_parameterization as zp
from . import pole_w_expansion as pwe
import numpy as np 


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

        self._ff_fit_methods = {
            "one pole": (pole.format_parameters_one_pole, pole.f_one_pole),
            "double pole 1": (pole.format_parameters_double_pole_1, pole.f_double_pole_1),
            "double pole 2": (pole.format_parameters_double_pole_2, pole.f_double_pole_2),
            "BCL 1": (zp.format_parameter_BCL_1, zp.f_BCL_1),
            "BCL 2": (zp.format_parameter_BCL_2, zp.f_BCL_2),
            "BCL 3": (zp.format_parameter_BCL_3, zp.f_BCL_3),
            "BCL 4": (zp.format_parameter_BCL_4, zp.f_BCL_4),
            "z-expansions 1": (lambda x: x, zp.f_z_expansions_1),
            "z-expansions 2": (lambda x: x, zp.f_z_expansions_2),
            "z-expansions 3": (lambda x: x, zp.f_z_expansions_3),
            "Horgan 2015": (lambda x: x, zp.f_horgan_2015),
            "pole w expansion": (
                pwe.format_parameters_pole_w_expansion,
                pwe.f_pole_w_expansion,
            ),
            "BCL 5": (
                zp.format_parameter_BCL_5,
                zp.f_BCL_5,
            ),
        }

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
        ffs = self.config.get("form factors")
        return list(ffs.keys()) if ffs else []

    def form_factor_function(self, ff_name) -> Callable[[float], float]:
        """获取形状因子对应的拟合函数: f(qsq)"""

        if ff_name not in self.form_factor_names:
            raise KeyError(f"'{ff_name}' not found in Impl '{self.name}'")

        ff_config = self.config.get("form factors").get(ff_name)
        ff_data = deepcopy(ff_config.get("parameter"))

        class_func = ff_config.get("parameterization")
        if class_func == "pole w expansion":
            ff_data = pwe.prepare(ff_name, ff_data, self.config)
        elif class_func == "BCL 5":
            ff_data = zp.bcl5_prepare(ff_name, ff_data, self.config)
        elif class_func == "BCL 4" and ff_config.get("endpoint"):
            ff_data = zp.bcl4_endpoint_prepare(
                ff_name, ff_data, ff_config["endpoint"], self.config
            )

        format_func, param_func = self._ff_fit_methods[class_func]
        ff_data = format_func(ff_data)

        # 如果形状因子f_0需要f_+的信息, 则需要更新f_0中的pars
        if "a0_last" in ff_config:
            if ff_config.get("a0_last") == "by_ap":
                fp_config = self.config.get("form factors").get("f+")

                fp_format_func, fp_func = self._ff_fit_methods[fp_config.get("parameterization")]

                # format the parameter of f+
                fp_data = fp_format_func(deepcopy(fp_config.get("parameter")))

                f0_func = param_func

                # add a0_N-1 from ap by using the relation f_p(0) = f_0(0)
                ff_data = zp.add_a0_last_from_ap(f0_func, ff_data, fp_func, fp_data)

                # delete the key "a0_last" and its value
                ff_data.pop("a0_last", None)
            else:
                raise ValueError(f"Invalid value for a0_last: {ff_config.get('a0_last')}. Expected 'by_ap' or None.")

        ff_func = partial(param_func, pars=ff_data)

        # 标量输入返回原生 Python float (避免在 notebook 中显示为 numpy.float64),
        # 数组输入 (如 np.linspace, 用于绘图) 保持 numpy 数组.
        def scalar_float_wrapper(qsq):
            res = ff_func(qsq)
            if np.ndim(res) == 0:
                return float(res)
            return res

        return scalar_float_wrapper

    def get_central_values(self, qsq):
        """返回此文章中包含的所有形状因子在特定qsq时的中心值"""
        return {ff: self.form_factor_function(ff)(qsq) for ff in self.form_factor_names}


    def get_sigma_f_stat(self, ff_name):

        ff_config = self.config.get("form factors").get(ff_name)

        pars = deepcopy(ff_config.get("parameter"))
        class_func = ff_config.get("parameterization")
        if class_func == "pole w expansion":
            pars = pwe.prepare(ff_name, pars, self.config)
        elif class_func == "BCL 5":
            pars = zp.bcl5_prepare(ff_name, pars, self.config)
        elif class_func == "BCL 4" and ff_config.get("endpoint"):
            pars = zp.bcl4_endpoint_prepare(
                ff_name, pars, ff_config["endpoint"], self.config
            )
        format_func, param_func = self._ff_fit_methods[class_func]
        pars = format_func(pars)
        cov_a = pars.get("cov_matrices")
        gradient_indices = None
        gradient_local_indices = None
        if cov_a is None and class_func == "pole w expansion":
            # 全局协方差矩阵 (来自 ancillary 文件), 参数顺序见 covariance_matrix.order
            covariance_config = self.config.get("covariance_matrix", {})
            cov_a = covariance_config.get("value")
            order = covariance_config.get("order")
            if cov_a is not None and order is not None:
                index = {tuple(k): i for i, k in enumerate(order)}
                pars["_a0_linear"], pars["_a1_linear"] = pwe.linear_maps(ff_name, pars, index)
                pars["_pole_w_cov_dim"] = len(order)
        elif cov_a is None and class_func == "BCL 5":
            # 全局协方差矩阵 (来自 ancillary 文件), 参数顺序见 covariance_matrix.order
            covariance_config = self.config.get("covariance_matrix", {})
            cov_a = covariance_config.get("value")
            order = covariance_config.get("order")
            if cov_a is not None and order is not None:
                index = {tuple(k): i for i, k in enumerate(order)}
                pars["_a0_linear"], pars["_a1_linear"] = zp.bcl5_linear_maps(ff_name, pars, index)
                pars["_bcl5_cov_dim"] = len(order)
        elif cov_a is None and class_func == "BCL 4" and self.config.get("covariance_matrix"):
            # 全局协方差矩阵 (来自 ancillary 文件), 参数顺序见 covariance_matrix.order
            # (Xi_c->Xi LQCD-2025: endpoint 约束经 linear maps 传播到全局参数)
            covariance_config = self.config.get("covariance_matrix", {})
            cov_a = covariance_config.get("value")
            order = covariance_config.get("order")
            if cov_a is not None and order is not None:
                index = {tuple(k): i for i, k in enumerate(order)}
                pars["_xicxi_a_linear"] = zp.bcl4_endpoint_linear_maps(
                    ff_name, pars, ff_config.get("endpoint"), index
                )
                pars["_xicxi_cov_dim"] = len(order)
        elif cov_a is None and class_func.startswith("z-expansions"):
            covariance_config = self.config.get("covariance_matrix", {})
            cov_a = covariance_config.get("value")
            if cov_a is not None:
                ff_names = self.form_factor_names
                if class_func == "z-expansions 1":
                    # Published order: [f(0), c_0, c_+, P_S, P_V].
                    covariance_ff_order = sorted(
                        ff_names,
                        key=lambda name: {"f0": 0, "f+": 1}.get(name, ff_names.index(name)),
                    )
                    ff_position = covariance_ff_order.index(ff_name)
                    gradient_indices = [
                        0,
                        1 + ff_position,
                        1 + len(ff_names) + ff_position,
                    ]
                    gradient_local_indices = [0, 1, 2]
                else:
                    # z-expansions 2/3 do not include the fixed pole parameter
                    # in the published covariance matrix.
                    ff_position = ff_names.index(ff_name)
                    gradient_indices = [0, 1 + ff_position]
                    gradient_local_indices = [0, 1]
        if cov_a is None and class_func == "Horgan 2015":
            covariance_key = "tensor_covariance_matrix" if ff_name.startswith("T") else "covariance_matrix"
            covariance_config = self.config.get(covariance_key, {})
            sigmas = np.asarray(covariance_config.get("sigmas", []), dtype=float)
            correlations = np.asarray(covariance_config.get("correlations", []), dtype=float)
            covariance_order = covariance_config.get("order", [])
            if sigmas.size and correlations.shape == (sigmas.size, sigmas.size):
                cov_a = correlations * np.outer(sigmas, sigmas)
                parameter_names = [f"{ff_name}_a0", f"{ff_name}_a1"]
                gradient_indices = [covariance_order.index(name) for name in parameter_names]
                gradient_local_indices = [0, 1]
        if cov_a is None:
            # 返回一个始终返回0的函数
            return lambda qsq: np.zeros_like(qsq) if hasattr(qsq, '__len__') else 0.0
        
        return partial(
            zp.sigma_f_analytical,
            pars=pars,
            cov_a=cov_a,
            class_func=class_func,
            gradient_indices=gradient_indices,
            gradient_local_indices=gradient_local_indices,
        )

    import numpy as np











