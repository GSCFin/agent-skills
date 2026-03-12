#!/bin/bash
# sync_recommended_skills.sh
# Syncs only the recommended skills from the repository to a target library folder.

set -e

# Detect Repository Root (one level up from scripts/)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

# Default Paths (Overrideable via environment variables)
# SOURCE_REPO: Where the skills come from
# TARGET_LIBRARY: Where the skills are synced to
SOURCE_REPO="${SOURCE_REPO:-$REPO_ROOT/skills}"
TARGET_LIBRARY="${TARGET_LIBRARY:-$HOME/.agent/skills}"

DRY_RUN=false

# Simple CLI Argument Parsing
for arg in "$@"; do
    case $arg in
        --dry-run)
            DRY_RUN=true
            shift
            ;;
        --help)
            echo "Usage: $0 [--dry-run]"
            echo "Environment variables:"
            echo "  SOURCE_REPO: Currently $SOURCE_REPO"
            echo "  TARGET_LIBRARY: Currently $TARGET_LIBRARY"
            exit 0
            ;;
    esac
done

# 35 Recommended Skills
RECOMMENDED_SKILLS=(
    # Tier S - Core Development (13)
    "systematic-debugging"
    "test-driven-development"
    "writing-skills"
    "doc-coauthoring"
    "planning-with-files"
    "concise-planning"
    "software-architecture"
    "senior-architect"
    "senior-fullstack"
    "verification-before-completion"
    "git-pushing"
    "address-github-comments"
    "javascript-mastery"
    
    # Tier A - Your Projects (12)
    "docx-official"
    "pdf-official"
    "pptx-official"
    "xlsx-official"
    "react-best-practices"
    "web-design-guidelines"
    "frontend-dev-guidelines"
    "webapp-testing"
    "playwright-skill"
    "mcp-builder"
    "notebooklm"
    "ui-ux-pro-max"
    
    # Marketing & SEO (1)
    "content-creator"
    
    # Corporate (4)
    "brand-guidelines-anthropic"
    "brand-guidelines-community"
    "internal-comms-anthropic"
    "internal-comms-community"
    
    # Planning & Documentation (1)
    "writing-plans"
    
    # AI & Automation (5)
    "workflow-automation"
    "llm-app-patterns"
    "autonomous-agent-patterns"
    "prompt-library"
    "github-workflow-automation"
)

echo "🔄 Sync Recommended Skills"
if [ "$DRY_RUN" = true ]; then echo "🧪 [DRY RUN] No changes will be made"; fi
echo "========================="
echo ""
echo "📍 Source: $SOURCE_REPO"
echo "📍 Target: $TARGET_LIBRARY"
echo "📊 Skills to sync: ${#RECOMMENDED_SKILLS[@]}"
echo ""

# Validation
if [ ! -d "$SOURCE_REPO" ]; then
    echo "❌ Error: Source directory does not exist: $SOURCE_REPO"
    exit 1
fi

if [ "$DRY_RUN" = false ]; then
    mkdir -p "$TARGET_LIBRARY"
    BACKUP_DIR="${TARGET_LIBRARY}_backup_$(date +%Y%m%d_%H%M%S)"
    
    # Create backup
    if [ -d "$TARGET_LIBRARY" ] && [ "$(ls -A "$TARGET_LIBRARY")" ]; then
        echo "📦 Creating backup at: $BACKUP_DIR"
        cp -r "$TARGET_LIBRARY" "$BACKUP_DIR"
        echo "✅ Backup created"
    fi
    echo ""

    # Clear target library (keep hidden files/dirs if any)
    echo "🗑️  Clearing target library..."
    find "$TARGET_LIBRARY" -maxdepth 1 -mindepth 1 -type d ! -name ".*" -exec rm -rf {} +
    echo "✅ Target library cleared"
    echo ""
fi

# Copy recommended skills
echo "📋 Syncing recommended skills..."
SUCCESS_COUNT=0
MISSING_COUNT=0

for skill in "${RECOMMENDED_SKILLS[@]}"; do
    if [ -d "$SOURCE_REPO/$skill" ]; then
        if [ "$DRY_RUN" = true ]; then
            echo "  [SKIP] Would copy: $skill"
        else
            cp -r "$SOURCE_REPO/$skill" "$TARGET_LIBRARY/"
            echo "  ✅ $skill"
        fi
        ((SUCCESS_COUNT++))
    else
        echo "  ⚠️  $skill (not found in source)"
        ((MISSING_COUNT++))
    fi
done

echo ""
echo "📊 Summary"
echo "=========="
echo "✅ Processed: $SUCCESS_COUNT skills"
echo "⚠️  Missing: $MISSING_COUNT skills"

if [ "$DRY_RUN" = true ]; then
    echo "🧪 Dry run complete. No files were modified."
else
    FINAL_COUNT=$(find "$TARGET_LIBRARY" -maxdepth 1 -type d ! -name ".*" ! -name "$(basename "$TARGET_LIBRARY")" | wc -l | tr -d ' ')
    echo "🎯 Final count in target library: $FINAL_COUNT skills"
    echo "📦 Backup: $BACKUP_DIR"
    echo ""
    echo "Done! Target library updated."
fi
