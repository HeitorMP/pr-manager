package cmd

import (
	"fmt"
	"os"
	"text/tabwriter"

	"github.com/fatih/color"
	"github.com/spf13/cobra"
)

var (
	listOwner string
	listRepo  string
	listState string
	listLimit int
)

var listCmd = &cobra.Command{
	Use:   "list",
	Short: "List pull requests in a repository",
	Long:  `List pull requests in a GitHub repository with filtering options.`,
	RunE: func(cmd *cobra.Command, args []string) error {
		prs, err := client.ListPullRequests(listOwner, listRepo, listState, listLimit)
		if err != nil {
			return err
		}

		if len(prs) == 0 {
			color.Yellow("No %s pull requests found in %s/%s", listState, listOwner, listRepo)
			return nil
		}

		// Print header
		cyan := color.New(color.FgCyan, color.Bold)
		cyan.Printf("\nPull Requests in %s/%s (%s)\n\n", listOwner, listRepo, listState)

		// Create table writer
		w := tabwriter.NewWriter(os.Stdout, 0, 0, 3, ' ', 0)
		fmt.Fprintln(w, "#\tTitle\tAuthor\tState\tDraft\tUpdated")
		fmt.Fprintln(w, "─\t─────\t──────\t─────\t─────\t───────")

		for _, pr := range prs {
			draftStatus := ""
			if pr.Draft {
				draftStatus = "✓"
			}

			stateIcon := "🟢"
			if pr.State != "open" {
				stateIcon = "🔴"
			}

			// Truncate title if too long
			title := pr.Title
			if len(title) > 60 {
				title = title[:57] + "..."
			}

			fmt.Fprintf(w, "%d\t%s\t%s\t%s %s\t%s\t%s\n",
				pr.Number,
				title,
				pr.Author,
				stateIcon,
				pr.State,
				draftStatus,
				pr.UpdatedAt,
			)
		}
		w.Flush()

		color.New(color.Faint).Printf("\nTotal: %d pull request(s)\n\n", len(prs))

		return nil
	},
}

func init() {
	rootCmd.AddCommand(listCmd)

	listCmd.Flags().StringVarP(&listOwner, "owner", "o", "", "Repository owner (organization or user) (required)")
	listCmd.Flags().StringVarP(&listRepo, "repo", "r", "", "Repository name (required)")
	listCmd.Flags().StringVarP(&listState, "state", "s", "open", "PR state to filter (open, closed, all)")
	listCmd.Flags().IntVarP(&listLimit, "limit", "l", 10, "Maximum number of PRs to list")

	listCmd.MarkFlagRequired("owner")
	listCmd.MarkFlagRequired("repo")
}
