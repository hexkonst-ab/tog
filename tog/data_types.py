from typing import List, Literal, Optional
from datetime import datetime
from pydantic import BaseModel, Field, field_serializer


class Project(BaseModel):
    id: int
    workspace_id: int
    client_id: int
    name: str
    is_private: bool
    active: bool
    at: datetime  # last update
    created_at: datetime  # creation
    actual_hours: int
    actual_seconds: int


class TimeEntry(BaseModel):
    id: int
    workspace_id: int
    project_id: int | None
    task_id: int | None
    billable: bool
    start: datetime
    stop: datetime | None
    duration: int
    description: str
    tags: List[str]
    tag_ids: List[int]
    duronly: bool
    at: datetime
    server_deleted_at: datetime | None
    user_id: int


class Workspace(BaseModel):
    admin: bool
    api_token: str
    at: str
    business_ws: bool
    # csv_upload: any
    default_currency: str
    default_hourly_rate: float | None
    ical_enabled: bool
    ical_url: str
    id: int
    logo_url: str
    max_data_retention_days: Optional[int] = None
    name: str
    only_admins_may_create_projects: bool
    only_admins_may_create_tags: bool
    only_admins_see_billable_rates: bool
    only_admins_see_team_dashboard: bool
    organization_id: int
    premium: bool
    profile: int
    projects_billable_by_default: bool
    rate_last_updated: str | None
    reports_collapse: bool
    role: str
    rounding: int
    rounding_minutes: int
    server_deleted_at: str | None
    # subscription: any
    suspended_at: str | None
    # te_constraints: any
    working_hours_in_minutes: int | None


class Me(BaseModel):
    id: int
    email: str
    fullname: str
    timezone: str
    toggl_accounts_id: str
    default_workspace_id: int
    beginning_of_week: int
    image_url: str
    created_at: datetime
    updated_at: datetime
    country_id: int
    has_password: bool
    at: datetime
    intercom_hash: str
    oauth_providers: List[str]


class StartTimeEntryRequest(BaseModel):
    created_with: str = "https://github.com/hexkonst-ab/tog"
    description: str
    tags: Optional[List[str]] = []
    billable: Optional[bool] = False
    project_id: Optional[int] = None
    workspace_id: int
    duration: Optional[int] = -1
    start: Optional[datetime] = Field(
        default_factory=lambda: datetime.utcnow())
    stop: Literal[None] = None

    @field_serializer('start')
    def serialize_start(self, start: datetime):
        return start.isoformat(timespec="seconds") + "Z"
