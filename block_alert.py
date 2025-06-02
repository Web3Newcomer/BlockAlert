import requests
import time
from datetime import datetime
import json
import smtplib
from email.mime.text import MIMEText
from email.header import Header
from config import EMAIL_CONFIG, BLOCK_CONFIG

class BlockAlert:
    def __init__(self, target_heights, email_config, notify_first_n):
        self.target_heights = sorted(target_heights)  # 排序目标区块高度
        self.base_url = "https://mempool.space/api"
        self.last_checked_height = None
        self.email_config = email_config
        self.notified_heights = set()  # 记录已通知的区块高度
        self.notify_first_n = notify_first_n

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

    def send_email(self, subject, content):
        try:
            msg = MIMEText(content, 'plain', 'utf-8')
            msg['Subject'] = Header(subject, 'utf-8')
            msg['From'] = self.email_config['from_email']
            msg['To'] = self.email_config['to_email']

            with smtplib.SMTP_SSL(self.email_config['smtp_server'], self.email_config['smtp_port']) as server:
                server.login(self.email_config['username'], self.email_config['password'])
                server.send_message(msg)
            print(f"邮件发送成功: {subject}")
        except Exception as e:
            print(f"发送邮件时出错: {e}")

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

        # 如果是前N个区块，发送邮件通知
        if block_info['height'] in self.target_heights[:self.notify_first_n]:
            subject = f"比特币区块提醒 - 区块高度 {block_info['height']}"
            content = f"=== 区块提醒 ===\n{self.format_block_info(block_info)}\n=============="
            self.send_email(subject, content)

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
        email_config=EMAIL_CONFIG,
        notify_first_n=BLOCK_CONFIG['notify_first_n_blocks']
    )
    alert.monitor(check_interval=BLOCK_CONFIG['check_interval']) 