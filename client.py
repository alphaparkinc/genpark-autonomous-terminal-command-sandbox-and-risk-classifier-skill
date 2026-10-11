"""Autonomous Terminal Command Sandbox & Risk Classifier.
100% Python Standard Library.
"""

import re

class TerminalCommandRiskClassifier:
    """Classifies shell/SSH commands by blast radius and blocks destructive or privilege-escalation vectors."""

    CRITICAL_PATTERNS = [
        (r"rm\s+-rf\s+(/|\*)", "Catastrophic recursive filesystem deletion"),
        (r"mkfs\.", "Disk formatting command"),
        (r"chmod\s+-R\s+777", "Insecure world-writable recursive permission grant"),
        (r"curl\s+.*\|\s*(ba)?sh", "Unverified remote script pipe execution"),
        (r"dd\s+if=.*of=/dev/", "Direct raw block device overwrite")
    ]

    @classmethod
    def classify_command(cls, command: str) -> dict:
        matched_risks = []
        for pat, desc in cls.CRITICAL_PATTERNS:
            if re.search(pat, command, re.IGNORECASE):
                matched_risks.append({"pattern": pat, "description": desc, "severity": "CRITICAL"})

        if matched_risks:
            risk_level = "BLOCKED_CRITICAL"
            allow_exec = False
        elif any(tok in command.split() for tok in ["sudo", "kill", "reboot", "systemctl"]):
            risk_level = "REQUIRES_HUMAN_APPROVAL"
            allow_exec = False
        else:
            risk_level = "SAFE_AUTO_EXECUTE"
            allow_exec = True

        return {
            "command": command,
            "risk_level": risk_level,
            "allow_autonomous_execution": allow_exec,
            "findings": matched_risks
        }
