# State

- **Question**: When apply runs, how does your tool decide what to write, what to remove, and what to leave alone?

First, our app checks whether the requested profile exists in the profiles folder. If `apply` is called for the first time, Covas will create Claude's home directory.

Covas then iterates over a fixed list of files in the chosen profile folder: `CLAUDE.md`, `skills`, and `mcp.json`. For the first two, it creates symlinks at the target locations. The `mcp.json` file is copied and then injected with secrets sourced from our dedicated environment file.

# Switching cleanly

- **Question**: How do you make sure switching profiles doesn't leave files from the old one behind? What's your strategy and what could go wrong with it?

When switching profiles, any files or symlinks previously placed at the managed locations are overwritten by the incoming profile's equivalents. A potential issue arises when Covas is adopted by a user who already has existing Claude Code configuration at those locations — their original files would be silently replaced without a backup.

# Secrets

- **Question**: Where do API tokens live, and why is that location safer than putting them in the profile file?

API tokens are stored in a `donttell.env` file inside our app's home directory. Keeping secrets there, rather than inside a profile file, reduces the risk of them being accidentally committed to version control.

# One thing you'd do differently with more time

I would have added an import flow that converts a user's pre-existing, manually configured Claude Code setup into a valid Covas profile. This would make onboarding smoother for users who already have an established configuration.
