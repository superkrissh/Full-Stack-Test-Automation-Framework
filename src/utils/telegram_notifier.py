import os
import requests
from typing import Optional, Dict, Any


class TelegramNotifier:
    def __init__(self):
        self.enabled = os.getenv("TELEGRAM_ENABLED", "false").lower() == "true"
        self.bot_token = os.getenv("TELEGRAM_BOT_TOKEN", "")
        self.chat_id = os.getenv("TELEGRAM_CHAT_ID", "")
        self.parse_mode = os.getenv("TELEGRAM_PARSE_MODE", "HTML")

        self.base_url = f"https://api.telegram.org/bot{self.bot_token}"

    def _is_config_valid(self) -> bool:
        return bool(self.bot_token and self.chat_id)

    def send_message(self, text: str, disable_web_preview: bool = True) -> Dict[str, Any]:
        """
        Sends a text message to Telegram.
        Returns Telegram API JSON response (or error dict if disabled/misconfigured).
        """
        if not self.enabled:
            return {"ok": False, "disabled": True, "reason": "TELEGRAM_ENABLED is false"}

        if not self._is_config_valid():
            return {"ok": False, "error": "Missing TELEGRAM_BOT_TOKEN or TELEGRAM_CHAT_ID"}

        url = f"{self.base_url}/sendMessage"
        payload = {
            "chat_id": self.chat_id,
            "text": text,
            "parse_mode": self.parse_mode,
            "disable_web_page_preview": disable_web_preview,
        }

        try:
            resp = requests.post(url, json=payload, timeout=20)
            return resp.json()
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def send_file(self, file_path: str, caption: Optional[str] = None) -> Dict[str, Any]:
        """
        Sends a file (HTML report, zip, screenshots, etc.) to Telegram as a document.
        """
        if not self.enabled:
            return {"ok": False, "disabled": True, "reason": "TELEGRAM_ENABLED is false"}

        if not self._is_config_valid():
            return {"ok": False, "error": "Missing TELEGRAM_BOT_TOKEN or TELEGRAM_CHAT_ID"}

        if not os.path.exists(file_path):
            return {"ok": False, "error": f"File not found: {file_path}"}

        url = f"{self.base_url}/sendDocument"
        data = {
            "chat_id": self.chat_id,
            "caption": caption or "",
            "parse_mode": self.parse_mode,
        }

        try:
            with open(file_path, "rb") as f:
                files = {"document": f}
                resp = requests.post(url, data=data, files=files, timeout=60)
            return resp.json()
        except Exception as e:
            return {"ok": False, "error": str(e)}
