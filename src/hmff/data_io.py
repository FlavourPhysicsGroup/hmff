"""读入YAML数据文件, 通过 LazyFormFactorLoader 字典类调用信息,
这样可以提高加载时的效率, 避免重复加载."""

import yaml
import importlib.resources as pkg_resources


class LazyFormFactorLoader:
    """懒加载器, 使用上类似 dict, 但是只有在取值时才会加载数据"""

    @staticmethod
    def read_yaml(data_pkg_name):
        """读取data/*.yaml文件, data_pkg_name: 以包名为根目录的相对路径, 如 HMFF.src.data"""
        result = {}
        with pkg_resources.path(data_pkg_name, "") as data_dir:
            for file in data_dir.iterdir():
                if file.name not in ["P_P.yaml", "P_V.yaml", "B_B.yaml"]:
                    continue
                if file.is_file() and file.suffix.lower() in (".yaml", ".yml"):
                    try:
                        with open(file, "r", encoding="utf-8") as f:
                            content = yaml.safe_load(f) or {}
                            result.update(content)
                    except Exception as e:
                        print(f"[Error] Failed to load {file.name}: {e}")
        return result

    @staticmethod
    def build_formfactors(configs: dict) -> dict:
        from .classes import FormFactor

        return {
            name: FormFactor(name, impl_configs)
            for name, impl_configs in configs.items()
        }

    def __init__(self, package="hmff.data"):
        self.package = package
        self._cache = None

    def reload(self):
        self._cache = None
        self._load()

    def _load(self):
        if self._cache is None:
            raw_data = self.read_yaml(self.package)
            self._cache = self.build_formfactors(raw_data)
        return self._cache

    def get_formfactor(self, name):
        return self._load().get(name)

    def __getitem__(self, item):
        return self.get_formfactor(item)

    def keys(self):
        return self._load().keys()

    def items(self):
        return self._load().items()
