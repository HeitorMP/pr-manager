package github

import (
	"context"
	"fmt"
	"os"

	"github.com/google/go-github/v58/github"
	"golang.org/x/oauth2"
)

// Client wraps the GitHub API client
type Client struct {
	client *github.Client
	ctx    context.Context
}

// NewClient creates a new GitHub client with authentication
func NewClient(token string) (*Client, error) {
	if token == "" {
		token = os.Getenv("GITHUB_TOKEN")
	}
	
	if token == "" {
		return nil, fmt.Errorf("GitHub token is required. Set GITHUB_TOKEN environment variable or pass token parameter")
	}

	ctx := context.Background()
	ts := oauth2.StaticTokenSource(
		&oauth2.Token{AccessToken: token},
	)
	tc := oauth2.NewClient(ctx, ts)
	
	client := github.NewClient(tc)

	return &Client{
		client: client,
		ctx:    ctx,
	}, nil
}

// PullRequest represents a simplified pull request
type PullRequest struct {
	Number         int
	Title          string
	Author         string
	State          string
	CreatedAt      string
	UpdatedAt      string
	URL            string
	Base           string
	Head           string
	Mergeable      *bool
	MergeableState string
	Draft          bool
	Body           string
	Comments       int
	Commits        int
	Additions      int
	Deletions      int
	ChangedFiles   int
}

// ListPullRequests lists pull requests in a repository
func (c *Client) ListPullRequests(owner, repo, state string, limit int) ([]*PullRequest, error) {
	opts := &github.PullRequestListOptions{
		State:     state,
		Sort:      "created",
		Direction: "desc",
		ListOptions: github.ListOptions{
			PerPage: limit,
		},
	}

	pulls, _, err := c.client.PullRequests.List(c.ctx, owner, repo, opts)
	if err != nil {
		return nil, fmt.Errorf("error listing pull requests: %w", err)
	}

	prs := make([]*PullRequest, 0, len(pulls))
	for _, pr := range pulls {
		prs = append(prs, &PullRequest{
			Number:         pr.GetNumber(),
			Title:          pr.GetTitle(),
			Author:         pr.GetUser().GetLogin(),
			State:          pr.GetState(),
			CreatedAt:      pr.GetCreatedAt().Format("2006-01-02 15:04:05"),
			UpdatedAt:      pr.GetUpdatedAt().Format("2006-01-02 15:04:05"),
			URL:            pr.GetHTMLURL(),
			MergeableState: pr.GetMergeableState(),
			Draft:          pr.GetDraft(),
		})
	}

	return prs, nil
}

// GetPullRequest gets details of a specific pull request
func (c *Client) GetPullRequest(owner, repo string, number int) (*PullRequest, error) {
	pr, _, err := c.client.PullRequests.Get(c.ctx, owner, repo, number)
	if err != nil {
		return nil, fmt.Errorf("error getting pull request #%d: %w", number, err)
	}

	return &PullRequest{
		Number:         pr.GetNumber(),
		Title:          pr.GetTitle(),
		Body:           pr.GetBody(),
		Author:         pr.GetUser().GetLogin(),
		State:          pr.GetState(),
		CreatedAt:      pr.GetCreatedAt().Format("2006-01-02 15:04:05"),
		UpdatedAt:      pr.GetUpdatedAt().Format("2006-01-02 15:04:05"),
		URL:            pr.GetHTMLURL(),
		Base:           pr.GetBase().GetRef(),
		Head:           pr.GetHead().GetRef(),
		Mergeable:      pr.Mergeable,
		MergeableState: pr.GetMergeableState(),
		Draft:          pr.GetDraft(),
		Comments:       pr.GetComments(),
		Commits:        pr.GetCommits(),
		Additions:      pr.GetAdditions(),
		Deletions:      pr.GetDeletions(),
		ChangedFiles:   pr.GetChangedFiles(),
	}, nil
}

// AddComment adds a comment to a pull request
func (c *Client) AddComment(owner, repo string, number int, comment string) error {
	issueComment := &github.IssueComment{
		Body: github.String(comment),
	}

	_, _, err := c.client.Issues.CreateComment(c.ctx, owner, repo, number, issueComment)
	if err != nil {
		return fmt.Errorf("error adding comment to PR #%d: %w", number, err)
	}

	return nil
}

// ApprovePullRequest approves a pull request
func (c *Client) ApprovePullRequest(owner, repo string, number int, comment string) error {
	if comment == "" {
		comment = "Approved via pr-manager CLI"
	}

	review := &github.PullRequestReviewRequest{
		Body:  github.String(comment),
		Event: github.String("APPROVE"),
	}

	_, _, err := c.client.PullRequests.CreateReview(c.ctx, owner, repo, number, review)
	if err != nil {
		return fmt.Errorf("error approving PR #%d: %w", number, err)
	}

	return nil
}

// RequestChanges requests changes on a pull request
func (c *Client) RequestChanges(owner, repo string, number int, comment string) error {
	review := &github.PullRequestReviewRequest{
		Body:  github.String(comment),
		Event: github.String("REQUEST_CHANGES"),
	}

	_, _, err := c.client.PullRequests.CreateReview(c.ctx, owner, repo, number, review)
	if err != nil {
		return fmt.Errorf("error requesting changes on PR #%d: %w", number, err)
	}

	return nil
}

// MergePullRequest merges a pull request
func (c *Client) MergePullRequest(owner, repo string, number int, commitMessage, mergeMethod string) error {
	opts := &github.PullRequestOptions{
		MergeMethod: mergeMethod,
	}

	if commitMessage != "" {
		opts.CommitMessage = commitMessage
	}

	result, _, err := c.client.PullRequests.Merge(c.ctx, owner, repo, number, "", opts)
	if err != nil {
		return fmt.Errorf("error merging PR #%d: %w", number, err)
	}

	if !result.GetMerged() {
		return fmt.Errorf("failed to merge PR #%d: %s", number, result.GetMessage())
	}

	return nil
}
