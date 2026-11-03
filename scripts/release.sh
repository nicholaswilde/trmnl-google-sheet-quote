#!/usr/bin/env bash
set -e

# Pull latest changes and tags
echo "Fetching latest tags and commits from origin..."
git fetch --tags origin
git pull --rebase origin main

# Extract base version
ACTION="${1:-}"
LATEST_TAG=$(git tag --sort=-v:refname | head -n 1)
CURRENT_VER=$(node -p "require('./package.json').version")

if [ -n "$LATEST_TAG" ]; then
    BASE_VER="${LATEST_TAG#v}"
else
    BASE_VER="$CURRENT_VER"
fi

IFS='.' read -ra VER_PARTS <<< "$BASE_VER"
MAJOR=${VER_PARTS[0]:-0}
MINOR=${VER_PARTS[1]:-0}
PATCH=${VER_PARTS[2]:-0}

if [ -z "$ACTION" ]; then
    NEW_VER="${MAJOR}.${MINOR}.$((PATCH + 1))"
else
    case "$ACTION" in
        major)
            NEW_VER="$((MAJOR + 1)).0.0"
            ;;
        minor)
            NEW_VER="${MAJOR}.$((MINOR + 1)).0"
            ;;
        patch)
            NEW_VER="${MAJOR}.${MINOR}.$((PATCH + 1))"
            ;;
        v*)
            NEW_VER="${ACTION#v}"
            ;;
        [0-9]*)
            NEW_VER="$ACTION"
            ;;
        *)
            echo "Unknown release action: $ACTION. Use: patch, minor, major, or explicit version (e.g. 1.2.0)"
            exit 1
            ;;
    esac
fi
NEW_TAG="v$NEW_VER"

if git rev-parse "$NEW_TAG" >/dev/null 2>&1; then
    echo "Error: Git tag $NEW_TAG already exists."
    exit 1
fi

echo "Current version: ${LATEST_TAG:-none (package.json: $CURRENT_VER)}"
echo "Target version:  $NEW_TAG"

echo "Running pre-release validation (lint & test)..."
task lint
task test

if [ "$CURRENT_VER" != "$NEW_VER" ]; then
    echo "Validation passed. Bumping version in package.json and package-lock.json..."
    npm version "$NEW_VER" --no-git-tag-version

    echo "Checking git status..."
    if [ -z "$(git status --porcelain package.json)" ]; then
        echo "Error: package.json was not modified."
        exit 1
    fi

    git add package.json package-lock.json
    git commit -m "chore(release): bump version to $NEW_TAG"
else
    echo "Validation passed. package.json already matches target version $NEW_VER."
fi

if [ -n "$(git status --porcelain --untracked-files=no)" ]; then
    echo "Error: Working directory not clean after bumping version."
    exit 1
fi

echo "Tagging release..."
git tag -a "$NEW_TAG" -m "Release $NEW_TAG"

echo "Pushing atomically..."
git push --atomic origin main "$NEW_TAG"

echo "Release $NEW_TAG published successfully! Now run 'task release:summary' to generate release notes."
