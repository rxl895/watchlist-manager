#!/bin/bash

# GitHub Release Script
# Automates the process of creating a new release

set -e

echo "🚀 GitHub Release Creator"
echo "========================"

# Check if we're in a git repository
if ! git rev-parse --git-dir > /dev/null 2>&1; then
    echo "❌ This is not a git repository"
    exit 1
fi

# Check if there are uncommitted changes
if ! git diff-index --quiet HEAD --; then
    echo "❌ You have uncommitted changes. Please commit or stash them first."
    exit 1
fi

# Get current version from package.json
current_version=$(grep '"version"' frontend/package.json | sed 's/.*"version": "\(.*\)".*/\1/')
echo "📦 Current version: $current_version"

# Ask for new version
echo "📝 Enter new version (e.g., 1.0.1):"
read new_version

if [ -z "$new_version" ]; then
    echo "❌ Version cannot be empty"
    exit 1
fi

# Update version in package.json
sed -i.bak "s/\"version\": \"$current_version\"/\"version\": \"$new_version\"/" frontend/package.json
rm frontend/package.json.bak

# Ask for release notes
echo "📝 Enter release notes (press Ctrl+D when done):"
release_notes=$(cat)

# Commit version change
git add frontend/package.json
git commit -m "🔖 Bump version to $new_version"

# Create and push tag
git tag -a "v$new_version" -m "$release_notes"
git push origin main
git push origin "v$new_version"

echo "✅ Release v$new_version created successfully!"
echo "🌐 Check GitHub for the new release: https://github.com/rxl895/watchlist-manager/releases"

# Optional: Create GitHub release using gh CLI if available
if command -v gh &> /dev/null; then
    echo "📦 Creating GitHub release..."
    echo "$release_notes" | gh release create "v$new_version" --title "Release v$new_version" --notes-file -
    echo "✅ GitHub release created!"
else
    echo "💡 Install GitHub CLI (gh) to automatically create GitHub releases"
fi
