# 测试执行入口脚本
import pytest
import json
from core.yaml_loader import load_all_cases
from core.request_util import send_request
from core.variable_manager import VariableManager

def extract_json_value(data, path):
    """通用提取 JSON 值"""
    if not path:
        return None

    current = None
    if path.startswith("json."):
        current = data.get("json", {})
        path = path[5:]
    elif path.startswith("status."):
        current = data.get("status", {})
        path = path[7:]
    else:
        # 先直接找根 key，再去 json 查
        current = data.get(path, data.get("json", {}))
        if current != data.get(path):
            return current  # 如果根 key 找到直接返回

    for part in path.split("."):
        if "[" in part and "]" in part:
            key, index_str = part[:-1].split("[")
            current = current.get(key, [])
            try:
                index = int(index_str)
                current = current[index]
            except (ValueError, IndexError, TypeError):
                return None
        else:
            if isinstance(current, dict):
                current = current.get(part)
            else:
                return None

        if current is None:
            return None
    return current

@pytest.mark.parametrize("case", load_all_cases())
def test_api(case):
    data = case["content"]
    if "single_cases" in data:
        data = data["single_cases"][0]

    name = data.get("name")
    print(f"\n🧩 正在执行用例: {name}")

    method = data.get("method", "get").lower()
    url = data.get("url")
    json_data = data.get("json", {})
    params = data.get("params", {})
    headers = data.get("headers", {})

    res = send_request(method, url, json=json_data, params=params, headers=headers)

    print(f"响应状态码: {res.status_code}")
    try:
        resp_json = res.json()
        print("响应结果:", json.dumps(resp_json, ensure_ascii=False, indent=2))
    except Exception:
        print("响应非JSON:", res.text)
        resp_json = {}

    # -------------------- 提取变量 --------------------
    extract = data.get("extract", [])
    if isinstance(extract, list):
        for item in extract:
            var_name = item.get("name")
            path = item.get("path")
            is_global = item.get("global", False)
            value = extract_json_value({"json": resp_json}, path)
            if is_global:
                VariableManager.set(var_name, value)
                print(f"🔧 全局变量已保存: {var_name} = {value}")
            else:
                case[var_name] = value

    # -------------------- 断言 --------------------
    data_for_assert = {"json": resp_json, "status": {"code": res.status_code}}
    validate_rules = data.get("validate_rules", [])
    for rule in validate_rules:
        check = rule.get("check")
        comparator = rule.get("comparator")
        expected = rule.get("expected")

        actual_value = extract_json_value(data_for_assert, check)

        if comparator == "eq":
            assert actual_value == expected, f"❌ {check} 实际为 {actual_value}, 预期为 {expected}"
        elif comparator == "ne":
            assert actual_value != expected, f"❌ {check} 实际为 {actual_value}, 不应等于 {expected}"
        elif comparator == "gt":
            assert actual_value > expected, f"❌ {check} 实际为 {actual_value}, 应大于 {expected}"
        elif comparator == "lt":
            assert actual_value < expected, f"❌ {check} 实际为 {actual_value}, 应小于 {expected}"

    print(f"✅ 用例 [{name}] 执行完成\n")
