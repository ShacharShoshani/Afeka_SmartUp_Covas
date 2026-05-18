# Covas 🎭

[![CI](https://github.com/your-username/covas/actions/workflows/ci.yml/badge.svg)](https://github.com/your-username/covas/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)

**Covas** is a lightweight CLI tool to manage multiple **Claude Code** environments and profiles seamlessly. 

Instead of manually editing configuration files when switching contexts (e.g., from DevOps to Frontend), Covas swaps your active profile using symbolic links and automated secret injection.

---

## ✨ Features

- **🚀 Fast Profile Switching:** Swap roles in a single command.
- **🔗 Smart Symlinking:** Updates your `~/.claude` directory using symbolic links (with copy fallbacks for Windows).
- **🔒 Secret Injection:** Securely injects tokens into `mcp.json` from a private `.env` file outside your repository.
- **🔍 Environment Inspection:** Quickly verify which links are active and which secrets are missing.
- **🛠️ Extensible:** Easy to add new profiles and MCP configurations.

---

## 📂 Project Structure

```text
covas/
├── covas/              # Core logic
│   ├── cli.py          # Click CLI entry point
│   ├── manager.py      # Profile & symlink management
│   ├── state.py        # Persistence for active profile
│   └── constants.py    # Shared paths and configuration
├── profiles/           # Profile templates
│   ├── devops/
│   │   ├── CLAUDE.md
│   │   ├── mcp.json    # Supports ${SECRET_NAME} placeholders
│   │   └── skills/
│   └── ...
├── tests/              # Pytest suite
└── README.md
```

---

## 🚀 Getting Started

### 1. Installation

```bash
# Clone the repository
git clone https://github.com/your-username/covas.git
cd covas

# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install in editable mode
pip install -e .
```

### 2. Initialization

Setup the required directories (`~/.claude` and `~/.covas`):

```bash
covas init
```

### 3. Setup Secrets

Add your sensitive tokens to `~/.covas/donttell.env`:

```env
AWS_TOKEN=your_secret_aws_token
FIGMA_TOKEN=your_figma_token
```

*Note: Profiles use `${VARIABLE_NAME}` in their `mcp.json` templates to reference these secrets.*

---

## 🛠️ Usage

### Switch Profile
```bash
covas switch devops
```

### Check Status
```bash
covas status
```

### Inspect Environment
Verify links and secret coverage:
```bash
covas inspect
```

---

## 🧪 Testing

Install test dependencies and run the suite:

```bash
pip install -e ".[test]"
pytest
```

---

## 🤝 Contributing

1. Fork the repository.
2. Create a feature branch (`git checkout -b feature/cool-thing`).
3. Commit your changes.
4. Push to the branch.
5. Open a Pull Request.

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
