import os
from pathlib import Path

import pytest
import yaml

# 数据 yaml 目录: 仓库根/src/hmff/data (重构后位置, 旧路径 HMFF/src/data 已不存在)
DATA_DIR = Path(__file__).parent.parent / "src" / "hmff" / "data"

_YAML_FILES = sorted(f for f in os.listdir(DATA_DIR) if f.endswith((".yaml", ".yml")))


@pytest.mark.parametrize("yaml_file", _YAML_FILES)
def test_yaml_top_level_keys(yaml_file):
    """顶层键须形如 '初态->末态'; 每个实现须为 dict, 其 form factors 为非空 dict."""
    with open(DATA_DIR / yaml_file, encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}
    assert isinstance(data, dict), f"{yaml_file} 顶层不是 dict"

    for key, impls in data.items():
        # 顶层键: "初态->末态"
        assert isinstance(key, str) and key.count("->") == 1, (
            f"顶层键 '{key}' 须恰好含一个 '->' (格式 初态->末态)"
        )
        assert isinstance(impls, dict) and impls, f"'{key}' 须为非空 dict"

        for impl_name, impl_cfg in impls.items():
            assert isinstance(impl_cfg, dict), f"{key}/{impl_name} 不是 dict"
            ffs = impl_cfg.get("form factors")
            if ffs is not None:
                assert isinstance(ffs, dict) and ffs, f"{key}/{impl_name}: form factors 须为非空 dict"
                for ff_name, ff_cfg in ffs.items():
                    assert isinstance(ff_cfg, dict), f"{key}/{impl_name}/{ff_name} 不是 dict"

