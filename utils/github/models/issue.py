

from datetime import datetime
from typing import List, Union, Optional

from pydantic import BaseModel as _BaseModel

from . import BaseModel, PaginatedList

from .user import User
from .label import Label
from .comment import Comment
from .timeline import (
    TimelineEvent, TimelineEventCommited, TimelineEventForcePushed,
    TimelineEventHeadDeleted, TimelineEventReferenced, TimelineEventCommented,
    TimelineEventCommentDeleted, TimelineEventAssigned, TimelineEventMentioned,
    TimelineEventSubscribed, TimelineEventUnsubscribed, TimelineEventReviewed,
    TimelineEventReviewRequested, TimelineEventReviewRemoved,
    TimelineEventReviewDismissed, TimelineEventRenamed, TimelineEventLabeled,
    TimelineEventUnlabeled, TimelineEventMerged, TimelineEventDeployed,
    TimelineEventClosed, TimelineEventAddedToProject,
    TimelineEventMovedColumnsInProject, TimelineEventRemovedFromProject,
    TimelineEventMilestoned, TimelineEventDemilestoned)


class IssuePullRequest(_BaseModel):
    url: str
    html_url: str
    diff_url: str
    patch_url: str


class Issue(BaseModel):
    id: int
    node_id: str
    url: str
    repository_url: str
    labels_url: str
    comments_url: str
    events_url: str
    timeline_url: str
    html_url: str
    number: int
    state: str
    title: str
    body: Optional[str]
    body_text: Optional[str]
    body_html: Optional[str]
    user: User
    labels: List[Label]
    assignee: Optional[User]
    assignees: List[User]
    # milestone: Optional[Milestone]
    locked: bool
    active_lock_reason: Optional[str]
    comments: int
    pull_request: Optional[IssuePullRequest]
    closed_at: Optional[datetime]
    created_at: datetime
    updated_at: datetime
    closed_by: Optional[User]
    author_association: str

    @property
    def is_pull_request(self) -> bool:
        return bool(self.pull_request)

    async def get_comments(self) -> PaginatedList[Comment]:
        """
        GET /repo/:full_name/issues/:number/comments

        https://docs.github.com/en/rest/reference/issues#list-issue-comments
        """
        headers = {"Accept": "application/vnd.github.v3.full+json"}
        return PaginatedList(Comment,
                             self.requester,
                             "GET",
                             self.comments_url,
                             headers=headers)

    async def get_timeline(self) -> PaginatedList[TimelineEvent]:
        """
        GET /repo/:full_name/issues/:number/timeline

        https://docs.github.com/en/rest/reference/issues#list-timeline-events-for-an-issue
        """
        headers = {
            "Accept": "application/vnd.github.mockingbird-preview.full+json, "
                      "application/vnd.github.starfox-preview+json"
        }
        return PaginatedList(
            Union[TimelineEventCommited, TimelineEventForcePushed,
                  TimelineEventHeadDeleted, TimelineEventReferenced,
                  TimelineEventCommented, TimelineEventCommentDeleted,
                  TimelineEventAssigned, TimelineEventMentioned,
                  TimelineEventSubscribed, TimelineEventUnsubscribed,
                  TimelineEventReviewed, TimelineEventReviewRequested,
                  TimelineEventReviewRemoved, TimelineEventReviewDismissed,
                  TimelineEventRenamed, TimelineEventLabeled,
                  TimelineEventUnlabeled, TimelineEventMerged,
                  TimelineEventDeployed, TimelineEventClosed,
                  TimelineEventAddedToProject,
                  TimelineEventMovedColumnsInProject,
                  TimelineEventRemovedFromProject, TimelineEventMilestoned,
                  TimelineEventDemilestoned, TimelineEvent],
            self.requester,
            "GET",
            self.timeline_url,
            headers=headers)

    async def get_diff(self) -> str:
        """
        GET /repo/:full_name/pull/:number.diff
        """
        if not self.is_pull_request:
            raise RuntimeError(f"Issue {self.number} is not a pull request")

        response = await self.requester.request(
            "GET",
            self.pull_request.diff_url  # type: ignore
        )
        return response.text
