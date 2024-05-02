## Class: FormFactor()
### 初始化：init(IS, FS)
```python
class FormFactor():
    def __init__(self, IS, FS):
        self.name = f"{IS}->{FS} form factors"
        self.IS = IS
        self.FS = FS
        self.description = f"{IS}->{FS} form factors"
        self.implementations = {}
```

### 属性
#### IS (str): 初态强子名称, e.g. "B"
#### FS (str): 末态强子名称, e.g. "K"
#### name (str): 简短, 具有唯一性即可

#### description (str): 可以长篇大论

#### ff_names (list): e.g. ['f+', 'f0', 'A1', 'A2', 'A3', 'T1', ...]

#### impl_names (list): 所有实现（implementations）的名称

#### impls (dict): 所有实现的集合, e.g. {'one-pole': impl_obj}, 其中 impl_obj (Impl): Impl 类的对象 (object)


### 方法
#### set_description(des: str) -> none
```python
def set_description(self, des: str) -> none:
    self.description = des
```

#### add_impl(impl_obj: Impl) -> none
```python
def add_impl(self, impl_obj: Impl):
    # impl_obj (Impl): Impl 类的对象 (object)
    self.impl_name.append(impl_obj.name)
    self.impls[impl_obj.name] = impl_obj
```

#### get_impl(impl_name: str = 'one-pole') -> Impl: 判断名称存在与否, 若存在, 返回名称为 impl_name 的 impl_obj.
选做: 可以设置一个默认的名称, 若要求的实现不存在, 抛出警告, 返回默认实现.

## Class: Impl()
### init(name)
### 属性
#### name (str)
#### description (str): e.g. "只实现了标量形状因子: f+, f0. 参考了 XX 文章. 存在 XX 问题"
#### ff_names (list): e.g. ['f+', 'f0']
#### ff_tex_names (list): e.g. [r'$f_+$', r'$f_0$']
#### param_form (str): e.g. 'z-param', 'BGL' or 'one-pole'
#### methods (str): e.g. 'LQCD', 'LCSR' or 'HQEFT'
#### ref (str or list): e.g. 'arxiv:hep-ph/0412079' or 'doi:xxxx'
#### ff_obj (FormFactor): 隶属于哪个形状因子类
#### _internal_params (dict) = io.read_yaml(file)

### 方法
#### get_ref() -> str
```python
def get_ref(self) -> str:
    return self.ref
```

#### get_central_values() -> dict
```python
def get_central_values(self, qsq: float) -> dict:
    IS = self.ff_obj.IS
    FS = self.ff_obj.FS
    fp = self._internal_func_1(IS, FS, qsq)
    f0 = self._internal_func_2(IS, FS, qsq)
    return {'f+': fp, 'f0': f0}
```

#### get_values() -> dict: 留做后续考虑误差时的接口

#### _internal_func_1(): 计算具体的某个形状因子的表达式. 可以从一般形式中调用. 如 `z_param.f0`


## 数据 I/O
### 注释: 数据在磁盘中, 以 yaml 文件存储. 数据在内存中, 以 float, str, list, dict 等格式存储. 将内存中的数据存储进磁盘叫 "序列化". 可百度.有现成的 python 包可以使用, 如: yaml, pickle 等.

### read_yaml(file_name: str, Path)
### dump_yaml(file_name, data)

## 形状因子参数化形式
### 注释: 可以将参数化的最一般形式写在单独的文件中. 在 Impl 类实例化时直接调用一般形式的函数. 即 `self._internal_func_1 = z_param.f0` 之类.
### z-param.py
### one-pole.py
### BGL.py
