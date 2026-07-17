# Provider contract

The skill separates orchestration from provider details.

## Image provider result

Every image provider must return or produce:

```json
{
  "id": "scene-01-start",
  "localPath": "assets/source-images/scene-01-start.png",
  "width": 1024,
  "height": 1536,
  "sha256": "...",
  "provider": "chatgpt_image_gen",
  "promptFile": "prompts/scene-01-start.txt"
}
```

## Video provider request

```json
{
  "id": "scene-01-motion",
  "provider": "higgsfield_cli",
  "model": "seedance_2_0",
  "startImage": "assets/source-images/scene-01-start.png",
  "endImage": null,
  "referenceImages": [],
  "promptFile": "prompts/scene-01-motion.txt",
  "aspectRatio": "9:16",
  "durationSeconds": 8,
  "output": "provider-output/scene-01.mp4"
}
```

## Video provider result

```json
{
  "id": "scene-01-motion",
  "status": "completed",
  "localPath": "provider-output/scene-01.mp4",
  "providerJobId": "optional",
  "model": "seedance_2_0",
  "width": 1080,
  "height": 1920,
  "durationSeconds": 8.0,
  "sha256": "..."
}
```

## Adapter types

### higgsfield_cli

The runner builds a CLI command from a provider template. The selected model schema must be checked
before using optional parameters. Authentication remains the user's responsibility.

### generic_shell

The project provides a command template. Tokens may include:

- `{prompt_file}`
- `{start_image}`
- `{end_image}`
- `{output}`
- `{aspect_ratio}`
- `{duration}`
- `{model}`

### generic_http

The runner can create a request plan but deliberately does not guess one provider's authentication,
upload, polling, or response schema. Supply explicit endpoint, headers through environment-variable
names, JSON body mapping, job-id JSON path, polling endpoint, result URL path, and download target.

### manual

The runner writes an instruction bundle. The user uploads source images to any service and places the
returned video at the requested path. The rest of the pipeline remains automatic.
