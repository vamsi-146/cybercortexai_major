"""Suspicious PowerShell Detection Rule."""

from typing import Dict, Any, List, Optional
from .base import BaseDetectionRule


class SuspiciousPowerShellRule(BaseDetectionRule):
    """
    Detect suspicious PowerShell command-line activity.

    Triggers when PowerShell execution contains indicators of
    obfuscation, download, or suspicious activity.
    """

    def __init__(self):
        super().__init__()
        self.name = "Suspicious PowerShell Detection"
        self.description = "Detects suspicious PowerShell command-line indicators"
        self.enabled = True
        self.severity = "high"
        self.source_types = ["windows"]
        self.event_types = ["process"]
        self.mitre_techniques = ["T1059.001"]  # PowerShell
        self.threshold = 2  # Minimum suspicious indicators
        self.time_window_seconds = 0  # Not time-based

        # Suspicious PowerShell indicators
        self.suspicious_indicators = [
            "-EncodedCommand",
            "-enc",
            "FromBase64String",
            "DownloadString",
            "Invoke-WebRequest",
            "IEX",
            "Invoke-Expression",
            "Invoke-Item",
            "Start-BitsTransfer",
            "Net.WebClient",
            "Hidden",
            "WindowStyle",
            "NonInteractive",
            "ExecutionPolicy",
            "Bypass",
            "Unrestricted",
        ]

    async def evaluate(
        self,
        event: Dict[str, Any],
        context: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """Evaluate if this PowerShell execution is suspicious."""
        if not self.check_source_type(event) or not self.check_event_type(event):
            return None

        # Check if it's PowerShell
        process_name = event.get("process_name", "").lower()
        if "powershell" not in process_name and "pwsh" not in process_name:
            return None

        command_line = event.get("command_line", "")
        if not command_line:
            return None

        # Count suspicious indicators
        found_indicators = []
        for indicator in self.suspicious_indicators:
            if indicator.lower() in command_line.lower():
                found_indicators.append(indicator)

        if len(found_indicators) >= self.threshold:
            evidence = [
                f"PowerShell execution with {len(found_indicators)} suspicious indicators",
                f"Process: {process_name}",
                f"Command line length: {len(command_line)} characters",
                f"Found indicators: {found_indicators}"
            ]

            # Truncate command line for evidence
            if len(command_line) > 200:
                evidence.append(f"Command line (truncated): {command_line[:200]}...")
            else:
                evidence.append(f"Command line: {command_line}")

            return self.create_detection_result(
                event,
                context,
                f"Suspicious PowerShell detected with {len(found_indicators)} indicators",
                evidence
            )

        return None
