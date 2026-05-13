import asyncio
import sys
import argparse
import os
from playwright.async_api import async_playwright
from playwright_stealth import Stealth

async def run_test(api_url, api_key, model_name):
    async with async_playwright() as p:
        # 启动浏览器，使用 stealth 插件绕过检测
        # 如果遇到较强的人机验证，可以尝试 headless=False
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        )
        page = await context.new_page()
        await Stealth().apply_stealth_async(page)

        print(f"正在访问 https://hvoy.ai/ ...")
        try:
            await page.goto("https://hvoy.ai/", wait_until="networkidle", timeout=60000)
        except Exception as e:
            print(f"访问页面失败: {e}")
            await browser.close()
            return

        # 处理 Cloudflare 可能出现的 Turnstile 验证
        try:
            # 等待输入框出现，作为页面加载完成的标志
            await page.wait_for_selector('input[placeholder*="api.anthropic.com"]', timeout=15000)
        except:
            print("页面未按预期加载，检查是否触发 Cloudflare 验证...")
            # 尝试查找 Turnstile 按钮
            try:
                # Turnstile 通常在 iframe 中
                frames = page.frames
                for frame in frames:
                    if "cloudflare" in frame.url or "turnstile" in frame.url:
                        print("检测到 Cloudflare Turnstile，尝试模拟点击...")
                        # 尝试点击复选框 (通常是这个选择器)
                        checkbox = await frame.query_selector('input[type="checkbox"]')
                        if checkbox:
                            await checkbox.click()
                            print("已点击验证复选框")
                            await asyncio.sleep(5)
                            break
                
                # 再次检查输入框
                await page.wait_for_selector('input[placeholder*="api.anthropic.com"]', timeout=10000)
                print("验证通过或页面已加载")
            except Exception as cf_e:
                print(f"尝试处理 Cloudflare 失败: {cf_e}")
                await page.screenshot(path="claw/cloudflare_blocked.png")
                print("已保存拦截截图至 claw/cloudflare_blocked.png")

        print(f"正在填写 API 配置...")
        # 填写 API 接口地址
        try:
            # 尝试通过 placeholder 获取输入框
            await page.get_by_placeholder("https://api.anthropic.com").fill(api_url)
            # 填写 API KEY
            await page.get_by_placeholder("sk-...").fill(api_key)
        except Exception as fill_e:
            print(f"填写配置失败，尝试备用选择器: {fill_e}")
            # 备用选择器：通过相邻文本或 input 类型
            try:
                await page.locator('input').nth(0).fill(api_url)
                await page.locator('input').nth(1).fill(api_key)
            except:
                print("所有选择器均失败")
                await page.screenshot(path="claw/fill_error.png")

        # 选择目标模型
        print(f"正在选择模型: {model_name}")
        try:
            # 优先点击“目标模型”区域下的按钮
            # 页面结构中，模型名称下方通常紧跟着模型 ID
            # 我们寻找包含模型名称的 div 或 button，并确保它不是菜单项
            model_elements = await page.get_by_text(model_name).all()
            for el in model_elements:
                if await el.is_visible():
                    # 检查是否在目标区域（可以通过父级特征判断）
                    await el.click()
                    print(f"成功选择模型: {model_name}")
                    break
        except Exception as e:
            print(f"选择模型失败: {e}")

        # 点击开始检测
        print("点击 '开始检测'...")
        try:
            # 根据截图，按钮文本为 "开始检测"
            start_btn = page.get_by_text("开始检测")
            await start_btn.click()
        except Exception as e:
            print(f"点击开始检测按钮失败: {e}")
            await page.screenshot(path="claw/debug_click_failed.png")
            await browser.close()
            return

        # 等待结果出现
        print("正在等待检测结果 (预计 30-60s)...")
        # 结果出现后通常会有表格或者特定的评分文字
        try:
            # 等待包含 "评分" 或 "结果" 的内容出现，或者等待表格更新
            # 这里设置较长的超时时间
            await page.wait_for_selector("text=检测结果", timeout=90000) 
            print("检测完成！正在保存结果截图...")
            
            # 滚动到结果区域并截图
            await page.screenshot(path="claw/test_result.png", full_page=True)
            print("结果已保存至 claw/test_result.png")
            
            # 提取一些关键结果打印到控制台
            # 假设结果在某个特定的 div 中
            # results = await page.inner_text(".result-container") # 需要根据实际 DOM 调整
            # print(f"提取结果文本: {results}")
            
        except Exception as e:
            print(f"等待结果超时或出错: {e}")
            await page.screenshot(path="claw/timeout_debug.png")

        await browser.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Hvoy.ai 模型自动化测试工具")
    parser.add_argument("--url", help="API 接口地址", default="https://api.anthropic.com")
    parser.add_argument("--key", help="API KEY", required=True)
    parser.add_argument("--model", help="目标模型名称 (如 'Opus 4.7', 'GPT 5.5')", default="Opus 4.7")
    
    args = parser.parse_args()
    
    if not args.key:
        print("错误: 必须提供 --key 参数")
        sys.exit(1)
        
    asyncio.run(run_test(args.url, args.key, args.model))
