"""
PR Files View - Widget for displaying file changes in a pull request
"""

import re
from github import PullRequest
from rich.console import Group
from rich.table import Table
from rich.text import Text
from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import VerticalScroll
from textual.widgets import Static


class PRFilesView(VerticalScroll):
    """Widget to display PR file changes"""
    
    BINDINGS = [
        Binding("down,j", "scroll_down", "Scroll Down", show=False),
        Binding("up,k", "scroll_up", "Scroll Up", show=False),
        Binding("pagedown", "page_down", "Page Down", show=False),
        Binding("pageup", "page_up", "Page Up", show=False),
    ]

    def __init__(self, pr: PullRequest.PullRequest):
        super().__init__()
        self.pr = pr

    def compose(self) -> ComposeResult:
        """Compose the files view"""
        yield Static("Loading file changes...")
    
    def _parse_hunk_header(self, line: str):
        """Parse hunk header to get line numbers"""
        # Format: @@ -old_start,old_count +new_start,new_count @@
        match = re.match(r'@@ -(\d+),?(\d*) \+(\d+),?(\d*) @@', line)
        if match:
            old_start = int(match.group(1))
            new_start = int(match.group(3))
            return old_start, new_start
        return None, None
    
    def _create_side_by_side_diff(self, patch: str) -> Table:
        """Create a side-by-side diff table"""
        table = Table(
            show_header=True,
            header_style="bold cyan",
            box=None,
            padding=(0, 1),
            expand=True,
        )
        
        table.add_column("Line", style="dim", width=5, justify="right")
        table.add_column("Original", style="", ratio=1)
        table.add_column("Line", style="dim", width=5, justify="right")
        table.add_column("Modified", style="", ratio=1)
        
        old_line_num = 0
        new_line_num = 0
        
        for line in patch.split('\n'):
            if line.startswith('@@'):
                # Parse hunk header
                old_start, new_start = self._parse_hunk_header(line)
                if old_start and new_start:
                    old_line_num = old_start
                    new_line_num = new_start
                
                # Add hunk header row spanning all columns
                hunk_text = Text(line, style="bold cyan on #1f2937")
                table.add_row("", hunk_text, "", "")
                
            elif line.startswith('---') or line.startswith('+++'):
                # Skip file headers in the table
                continue
                
            elif line.startswith('-'):
                # Removed line - show only on left
                content = line[1:]  # Remove the '-' prefix
                old_text = Text(content, style="#ef4444 on #7f1d1d")
                table.add_row(
                    str(old_line_num),
                    old_text,
                    "",
                    Text("", style="on #1f2937")
                )
                old_line_num += 1
                
            elif line.startswith('+'):
                # Added line - show only on right
                content = line[1:]  # Remove the '+' prefix
                new_text = Text(content, style="#22c55e on #14532d")
                table.add_row(
                    "",
                    Text("", style="on #1f2937"),
                    str(new_line_num),
                    new_text
                )
                new_line_num += 1
                
            elif line.startswith(' '):
                # Context line - show on both sides
                content = line[1:]  # Remove the ' ' prefix
                context_text = Text(content, style="white on #1f2937")
                table.add_row(
                    str(old_line_num),
                    context_text,
                    str(new_line_num),
                    Text(content, style="white on #1f2937")
                )
                old_line_num += 1
                new_line_num += 1
            elif line.strip():
                # Other content
                table.add_row("", Text(line, style="dim"), "", "")
        
        return table
    
    def on_mount(self) -> None:
        """Load and display file changes when mounted"""
        try:
            files = self.pr.get_files()
            
            # Build rich content
            content_parts = []
            
            # Header
            header = Text()
            header.append(f"File Changes for PR #{self.pr.number}\n\n", style="bold bright_cyan")
            header.append(f"Total Files Changed: ", style="white")
            header.append(f"{self.pr.changed_files}", style="bold yellow")
            header.append(" | ", style="dim white")
            header.append(f"Additions: ", style="white")
            header.append(f"+{self.pr.additions}", style="bold green")
            header.append(" | ", style="dim white")
            header.append(f"Deletions: ", style="white")
            header.append(f"-{self.pr.deletions}", style="bold red")
            header.append("\n\n")
            
            content_parts.append(header)
            content_parts.append(Text("─" * 80 + "\n\n", style="dim white"))
            
            for file in files:
                status_icon = {
                    "added": "🆕",
                    "removed": "🗑️",
                    "modified": "✏️",
                    "renamed": "📝",
                }
                
                icon = status_icon.get(file.status, "📄")
                
                # File header
                file_header = Text()
                file_header.append(f"\n{icon} ", style="")
                file_header.append(f"{file.filename}", style="bold bright_yellow")
                file_header.append("\n", style="")
                
                # File info
                file_info = Text()
                file_info.append(f"Status: ", style="dim white")
                
                status_colors = {
                    "added": "bold green",
                    "removed": "bold red",
                    "modified": "bold yellow",
                    "renamed": "bold blue",
                }
                file_info.append(f"{file.status.upper()}", style=status_colors.get(file.status, "white"))
                file_info.append(" | ", style="dim white")
                file_info.append(f"Changes: ", style="dim white")
                file_info.append(f"+{file.additions}", style="green")
                file_info.append(f" -{file.deletions}", style="red")
                file_info.append("\n", style="")
                
                if file.status == "renamed":
                    file_info.append(f"Previous name: {file.previous_filename}\n", style="dim white")
                
                content_parts.append(file_header)
                content_parts.append(file_info)
                content_parts.append(Text("\n"))
                
                # Patch content - side by side
                if file.patch:
                    # Create side-by-side diff table
                    diff_table = self._create_side_by_side_diff(file.patch)
                    content_parts.append(diff_table)
                    content_parts.append(Text("\n"))
                else:
                    no_patch = Text("No patch available (binary file or too large)\n", style="dim italic")
                    content_parts.append(no_patch)
                
                # Separator
                content_parts.append(Text("\n" + "─" * 80 + "\n", style="dim white"))
            
            # Update with all content parts (mix of Text and Table objects)
            static_widget = self.query_one(Static)
            static_widget.update(Group(*content_parts))
            
        except Exception as e:
            error_text = Text()
            error_text.append("Error Loading Files\n\n", style="bold red")
            error_text.append(str(e), style="white")
            self.query_one(Static).update(error_text)
