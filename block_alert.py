import requests
import time
from datetime import datetime
import json
from config import WECOM_CONFIG, BLOCK_CONFIG

class BlockAlert:
    def __init__(self, target_heights, wecom_config, early_alert_diff):
        self.target_heights = sorted(target_heights)  # 排序目标区块高度
        self.base_url = "https://mempool.space/api"
        self.last_checked_height = None
        self.wecom_config = wecom_config
        self.early_alert_diff = early_alert_diff
        self.notified_heights = set()  # 记录已通知的区块高度

    def get_current_height(self):
        try:
            response = requests.get(f"{self.base_url}/blocks/tip/height")
            if response.status_code == 200:
                return int(response.text)
            return None
        except Exception as e:
            print(f"获取区块高度时出错: {e}")
            return None

    def get_block_info(self, height):
        try:
            response = requests.get(f"{self.base_url}/block-height/{height}")
            if response.status_code == 200:
                block_hash = response.text
                block_info = requests.get(f"{self.base_url}/block/{block_hash}")
                if block_info.status_code == 200:
                    return block_info.json()
            return None
        except Exception as e:
            print(f"获取区块信息时出错: {e}")
            return None

    def send_wecom_alert(self, content):
        try:
            data = {
                "msgtype": "text",
                "text": {
                    "content": f"比特币区块提醒\n{content}"
                }
            }
            response = requests.post(
                self.wecom_config['webhook_url'],
                json=data
            )
            if response.status_code == 200:
                print(f"企业微信提醒发送成功")
            else:
                print(f"企业微信通知发送失败: {response.text}")
        except Exception as e:
            print(f"发送企业微信通知时出错: {e}")

    def format_alert(self, current_height, target_height):
        info = []
        info.append(f"时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        info.append(f"当前区块高度: {current_height}")
        info.append(f"目标区块高度: {target_height}")
        info.append(f"剩余区块数: {target_height - current_height}")
        info.append(f"预计到达时间: 约 {(target_height - current_height) * 10} 分钟")
        return "\n".join(info)

    def check_alert(self, current_height):
        for target_height in self.target_heights:
            # 检查目标区块的前三个区块
            for i in range(1, self.early_alert_diff + 1):
                check_height = target_height - i
                if current_height >= check_height and check_height not in self.notified_heights:
                    alert_content = self.format_alert(current_height, target_height)
                    self.send_wecom_alert(alert_content)
                    self.notified_heights.add(check_height)
                    print(f"\n区块 {check_height} 提醒已发送")
                    print(alert_content)
            
            # 如果达到目标区块，返回True表示监控结束
            if current_height >= target_height:
                return True
        return False

    def monitor(self, check_interval=60):
        print(f"开始监控区块高度: {', '.join(map(str, self.target_heights))}")
        print("按 Ctrl+C 停止监控")
        
        while True:
            current_height = self.get_current_height()
            
            if current_height is None:
                print("无法获取当前区块高度，将在稍后重试...")
                time.sleep(check_interval)
                continue

            if current_height != self.last_checked_height:
                print(f"当前区块高度: {current_height}", end="\r")
                self.last_checked_height = current_height

            # 检查是否需要发送提醒
            if self.check_alert(current_height):
                print("\n目标区块已到达，监控结束！")
                break

            time.sleep(check_interval)

if __name__ == "__main__":
    alert = BlockAlert(
        target_heights=BLOCK_CONFIG['target_heights'],
        wecom_config=WECOM_CONFIG,
        early_alert_diff=BLOCK_CONFIG['early_alert_diff']
    )
    alert.monitor(check_interval=BLOCK_CONFIG['check_interval']) 