import one_pole
import yaml
import codecs
import os
import z_param
import matplotlib.pyplot as plt
import numpy as np


class FormFactor:

    def __init__(self, IS, FS):
        self.name = f"f{IS}{FS}"  # 形状因子的名称，使用'f'、初始状态和最终状态构建
        self.IS = IS  # 初始状态名称, e.g. "B"
        self.FS = FS  # 最终状态名称, e.g. "K"
        self.description = f"{IS}->{FS} form factors"  # 作学术方面介绍
        self.ff_names = []  # 存储形状因子名称的列表,e.g. ['f+', 'f0', 'A1', 'A2', 'A3', 'T1', ...]
        self.impl_names = []  # 存储实现名称的列表,e.g."one-pole"
        self.impls = {
        }  # 存储实现对象的字典, e.g. {'one-pole': impl_obj}, 其中 impl_obj (Impl): Impl 类的对象 (object)

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

    def __init__(self, name):
        self.name = name  # 实现的名称
        self.description = ""  # e.g. "只实现了标量形状因子: f+, f0. 参考了 XX 文章. 存在 XX 问题"
        self.ff_names = []  # 存储形状因子名称的列表，e.g. ['f+', 'f0']
        self.ff_tex_names = []  # 存储表单因子的TeX名称的列表
        self.param_form = ""  # 参数形式，e.g. 'z-param', 'BGL' or 'one-pole'
        self.methods = ""  # 方法说明，e.g. 'LQCD', 'LCSR' or 'HQEFT'
        self.ref = ""  # 参考资料
        self.ff_obj = None  # 形状因子对象
        self._internal_params = {}  # 内部参数

    def get_ref(self):
        print(self.ref)  # 返回参考资料

    def get_central_values(self, qsq):
        IS = self.ff_obj.IS
        FS = self.ff_obj.FS
        if self.param_form == 'one-pole':
            fp = self._internal_func_1(IS, FS, qsq)  # 调用内部函数计算中心值（使用one-pole参数形式）
        elif self.param_form == 'z-param':
            fp = self._internal_func_2(IS, FS, qsq)  # 调用内部函数计算中心值（使用z-param参数形式）
        return fp

    def _internal_func_1(self, IS, FS, qsq):
        return one_pole.ff(IS, FS, qsq)  # 调用one_pole模块中的ff函数计算表单因子值

    def _internal_func_2(self, IS, FS, qsq):
        return z_param.ff(IS, FS, qsq)  # 调用z_param模块中的ff函数计算表单因子值

    def draw(self, x, y):  # 绘制形状因子图像
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


def read_yaml(file_name):
    with codecs.open(os.path.join(os.path.dirname(os.path.abspath(__file__)), file_name),
                     'r',
                     encoding='utf-8') as file:
        data = yaml.load(file, Loader=yaml.FullLoader)
    return data


# -----------------------------------已完成物理过程
fBpi = FormFactor("B", "pi")
fBpi.set_description("描述B和pi介子相互作用的形式因子")

fBpi_zp = Impl("fBpi_zp")
fBpi_zp.ff_obj = fBpi
fBpi_zp.ff_names = ['f+', 'f0', 'fT']
fBpi_zp.param_form = 'z-param'
fBpi_zp.ref = 'FLAG'
fBpi_zp.methods = 'LQCD'
fBpi_zp.description = f"用{fBpi_zp.param_form}参数化，实现了{fBpi_zp.ff_names}，参考了{fBpi_zp.ref}"
fBpi.add_impl(fBpi_zp)

fBpi_op = Impl("fBpi_op")
fBpi_op.ff_names = ['f+', 'f0', 'fT']
fBpi_op.param_form = 'one-pole'
fBpi_op.ref = 'arxiv:hep-ph/0406232'
fBpi_op.methods = 'LQCD'
fBpi_op.description = f"用{fBpi_op.param_form}参数化，实现了{fBpi_op.ff_names}，参考了{fBpi_op.ref}"
fBpi_op.ff_obj = fBpi
fBpi.add_impl(fBpi_op)
# -----------------------------------
fBD = FormFactor("B", "D")

fBD_zp = Impl("fBD_zp")
fBD_zp.ff_obj = fBD
fBD_zp.ff_names = ['f+', 'f0']
fBD_zp.param_form = 'z-param'
fBD_zp.ref = 'FLAG'
fBD_zp.methods = 'LQCD'
fBD_zp.description = f"用{fBD_zp.param_form}参数化，实现了{fBD_zp.ff_names}，参考了{fBD_zp.ref}"
fBD.add_impl(fBD_zp)
# -----------------------------------
fBK = FormFactor("B", "K")

fBK_op = Impl("fBK_op")
fBK_op.ff_obj = fBK
fBK_op.ff_names = read_yaml('one_pole.yaml')['B->K form factor'].keys()
fBK_op.param_form = 'one-pole'
fBK_op.ref = 'arxiv:hep-ph/0406232'
fBK_op.methods = 'LQCD'
fBK_op.description = f"用{fBK_op.param_form}参数化，实现了{fBK_op.ff_names}，参考了{fBK_op.ref}"
fBK.add_impl(fBK_op)

fBK_zp = Impl("fBK_zp")
fBK_zp.ff_obj = fBK
fBK_zp.ff_names = ['f+', 'f0', 'fT']
fBK_zp.param_form = 'z-param'
fBK_zp.ref = 'FLAG'
fBK_zp.methods = 'LQCD'
fBK_zp.description = f"用{fBK_zp.param_form}参数化，实现了{fBK_zp.ff_names}，参考了{fBK_zp.ref}"
fBK.add_impl(fBK_zp)
# -----------------------------------
fBeta = FormFactor("B", "eta")

fBeta_op = Impl("fBeta_op")
fBeta_op.ff_obj = fBeta
fBeta_op.ff_names = read_yaml('one_pole.yaml')['B->eta form factor'].keys()
fBeta_op.param_form = 'one-pole'
fBeta_op.ref = 'arxiv:hep-ph/0406232'
fBeta_op.methods = 'LQCD'
fBeta_op.description = f"用{fBeta_op.param_form}参数化，实现了{fBeta_op.ff_names}，参考了{fBeta_op.ref}"
fBeta.add_impl(fBeta_op)
# -----------------------------------
fBrho = FormFactor("B", "rho")

fBrho_op = Impl("fBrho_op")
fBrho_op.ff_obj = fBrho
fBrho_op.ff_names = read_yaml('one_pole.yaml')['B->rho form factor'].keys()
fBrho_op.param_form = 'one-pole'
fBrho_op.ref = 'arxiv:hep-ph/0412079'
fBrho_op.methods = 'LQCD'
fBrho_op.description = f"用{fBrho_op.param_form}参数化，实现了{fBrho_op.ff_names}，参考了{fBrho_op.ref}"
fBrho.add_impl(fBrho_op)
# -----------------------------------
fBsKstar = FormFactor("Bs", "K*")

fBsKstar_op = Impl("fBsKstar_op")
fBsKstar_op.ff_obj = fBsKstar
fBsKstar_op.ff_names = read_yaml('one_pole.yaml')['Bs->K* form factor'].keys()
fBsKstar_op.param_form = 'one-pole'
fBsKstar_op.ref = 'arxiv:hep-ph/0412079'
fBsKstar_op.methods = 'LQCD'
fBsKstar_op.description = f"用{fBsKstar_op.param_form}参数化，实现了{fBsKstar_op.ff_names}，" \
    + f"参考了{fBsKstar_op.ref}"
fBsKstar.add_impl(fBsKstar_op)
# -----------------------------------
fBKstar = FormFactor("B", "K*")

fBKstar_op = Impl("fBKstar_op")
fBKstar_op.ff_obj = fBKstar
fBKstar_op.ff_names = read_yaml('one_pole.yaml')['B->K* form factor'].keys()
fBKstar_op.param_form = 'one-pole'
fBKstar_op.ref = 'arxiv:hep-ph/0412079'
fBKstar_op.methods = 'LQCD'
fBKstar_op.description = f"用{fBKstar_op.param_form}参数化，实现了{fBKstar_op.ff_names}，参考了{fBKstar_op.ref}"
fBKstar.add_impl(fBKstar_op)

# -----------------------------------
fBomega = FormFactor("B", "omega")

fBomega_op = Impl("fBomega_op")
fBomega_op.ff_obj = fBomega
fBomega_op.ff_names = read_yaml('one_pole.yaml')['B->omega form factor'].keys()
fBomega_op.param_form = 'one-pole'
fBomega_op.ref = 'arxiv:hep-ph/0412079'
fBomega_op.methods = 'LQCD'
fBomega_op.description = f"用{fBomega_op.param_form}参数化，实现了{fBomega_op.ff_names}，参考了{fBomega_op.ref}"
fBomega.add_impl(fBomega_op)
# -----------------------------------
fBsphi = FormFactor("Bs", "phi")

fBsphi_op = Impl("fBsphi_op")
fBsphi_op.ff_obj = fBsphi
fBsphi_op.ff_names = read_yaml('one_pole.yaml')['Bs->phi form factor'].keys()
fBsphi_op.param_form = 'one-pole'
fBsphi_op.ref = 'arxiv:hep-ph/0412079'
fBsphi_op.methods = 'LQCD'
fBsphi_op.description = f"用{fBsphi_op.param_form}参数化，实现了{fBsphi_op.ff_names}，参考了{fBsphi_op.ref}"
fBsphi.add_impl(fBsphi_op)
# -----------------------------------
fDK = FormFactor("D", "K")

fDK_zp = Impl("fDK_zp")
fDK_zp.ff_obj = fDK
fDK_zp.ff_names = ['f+', 'f0']
fDK_zp.param_form = 'z-param'
fDK_zp.ref = 'arXiv:1706.03017'
fDK_zp.methods = 'LQCD'
fDK_zp.description = f"用{fDK_zp.param_form}参数化，实现了{fDK_zp.ff_names}，参考了{fDK_zp.ref}"
fDK.add_impl(fDK_zp)
# -----------------------------------
fDpi = FormFactor("D", "pi")

fDpi_zp = Impl("fDpi_zp")
fDpi_zp.ff_obj = fDpi
fDpi_zp.ff_names = ['f+', 'f0']
fDpi_zp.param_form = 'z-param'
fDpi_zp.ref = 'arXiv:1706.03017'
fDpi_zp.methods = 'LQCD'
fDpi_zp.description = f"用{fDpi_zp.param_form}参数化，实现了{fDpi_zp.ff_names}，参考了{fDpi_zp.ref}"
fDpi.add_impl(fDpi_zp)
# -----------------------------------
fBsK = FormFactor("Bs", "K")

fBsK_zp = Impl("fBsK_zp")
fBsK_zp.ff_obj = fBsK
fBsK_zp.ff_names = ['f+', 'f0']
fBsK_zp.param_form = 'z-param'
fBsK_zp.ref = 'FLAG'
fBsK_zp.methods = 'LQCD'
fBsK_zp.description = f"用{fBsK_zp.param_form}参数化，实现了{fBsK_zp.ff_names}，参考了{fBsK_zp.ref}"
fBsK.add_impl(fBsK_zp)
print(fBpi.impls)
