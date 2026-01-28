# PR Manager (Go)

CLI tool written in Go to manage GitHub Pull Requests.

## Features

- ✅ List PRs from a repository
- ✅ View detailed information about a specific PR
- ✅ Add comments to PRs
- ✅ Approve PRs
- ✅ Request changes on PRs
- ✅ Merge PRs

## Installation

### Prerequisites

- Go 1.21+
- GitHub personal access token

### Steps

1. Clone the repository:
```bash
git clone <your-repository>
cd pr-manager/go-version
```

2. Download dependencies:
```bash
go mod download
```

3. Build the binary:
```bash
make build
# or
go build -o pr-manager main.go
```

4. (Optional) Install globally:
```bash
make install
# or
go install
```

5. Configure your GitHub token:
```bash
cp .env.example .env
# Edit the .env file and add your token
```

### Creating a GitHub Token

1. Go to https://github.com/settings/tokens
2. Click "Generate new token" → "Generate new token (classic)"
3. Give it a descriptive name
4. Select the `repo` scope (full control of private repositories)
5. Click "Generate token"
6. Copy the token and add it to the `.env` file

## Usage

### Configure Token

You can provide the token in three ways:

1. `.env` file:
```bash
GITHUB_TOKEN=your_token_here
```

2. Environment variable:
```bash
export GITHUB_TOKEN=your_token_here
```

3. Command line parameter:
```bash
pr-manager --token=your_token_here <command>
```

### Available Commands

#### List Pull Requests

```bash
# List open PRs (default)
pr-manager list --owner <owner> --repo <repo>

# List closed PRs
pr-manager list --owner <owner> --repo <repo> --state closed

# List all PRs
pr-manager list --owner <owner> --repo <repo> --state all

# Limit number of results
pr-manager list --owner <owner> --repo <repo> --limit 5
```

Example:
```bash
pr-manager list -o facebook -r react --limit 5
```

#### Show PR Details

```bash
pr-manager show --owner <owner> --repo <repo> --pr <number>
```

Example:
```bash
pr-manager show -o facebook -r react -p 12345
```

#### Add Comment

```bash
pr-manager comment --owner <owner> --repo <repo> --pr <number> --message "Your comment"
```

Example:
```bash
pr-manager comment -o myorg -r myrepo -p 42 -m "LGTM! 🚀"
```

#### Approve PR

```bash
# Approve without comment
pr-manager approve --owner <owner> --repo <repo> --pr <number>

# Approve with comment
pr-manager approve --owner <owner> --repo <repo> --pr <number> --message "Looks good!"
```

Example:
```bash
pr-manager approve -o myorg -r myrepo -p 42 -m "Code reviewed and approved!"
```

#### Request Changes

```bash
pr-manager request-changes --owner <owner> --repo <repo> --pr <number> --message "Please adjust..."
```

Example:
```bash
pr-manager request-changes -o myorg -r myrepo -p 42 -m "Please add unit tests."
```

#### Merge PR

```bash
# Default merge
pr-manager merge --owner <owner> --repo <repo> --pr <number>

# Squash merge
pr-manager merge --owner <owner> --repo <repo> --pr <number> --method squash

# Rebase merge
pr-manager merge --owner <owner> --repo <repo> --pr <number> --method rebase

# With custom commit message
pr-manager merge --owner <owner> --repo <repo> --pr <number> --message "Custom commit message"

# Skip confirmation
pr-manager merge --owner <owner> --repo <repo> --pr <number> --yes
```

Example:
```bash
pr-manager merge -o myorg -r myrepo -p 42 --method squash -y
```

### Help

To see all available commands:
```bash
pr-manager --help
```

For help on a specific command:
```bash
pr-manager list --help
pr-manager approve --help
```

## Project Structure

```
go-version/
├── cmd/
│   ├── root.go              # Root command and configuration
│   ├── list.go              # List command
│   ├── show.go              # Show command
│   ├── comment.go           # Comment command
│   ├── approve.go           # Approve command
│   ├── request_changes.go   # Request-changes command
│   └── merge.go             # Merge command
├── pkg/
│   └── github/
│       └── client.go        # GitHub API client
├── main.go                  # Entry point
├── go.mod                   # Go modules
├── Makefile                 # Build automation
├── .env.example            # Configuration example
├── .gitignore
└── README.md
```

## Main Dependencies

- **google/go-github**: Official Go client for GitHub API
- **spf13/cobra**: Framework for building robust CLIs
- **joho/godotenv**: Environment variable management
- **fatih/color**: Terminal output colorization
- **golang.org/x/oauth2**: OAuth2 authentication

## Makefile

The project includes a Makefile to facilitate development:

```bash
make build      # Build the binary
make install    # Install globally
make clean      # Remove build artifacts
make deps       # Download dependencies
make test       # Run tests
make fmt        # Format code
make lint       # Run linter
make help       # Show available commands
```

## Comparison with Python

### Advantages of the Go version:
- ✅ **Single binary**: Distribute only one executable file
- ✅ **Performance**: Much faster than Python
- ✅ **No dependencies**: No need to install runtime or libs
- ✅ **Cross-compile**: Compile for Windows, Linux, macOS at once
- ✅ **Static typing**: Fewer runtime errors
- ✅ **Lower memory consumption**

### Cross-compilation example:
```bash
# Linux
GOOS=linux GOARCH=amd64 go build -o pr-manager-linux main.go

# Windows
GOOS=windows GOARCH=amd64 go build -o pr-manager.exe main.go

# macOS Intel
GOOS=darwin GOARCH=amd64 go build -o pr-manager-darwin-amd64 main.go

# macOS Apple Silicon
GOOS=darwin GOARCH=arm64 go build -o pr-manager-darwin-arm64 main.go
```

## Development

To contribute to the project:

1. Fork the repository
2. Create a branch for your feature (`git checkout -b feature/new-feature`)
3. Commit your changes (`git commit -am 'Add new feature'`)
4. Push to the branch (`git push origin feature/new-feature`)
5. Open a Pull Request

## Tests

```bash
# Run all tests
go test ./...

# With verbose output
go test -v ./...

# With coverage
go test -cover ./...
```

## License

MIT

## Author

Built with ❤️ to make managing GitHub Pull Requests easier.
