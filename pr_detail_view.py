"""
PR Detail View - Widget for displaying pull request details
"""

from github import PullRequest
from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import VerticalScroll
from textual.widgets import Static


class PRDetailView(VerticalScroll):
    """Widget to display PR details"""
    
    BINDINGS = [
        Binding("down,j", "scroll_down", "Scroll Down", show=False),
        Binding("up,k", "scroll_up", "Scroll Up", show=False),
        Binding("pagedown", "page_down", "Page Down", show=False),
        Binding("pageup", "page_up", "Page Up", show=False),
        Binding("d", "view_files", "View Files", show=True),
    ]
    
    def action_view_files(self) -> None:
        """Show file changes for this PR"""
        self.app.show_pr_files(self.pr)

    def __init__(self, pr: PullRequest.PullRequest):
        super().__init__()
        self.pr = pr

    def compose(self) -> ComposeResult:
        """Compose the detail view"""
        # Format the PR details
        created_at = self.pr.created_at.strftime("%Y-%m-%d %H:%M:%S")
        updated_at = self.pr.updated_at.strftime("%Y-%m-%d %H:%M:%S")
        
        status = "🟢 Open" if self.pr.state == "open" else "🔴 Closed"
        mergeable = "✅ Yes" if self.pr.mergeable else "❌ No" if self.pr.mergeable is False else "⏳ Checking..."
        
        details = f"""
# {self.pr.title}

**Status:** {status}
**Number:** #{self.pr.number}
**Author:** {self.pr.user.login}
**Repository:** {self.pr.base.repo.full_name}
**Branch:** {self.pr.head.ref} → {self.pr.base.ref}
**Created:** {created_at}
**Updated:** {updated_at}
**Mergeable:** {mergeable}
**Comments:** {self.pr.comments}
**Commits:** {self.pr.commits}
**Changed Files:** {self.pr.changed_files}
**Additions:** +{self.pr.additions} / **Deletions:** -{self.pr.deletions}

---

## Description

{self.pr.body or "*No description provided*"}

---

**URL:** {self.pr.html_url}
"""
        yield Static(details)
