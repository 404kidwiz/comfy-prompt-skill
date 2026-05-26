#!/usr/bin/env bats
# Recipe smoke tests with --dry-run (no API calls).
#
# Requires: bats-core (install: brew install bats-core)
# Run: bats tests/test_recipes.bats

setup() {
    export SKILL_DIR="$HOME/.claude/skills/comfy-prompt"
    export COMFY_API_KEY="test-key-not-used-in-dry-run"
    cd "$SKILL_DIR"
}

@test "character-sheet --dry-run prints commands without executing" {
    run ./recipes/character-sheet.sh "test character" --dry-run --skip-on-fail
    [ "$status" -eq 0 ] || [ "$status" -eq 1 ]
    [[ "$output" == *"DRY-RUN"* ]]
    [[ "$output" != *"--api-key"* ]]   # don't leak in output
}

@test "storyboard-5shot --dry-run prints 5 steps" {
    run ./recipes/storyboard-5shot.sh "test subject" "test location" "test style" --dry-run --skip-on-fail
    [[ "$output" == *"DRY-RUN"* ]]
    [[ "$output" == *"Shot 1/5"* ]]
    [[ "$output" == *"Shot 5/5"* ]]
}

@test "product-lifestyle --dry-run prints 4 scenes" {
    run ./recipes/product-lifestyle.sh "test product" --dry-run --skip-on-fail
    [[ "$output" == *"DRY-RUN"* ]]
    [[ "$output" == *"scandi-morning"* ]] || [[ "$output" == *"Scene"* ]]
}

@test "product-3angle --dry-run prints 4 angles" {
    run ./recipes/product-3angle.sh "test product" --dry-run --skip-on-fail
    [[ "$output" == *"DRY-RUN"* ]]
    [[ "$output" == *"Hero front"* ]] || [[ "$output" == *"1/4"* ]]
}

@test "thumbnail-set --dry-run prints 4 thumbnails" {
    run ./recipes/thumbnail-set.sh "test topic" "test scene" --dry-run --skip-on-fail
    [[ "$output" == *"DRY-RUN"* ]]
    [[ "$output" == *"YouTube"* ]]
}

@test "mood-board --dry-run prints 9 tiles" {
    run ./recipes/mood-board.sh "test brief" --dry-run --skip-on-fail
    [[ "$output" == *"DRY-RUN"* ]]
    [[ "$output" == *"Tile 1/9"* ]]
    [[ "$output" == *"Tile 9/9"* ]]
}

@test "instagram-ad --dry-run prints pipeline steps" {
    run ./recipes/instagram-ad.sh "test product" "test bg" --dry-run --skip-on-fail
    [[ "$output" == *"DRY-RUN"* ]]
    [[ "$output" == *"Step 1/5"* ]]
}

@test "all recipes have --dry-run flag" {
    for f in recipes/*.sh; do
        [[ "$(basename "$f")" == "_runlib.sh" ]] && continue
        grep -q "dry-run" "$f" || { echo "missing dry-run in $f"; return 1; }
    done
}

@test "no recipe uses --aspect_ratio inline anymore" {
    # Search recipes for hardcoded --aspect_ratio (should all use AF helper now)
    run grep -rn "aspect_ratio" recipes/
    [ -z "$output" ] || [ "$status" -eq 1 ]   # grep returns 1 when no match
}
