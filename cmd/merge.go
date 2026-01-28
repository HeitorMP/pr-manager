package cmd

import (
	"fmt"

	"github.com/fatih/color"
	"github.com/spf13/cobra"
)

var (
	mergeOwner   string
	mergeRepo    string
	mergePR      int
	mergeMethod  string
	mergeMessage string
	mergeConfirm bool
)

var mergeCmd = &cobra.Command{
	Use:   "merge",
	Short: "Merge a pull request",
	Long:  `Merge a pull request using the specified merge method (merge, squash, or rebase).`,
	RunE: func(cmd *cobra.Command, args []string) error {
		// Confirmation prompt
		if !mergeConfirm {
			fmt.Printf("Are you sure you want to merge PR #%d? [y/N]: ", mergePR)
			var response string
			fmt.Scanln(&response)
			if response != "y" && response != "Y" {
				color.Yellow("Merge cancelled")
				return nil
			}
		}

		err := client.MergePullRequest(mergeOwner, mergeRepo, mergePR, mergeMessage, mergeMethod)
		if err != nil {
			return err
		}

		color.Green("✓ PR #%d merged successfully using %s method!", mergePR, mergeMethod)
		return nil
	},
}

func init() {
	rootCmd.AddCommand(mergeCmd)

	mergeCmd.Flags().StringVarP(&mergeOwner, "owner", "o", "", "Repository owner (organization or user) (required)")
	mergeCmd.Flags().StringVarP(&mergeRepo, "repo", "r", "", "Repository name (required)")
	mergeCmd.Flags().IntVarP(&mergePR, "pr", "p", 0, "Pull request number (required)")
	mergeCmd.Flags().StringVarP(&mergeMethod, "method", "M", "merge", "Merge method (merge, squash, or rebase)")
	mergeCmd.Flags().StringVarP(&mergeMessage, "message", "m", "", "Optional commit message")
	mergeCmd.Flags().BoolVarP(&mergeConfirm, "yes", "y", false, "Skip confirmation prompt")

	mergeCmd.MarkFlagRequired("owner")
	mergeCmd.MarkFlagRequired("repo")
	mergeCmd.MarkFlagRequired("pr")
}
