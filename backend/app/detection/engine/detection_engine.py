"""Detection engine for evaluating security events against rules."""

from typing import Dict, Any, List, Optional
from datetime import datetime
from .rules.base import BaseDetectionRule
from .rules.brute_force import BruteForceRule
from .rules.success_after_failures import SuccessAfterFailuresRule
from .rules.port_scan import PortScanRule
from .rules.multiple_host_scan import MultipleHostScanRule
from .rules.suspicious_powershell import SuspiciousPowerShellRule
from .rules.privileged_group_modification import PrivilegedGroupModificationRule
from .rules.new_account_privilege_escalation import NewAccountPrivilegeEscalationRule
from .rules.account_lockout_burst import AccountLockoutBurstRule


class DetectionEngine:
    """Engine for evaluating events against detection rules."""

    def __init__(self):
        self.rules: Dict[str, BaseDetectionRule] = {}
        self._register_default_rules()

    def _register_default_rules(self):
        """Register the default detection rules."""
        self.register_rule(BruteForceRule())
        self.register_rule(SuccessAfterFailuresRule())
        self.register_rule(PortScanRule())
        self.register_rule(MultipleHostScanRule())
        self.register_rule(SuspiciousPowerShellRule())
        self.register_rule(PrivilegedGroupModificationRule())
        self.register_rule(NewAccountPrivilegeEscalationRule())
        self.register_rule(AccountLockoutBurstRule())

    def register_rule(self, rule: BaseDetectionRule):
        """
        Register a detection rule.

        Args:
            rule: The detection rule instance
        """
        self.rules[rule.rule_id] = rule

    def unregister_rule(self, rule_id: str):
        """
        Unregister a detection rule.

        Args:
            rule_id: The rule ID to unregister
        """
        if rule_id in self.rules:
            del self.rules[rule_id]

    def get_rule(self, rule_id: str) -> Optional[BaseDetectionRule]:
        """
        Get a specific rule by ID.

        Args:
            rule_id: The rule ID

        Returns:
            Rule instance or None
        """
        return self.rules.get(rule_id)

    def get_all_rules(self) -> List[BaseDetectionRule]:
        """Return all registered rules."""
        return list(self.rules.values())

    def get_enabled_rules(self) -> List[BaseDetectionRule]:
        """Return only enabled rules."""
        return [rule for rule in self.rules.values() if rule.enabled]

    async def evaluate_event(
        self,
        event: Dict[str, Any],
        correlation_context: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """
        Evaluate an event against all enabled detection rules.

        Args:
            event: The normalized event
            correlation_context: Correlation context from correlation engine

        Returns:
            List of detection results from triggered rules
        """
        detections = []

        for rule in self.get_enabled_rules():
            try:
                result = await rule.evaluate(event, correlation_context)
                if result:
                    detections.append(result)
            except Exception as e:
                # Log error but continue with other rules
                print(f"Error evaluating rule {rule.rule_id}: {e}")

        return detections

    async def evaluate_event_with_rule(
        self,
        event: Dict[str, Any],
        correlation_context: Dict[str, Any],
        rule_id: str
    ) -> Optional[Dict[str, Any]]:
        """
        Evaluate an event against a specific rule.

        Args:
            event: The normalized event
            correlation_context: Correlation context
            rule_id: The specific rule ID to evaluate

        Returns:
            Detection result or None
        """
        rule = self.get_rule(rule_id)
        if not rule:
            return None

        if not rule.enabled:
            return None

        try:
            return await rule.evaluate(event, correlation_context)
        except Exception as e:
            print(f"Error evaluating rule {rule_id}: {e}")
            return None

    def get_rule_statistics(self) -> Dict[str, Any]:
        """
        Get statistics about registered rules.

        Returns:
            Dictionary with rule statistics
        """
        total = len(self.rules)
        enabled = len(self.get_enabled_rules())
        disabled = total - enabled

        by_severity = {}
        for rule in self.rules.values():
            severity = rule.severity
            by_severity[severity] = by_severity.get(severity, 0) + 1

        return {
            "total_rules": total,
            "enabled_rules": enabled,
            "disabled_rules": disabled,
            "by_severity": by_severity,
            "rule_ids": list(self.rules.keys()),
        }
