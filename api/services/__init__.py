from services.auth_service import login, get_current_user_info
from services.user_service import get_users, get_user_by_id, create_user, update_user, delete_user
from services.role_service import get_roles, get_role_by_id, create_role, update_role, delete_role, get_permissions, create_permission
from services.report_service import (
    get_reports, get_report_by_id, create_report, update_report, delete_report,
    approve_report, reject_report, return_report, get_timeline, get_dashboard_stats
)

__all__ = [
    "login", "get_current_user_info",
    "get_users", "get_user_by_id", "create_user", "update_user", "delete_user",
    "get_roles", "get_role_by_id", "create_role", "update_role", "delete_role", "get_permissions", "create_permission",
    "get_reports", "get_report_by_id", "create_report", "update_report", "delete_report",
    "approve_report", "reject_report", "return_report", "get_timeline", "get_dashboard_stats"
]
