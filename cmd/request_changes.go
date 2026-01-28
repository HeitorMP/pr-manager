package cmd

import (
	"github.com/fatih/color"
	"github.com/spf13/cobra"
)

var (
	changesOwner   string
	changesRepo    string
	changesPR      int
	changesMessage string
)

var requestChangesCmd = &cobra.Command{
	Use:   "request-changes",
	Short: "Request changes on a pull request",
	Long:  `Submit a review requesting changes on a pull request.`,
	RunE: func(cmd *cobra.Command, args []string) error {
		err := client.RequestChanges(changesOwner, changesRepo, changesPR, changesMessage)
		if err != nil {
			return err
		}

		color.Yellow("Changes requested on PR #%d", changesPR)
		return nil
	},
}

func init() {
	rootCmd.AddCommand(requestChangesCmd)

	requestChangesCmd.Flags().StringVarP(&changesOwner, "owner", "o", "", "Repository owner (organization or user) (required)")
	requestChangesCmd.Flags().StringVarP(&changesRepo, "repo", "r", "", "Repository name (required)")
	requestChangesCmd.Flags().IntVarP(&changesPR, "pr", "p", 0, "Pull request number (required)")
	requestChangesCmd.Flags().StringVarP(&changesMessage, "message", "m", "", "Comment explaining required changes (required)")

	requestChangesCmd.MarkFlagRequired("owner")
	requestChangesCmd.MarkFlagRequired("repo")
	requestChangesCmd.MarkFlagRequired("pr")
	requestChangesCmd.MarkFlagRequired("message")
}
