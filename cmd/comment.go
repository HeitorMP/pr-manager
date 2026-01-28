package cmd

import (
	"github.com/fatih/color"
	"github.com/spf13/cobra"
)

var (
	commentOwner   string
	commentRepo    string
	commentPR      int
	commentMessage string
)

var commentCmd = &cobra.Command{
	Use:   "comment",
	Short: "Add a comment to a pull request",
	Long:  `Post a comment on a specific pull request.`,
	RunE: func(cmd *cobra.Command, args []string) error {
		err := client.AddComment(commentOwner, commentRepo, commentPR, commentMessage)
		if err != nil {
			return err
		}

		color.Green("✓ Comment added successfully to PR #%d", commentPR)
		return nil
	},
}

func init() {
	rootCmd.AddCommand(commentCmd)

	commentCmd.Flags().StringVarP(&commentOwner, "owner", "o", "", "Repository owner (organization or user) (required)")
	commentCmd.Flags().StringVarP(&commentRepo, "repo", "r", "", "Repository name (required)")
	commentCmd.Flags().IntVarP(&commentPR, "pr", "p", 0, "Pull request number (required)")
	commentCmd.Flags().StringVarP(&commentMessage, "message", "m", "", "Comment text (required)")

	commentCmd.MarkFlagRequired("owner")
	commentCmd.MarkFlagRequired("repo")
	commentCmd.MarkFlagRequired("pr")
	commentCmd.MarkFlagRequired("message")
}
