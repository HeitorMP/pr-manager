package cmd

import (
	"github.com/fatih/color"
	"github.com/spf13/cobra"
)

var (
	approveOwner   string
	approveRepo    string
	approvePR      int
	approveMessage string
)

var approveCmd = &cobra.Command{
	Use:   "approve",
	Short: "Approve a pull request",
	Long:  `Submit an approval review for a pull request.`,
	RunE: func(cmd *cobra.Command, args []string) error {
		err := client.ApprovePullRequest(approveOwner, approveRepo, approvePR, approveMessage)
		if err != nil {
			return err
		}

		color.Green("✓ PR #%d approved successfully!", approvePR)
		return nil
	},
}

func init() {
	rootCmd.AddCommand(approveCmd)

	approveCmd.Flags().StringVarP(&approveOwner, "owner", "o", "", "Repository owner (organization or user) (required)")
	approveCmd.Flags().StringVarP(&approveRepo, "repo", "r", "", "Repository name (required)")
	approveCmd.Flags().IntVarP(&approvePR, "pr", "p", 0, "Pull request number (required)")
	approveCmd.Flags().StringVarP(&approveMessage, "message", "m", "", "Optional review comment")

	approveCmd.MarkFlagRequired("owner")
	approveCmd.MarkFlagRequired("repo")
	approveCmd.MarkFlagRequired("pr")
}
