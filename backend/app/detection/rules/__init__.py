"""Detection rules for security event analysis."""

from .base import BaseDetectionRule
from .brute_force import BruteForceRule
from .success_after_failures import SuccessAfterFailuresRule
from .port_scan import PortScanRule
from .multiple_host_scan import MultipleHostScanRule
from .suspicious_powershell import SuspiciousPowerShellRule
from .privileged_group_modification import PrivilegedGroupModificationRule
from .new_account_privilege_escalation import NewAccountPrivilegeEscalationRule
from .account_lockout_burst import AccountLockoutBurstRule

__all__ = [
    "BaseDetectionRule",
    "BruteForceRule",
    "SuccessAfterFailuresRule",
    "PortScanRule",
    "MultipleHostScanRule",
    "SuspiciousPowerShellRule",
    "PrivilegedGroupModificationRule",
    "NewAccountPrivilegeEscalationRule",
    "AccountLockoutBurstRule",
]
