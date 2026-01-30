from typing import List, Dict, Optional
from src.utils.telegram_notifier import TelegramNotifier


class TelegramReportMiddleware:
    """
    Middleware responsible for preparing and sending
    pytest execution summary to Telegram
    """

    def __init__(
        self,
        base_url: str,
        browser: str,
        headless: bool,
    ):
        self.base_url = base_url
        self.browser = browser
        self.headless = headless
        self.tg = TelegramNotifier()

    def _build_summary(
        self,
        test_results: List[Dict],
        exitstatus: int,
    ) -> str:
        total = len(test_results)
        passed = sum(1 for t in test_results if t["status"] == "PASSED")
        failed = sum(1 for t in test_results if t["status"] == "FAILED")

        return (
            f"<b>🧪 Pytest Run Finished</b>\n\n"
            f"📊 <b>Summary</b>\n"
            f"• Total: <b>{total}</b>\n"
            f"• ✅ Passed: <b>{passed}</b>\n"
            f"• ❌ Failed: <b>{failed}</b>\n\n"
            f"⚙️ <b>Execution Info</b>\n"
            f"• Exit status: <b>{exitstatus}</b>\n"
            f"• Base URL: <code>{self.base_url}</code>\n"
            f"• Browser: <code>{self.browser}</code>\n"
            f"• Headless: <code>{self.headless}</code>"
        )

    def send(
        self,
        test_results: List[Dict],
        exitstatus: int,
        report_path: Optional[str] = None,
    ) -> None:
        """
        Public middleware method to send Telegram report
        """

        if not test_results:
            self.tg.send_message(
                "<b>⚠️ Pytest finished but no test results were collected.</b>"
            )
            return

        summary = self._build_summary(test_results, exitstatus)

        # Send summary
        self.tg.send_message(summary)

        # Send report file if available
        if report_path:
            self.tg.send_file(
                report_path,
                caption="📄 Automated Test Report (HTML)",
            )
