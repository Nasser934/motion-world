# Codex image generation

Use when Codex CLI is installed and authenticated.

Example:

```bash
codex exec -C "$PROJECT" -s workspace-write --skip-git-repo-check \
  'Use the image generation tool ($imagegen) to generate the image described in prompts/scene-01.txt. Save it as assets/source-images/scene-01.png. Do not do anything else.'
```

Use one image model/source for a cohesive batch. Review each result before video generation.
