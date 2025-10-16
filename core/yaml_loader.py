 # 自动加载yaml
import os
import yaml

def load_all_cases(case_dir="cases"):
    """加载cases目录下所有yaml文件"""
    cases = []
    for filename in sorted(os.listdir(case_dir)):
        if filename.endswith(".yaml"):
            path = os.path.join(case_dir, filename)
            with open(path, encoding="utf-8") as f:
                content = yaml.safe_load(f)
                cases.append({"file": filename, "content": content})
    return cases
