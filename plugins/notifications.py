import requests
import os


class TelegramNotifier:
    def __init__(self, token: str = None, chat_id: str = None):
        self.token = token or os.getenv("TELEGRAM_BOT_TOKEN")
        self.chat_id = chat_id or os.getenv("TELEGRAM_CHAT_ID")
        
    def send(self, message: str):
        if not self.token or not self.chat_id:
            return False
        url = f"https://api.telegram.org/bot{self.token}/sendMessage"
        data = {"chat_id": self.chat_id, "text": message}
        try:
            requests.post(url, json=data, timeout=10)
            return True
        except Exception:
            return False


class SlackNotifier:
    def __init__(self, webhook: str = None):
        self.webhook = webhook or os.getenv("SLACK_WEBHOOK")
        
    def send(self, message: str):
        if not self.webhook:
            return False
        try:
            requests.post(self.webhook, json={"text": message}, timeout=10)
            return True
        except Exception:
            return False