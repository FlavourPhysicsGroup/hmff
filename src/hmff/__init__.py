"""通过 formfactors 字典获取所有信息, 形如: HMFF.formfactors['B->K']"""

from hmff import data_io

formfactors = data_io.LazyFormFactorLoader()
