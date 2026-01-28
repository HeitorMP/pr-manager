"""
Comment Screen - Modal screen for adding comments to PRs
"""

from textual.app import ComposeResult
from textual.containers import Container, Vertical
from textual.screen import ModalScreen
from textual.widgets import Button, Label, TextArea


class CommentScreen(ModalScreen[str | None]):
    """Modal screen for adding a comment to a PR"""
    
    CSS = """
    CommentScreen {
        align: center middle;
    }
    
    #dialog {
        width: 80;
        height: auto;
        border: thick $primary;
        background: $surface;
        padding: 1 2;
    }
    
    #title {
        text-align: center;
        text-style: bold;
        color: $accent;
        margin-bottom: 1;
    }
    
    #comment-area {
        height: 10;
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
    
    BINDINGS = [
        ("escape,q", "cancel", "Cancel"),
    ]
    
    def __init__(self, pr_number: int):
        super().__init__()
        self.pr_number = pr_number
    
    def compose(self) -> ComposeResult:
        """Compose the comment dialog"""
        with Container(id="dialog"):
            yield Label(f"Add Comment to PR #{self.pr_number}", id="title")
            yield Label("Write your comment below (Ctrl+S or click Send to submit):")
            yield TextArea(id="comment-area", language="markdown")
            with Vertical(id="buttons"):
                yield Button("Send Comment", variant="success", id="send-button")
                yield Button("Cancel (Q)", variant="default", id="cancel-button")
    
    def on_mount(self) -> None:
        """Focus on text area when mounted"""
        self.query_one("#comment-area", TextArea).focus()
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button presses"""
        if event.button.id == "send-button":
            # Get the comment text
            comment_text = self.query_one("#comment-area", TextArea).text.strip()
            if comment_text:
                self.dismiss(comment_text)
            else:
                # Don't allow empty comments
                pass
        elif event.button.id == "cancel-button":
            self.dismiss(None)
    
    def action_cancel(self) -> None:
        """Cancel and close dialog"""
        self.dismiss(None)
