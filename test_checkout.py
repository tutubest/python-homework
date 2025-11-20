import requests
import multiprocessing
import time
import sys
import os

# 这一步是为了让测试脚本能找到刚写的 checkout_service.py
sys.path.append(os.getcwd())
from checkout_service import app

def run_server():
    # 启动服务
    app.run(port=5000)

def test_checkout_total():
    # 1. 在后台启动 Flask 服务
    p = multiprocessing.Process(target=run_server)
    p.daemon = True
    p.start()
    
    # 2. 等待 3 秒，确保服务完全启动
    time.sleep(3)

    try:
        # 3. 准备数据：20块钱的东西，买3个
        data = {"items": [{"price": 20, "quantity": 3}]}
        
        # 4. 发送请求给自己的服务
        res = requests.post("http://127.0.0.1:5000/checkout", json=data)
        
        # 5. 验证：状态码是200，总价是60
        assert res.status_code == 200
        assert res.json()["total"] == 60
        print("微服务测试通过！总价正确！")
        
    finally:
        # 6. 测试结束，关闭服务，释放电脑资源
        p.terminate()
