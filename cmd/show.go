package cmd

import (
	"fmt"

	"github.com/fatih/color"
	"github.com/spf13/cobra"
)

var (
	showOwner string
	showRepo  string
	showPR    int
)

var showCmd = &cobra.Command{
	Use:   "show",
	Short: "Show detailed information about a pull request",
	Long:  `Display comprehensive details about a specific pull request.`,
	RunE: func(cmd *cobra.Command, args []string) error {
		pr, err := client.GetPullRequest(showOwner, showRepo, showPR)
		if err != nil {
			return err
		}

		// Print PR details
		cyan := color.New(color.FgCyan, color.Bold)
		cyan.Printf("\n═══ PR #%d ═══\n\n", pr.Number)

		fmt.Printf("Title:    %s\n", pr.Title)
		fmt.Printf("Author:   %s\n", pr.Author)
		fmt.Printf("State:    %s\n", pr.State)
		fmt.Printf("Draft:    %v\n", pr.Draft)
		fmt.Printf("Base:     %s ← Head: %s\n", pr.Base, pr.Head)
		fmt.Printf("Created:  %s\n", pr.CreatedAt)
		fmt.Printf("Updated:  %s\n", pr.UpdatedAt)
		fmt.Printf("URL:      %s\n", pr.URL)

		color.New(color.FgYellow, color.Bold).Println("\nStats:")
		fmt.Printf("  • Comments:      %d\n", pr.Comments)
		fmt.Printf("  • Commits:       %d\n", pr.Commits)
		fmt.Printf("  • Files changed: %d\n", pr.ChangedFiles)
		fmt.Printf("  • +%d / -%d lines\n", pr.Additions, pr.Deletions)

		mergeableStr := "unknown"
		if pr.Mergeable != nil {
			mergeableStr = fmt.Sprintf("%v", *pr.Mergeable)
		}
		fmt.Printf("\nMergeable: %s (%s)\n", mergeableStr, pr.MergeableState)

		if pr.Body != "" {
			color.New(color.FgGreen, color.Bold).Println("\nDescription:")
			fmt.Println(pr.Body)
		}

		fmt.Println()
		return nil
	},
}

func init() {
	rootCmd.AddCommand(showCmd)

	showCmd.Flags().StringVarP(&showOwner, "owner", "o", "", "Repository owner (organization or user) (required)")
	showCmd.Flags().StringVarP(&showRepo, "repo", "r", "", "Repository name (required)")
	showCmd.Flags().IntVarP(&showPR, "pr", "p", 0, "Pull request number (required)")

	showCmd.MarkFlagRequired("owner")
	showCmd.MarkFlagRequired("repo")
	showCmd.MarkFlagRequired("pr")
}
