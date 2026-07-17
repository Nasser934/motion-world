# Security policy

## Reporting

Do not open a public issue for a credential leak or a vulnerability that exposes private media. Contact the repository owner privately through GitHub.

## Secrets

Motion World does not need to store provider credentials. Keep authentication in the provider CLI, environment, operating-system keychain, or a local wrapper.

Never commit:

- API keys or access tokens.
- Signed download URLs.
- Private start/end images.
- Provider JSON responses containing account data.
- `.env` files.

## Generated media

Review generated images and video before publication. Confirm that you have rights to use source media, brand assets, likenesses, audio, and provider outputs.
