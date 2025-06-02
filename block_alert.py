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

    def format_block_info(self, block_info):
        info = []
        info.append(f"时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        info.append(f"区块高度: {block_info['height']}")
        info.append(f"区块哈希: {block_info['id']}")
        info.append(f"区块大小: {block_info['size']} 字节")
        info.append(f"交易数量: {block_info['tx_count']}")
        info.append(f"区块时间戳: {datetime.fromtimestamp(block_info['timestamp']).strftime('%Y-%m-%d %H:%M:%S')}")
        info.append(f"区块权重: {block_info['weight']} WU")
        info.append(f"区块版本: {block_info['version']}")
        info.append(f"默克尔根: {block_info['merkle_root']}")
        info.append(f"难度: {block_info['difficulty']}")
        return "\n".join(info)

    def send_alert(self, block_info):
        # 打印到控制台
        print("\n=== 区块提醒 ===")
        print(self.format_block_info(block_info))
        print("==============\n")

        # 发送企业微信通知
        content = self.format_block_info(block_info)
        self.send_wecom_alert(content)

    def check_early_alert(self, current_height):
        for target_height in self.target_heights:
            if current_height >= (target_height - self.early_alert_diff) and current_height < target_height:
                if current_height not in self.notified_heights:
                    alert_content = f"时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
                    alert_content += f"当前区块高度: {current_height}\n"
                    alert_content += f"目标区块高度: {target_height}\n"
                    alert_content += f"剩余区块数: {target_height - current_height}\n"
                    alert_content += f"预计到达时间: 约 {(target_height - current_height) * 10} 分钟"
                    self.send_wecom_alert(alert_content)
                    self.notified_heights.add(current_height)
                    print("\n=== 提前提醒已发送 ===")
                    print(alert_content)
                    print("====================\n")

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

            # 检查是否需要发送提前提醒
            self.check_early_alert(current_height)

            # 检查所有目标区块
            for target_height in self.target_heights:
                if current_height >= target_height and target_height not in self.notified_heights:
                    block_info = self.get_block_info(target_height)
                    if block_info:
                        self.send_alert(block_info)
                        self.notified_heights.add(target_height)

            # 如果所有目标区块都已通知，则退出
            if len(self.notified_heights) == len(self.target_heights):
                print("\n所有目标区块已通知完成！")
                break

            time.sleep(check_interval)

if __name__ == "__main__":
    alert = BlockAlert(
        target_heights=BLOCK_CONFIG['target_heights'],
        wecom_config=WECOM_CONFIG,
        early_alert_diff=BLOCK_CONFIG['early_alert_diff']
    )
    alert.monitor(check_interval=BLOCK_CONFIG['check_interval']) 