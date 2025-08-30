# Codebase Cleanup Report

## Executive Summary
The codebase contains 9 completely empty files and 1 directory that should be deleted. Following your code manifesto of "minimalism above all" and "the best code is no code", these files serve no purpose and add unnecessary clutter.

## Files to Delete (Entire Files)

### 1. Empty Documentation Files
**DELETE ENTIRELY:**
- `./README.md` - Empty file (0 bytes)
- `./docs/README.md` - Empty file (0 bytes)
- `./docs/api.md` - Empty file (0 bytes)
- `./docs/user_guide.md` - Empty file (0 bytes)

**Justification:** Per manifesto: "No README files unless asked" and "Create docs only when explicitly requested"

### 2. Empty Configuration Files
**DELETE ENTIRELY:**
- `./.pre-commit-config.yaml` - Empty file (0 bytes)
- `./pyproject.toml` - Empty file (0 bytes)
- `./requirements-dev.txt` - Empty file (0 bytes)

**Justification:** Unused configuration adds confusion. Keep only what's actively used.

### 3. Empty Python Files
**DELETE ENTIRELY:**
- `./src/__init__.py` - Empty file (0 bytes)
- `./tests/__init__.py` - Empty file (0 bytes)

**Justification:** Not needed for Python 3.3+ with namespace packages. The tool works without them.

### 4. Entire Directories to Remove
**DELETE ENTIRELY:**
- `./docs/` - Contains only empty files
- `./tests/` - Contains only empty __init__.py

**Justification:** Empty test directory suggests "just in case" thinking. Per manifesto: "Resist the urge to add 'just in case' features"

### 5. Generated Directories
**DELETE ENTIRELY:**
- `./src/__pycache__/` - Python bytecode cache

**Justification:** Should be in .gitignore, not tracked

## Files to Clean (Partial)

### TODO.md
**Current Issues:**
- Lines 46-78: Low priority tasks that violate "STOP HERE" directive
- Lines contain completed tasks marked with ✅

**Recommended Cleanup:**
- Remove all completed tasks (lines 5-43)
- Remove all low priority tasks below "STOP HERE" (lines 46-78)
- Keep only the boundary marker

### CLAUDE.md
**Current Issues:**
- Contains many rules that duplicate the manifesto
- Overly verbose for a personal tool

**Recommended Cleanup:**
- Could be reduced to just reference the manifesto files
- Or delete entirely since manifesto files exist

## USER-FILES Directory Notes

**IMPORTANT: NO ACTION REQUIRED IN USER-FILES/**

The USER-FILES directory contains:
- Input files that must remain untouched
- Output files that are user data
- Configuration templates that may be needed
- Knowledge base files that document the project

Per your instructions, these files should NEVER be moved or deleted programmatically.

## Dead Code Analysis

### src/main.py
**No dead code found** - All 175 lines are actively used. The lean refactor was successful.

**No issues found:**
- No unused imports
- No unused variables
- No unreachable code
- No debug print statements
- No duplicate code

## Summary of Recommended Deletions

### Immediate Deletions (Safe)
```bash
# Delete empty documentation
rm -rf docs/
rm README.md

# Delete empty config files
rm .pre-commit-config.yaml
rm pyproject.toml
rm requirements-dev.txt

# Delete empty Python files
rm src/__init__.py
rm -rf tests/

# Delete Python cache
rm -rf src/__pycache__/
```

### Files to Edit
- `TODO.md` - Remove completed tasks and everything below "STOP HERE"
- `CLAUDE.md` - Consider removing or reducing to one-liner

## Impact Analysis

**Before Cleanup:**
- 12 files in project root and subdirectories (excluding USER-FILES)
- 9 completely empty files
- 2 directories with only empty files

**After Cleanup:**
- 4 files: `src/main.py`, `requirements.txt`, `TODO.md`, `CLAUDE.md`
- 1 directory: `src/`
- 75% reduction in file count
- 100% functional code preserved

## Cleanup Command

Execute this to clean everything at once:
```bash
rm -rf docs/ tests/ src/__pycache__/ src/__init__.py && \
rm README.md .pre-commit-config.yaml pyproject.toml requirements-dev.txt
```

## Conclusion

This cleanup removes all "just in case" files, empty documentation, and unused configuration. The result is a minimal codebase that follows your manifesto: one tool (main.py), one purpose (image annotation), no fluff.

The codebase will be reduced to its essential components:
- The actual tool (`src/main.py`)
- Its dependencies (`requirements.txt`)
- Development notes (`TODO.md`, `CLAUDE.md`)

This achieves maximum minimalism while preserving all functionality.