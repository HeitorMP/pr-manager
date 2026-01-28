#!/usr/bin/env python3
"""
PR Manager TUI - A terminal user interface for managing pull requests
"""

import os
from datetime import datetime
from typing import List, Optional

from dotenv import load_dotenv
from github import Github, PullRequest
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Container, VerticalScroll
from textual.widgets import Footer, Header, ListItem, ListView, Static


# Load environment variables
load_dotenv()


class PRDetailView(VerticalScroll):
    """Widget to display PR details"""

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


class PRManagerApp(App):
    """A Textual app to manage pull requests."""

    CSS = """
    Screen {
        background: $surface;
    }

    ListView {
        height: 100%;
        border: solid $primary;
    }

    ListItem {
        padding: 1;
    }

    ListItem:hover {
        background: $boost;
    }

    PRDetailView {
        border: solid $primary;
        height: 100%;
        padding: 1 2;
    }

    Static {
        height: auto;
    }
    """

    BINDINGS = [
        Binding("q", "quit_or_back", "Quit/Back", show=True),
        Binding("enter", "show_detail", "View Details", show=True),
    ]

    def __init__(self):
        super().__init__()
        self.github_token = os.getenv("GITHUB_TOKEN")
        self.github_org = os.getenv("GITHUB_ORG")
        
        if not self.github_token:
            raise ValueError("GITHUB_TOKEN environment variable is required")
        if not self.github_org:
            raise ValueError("GITHUB_ORG environment variable is required")
        
        self.github = Github(self.github_token)
        self.prs: List[PullRequest.PullRequest] = []
        self.current_view = "list"  # "list" or "detail"

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        yield Header()
        yield Container(ListView(id="pr_list"))
        yield Footer()

    def on_mount(self) -> None:
        """Called when the app is mounted."""
        self.title = "PR Manager"
        self.sub_title = f"Organization: {self.github_org}"
        self.load_prs()

    def load_prs(self) -> None:
        """Load pull requests from GitHub organization"""
        self.prs = []
        list_view = self.query_one("#pr_list", ListView)
        list_view.clear()

        try:
            org = self.github.get_organization(self.github_org)
            
            # Get all repositories in the organization
            for repo in org.get_repos():
                # Get open pull requests for each repository
                for pr in repo.get_pulls(state="open"):
                    self.prs.append(pr)
                    
                    # Create a formatted list item
                    label = f"#{pr.number} - {pr.title} ({repo.name}) by {pr.user.login}"
                    list_view.append(ListItem(Static(label), id=f"pr_{pr.number}_{repo.name}"))
            
            if not self.prs:
                list_view.append(ListItem(Static("No open pull requests found")))
                
        except Exception as e:
            list_view.append(ListItem(Static(f"Error loading PRs: {str(e)}")))

    def action_show_detail(self) -> None:
        """Show details of the selected PR"""
        if self.current_view == "list" and self.prs:
            list_view = self.query_one("#pr_list", ListView)
            if list_view.index is not None and list_view.index < len(self.prs):
                selected_pr = self.prs[list_view.index]
                
                # Remove the list view and show detail view
                container = self.query_one(Container)
                container.remove_children()
                container.mount(PRDetailView(selected_pr))
                
                self.current_view = "detail"

    def action_quit_or_back(self) -> None:
        """Quit the app or go back to list view"""
        if self.current_view == "detail":
            # Go back to list view
            container = self.query_one(Container)
            container.remove_children()
            container.mount(ListView(id="pr_list"))
            self.load_prs()
            self.current_view = "list"
        else:
            # Quit the app
            self.exit()


def main():
    """Main entry point"""
    app = PRManagerApp()
    app.run()


if __name__ == "__main__":
    main()
