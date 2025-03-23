import os
from loguru import logger
from dotenv import load_dotenv
from XianyuAgent import XianyuReplyBot
from context_manager import ChatContextManager

# 加载环境变量
load_dotenv()

class ChatTester:
    def __init__(self):
        # 初始化XianyuReplyBot和ChatContextManager
        self.bot = XianyuReplyBot()
        self.context_manager = ChatContextManager()
        
        # 模拟用户和商品信息
        self.user_id = "test_user_001"
        self.item_id = "test_item_001"
        
        # 模拟商品描述
        self.item_desc = """
        二手iPhone 13 Pro Max 256GB 远峰蓝 
        - 购买日期：2022年5月
        - 使用时长：1年2个月
        - 成色：9成新，轻微使用痕迹
        - 电池健康：89%
        - 配件：原装充电器、数据线
        - 价格：4800元
        - 保修：已过保修期
        """
        
    def run_chat_test(self):
        """运行聊天测试"""
        logger.info("开始聊天测试...")
        
        test_messages = [
            "你好，这个手机还在卖吗？",
            "电池健康还有多少？",
            "能便宜一点吗？4500行不行？",
            "这款手机拍照效果怎么样？",
            "4600能接受吗？",
            "好的，我考虑一下",
        ]
        
        # 逐条发送测试消息并获取回复
        for i, msg in enumerate(test_messages):
            logger.info(f"用户消息 ({i+1}/{len(test_messages)}): {msg}")
            
            # 获取当前对话上下文
            context = self.context_manager.get_context(self.user_id, self.item_id)
            
            # 获取回复
            reply = self.bot.generate_reply(msg, self.item_desc, context)
            
            # 保存对话记录
            self.context_manager.add_message(self.user_id, self.item_id, "user", msg)
            self.context_manager.add_message(self.user_id, self.item_id, "assistant", reply)
            
            # 如果是议价消息，增加议价计数
            if "price" == self.bot.last_intent:
                self.context_manager.increment_bargain_count(self.user_id, self.item_id)
                logger.debug(f"议价次数增加，当前次数: {self.context_manager.get_bargain_count(self.user_id, self.item_id)}")
            
            logger.info(f"机器人回复: {reply}")
            logger.info(f"意图识别: {self.bot.last_intent}")
            logger.info("-" * 50)
            
def main():
    tester = ChatTester()
    tester.run_chat_test()

if __name__ == "__main__":
    main() 