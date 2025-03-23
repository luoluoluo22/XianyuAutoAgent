import os
from loguru import logger
from dotenv import load_dotenv
from openai import OpenAI

# 加载环境变量
load_dotenv()

def test_model_connection():
    """测试模型连接是否正常"""
    api_key = os.getenv("OPENAI_API_KEY")
    base_url = os.getenv("OPENAI_BASE_URL")
    model_name = os.getenv("DEFAULT_MODEL", "Qwen/Qwen2.5-7B-Instruct")
    
    if not api_key:
        logger.error("未设置OPENAI_API_KEY环境变量")
        return False
    
    if not base_url:
        logger.warning("未设置OPENAI_BASE_URL环境变量，使用默认值")
    
    logger.info(f"API Key: {api_key[:5]}...{api_key[-4:]}")
    logger.info(f"Base URL: {base_url}")
    logger.info(f"Model: {model_name}")
    
    try:
        client = OpenAI(
            api_key=api_key,
            base_url=base_url
        )
        
        # 发送简单请求测试连接
        response = client.chat.completions.create(
            model=model_name,
            messages=[
                {"role": "system", "content": "你是一个有用的助手。"},
                {"role": "user", "content": "你好，请用一句话介绍自己。"}
            ],
            temperature=0.7,
            max_tokens=100
        )
        
        content = response.choices[0].message.content
        logger.info(f"模型响应: {content}")
        logger.info("模型连接测试成功!")
        return True
    
    except Exception as e:
        logger.error(f"连接模型时出错: {e}")
        return False

def main():
    """主函数"""
    logger.info("开始测试模型连接...")
    test_model_connection()

if __name__ == "__main__":
    main() 