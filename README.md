# codeql-goose

> **Unofficial community project.** Not made, endorsed or supported by GitHub, the CodeQL team or the authors of Goose. It does not use CodeQL: it reads Goose source with a small lexer and reports through SARIF.

Goose here is the programming language at [aardappel/goose](https://github.com/aardappel/goose), not the Goose AI agent or the Goose database migration tool.

**Published on the GitHub Marketplace:** [Goose Analyzer for Code Scanning (unofficial)](https://github.com/marketplace/actions/goose-analyzer-for-code-scanning-unofficial).

Static checks for `*.goose` files that write [SARIF 2.1.0](https://docs.oasis-open.org/sarif/sarif/v2.1.0/sarif-v2.1.0.html), so results appear under Code scanning next to CodeQL.

CodeQL does not analyze Goose. This project fills that gap in a limited way.

## Rules

| Rule | Level | What it flags |
| --- | --- | --- |
| `unchecked-result` | warning | `read_file`, `write_file`, `write_file_atomic` or `env` called as a statement, so the returned `bool` is dropped |
| `read-outside-root` | warning | `read_file`, `write_file` or `write_file_atomic` on an absolute path or one containing `..` |
| `literal-secret` | error | a `password`, `secret`, `token` or `api_key` name assigned a non-empty string literal |

There is no Goose parser. A lexer skips comments and reads strings, so text inside either is never reported. Rules look at call shapes only, so expect misses (aliased functions, calls built at runtime) and some false positives. Text the lexer cannot read becomes a SARIF notification.

## Use it in a repository

Add a job that checks out your repository and runs the action, pinned to a full commit SHA:

```yaml
name: 🔬 Goose

on:
  push:
    branches: [main]
  pull_request:

permissions:
  contents: read

jobs:
  goose:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      security-events: write
    steps:
      - uses: actions/checkout@v7
        with:
          persist-credentials: false
      - uses: flisk-sh/codeql-goose@<full commit SHA>
```

Inputs:

- `patterns`: space-separated globs. Default `**/*.goose`.
- `category`: SARIF category in Code scanning. Default `/language:goose`.
- `fail-on-findings`: set to `"true"` to fail the step on any result. Default `"false"`, report only.

## Run it locally

```bash
python3 goose_analyze.py --root path/to/project --output codeql-goose.sarif
python3 -m unittest tests.test_rules -v
```

Python 3.9 or newer is enough. There are no dependencies.

## Status

Early. The rule set is small, each rule has tests, and the rules come from the standard library docs at [aardappel/goose](https://github.com/aardappel/goose). The action has not yet run from a caller on GitHub.

## License

MIT. See [LICENSE](LICENSE).
