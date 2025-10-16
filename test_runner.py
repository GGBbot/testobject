import os
import time
import pytest

# ------------------ 1️⃣ 生成唯一的报告文件夹 ------------------
timestamp = time.strftime("%Y%m%d_%H%M%S")
report_dir = os.path.join("report", timestamp)
os.makedirs(report_dir, exist_ok=True)
print(f"📂 测试报告目录: {report_dir}")

# ------------------ 2️⃣ 配置 pytest 参数 ------------------
pytest_args = [
    "tests",  # 测试用例目录
    f"--alluredir={report_dir}",  # Allure 原始数据输出
    "--clean-alluredir",          # 每次清理原始数据
]

# ------------------ 3️⃣ 运行测试 ------------------
exit_code = pytest.main(pytest_args)

# ------------------ 4️⃣ 生成 HTML 报告 ------------------
html_report_dir = os.path.join(report_dir, "html")
os.system(f"allure generate {report_dir} -o {html_report_dir} --clean")
print(f"✅ Allure HTML 报告生成完成: {html_report_dir}")

# ------------------ 5️⃣ 自动打开报告 ------------------
os.system(f"allure open {html_report_dir}")

# ------------------ 6️⃣ 退出码 ------------------
exit(exit_code)
