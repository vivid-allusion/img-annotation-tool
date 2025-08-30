# TODO

## High Priority Tasks (Quick Wins - ~1 hour total)

### 1. Remove Unused Imports (2 minutes) ✅
- [x] Remove `from collections import defaultdict` from line 9 in src/main.py
- [x] Remove `from urllib.parse import quote, unquote` from line 10 in src/main.py

### 2. Extract Methods from `generate_markdown()` (30 minutes) ✅
- [x] Create `_generate_header()` method for metadata section
- [x] Create `_generate_shot_tables()` method for image table generation
- [x] Create `_generate_prompt_section()` method for prompt handling
- [x] Create `_generate_critique_section()` method for critique blocks
- [x] Define constants for HTML comment markers (REVIEW_START, REVIEW_END, etc.)

### 3. Create Configuration Management (20 minutes) ✅
- [x] Create config.py with GenerationConfig dataclass
- [x] Move hardcoded paths to configuration:
  - `USER-FILES/04.INPUT/04.1.IMAGE_URL`
  - `USER-FILES/04.INPUT/04.2.PROMPT`
  - `USER-FILES/05.OUTPUT/`
- [x] Make `max_cols = 3` configurable
- [x] Consider environment variables for override

## Medium Priority Tasks (~1 hour total)

### 4. Improve Error Handling (15 minutes) ✅
- [x] Replace generic `except Exception` with specific exceptions in `match_urls_across_folders()`
- [x] Add specific handling for IOError, ValueError, FileNotFoundError
- [x] Improve error messages with more context

### 5. Create Domain Models with Dataclasses (30 minutes) ✅
- [x] Create ShotData dataclass to replace Dict[str, Optional[str]]
- [x] Create GenerationConfig dataclass for configuration
- [x] Update type hints throughout the codebase
- [x] Consider creating URLFile and PromptFile models

### 6. Extract File Discovery Logic (20 minutes) ✅
- [x] Create FileDiscovery class for finding folders and files
- [x] Move `discover_url_folders()` to FileDiscovery
- [x] Move `discover_prompts()` to FileDiscovery
- [x] Add validation methods for paths

## Low Priority Tasks (~3 hours total)

### 7. Add Unit Tests (2 hours)
- [ ] Create test_file_discovery.py for folder/file discovery
- [ ] Create test_url_processing.py for URL cleaning and validation
- [ ] Create test_markdown_generation.py for markdown output
- [ ] Create test_matching.py for position-based file matching
- [ ] Add pytest configuration
- [ ] Set up coverage reporting

### 8. Performance Improvements (1 hour)
- [ ] Implement batch file reading for large datasets
- [ ] Consider async I/O for parallel file reading
- [ ] Profile memory usage with large datasets
- [ ] Optimize string building for very large documents

### 9. Logging Configuration (15 minutes)
- [ ] Create logging.yaml configuration file
- [ ] Add log rotation settings
- [ ] Configure different log levels for production/debug
- [ ] Add performance metrics logging

## Additional Refactoring Opportunities

### 10. Separate Concerns into Classes
- [ ] Create MarkdownGenerator class for all markdown operations
- [ ] Create URLProcessor class for URL cleaning and validation
- [ ] Create ImageAnnotationTool main orchestrator class

### 11. Code Quality Improvements
- [ ] Add docstrings to all functions
- [ ] Add inline comments for complex logic
- [ ] Consider adding pre-commit hooks for formatting
- [ ] Set up GitHub Actions for automated testing

### ⛔ STOP HERE ⛔

### DO NOT IMPLEMENT ANYTHING BELOW THIS LINE WITHOUT EXPLICIT USER REQUEST


