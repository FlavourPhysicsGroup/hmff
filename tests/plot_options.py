#!/usr/bin/python
from matplotlib.colors import LinearSegmentedColormap as lsc

frame_line_width = 1.1
default_rcParams = {
    'figure.figsize': (5, 4),
    'font.family': 'Times New Roman',
    # 'font.family': 'Latin Modern Mono',
    # 'font.family': 'Courier Mono',
    # 'font.monospace': 'Courier Mono',
    'font.size': 14,
    'axes.linewidth': frame_line_width,
    'axes.labelsize': 18,  # 'axes.labelweight': 'bold',
    'axes.titlesize': 18,  # 'axes.titleweight': 'bold',
    'xtick.top': True,
    'ytick.right': True,
    'xtick.minor.visible': True,
    'ytick.minor.visible': True,
    # 'xtick.major.size': 7,
    # 'ytick.major.size': 7,
    # 'xtick.minor.size': 4,
    # 'ytick.minor.size': 4,
    'xtick.major.width': frame_line_width,
    'ytick.major.width': frame_line_width,
    'xtick.minor.width': frame_line_width,
    'ytick.minor.width': frame_line_width,
    'xtick.major.size': 5,
    'ytick.major.size': 5,
    'xtick.minor.size': 3,
    'ytick.minor.size': 3,
    'xtick.direction': 'in',
    'ytick.direction': 'in',
    'xtick.labelsize': 14,
    'ytick.labelsize': 14,
    'legend.frameon': True,
    'lines.linewidth': 1,
    'mathtext.fontset': 'cm',
    # 'mathtext.cal': 'Noto Serif',
    # 'mathtext.bf': 'serif:bold:italic',
    # 'mathtext.it': 'sans:italic',
    # 'mathtext.default': 'it',
    # 'text.usetex': True,
    # 'text.latex.rcfonts': False,
    # 'text.latex.preamble': '\n'.join([
    #     r'\usepackage{amsmath}',
    # r"\usepackage{unicode-math}",   # unicode math setup
    # r"\setmainfont{Times New Roman}",  # serif font via preamble
    #  ])
}

# matplotlib.rcParams.update({
#     'figure.figsize': (7, 6),
#     'font.family': 'Times New Roman',
#     'axes.linewidth': 2,
#     'axes.labelsize': 16,  #'axes.labelweight':'bold',
#     'axes.titlesize': 16,  #'axes.titleweight':'bold',
#     'xtick.top': True,
#     'ytick.right': True,
#     'xtick.minor.visible': True,
#     'ytick.minor.visible': True,
#     'xtick.major.size': 7,
#     'ytick.major.size': 7,
#     'xtick.minor.size': 4,
#     'ytick.minor.size': 4,
#     'xtick.major.width': 2,
#     'ytick.major.width': 2,
#     'xtick.minor.width': 2,
#     'ytick.minor.width': 2,
#     'xtick.direction': 'in',
#     'ytick.direction': 'in',
#     'xtick.labelsize': 16,
#     'ytick.labelsize': 16,
#     'legend.frameon': True,
#     'mathtext.fontset': 'cm',
#     'mathtext.cal': 'Noto Serif',
#     'mathtext.bf': 'serif:bold:italic',
#     'mathtext.it': 'sans:italic',
#     'mathtext.default': 'it',
# })

colors = {
    'deeppink': '#ff4450',
    'pink': '#FFA0A0',
    'lightpink': '#FFCFCF',
    'white': '#FFFFFF',
    'purple': '#4D1D82',
    'green': '#297D45',
    'lightgray': '#EEEEEE',
    'chinese-xinhelv': '#d2b116',
    'chinese-ganlanlv': '#5e5314',
    'chinese-shilv': '#57c3c2',
    'chinese-weilan': '#29b7cb',
    'chinese-yanlan': '#1622EE',
}

# 紫-白-绿 渐变色
cm_pwg = lsc.from_list("Hcolor", [(0, '#6A4395'), (0.4999, '#E0CEF5'), (0.5, '#FFFFFF'),
                                  (0.5001, '#C0F6D2'), (1, '#3B8855')],
                       N=256)
cm_lwg = lsc.from_list("Hcolor1", [(0, '#CDEFF3'), (0.4999, '#29b7cb'), (0.5, '#000000'),
                                   (0.5001, '#6FC88E'), (1, '#EAFEFA')],
                       N=256)

fd = dict(fontsize=18, color='k', family='Times New Roman')
