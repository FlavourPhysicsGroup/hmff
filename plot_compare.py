import matplotlib
import numpy as np
from IPython.display import display
from matplotlib import pyplot as plt
from PIL import Image
from pdf2image import convert_from_path

import HMFF
from tests import plot_options as opt

matplotlib.rcParams.update(opt.default_rcParams)


def plot_data(infos: dict, ffs_func: list, ffs_tex: list, normalize: bool =False , debug=False) -> None:
    """使用HMFF模块绘制形状因子"""
    # 得到qsq的数据列表，并计算形状因子数据
    qsq = np.linspace(infos["qsq_min"], infos["qsq_max"], infos["qsq_steps"])
    ffs_data = [ff_func(qsq) for ff_func in ffs_func]

    plt.figure(figsize=(8, 6))
    x_data = qsq / infos["qsq_max"] if normalize else qsq
    [plt.plot(x_data, ffs_data[ii], label=ffs_tex[ii]) for ii in range(len(ffs_data))]

    if normalize:
        plt.xlim(infos["qsq_min"]/infos["qsq_max"], 1.0)  # 归一化后最大值为1
        plt.xlabel(r"$q^2/q^2_{max}$")
    else:
        plt.xlim(infos["qsq_min"], infos["qsq_max"])
        plt.xlabel(r"$q^2$")

    plt.ylim(infos["f_min"], infos["f_max"])
    plt.legend()
    plt.tight_layout()
    if debug:
        plt.show()
    else:
        plt.savefig(infos["figure_path"])
        plt.close()


def combine_plots(infos: dict, fig1: str, fig2: str, debug=True) -> None:
    """合并HMFF的结果图与参考图"""

    # 打开两张图片
    def load_image(fig):
        if "png" in fig:
            return Image.open(fig)
        elif "pdf" in fig:
            return convert_from_path(fig)[0]
        else:
            raise ValueError("Invalid file format")

    img1 = load_image(fig1)
    img2 = load_image(fig2)

    # 假设你想根据第一张图片的高度调整第二张图片的高度
    new_height = img1.height  # 新高度为第一张图片的高度
    new_width2 = int(img2.width * (new_height / img2.height))  # 按比例调整第二张图片的宽度

    # 调整图片大小
    img2_resized = img2.resize((new_width2, new_height))

    # 创建一个新的空白图片，宽度是两张图片宽度之和，高度取两者中较大者
    total_width = img1.width + img2_resized.width
    max_height = max(img1.height, img2_resized.height)
    combined_img = Image.new("RGB", (total_width, max_height))

    # 将两张图片粘贴到新的空白图片上
    combined_img.paste(img1, (0, 0))
    combined_img.paste(img2_resized, (img1.width, 0))

    # 保存结果
    if debug:
        display(combined_img)
    else:
        combined_img.save(infos["combined_figure_path"])


def compare(process, impl, test_info):
    """通过基本信息, 绘制对比图. 为了隐藏内部实现, 通用性有待进一步验证."""
    # 基础信息重新排列, 使符合函数要求
    impl_info = test_info[process][impl]
    if impl_info.get("combined"):
        ffs_names = tuple(impl_info["form factors"].keys())
        ffs_tex = [impl_info["form factors"][ff]["tex"] for ff in ffs_names]
        infos = impl_info["form factors"][ffs_names[0]]

        ffs_impl = HMFF.formfactors[process].get_impl(impl)
        ffs_func = [ffs_impl.form_factor_function(ff) for ff in ffs_names]
        normalize = impl_info.get("normalize_qsq", False)

        plot_data(infos, ffs_func, ffs_tex, normalize)
        combine_plots(infos, infos["figure_path"], infos["ref_figure_path"])
    else:
        ffs_names = tuple(impl_info["form factors"].keys())
        for ff in ffs_names:
            infos = impl_info["form factors"][ff]
            ffs_tex = [
                infos["tex"],
            ]
            ffs_func = [
                HMFF.formfactors[process].get_impl(impl).form_factor_function(ff),
            ]
            normalize = impl_info.get("normalize_qsq", False)

            plot_data(infos, ffs_func, ffs_tex, normalize)
            combine_plots(infos, infos["figure_path"], infos["ref_figure_path"])
