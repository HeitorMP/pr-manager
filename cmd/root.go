package cmd

import (
	"fmt"
	"os"

	"github.com/joho/godotenv"
	"github.com/spf13/cobra"
	"github.com/yourusername/pr-manager/pkg/github"
)

var (
	token string
	client *github.Client
)

var rootCmd = &cobra.Command{
	Use:   "pr-manager",
	Short: "PR Manager - GitHub Pull Request Management CLI",
	Long:  `A simple CLI tool to manage GitHub Pull Requests: list, comment, approve, and merge PRs.`,
	PersistentPreRunE: func(cmd *cobra.Command, args []string) error {
		// Load .env file if it exists
		_ = godotenv.Load()

		// Initialize GitHub client
		var err error
		client, err = github.NewClient(token)
		if err != nil {
			return err
		}
		return nil
	},
}

// Execute runs the root command
func Execute() {
	if err := rootCmd.Execute(); err != nil {
		fmt.Fprintf(os.Stderr, "Error: %v\n", err)
		os.Exit(1)
	}
}

func init() {
	rootCmd.PersistentFlags().StringVar(&token, "token", "", "GitHub personal access token (or set GITHUB_TOKEN env var)")
}
