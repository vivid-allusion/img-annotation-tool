# TODO

## Setup Tasks
- [x] Create src/ directory structure
- [x] Create requirements.txt with dependencies (natsort, loguru)
- [x] Create main.py file with proper imports and type hints

## Core Discovery Functions
- [x] Implement `discover_image_folders()` to find subdirectories in USER-FILES/04.INPUT/04.1.IMAGE_URL
- [x] Implement `discover_prompts()` to find .txt files in USER-FILES/04.INPUT/04.2.PROMPT
- [x] Add natural sorting to both discovery functions using natsort

## Image Matching Logic
- [x] Implement `match_images_across_folders()` to group images by filename
- [x] Handle mismatched images gracefully (log warnings, continue)
- [x] Support image formats: .jpg, .jpeg, .png, .webp

## Markdown Generation
- [x] Implement `generate_markdown_header()` with timestamp and metadata
- [x] Implement `generate_table_row()` with dynamic column support (1 to N folders)
- [x] Implement `generate_prompt_section()` with HTML comment markers
- [x] Implement `generate_critique_section()` with placeholder text
- [x] Combine all sections in `generate_markdown()` main function

## Output Management
- [x] Create timestamped output directory (YYMMDD_HHMMSS format)
- [x] Generate output filename: Image_Review_{YYMMDD_HHMMSS}.md
- [x] Write markdown content to output file
- [x] Ensure USER-FILES/05.OUTPUT path exists

## Error Handling
- [x] Add validation for missing image folders (exit with clear message)
- [x] Add validation for missing prompt files (exit with clear message)
- [x] Implement proper exit codes (0 for success, 1 for error)
- [x] Add loguru logging for all major steps

## Main Orchestration
- [x] Implement `main()` function to orchestrate entire process
- [x] Add proper error handling with try/except blocks
- [x] Log success message with output file path
- [x] Ensure script runs with `python3 -m src.main`

## Testing & Verification
- [x] Test with 1 image folder (single column layout)
- [x] Test with 2 image folders (two column layout)
- [x] Test with 3+ image folders (multi-column layout)
- [x] Verify HTML comment markers are correctly placed
- [x] Verify natural sorting works correctly
- [x] Test error messages for missing inputs
- [x] Ensure output matches few_shot examples in format







### ⛔ STOP HERE ⛔

### DO NOT IMPLEMENT ANYTHING BELOW THIS LINE WITHOUT EXPLICIT USER REQUEST


