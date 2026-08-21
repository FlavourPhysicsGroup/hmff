import matplotlib
import numpy as np
import os
from IPython.display import display
from matplotlib import pyplot as plt
from PIL import Image
from pdf2image import convert_from_path
from HMFF.src import z_parameterization as zp
import HMFF
from tests import plot_options as opt
import yaml
matplotlib.rcParams.update(opt.default_rcParams)


def plot_data(infos: dict, ffs_func: list, f_error_stat, ff, ffs_tex: list, normalize: bool =False, is_HO: bool =False,
              process: str =None, ho_impl: str =None, nominal_impl: str =None, xaxis: str =None) -> None:
    debug=False
    """使用HMFF模块绘制形状因子

    xaxis='w' 时横轴画成 w (=v·v'), 与论文面板 (arXiv:2107.13140 Fig.8/9) 对齐;
    此时 infos 需要提供 w_min/w_max, 质量从形状因子参数中的 m_initial/m_final 获取.
    """
    plot_w = (xaxis == "w")
    if plot_w:
        # 从形状因子参数中取初末态重子质量, 把 w 网格换算成 q^2 再求值
        impl_obj = HMFF.formfactors[process].get_impl(ho_impl)
        pars = impl_obj.config["form factors"][ff]["parameter"]
        m_initial = pars.get("m_initial")
        m_final = pars.get("m_final")
        w_pts = np.linspace(infos["w_min"], infos["w_max"], infos["qsq_steps"])
        qsq = m_initial**2 + m_final**2 - 2 * m_initial * m_final * w_pts
    else:
        qsq = np.linspace(infos["qsq_min"], infos["qsq_max"], infos["qsq_steps"])
    # 得到qsq的数据列表，并计算形状因子数据
    ffs_data = [ff_func(qsq) for ff_func in ffs_func]



    plt.figure(figsize=(8, 6))
    if plot_w:
        x_data = w_pts
    else:
        x_data = qsq / infos["qsq_max"] if normalize else qsq

    # 填充不确定区域 - 只给第一个填充添加标签避免重复
    if f_error_stat is not None:
        if callable(f_error_stat):
            f_std = [f_error_stat(qsq)]
        else:
            f_std = [error_func(qsq) for error_func in f_error_stat]

        # 检查误差是否全为0（即没有协方差数据的情况）
        if any(not np.allclose(std, 0) for std in f_std):
            for ii in range(len(ffs_data)):
                plt.fill_between(x_data, 
                         ffs_data[ii] - f_std[ii], 
                         ffs_data[ii] + f_std[ii], 
                         color='#87CEFA', alpha=0.3, 
                         label='Statistical Uncertainty' if ii == 0 else "")

    # Draw central curves after the bands so nearby curves remain visible.
    for ii in range(len(ffs_data)):
        plt.plot(x_data, ffs_data[ii], label=ffs_tex[ii], linewidth=1.8, zorder=3)


    #添加总误差的填充区域
    if is_HO is True:
        ho_obj = HMFF.formfactors[process].get_impl(ho_impl)
        nominal_obj = HMFF.formfactors[process].get_impl(nominal_impl)
        o_ho = ho_obj.form_factor_function(ff)(qsq)
        o = nominal_obj.form_factor_function(ff)(qsq)
        sigma_O_HO = ho_obj.get_sigma_f_stat(ff)(qsq)
        sigma_O = nominal_obj.get_sigma_f_stat(ff)(qsq)
        f_error_syst = []
        f_error_total = []
        for ii in range(len(o_ho)):
            a = zp.calculate_systematic_error_v2(o[ii], o_ho[ii], sigma_O[ii], sigma_O_HO[ii])
            b = zp.calculate_total_error(sigma_O[ii], a)
            f_error_syst.append(a)
            f_error_total.append(b)

        f_total = f_error_total
        for ii in range(len(ffs_data)):
            plt.fill_between(x_data, 
                    ffs_data[ii] - f_total[ii], 
                    ffs_data[ii] + f_total[ii], 
                    color='#FFB6C1', alpha=0.3, 
                    label='Total Uncertainty' if ii == 0 else "")


    if plot_w:
        plt.xlim(infos["w_min"], infos["w_max"])
        plt.xlabel(r"$w$")
    elif normalize:
        plt.xlim(infos["qsq_min"]/infos["qsq_max"], 1.0)  # 归一化后最大值为1
        plt.xlabel(r"$q^2/q^2_{max}$")
    else:
        plt.xlim(infos["qsq_min"], infos["qsq_max"])
        plt.xlabel(r"$q^2$")

    plt.ylim(infos["f_min"], infos["f_max"])
    if infos.get("title"):
        plt.title(infos["title"])
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
    if not os.path.exists(fig2):
        if debug:
            display(img1)
        return
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
    if "groups" in impl_info:
        ffs_impl = HMFF.formfactors[process].get_impl(impl)
        for group_info in impl_info["groups"].values():
            ffs_names = tuple(group_info["form factors"])
            ffs_func = [ffs_impl.form_factor_function(ff) for ff in ffs_names]
            ffs_tex = [group_info.get("tex", {}).get(ff, ff) for ff in ffs_names]
            f_error = [ffs_impl.get_sigma_f_stat(ff) for ff in ffs_names]
            plot_data(group_info, ffs_func, f_error, 0, ffs_tex, False, is_HO=False)
            combine_plots(group_info, group_info["figure_path"], group_info["ref_figure_path"])
        return

    if "plots" in impl_info:
        ffs_impl = HMFF.formfactors[process].get_impl(impl)
        for plot_info in impl_info["plots"].values():
            ffs_names = tuple(plot_info["form factors"])
            ffs_tex = [plot_info["form factors"][ff]["tex"] for ff in ffs_names]
            infos = plot_info["form factors"][ffs_names[0]]
            ffs_func = [ffs_impl.form_factor_function(ff) for ff in ffs_names]
            f_error = [ffs_impl.get_sigma_f_stat(ff) for ff in ffs_names]
            plot_data(infos, ffs_func, f_error, 0, ffs_tex, False, is_HO=False)
            combine_plots(infos, infos["figure_path"], infos["ref_figure_path"])
        return

    plot_info = impl_info.get("plot", impl_info)
    if plot_info.get("combined"):
        ffs_names = tuple(plot_info["form factors"].keys())
        ffs_tex = [plot_info["form factors"][ff]["tex"] for ff in ffs_names]
        infos = plot_info["form factors"][ffs_names[0]]

        ffs_impl = HMFF.formfactors[process].get_impl(impl)
        ffs_func = [ffs_impl.form_factor_function(ff) for ff in ffs_names]
        normalize = impl_info.get("normalize_qsq", False)
        f_error = [ffs_impl.get_sigma_f_stat(ff) for ff in ffs_names]

        plot_data(infos, ffs_func, f_error,0 , ffs_tex, normalize, is_HO=False)
        combine_plots(infos, infos["figure_path"], infos["ref_figure_path"])
    else:
        ffs_names = tuple(plot_info["form factors"].keys())
        # 通用地识别 "-HO" 实现: 若存在对应的 "-nominal" 实现, 则把 nominal 曲线
        # 与总(统计+系统)误差带一起画, 类似 Lambda_b->Lambda 的 LQCD-2016-HO 处理.
        is_HO = False
        nominal_impl_name = None
        if impl.endswith("-HO"):
            candidate = impl[:-3] + "nominal"
            if candidate in HMFF.formfactors[process].impl_names:
                is_HO = True
                nominal_impl_name = candidate
        for ff in ffs_names:
            infos = plot_info["form factors"][ff]
            ffs_tex = [
                infos["tex"],
            ]
            normalize = impl_info.get("normalize_qsq", False)
            xaxis = impl_info.get("xaxis")
            if is_HO:
                nominal_impl = HMFF.formfactors[process].get_impl(nominal_impl_name)
                ffs_func = [nominal_impl.form_factor_function(ff)]
                f_error_stat = nominal_impl.get_sigma_f_stat(ff)
            else:
                ffs_func = [HMFF.formfactors[process].get_impl(impl).form_factor_function(ff)]
                f_error_stat = HMFF.formfactors[process].get_impl(impl).get_sigma_f_stat(ff)

            plot_data(infos, ffs_func, f_error_stat, ff, ffs_tex, normalize, is_HO,
                      process=process, ho_impl=impl, nominal_impl=nominal_impl_name, xaxis=xaxis)
            combine_plots(infos, infos["figure_path"], infos["ref_figure_path"])


def compare_all(impl, test_info, processes=("B->K*", "Bs->phi", "Bs->K*"),
                figure_path="tests/figures/LQCD-2015-all-processes.pdf"):
    """Draw vector and tensor form factors for all processes in one 2x3 figure."""
    groups = ("vector", "tensor")
    fig, axes = plt.subplots(2, len(processes), figsize=(15, 8), squeeze=False)

    for column, process in enumerate(processes):
        impl_info = test_info[process][impl]
        plot_info = impl_info["plots"]
        ffs_impl = HMFF.formfactors[process].get_impl(impl)

        for row, group_name in enumerate(groups):
            group_info = plot_info[group_name]
            ffs_names = tuple(group_info["form factors"])
            first_info = group_info["form factors"][ffs_names[0]]
            qsq = np.linspace(
                first_info.get("qsq_min", group_info.get("qsq_min", 0)),
                first_info.get("qsq_max", group_info.get("qsq_max", 20)),
                first_info.get("qsq_steps", group_info.get("qsq_steps", 200)),
            )
            axis = axes[row, column]

            for ff_name in ffs_names:
                ff_func = ffs_impl.form_factor_function(ff_name)
                ff_values = ff_func(qsq)
                axis.plot(qsq, ff_values, label=group_info["form factors"][ff_name]["tex"])

                ff_error = ffs_impl.get_sigma_f_stat(ff_name)(qsq)
                if np.any(np.asarray(ff_error) != 0):
                    axis.fill_between(qsq, ff_values - ff_error, ff_values + ff_error, alpha=0.25)

            axis.set_xlim(qsq[0], qsq[-1])
            axis.set_ylim(first_info.get("f_min", 0), first_info.get("f_max", 2.5))
            axis.set_xlabel(r"$q^2$ (GeV$^2$)")
            axis.set_ylabel("form factor")
            title = {"B->K*": r"$B \to K^*$", "Bs->phi": r"$B_s \to \phi$", "Bs->K*": r"$B_s \to K^*$"}
            axis.set_title(title.get(process, process))
            axis.legend()

    fig.tight_layout()
    fig.savefig(figure_path)
    display(fig)
    plt.close(fig)
