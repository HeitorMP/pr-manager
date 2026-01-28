# PR Manager TUI

A Terminal User Interface (TUI) application for managing GitHub Pull Requests in your organization.

## Features

- 📋 List all open pull requests from your organization
- ⬆️⬇️ Navigate through PRs using arrow keys
- 👀 View detailed information about a PR by pressing Enter
- ⬅️ Go back to the list with Q key
- 🚪 Exit the application with Q key (from list view)

## Setup

1. Create a GitHub Personal Access Token:
   - Go to GitHub Settings → Developer settings → Personal access tokens → Tokens (classic)
   - Generate a new token with `repo` and `read:org` scopes

2. Copy `.env.example` to `.env` and fill in your details:
   ```bash
   cp .env.example .env
   ```

3. Edit `.env` file:
   ```
   GITHUB_TOKEN=your_github_token_here
   GITHUB_ORG=your_organization_name
   ```

4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

5. Run the application:
   ```bash
   python main.py
   ```

## Usage

- **Arrow Keys**: Navigate up/down through the PR list
- **Enter**: View detailed information about the selected PR
- **Q**: 
  - From detail view: Go back to the list
  - From list view: Exit the application

## Future Features

- Add comments to PRs
- Approve/Request changes on PRs
- Merge PRs
- Filter PRs by repository, author, or label
- Refresh PR list
