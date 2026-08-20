import pytest
import yaml
import os
from pathlib import Path

# 合法的初态和末态粒子名称
VALID_PARTICLES = {'B', 'Bs', 'K', 'pi', 'eta', 'D', 'rho', 'omega', 'phi', 'K*', 'Lambda_b', 'Lambda', 'Lambda_1520'}

# 扫描所有 .yaml 文件
DATA_DIR = Path(__file__).parent.parent / 'HMFF' / 'src' / 'data'

@pytest.mark.parametrize("yaml_file", [f for f in os.listdir(DATA_DIR) if f.endswith('.yaml')])
def test_yaml_top_level_keys(yaml_file):
    """
    测试每个 YAML 文件的顶层键是否符合格式：初态->末态
    且初态和末态必须在 VALID_PARTICLES 中
    """
    file_path = DATA_DIR / yaml_file
    with open(file_path, 'r') as f:
        data = yaml.safe_load(f)

    # 确保是字典
    assert isinstance(data, dict), f"Top level of {yaml_file} is not a dictionary"

    for key in data.keys():
        # 检查格式是否包含 '->'
        assert '->' in key, f"Key '{key}' in {yaml_file} does not contain '->'. Expected format: initial_state->final_state"

        parts = key.split('->')
        assert len(parts) == 2, f"Key '{key}' in {yaml_file} has more than one '->'. Expected format: initial_state->final_state"

        src, tgt = parts[0].strip(), parts[1].strip()

        # 检查粒子是否在白名单中
        assert src in VALID_PARTICLES, f"Initial state '{src}' in {yaml_file} not recognized. Valid particles: {VALID_PARTICLES}"
        assert tgt in VALID_PARTICLES, f"Final state '{tgt}' in {yaml_file} not recognized. Valid particles: {VALID_PARTICLES}"

        # 二级键名检查
        sub_dict = data[key]
        assert isinstance(sub_dict, dict), f"Value of key '{key}' in {yaml_file} is not a dictionary"

        for sub_key in sub_dict.keys():
            # 检查是否以 LQCD 或 LCSR 开头，且无空格
            assert sub_key.startswith(('LQCD-', 'LCSR-')), \
                f"Sub-key '{sub_key}' in {yaml_file} must start with 'LQCD' or 'LCSR'."
            assert ' ' not in sub_key, \
                f"Sub-key '{sub_key}' in {yaml_file} contains space(s). Not allowed."

            # 三级键检查
            third_level = sub_dict[sub_key]
            assert isinstance(third_level, dict), \
                f"Third-level value of '{sub_key}' in {yaml_file} is not a dictionary"

            allowed_keys = {
                'ref', 'author', 'citation key', 'method', 'comment', 'form factors',
                'covariance_matrix', 'combined', 'plot', 'plots', 'groups'
            }
            for k in third_level.keys():
                assert k in allowed_keys, \
                    f"Unexpected key '{k}' in {yaml_file}. Allowed keys: {allowed_keys}"

            required_keys = {'ref', 'author', 'form factors'}
            missing_keys = required_keys - set(third_level.keys())
            assert not missing_keys, \
                f"Missing required keys {missing_keys} in {yaml_file} under '{sub_key}'"
