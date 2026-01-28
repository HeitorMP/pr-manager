"""
PR List View - Widget for displaying the list of pull requests
"""

from textual.binding import Binding
from textual.widgets import ListView


class PRListView(ListView):
    """Custom ListView with bindings shown in footer"""
    
    BINDINGS = [
        Binding("enter", "select_cursor", "View Details", show=True),
        Binding("r", "reload", "Reload", show=True),
        Binding("o", "toggle_order", "Toggle Order", show=True),
        Binding("f", "filter_repo", "Filter Repo", show=True),
        Binding("0", "clear_filters", "Clear Filters", show=True),
    ]
    
    def action_reload(self) -> None:
        """Reload PRs from GitHub"""
        self.app.load_prs()
    
    def action_toggle_order(self) -> None:
        """Toggle sort order between newest and oldest"""
        self.app.toggle_sort_order()
    
    def action_filter_repo(self) -> None:
        """Open repository filter dialog"""
        self.app.open_repo_filter()
    
    def action_clear_filters(self) -> None:
        """Clear all filters"""
        self.app.clear_all_filters()
