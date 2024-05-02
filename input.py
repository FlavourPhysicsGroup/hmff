import classes as ff
import utils

fBpi = ff.FormFactor("B", "pi")
fBpi.set_description("描述B和pi介子相互作用的形状因子")
utils.formfactors[fBpi.name] = fBpi.obj_name

fBpi_zp = ff.Impl("fBpi_zp",
                  ff_names=['f+', 'f0'],
                  param_form='z-param',
                  ref='arXiv：1501.05373 [hep-lat]',
                  methods='LQCD')
fBpi_zp.ff_obj = fBpi
fBpi_zp.description = f"用{fBpi_zp.param_form}参数化，实现了{fBpi_zp.ff_names}，参考了{fBpi_zp.ref}"
fBpi.add_impl(fBpi_zp)

fBpi_op = ff.Impl("fBpi_op",
                  ff_names=['f+', 'f0', 'fT'],
                  param_form='one-pole',
                  ref='arxiv:hep-ph/0406232',
                  methods='LCSR')
fBpi_op.description = f"用{fBpi_op.param_form}参数化，实现了{fBpi_op.ff_names}，参考了{fBpi_op.ref}"
fBpi_op.ff_obj = fBpi
fBpi.add_impl(fBpi_op)
# -----------------------------------
fBD = ff.FormFactor("B", "D")
utils.formfactors[fBD.name] = fBD.obj_name

fBD_zp = ff.Impl("fBD_zp",
                 ff_names=['f+', 'f0'],
                 param_form='z-param',
                 ref='arXiv：1505.03925 [hep-lat]',
                 methods='LQCD')
fBD_zp.ff_obj = fBD
fBD_zp.description = f"用{fBD_zp.param_form}参数化，实现了{fBD_zp.ff_names}，参考了{fBD_zp.ref}"
fBD.add_impl(fBD_zp)
# -----------------------------------
fBK = ff.FormFactor("B", "K")
utils.formfactors[fBK.name] = fBK.obj_name

fBK_op = ff.Impl("fBK_op",
                 ff_names=['f+', 'f0', 'fT'],
                 param_form='one-pole',
                 ref='arxiv:hep-ph/0406232',
                 methods='LCSR')
fBK_op.ff_obj = fBK
fBK_op.description = f"用{fBK_op.param_form}参数化，实现了{fBK_op.ff_names}，参考了{fBK_op.ref}"
fBK.add_impl(fBK_op)

fBK_zp = ff.Impl("fBK_zp",
                 ff_names=['f+', 'f0', 'fT'],
                 param_form='z-param',
                 ref='arXiv:1501.00367 [hep-lat]',
                 methods='LQCD')
fBK_zp.ff_obj = fBK
fBK_zp.description = f"用{fBK_zp.param_form}参数化，实现了{fBK_zp.ff_names}，参考了{fBK_zp.ref}"
fBK.add_impl(fBK_zp)
# -----------------------------------
fBeta = ff.FormFactor("B", "eta")
utils.formfactors[fBeta.name] = fBeta.obj_name

fBeta_op = ff.Impl("fBeta_op",
                   ff_names=['f+', 'f0', 'fT'],
                   param_form='one-pole',
                   ref='arxiv:hep-ph/0406232',
                   methods='LCSR')
fBeta_op.ff_obj = fBeta
fBeta_op.description = f"用{fBeta_op.param_form}参数化，实现了{fBeta_op.ff_names}，参考了{fBeta_op.ref}"
fBeta.add_impl(fBeta_op)
# -----------------------------------
fBrho = ff.FormFactor("B", "rho")
utils.formfactors[fBrho.name] = fBrho.obj_name

fBrho_op = ff.Impl("fBrho_op",
                   ff_names=['V', 'A0', 'A1', 'A2', 'T1', 'T2', 'T3'],
                   param_form='one-pole',
                   ref='arxiv:hep-ph/0412079',
                   methods='LCSR')
fBrho_op.ff_obj = fBrho
fBrho_op.description = f"用{fBrho_op.param_form}参数化，实现了{fBrho_op.ff_names}，参考了{fBrho_op.ref}"
fBrho.add_impl(fBrho_op)
# -----------------------------------
fBsKstar = ff.FormFactor("Bs", "K*")
utils.formfactors[fBsKstar.name] = fBsKstar.obj_name

fBsKstar_op = ff.Impl("fBsKstar_op",
                      ff_names=['V', 'A0', 'A1', 'A2', 'T1', 'T2', 'T3'],
                      param_form='one-pole',
                      ref='arxiv:hep-ph/0412079',
                      methods='LCSR')
fBsKstar_op.ff_obj = fBsKstar
fBsKstar_op.description = f"用{fBsKstar_op.param_form}参数化，实现了{fBsKstar_op.ff_names}，\
    参考了{fBsKstar_op.ref}"
fBsKstar.add_impl(fBsKstar_op)
# -----------------------------------
fBKstar = ff.FormFactor("B", "K*")
utils.formfactors[fBKstar.name] = fBKstar.obj_name

fBKstar_op = ff.Impl("fBKstar_op",
                     ff_names=['V', 'A0', 'A1', 'A2', 'T1', 'T2', 'T3'],
                     param_form='one-pole',
                     ref='arxiv:hep-ph/0412079',
                     methods='LCSR')
fBKstar_op.ff_obj = fBKstar
fBKstar_op.description = f"用{fBKstar_op.param_form}参数化，实现了{fBKstar_op.ff_names}，参考了{fBKstar_op.ref}"
fBKstar.add_impl(fBKstar_op)

# -----------------------------------
fBomega = ff.FormFactor("B", "omega")
utils.formfactors[fBomega.name] = fBomega.obj_name

fBomega_op = ff.Impl("fBomega_op",
                     ff_names=['V', 'A0', 'A1', 'A2', 'T1', 'T2', 'T3'],
                     param_form='one-pole',
                     ref='arxiv:hep-ph/0412079',
                     methods='LCSR')
fBomega_op.ff_obj = fBomega
fBomega_op.description = f"用{fBomega_op.param_form}参数化，实现了{fBomega_op.ff_names}，参考了{fBomega_op.ref}"
fBomega.add_impl(fBomega_op)
# -----------------------------------
fBsphi = ff.FormFactor("Bs", "phi")
utils.formfactors[fBsphi.name] = fBsphi.obj_name

fBsphi_op = ff.Impl("fBsphi_op",
                    ff_names=['V', 'A0', 'A1', 'A2', 'T1', 'T2', 'T3'],
                    param_form='one-pole',
                    ref='arxiv:hep-ph/0412079',
                    methods='LCSR')
fBsphi_op.ff_obj = fBsphi
fBsphi_op.description = f"用{fBsphi_op.param_form}参数化，实现了{fBsphi_op.ff_names}，参考了{fBsphi_op.ref}"
fBsphi.add_impl(fBsphi_op)
# -----------------------------------
fDK = ff.FormFactor("D", "K")
utils.formfactors[fDK.name] = fDK.obj_name

fDK_zp = ff.Impl("fDK_zp",
                 ff_names=['f+', 'f0'],
                 param_form='z-param',
                 ref='arXiv:1706.03017[hep-lat]',
                 methods='LQCD')
fDK_zp.ff_obj = fDK
fDK_zp.description = f"用{fDK_zp.param_form}参数化，实现了{fDK_zp.ff_names}，参考了{fDK_zp.ref}"
fDK.add_impl(fDK_zp)
# -----------------------------------
fDpi = ff.FormFactor("D", "pi")
utils.formfactors[fDpi.name] = fDpi.obj_name

fDpi_zp = ff.Impl("fDpi_zp",
                  ff_names=['f+', 'f0'],
                  param_form='z-param',
                  ref='arXiv:1706.03017[hep-lat]',
                  methods='LQCD')
fDpi_zp.ff_obj = fDpi
fDpi_zp.description = f"用{fDpi_zp.param_form}参数化，实现了{fDpi_zp.ff_names}，参考了{fDpi_zp.ref}"
fDpi.add_impl(fDpi_zp)
# -----------------------------------
fBsK = ff.FormFactor("Bs", "K", ff_names=['f+', 'f0'])
utils.formfactors[fBsK.name] = fBsK.obj_name

fBsK_zp = ff.Impl("fBsK_zp",
                  ff_names=['f+', 'f0'],
                  param_form='z-param',
                  ref='arXiv：1501.05373 [hep-lat]',
                  methods='LQCD')
fBsK_zp.ff_obj = fBsK
fBsK_zp.description = f"用{fBsK_zp.param_form}参数化，实现了{fBsK_zp.ff_names}，参考了{fBsK_zp.ref}"
fBsK.add_impl(fBsK_zp)
