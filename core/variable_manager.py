 # 全局变量管理（保存token等）
class VariableManager:
    """全局变量管理器，用于保存token等"""
    _vars = {}

    @classmethod
    def set(cls, key, value):
        cls._vars[key] = value

    @classmethod
    def get(cls, key, default=None):
        return cls._vars.get(key, default)

    @classmethod
    def get_all(cls):
        return cls._vars
