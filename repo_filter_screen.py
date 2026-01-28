"""
Repository Filter Screen - Modal screen for filtering PRs by repository
"""

from textual.app import ComposeResult
from textual.containers import Container, Vertical
from textual.screen import ModalScreen
from textual.widgets import Button, Input, Label, ListItem, ListView, Static


class RepoFilterScreen(ModalScreen[str]):
    """Modal screen for selecting a repository to filter PRs"""
    
    CSS = """
    RepoFilterScreen {
        align: center middle;
    }
    
    #dialog {
        width: 80;
        height: auto;
        max-height: 30;
        border: thick $primary;
        background: $surface;
        padding: 1 2;
    }
    
    #filter-input {
        margin-bottom: 1;
        width: 100%;
    }
    
    #repo-list {
        height: 15;
        border: solid $primary;
        margin-bottom: 1;
    }
    
    #buttons {
        height: auto;
        align: center middle;
    }
    
    Button {
        margin: 0 1;
    }
    """
    
    def __init__(self, repos: list[str]):
        super().__init__()
        self.repos = sorted(repos)  # Sort alphabetically
        self.filtered_repos = self.repos.copy()
    
    def compose(self) -> ComposeResult:
        """Compose the filter dialog"""
        with Container(id="dialog"):
            yield Label("Filter by Repository", id="title")
            yield Label("Type to filter, then select a repository:", id="subtitle")
            yield Input(
                placeholder="Type to filter repositories...",
                id="filter-input"
            )
            yield ListView(id="repo-list")
            with Vertical(id="buttons"):
                yield Button("All Repos", variant="primary", id="all-button")
                yield Button("Cancel", variant="default", id="cancel-button")
    
    def on_mount(self) -> None:
        """Populate the repository list when mounted"""
        self._update_repo_list()
        self.query_one("#filter-input", Input).focus()
    
    def _update_repo_list(self, filter_text: str = "") -> None:
        """Update the repository list based on filter"""
        list_view = self.query_one("#repo-list", ListView)
        list_view.clear()
        
        # Filter repositories
        if filter_text:
            self.filtered_repos = [
                repo for repo in self.repos 
                if filter_text.lower() in repo.lower()
            ]
        else:
            self.filtered_repos = self.repos.copy()
        
        # Add filtered repos to list
        if self.filtered_repos:
            for repo in self.filtered_repos:
                list_view.append(ListItem(Label(repo)))
        else:
            list_view.append(ListItem(Label("No repositories found", id="no-results")))
    
    def on_input_changed(self, event: Input.Changed) -> None:
        """Handle input changes for filtering"""
        if event.input.id == "filter-input":
            self._update_repo_list(event.value)
    
    def on_list_view_selected(self, event: ListView.Selected) -> None:
        """Handle repository selection"""
        if event.item.id != "no-results":
            list_view = self.query_one("#repo-list", ListView)
            if list_view.index is not None and list_view.index < len(self.filtered_repos):
                selected_repo = self.filtered_repos[list_view.index]
                self.dismiss(selected_repo)
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button presses"""
        if event.button.id == "all-button":
            # Return None to show all repos
            self.dismiss(None)
        elif event.button.id == "cancel-button":
            # Dismiss without selection
            self.dismiss(None)
