import asyncio
from typing import Any

# 全局变量：记录哪些 API 已经添加成功，避免重复提交
ADD_SUCCESS_API = []


async def start(api: "MiShop"):
    """
    不断尝试将商品添加到购物车，如果成功则直接提交订单锁单。

    Args:
        api (MiShop): MiShop API 实例
    """
    while True:
        try:
            # 发送添加商品请求
            add_resp = await api.client.send(
                api.add_goods(
                    goods_id="GOODS_ID"  # TODO: 替换成实际商品 ID
                )
            )

            # 尝试解析响应
            result: dict[str, Any] = add_resp.json().get("data", {})

        except Exception as e:
            print(f"❌ 添加商品请求失败: {e}")
            await asyncio.sleep(1)
            continue

        # 避免重复执行
        if api in ADD_SUCCESS_API:
            print("该 API 已处理过，跳出循环")
            return

        # 添加成功，提交订单锁单
        if result.get("status") == "all_success":
            print("✅ 添加到购物车成功，开始提交订单锁单...")
            ADD_SUCCESS_API.append(api)

            await asyncio.gather(
                *[lock_order(api) for _ in range(3)]  # 默认并发锁单 3 次
            )
            return

        # 没成功，等待一会重试
        await asyncio.sleep(0.5)


async def lock_order(api: "MiShop"):
    """
    提交订单（锁单，不支付）
    """
    try:
        order_resp = await api.client.send(
            api.submit_order(
                pay_method="BALANCE",   # 支付方式可以先占位
                auto_pay=False          # 禁止自动支付，只锁单
            )
        )
        order_result = order_resp.json()

        if order_result.get("code") == 1:
            order_id = order_result["data"].get("orderId")
            print(f"📦 订单锁单成功! order_id={order_id}")
        else:
            print(f"⚠️ 锁单失败: {order_result}")

    except Exception as e:
        print(f"❌ 提交订单时异常: {e}")
