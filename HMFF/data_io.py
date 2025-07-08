"""读入YAML数据文件, 将结构化数据返回"""

import yaml
import importlib.resources as pkg_resources

def read_yaml(file_name):
    """读取data/*.yaml文件, file_name: 文件名(带后缀)"""
    result = {}
    with pkg_resources.path("HMFF.src.data", '') as data_dir:
        for file in data_dir.iterdir():
            if file.name not in ['P_P.yaml', 'P_V.yaml', 'B_B.yaml']:
                continue
            if file.is_file() and file.suffix.lower() in ('.yaml', '.yml'):
                try:
                    with open(file, 'r', encoding='utf-8') as f:
                        content = yaml.safe_load(f) or {}
                        result.update(content)
                except Exception as e:
                    print(f"[Error] Failed to load {file.name}: {e}")
    return result


def build_formfactors(configs: dict) -> dict:
    from .classes import FormFactor
    return {name: FormFactor(name, impl_configs)
            for name, impl_configs in configs.items()
            }


# 懒加载器
class LazyFormFactorLoader:
    def __init__(self, package="my_project.src.data"):
        self.package = package
        self._cache = None

    def reload(self):
        self._cache = None

    def _load(self):
        if self._cache is None:
            raw_data = read_yaml(self.package)
            self._cache = build_formfactors(raw_data)
        return self._cache

    def get_formfactor(self, name):
        return self._load().get(name)

    def __getitem__(self, item):
        return self.get_formfactor(item)

    def keys(self):
        return self._load().keys()

    def items(self):
        return self._load().items()


# 全局懒加载器实例
formfactors = LazyFormFactorLoader()