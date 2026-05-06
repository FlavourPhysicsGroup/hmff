# 类型说明

FormFactor 和 Impl 类都从 YAML 文件中读入的数据初始化.

## Class: FormFactor(name: str, configs: dict)

### 属性

- IS (str): 初态强子名称, e.g. "B"
- FS (str): 末态强子名称, e.g. "K"
- name (str): e.g. "B->K"
- description (str): 可以长篇大论
- ff_names (list): e.g. ['f+', 'f0', 'A1', 'A2', 'A3', 'T1', ...]
- impl_names (list): 所有实现（implementations）的名称
- \_impls (dict): 所有实现的集合, e.g. {'one-pole': impl_obj}
  , 其中 impl_obj (Impl): Impl 类的对象 (object)

### 方法

- set_description(des: str) -> none
- add_impl(impl_obj: Impl) -> none
- get_impl(impl_name: str = 'one-pole') -> Impl

## Class: Impl(name: str, configs: dict)

### 属性

- name (str)
- configs (dict)
- comment (str)
- ref (str)
- citation (str)
- method (str)
- form_factor_names (list of str) : e.g. ['f+', 'f0']

### 方法

- form_factor_function(ff_name: str) -> Callable[[float], float]
- get_central_values(qsq: float) -> dict
