# HMFF — Hadronic Matrix Form Factors

[![License: GPL v3](https://img.shields.io/badge/License-GPL%20v3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![Python 3.14+](https://img.shields.io/badge/python-3.14+-blue.svg)](https://www.python.org/downloads/)

HMFF 是一个收集文献中强子跃迁形状因子（hadronic transition form factors）参数化结果的 Python 库。所有形状因子通过不同的参数化形式给出，参数值取自文献，最终形状因子数值仅是转移动量平方 $q^2$ 的函数。本项目以库的形式发布，供粒子物理研究者直接调用。

[English README](README.md)

## 架构

项目采用三层设计：

| 层级 | 类/模块 | 说明 |
|------|---------|------|
| **顶层** | `FormFactor` | 代表一个物理过程（如 $B \to K$），包含该过程的所有文献实现 |
| **中层** | `Impl` | 代表某一篇文献中给出的参数化数据，包含该文献的所有形状因子 |
| **底层** | 参数化函数 | 具体的数学参数化形式（如 BCL 1、one pole 等），以 $q^2$ 为输入返回形状因子值 |

例如，$B \to K$ 过程对应一个 `FormFactor` 对象，它包含两篇文献的实现（`Impl`）：LCSR-pole 2004 和 LQCD-FLAG-2024。每个 `Impl` 内又包含 $f_+$、$f_0$、$f_T$ 等具体形状因子，各自使用不同的参数化函数。

## 已收录的过程与文献

### 赝标量介子 → 赝标量介子（P → P）

| 过程 | 文献实现 |
|------|----------|
| $B \to \pi$ | LCSR-pole 2004, LQCD-FLAG-2024, LQCD-z 2015 |
| $B \to K$ | LCSR-pole 2004, LQCD-FLAG-2024 |
| $B \to \eta$ | LCSR-pole 2004 |
| $B_s \to K$ | LQCD-z 2015, LQCD-FLAG-2024 |
| $B \to D$ | LQCD-FLAG-2024 |
| $D \to \pi$ | LQCD-z 2017 |
| $D \to K$ | LQCD-z 2017 |

### 赝标量介子 → 矢量介子（P → V）

| 过程 | 文献实现 |
|------|----------|
| $B \to \rho$ | LCSR-pole, LQCD-2008 |
| $B \to K^*$ | LCSR-pole, LQCD-2015 |
| $B \to \omega$ | LCSR-pole |
| $B_s \to K^*$ | LCSR-pole, LQCD-2015 |
| $B_s \to \phi$ | LCSR-pole, LQCD-2015 |

### 重子 → 重子（B → B）

| 过程 | 文献实现 |
|------|----------|
| $\Lambda_b \to \Lambda$ | LQCD-2016-nominal, LQCD-2016-HO |
| $\Lambda_b \to \Lambda(1520)$ | LQCD-2021-nominal, LQCD-2021-HO |
| $\Xi_c \to \Xi$ | （待补充） |

## 支持的参数化形式

| 名称 | 公式 | 说明 |
|------|------|------|
| one pole | $f = a / (1 - q^2/m^2)$ | 单极点参数化 |
| double pole 1 | $f = a_1/(1 - q^2/m_1^2) + a_2/(1 - q^2/m_2^2)$ | 双极点参数化（独立极点质量） |
| double pole 2 | $f = a_1/(1 - q^2/m^2) + a_2/(1 - q^2/m^2)^2$ | 双极点参数化（共享极点质量） |
| BCL 1 | Bourrely-Caprini-Lellouch 参数化（含极点因子与约束） | 最常用的 z 展开 |
| BCL 2 | BCL 参数化（含约束，无极点因子） | |
| BCL 3 | BCL 参数化（纯 z 展开，无极点因子无约束） | |
| BCL 4 | BCL 参数化（含极点因子，无约束） | |
| z-expansions 1/2/3 | 其他 z 展开形式 | 待实现 |

## 快速开始

### 从 PyPI 安装（待发布）

```bash
pip install hmff
```

或使用 uv：

```bash
uv pip install hmff
```

### 从源码安装

```bash
git clone https://github.com/FlavourPhysicsGroup/hmff.git
uv add /path/to/form-factor
```

### 使用示例

```python
import hmff

# 获取所有可用过程
formfactors = hmff.formfactors
print(formfactors.keys())
# dict_keys(['B->rho', 'B->K*', ..., 'B->pi', 'B->K', ..., 'D->pi', 'D->K'])

# 获取 $B \to K$ 过程
ff_bk = formfactors['B->K']

# 查看该过程收录的文献
print(ff_bk.impl_names)  # ['LCSR-pole 2004', 'LQCD-FLAG-2024']

# 获取某篇文献的实现
impl = ff_bk.get_impl('LQCD-FLAG-2024')
print(impl.ref)           # arXiv:2411.04268
print(impl.form_factor_names)  # ['f+', 'f0', 'fT']

# 计算形状因子在 $q^2 = 10\,\mathrm{GeV}^2$ 处的值
func_fplus = impl.form_factor_function("f+")
print(func_fplus(qsq=10))  # 1.68

# 同时获取所有形状因子在给定 $q^2$ 的值
print(impl.get_central_values(qsq=10))  # {f+: ..., f0: ..., fT: ...}
```

### 误差估计

对于提供了协方差矩阵的文献（如 LQCD-FLAG-2024），可以计算统计误差：

```python
sigma_func = impl.get_sigma_f_stat("f+")
print(sigma_func(qsq=10))  # 统计误差
```

## 项目结构

```
src/hmff/
├── __init__.py          # 入口：初始化 formfactors 字典
├── classes.py           # FormFactor 和 Impl 类定义
├── data_io.py           # 懒加载 YAML 数据的 LazyFormFactorLoader
├── z_parameterization.py  # BCL 及 z 展开参数化函数
├── pole_dominance.py    # 极点主导参数化函数
└── data/
    ├── P_P.yaml         # 赝标量→赝标量过程数据
    ├── P_V.yaml         # 赝标量→矢量过程数据
    └── B_B.yaml         # 重子→重子过程数据
```

## 数据格式

所有形状因子数据以 YAML 文件存储，格式如下：

```yaml
B->K:
  LQCD-FLAG-2024:
    ref: arXiv:2411.04268
    method: LQCD
    form factors:
      f+:
        parameterization: BCL 2
        parameter: {a: [0.0, 0.1, ...], mp_1: 5.28, mp_2: 0.494, m_star: 5.37,
                    cov_matrices: [[...], [...]]}
      f0:
        parameterization: BCL 3
        parameter: {a: [0.0, 0.1, ...], mp_1: 5.28, mp_2: 0.494}
```

其中 `parameter` 中的质量参数可以使用 `m` 或 `m_sq`（程序会自动转换），协方差矩阵为可选字段。

## 开发

本项目使用 uv 管理依赖：

```bash
# 安装开发依赖
uv sync --group dev

# 运行测试
uv run pytest tests/
```

## License

本项目采用 GPLv3 许可证，详见 [LICENSE](LICENSE)。
