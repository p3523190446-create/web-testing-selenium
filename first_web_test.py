"""第一条网页自动化练习：Selenium 官方示例，不是比赛真题。"""
import argparse
import json
import os
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

parser = argparse.ArgumentParser()
parser.add_argument("--show", action="store_true", help="显示浏览器窗口")
args = parser.parse_args()
here = Path(__file__).resolve().parent
evidence = here / "运行结果"
evidence.mkdir(exist_ok=True)
os.environ.setdefault("SE_AVOID_STATS", "true")
options = webdriver.ChromeOptions()
options.binary_location = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
if not args.show:
    options.add_argument("--headless=new")
options.add_argument("--window-size=1280,900")
driver = webdriver.Chrome(options=options)
result = {"练习": "填写并提交官方示例表单", "状态": "失败"}
try:
    driver.set_page_load_timeout(40)
    # 1. 打开专门用于学习的示例表单。
    driver.get("https://www.selenium.dev/selenium/web/web-form.html")
    wait = WebDriverWait(driver, 15)
    field = wait.until(EC.visibility_of_element_located((By.NAME, "my-text")))
    # 2. 填写内容，并确认输入框确实收到了文字。
    field.send_keys("Selenium practice")
    if field.get_attribute("value") != "Selenium practice":
        raise AssertionError("输入框内容不符合预期")
    driver.save_screenshot(str(evidence / "01-填写完成.png"))
    # 3. 点击提交，等待结果出现，再核对它是否符合预期。
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    wait.until(EC.text_to_be_present_in_element((By.ID, "message"), "Received!"))
    actual = driver.find_element(By.ID, "message").text
    if actual != "Received!":
        raise AssertionError(f"提交结果不符合预期：{actual!r}")
    driver.save_screenshot(str(evidence / "02-提交结果.png"))
    result.update({"状态": "通过", "预期": "Received!", "实际": actual,
                   "浏览器版本": driver.capabilities.get("browserVersion"),
                   "说明": "仅验证示例操作链路，不代表官方赛题完成或比赛环境验收"})
except Exception as exc:
    result["错误"] = str(exc)
    driver.save_screenshot(str(evidence / "失败现场.png"))
    raise
finally:
    (evidence / "result.json").write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    driver.quit()
print(json.dumps(result, ensure_ascii=False, indent=2))
