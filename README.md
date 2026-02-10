# ACME Cloud Docs (Sample Documentation Site)

This repository contains a **sample MkDocs documentation site** for a fictional product called **ACME Cloud**.

The site exists primarily as a **demo and testing environment** for:
- Docs-as-code workflows
- Vale style linting
- AI-assisted documentation tooling (for example, the AI Vale Workflow)

It is **not** intended to represent a complete or production-ready product.

---

## What this repo is for

This repository is designed to help users:

- Run a real MkDocs site locally
- Test Vale against realistic Markdown content
- Experiment safely with automated and AI-assisted documentation workflows
- See how style rules surface issues in real documentation

It is commonly used alongside the **AI Vale Workflow** demo.

---

## Repository structure

```
.
├── README.md           # Repo overview (this file)
├── mkdocs.yml          # MkDocs configuration
├── docs/               # Documentation content
│   ├── index.md
│   ├── concepts/
│   ├── product/
│   ├── tasks/
│   ├── references/
│   ├── images/
│   │   ├── acme-homepage.png
│   │   └── api-references.png
│   └── scripts/
│       └── ai_vale_workflow.py
├── .vale.ini           # Vale configuration
├── styles/             # Vale rule styles (for example, Microsoft)
└── scripts/            # Helper scripts (if any)
```

> The documentation content intentionally contains style issues so Vale and AI tools have something to flag and fix.

---

## Prerequisites

You’ll need the following tools to use this repo end-to-end:

- **Git**
- **Python 3.9+** and `pip`
- **MkDocs**
- **Vale CLI** (recommended)

---

## Install prerequisites

### Install Git

**macOS**
```bash
xcode-select --install
```
or
```bash
brew install git
```

**Linux (Debian/Ubuntu)**
```bash
sudo apt-get update
sudo apt-get install -y git
```

**Windows**
Install Git for Windows and verify:
```bash
git --version
```

---

### Install Python

**macOS**
```bash
brew install python
```

**Linux**
```bash
sudo apt-get install -y python3 python3-pip python3-venv
```

**Windows**
Install Python 3 and ensure it is added to PATH:
```bash
python --version
pip --version
```

---

### Install MkDocs

```bash
pip install mkdocs
mkdocs --version
```

---

### Install Vale

**macOS**
```bash
brew install vale
```

**Linux**
```bash
wget https://github.com/errata-ai/vale/releases/latest/download/vale_Linux_64-bit.tar.gz
tar -xvzf vale_Linux_64-bit.tar.gz
sudo mv vale /usr/local/bin/
```

**Windows**
Download `vale.exe` from the Vale GitHub releases page and add it to your PATH.

Verify:
```bash
vale --version
```

---

## Clone the repository

```bash
git clone https://github.com/wordsnlogic/demo-documentation-website.git
cd demo-documentation-website
```

---

## Set up a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

**Windows PowerShell**
```powershell
.\.venv\Scripts\Activate.ps1
```

---

## Run the site locally

```bash
mkdocs serve
```

Open your browser to:

```
http://127.0.0.1:8000/
```

---

## Site preview

Below are screenshots of the ACME Cloud documentation site rendered locally using MkDocs.

### Home page

![ACME Cloud documentation home page](https://raw.githubusercontent.com/wordsnlogic/demo-documentation-website/main/docs/images/acme-homepage.png)

### API reference

![ACME Cloud API reference](https://raw.githubusercontent.com/wordsnlogic/demo-documentation-website/main/docs/images/api-references.png)

---

## Using Vale with this repo

Run Vale against the documentation:

```bash
vale docs/
```

Style issues are expected and intentional.

---

## Using this repo with the AI Vale Workflow

1. Run the MkDocs site locally
2. Run Vale to surface issues
3. Run the AI Vale Workflow against `docs/`
4. Review and approve changes
5. Re-run Vale to confirm fixes

Refer to the AI Vale Workflow README for detailed instructions.

---

## Important notes

- This is a **demo repository**
- Content is intentionally imperfect
- ACME Cloud is fictional
- The goal is education and experimentation

---

## License

Add your preferred license here.
