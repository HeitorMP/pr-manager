#!/usr/bin/env python3
"""
PR Manager TUI - A terminal user interface for managing pull requests
"""

import os
from datetime import datetime
from typing import List, Optional

from dotenv import load_dotenv
from github import Auth, Github, PullRequest
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Container
from textual.widgets import Footer, Header, ListItem, ListView, Static

from pr_detail_view import PRDetailView
from pr_files_view import PRFilesView
from pr_list_view import PRListView
from repo_filter_screen import RepoFilterScreen


load_dotenv()


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
    ]

    def check_action(self, action: str, parameters: tuple) -> bool | None:
        """Control which actions are available based on current view"""
        return True

    def __init__(self):
        super().__init__()
        self.github_token = os.getenv("GITHUB_TOKEN")
        self.github_org = os.getenv("GITHUB_ORG")
        
        if not self.github_token:
            raise ValueError("GITHUB_TOKEN environment variable is required")
        if not self.github_org:
            raise ValueError("GITHUB_ORG environment variable is required")
        
        # Use new authentication method
        auth = Auth.Token(self.github_token)
        self.github = Github(auth=auth)
        self.prs: List[PullRequest.PullRequest] = []
        self.all_prs: List[PullRequest.PullRequest] = []  # Store all PRs before filtering
        self.pr_list_items: List[tuple[str, str]] = []  # Cache for list items (label, id)
        self.current_view = "list"  # Can be "list", "detail", or "files"
        self.current_pr = None  # Store current PR for navigation
        self.sort_order = "newest"  # Can be "newest" or "oldest"
        self.filtered_repo = None  # Currently filtered repository

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        yield Header()
        yield Container(PRListView(id="pr_list"))
        yield Footer()

    def on_mount(self) -> None:
        """Called when the app is mounted."""
        self.title = "PR Manager"
        self._update_subtitle()
        self.load_prs()
        # Force refresh of bindings to show initial state
        self.call_later(self.refresh_bindings)

    def toggle_sort_order(self) -> None:
        """Toggle sort order between newest and oldest"""
        if self.sort_order == "newest":
            self.sort_order = "oldest"
        else:
            self.sort_order = "newest"
        
        # Update subtitle
        self._update_subtitle()
        
        # Re-sort and display the current PRs
        self._sort_and_display_prs()
    
    def _update_subtitle(self) -> None:
        """Update subtitle with current order and filter info"""
        order_text = "Oldest First" if self.sort_order == "oldest" else "Newest First"
        subtitle = f"Organization: {self.github_org} | Order: {order_text}"
        if self.filtered_repo:
            subtitle += f" | Repo: {self.filtered_repo}"
        self.sub_title = subtitle
    
    def open_repo_filter(self) -> None:
        """Open repository filter dialog"""
        # Get unique repository names from all PRs
        repo_names = sorted(set(pr.base.repo.name for pr in self.all_prs))
        
        if not repo_names:
            return
        
        # Show the filter screen using push_screen_wait
        self.push_screen(RepoFilterScreen(repo_names), self._handle_repo_filter_result)
    
    def _handle_repo_filter_result(self, result: str | None) -> None:
        """Handle the result from the repo filter screen"""
        if result is not None:
            # Filter was applied (result is repo name or None for all)
            self.filtered_repo = result
            self._update_subtitle()
            self._apply_repo_filter()
    
    def _apply_repo_filter(self) -> None:
        """Apply repository filter to PRs"""
        if self.filtered_repo:
            # Filter PRs by repository
            self.prs = [pr for pr in self.all_prs if pr.base.repo.name == self.filtered_repo]
        else:
            # Show all PRs
            self.prs = self.all_prs.copy()
        
        # Re-sort and display
        self._sort_and_display_prs()
    
    def _sort_and_display_prs(self) -> None:
        """Sort and display PRs based on current sort order"""
        try:
            list_view = self.query_one("#pr_list", PRListView)
        except Exception:
            return
        
        # Sort PRs by created date
        if self.sort_order == "oldest":
            sorted_prs = sorted(self.prs, key=lambda pr: pr.created_at)
        else:
            sorted_prs = sorted(self.prs, key=lambda pr: pr.created_at, reverse=True)
        
        # Store sorted order
        self.prs = sorted_prs
        
        # Clear and rebuild list
        list_view.clear()
        self.pr_list_items = []
        
        for pr in self.prs:
            repo_name = pr.base.repo.name
            label = f"#{pr.number} - {pr.title} ({repo_name}) by {pr.user.login}"
            item_id = f"pr_{pr.base.repo.full_name.replace('/', '_').replace('-', '_')}_{pr.number}_{int(datetime.now().timestamp() * 1000000)}"
            self.pr_list_items.append((label, item_id))
            list_view.append(ListItem(Static(label), id=item_id))
        
        if not self.prs:
            list_view.append(ListItem(Static("No open pull requests found")))
        
        list_view.focus()
    
    def load_prs(self) -> None:
        """Load pull requests from GitHub organization"""
        self.prs = []
        self.all_prs = []
        self.pr_list_items = []
        self.filtered_repo = None  # Reset filter on reload
        
        try:
            list_view = self.query_one("#pr_list", PRListView)
        except Exception:
            # If list view doesn't exist, can't load PRs
            return
        
        # Clear existing items first
        list_view.clear()
        
        # Show loading message (without ID to avoid conflicts)
        list_view.append(ListItem(Static("Loading PRs...")))

        try:
            org = self.github.get_organization(self.github_org)
            
            # Clear loading message
            list_view.clear()
            
            # Get all repositories in the organization
            for repo in org.get_repos():
                # Get open pull requests for each repository
                for pr in repo.get_pulls(state="open"):
                    self.all_prs.append(pr)
            
            # Copy all PRs to prs (no filter initially)
            self.prs = self.all_prs.copy()
            
            # Sort and display
            self._sort_and_display_prs()
                
        except Exception as e:
            # Clear loading message on error
            list_view.clear()
            # Don't add ID to avoid conflicts when reloading
            list_view.append(ListItem(Static(f"Error loading PRs: {str(e)}")))
        finally:
            # Ensure list has focus
            list_view.focus()
    
    def restore_pr_list(self) -> None:
        """Restore PR list from cache without reloading from GitHub"""
        try:
            list_view = self.query_one("#pr_list", PRListView)
            list_view.clear()
        except Exception:
            # If query fails, create a new list view
            return
        
        if self.pr_list_items:
            for label, item_id in self.pr_list_items:
                list_view.append(ListItem(Static(label), id=item_id))
        else:
            # Don't add ID to avoid conflicts
            list_view.append(ListItem(Static("No open pull requests found")))

    def show_pr_files(self, pr: PullRequest.PullRequest) -> None:
        """Show file changes for a PR"""
        container = self.query_one(Container)
        container.remove_children()
        files_view = PRFilesView(pr)
        container.mount(files_view)
        files_view.focus()
        
        self.current_view = "files"
        self.current_pr = pr
        self.refresh_bindings()
    
    def on_list_view_selected(self, event: ListView.Selected) -> None:
        """Handle when a PR is selected from the list"""
        if self.current_view == "list" and self.prs:
            list_view = self.query_one("#pr_list", ListView)
            if list_view.index is not None and list_view.index < len(self.prs):
                selected_pr = self.prs[list_view.index]
                
                # Remove the list view and show detail view
                container = self.query_one(Container)
                container.remove_children()
                detail_view = PRDetailView(selected_pr)
                container.mount(detail_view)
                detail_view.focus()  # Give focus so arrow keys work
                
                self.current_view = "detail"
                self.current_pr = selected_pr
                self.refresh_bindings()  # Update footer bindings

    def action_show_detail(self) -> None:
        """Show details of the selected PR"""
        if self.current_view == "list" and self.prs:
            list_view = self.query_one("#pr_list", ListView)
            if list_view.index is not None and list_view.index < len(self.prs):
                selected_pr = self.prs[list_view.index]
                
                # Remove the list view and show detail view
                container = self.query_one(Container)
                container.remove_children()
                detail_view = PRDetailView(selected_pr)
                container.mount(detail_view)
                detail_view.focus()  # Give focus so arrow keys work
                
                self.current_view = "detail"
                self.current_pr = selected_pr
                self.refresh_bindings()  # Update footer bindings

    def action_quit_or_back(self) -> None:
        """Quit the app or go back to previous view"""
        if self.current_view == "files":
            # Go back to detail view
            if self.current_pr:
                container = self.query_one(Container)
                container.remove_children()
                detail_view = PRDetailView(self.current_pr)
                container.mount(detail_view)
                detail_view.focus()
                self.current_view = "detail"
                self.refresh_bindings()
        elif self.current_view == "detail":
            # Go back to list view (restore from cache, no reload)
            container = self.query_one(Container)
            container.remove_children()
            list_view = PRListView(id="pr_list")
            container.mount(list_view)
            self.restore_pr_list()  # Restore from cache instead of reloading
            list_view.focus()  # Give focus to the list so arrow keys work
            self.current_view = "list"
            self.current_pr = None
            self.refresh_bindings()  # Update footer bindings
        else:
            # Quit the app
            self.exit()


def main():
    """Main entry point"""
    app = PRManagerApp()
    app.run()


if __name__ == "__main__":
    main()
