# Copilot instructions — Python mini-projects workspace

Purpose: brief, actionable guidance for AI coding agents working in this repository.

- Workspace shape: many small, standalone Python projects grouped by topic.
  - Key folders: [money](money), [simpleGames](simpleGames), [simpleMath](simpleMath), [passwordMakerChecker](passwordMakerChecker), [textInterect](textInterect), [validacao](validacao)

- Big picture:
  - Each directory contains one or a few single-file scripts (small CLI programs or exercises).
  - Design intent is educational / utility scripts (no web services, no background daemons).
  - Typical data flow: user input → script logic → stdout or simple file I/O (see [textInterect/parquivo.txt](textInterect/parquivo.txt)).

- Project-specific conventions and patterns:
  - Filenames and identifiers often use Portuguese (e.g., hangMan.py uses Portuguese prompts). Preserve original language and user-facing strings unless the user requests translation.
  - Keep changes minimal and local: prefer editing the specific script requested rather than broad refactors across folders.
  - No virtualenv/requirements present by default; assume standard library unless a `requirements.txt` is added.
  - Prefer using `print()` and simple CLI `input()` flows to maintain pedagogical style.

- How to run and debug (examples):
  - Run a script from workspace root:
    ```bash
    python simpleGames/hangMan.py
    ```
  - If adding third-party libs, update `requirements.txt` at workspace root and instruct the user to `pip install -r requirements.txt`.
  - For VS Code debugging: open the target file (example: [simpleGames/hangMan.py](simpleGames/hangMan.py)) and launch the Python debug session for the current file.

- Integration and external deps:
  - Currently there are no external service integrations or third-party dependencies detectable in the codebase.
  - If introducing new packages, keep them minimal and document them in `requirements.txt`.

- When proposing changes:
  - Explain user-visible changes clearly (translations, CLI behavior changes, new files).
  - Avoid renaming many files or moving code between modules without explicit user approval.
  - If adding tests or CI, propose a small incremental change: add `tests/` with one or two pytest cases and a minimal `requirements-dev.txt`.

- Quick file examples to inspect before edits:
  - [simpleGames/hangMan.py](simpleGames/hangMan.py)
  - [money/monetario.py](money/monetario.py)
  - [passwordMakerChecker/passwordEncrypt.py](passwordMakerChecker/passwordEncrypt.py)
  - [simpleMath/fatorial.py](simpleMath/fatorial.py)

If anything is unclear or you want the agent to follow a stricter standard (type hints, tests, translations), tell me which direction and I will update this file.
