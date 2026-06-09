# AI Image Generation Annotation Tool

Generates an Image Review markdown document for AI image generation annotation. Reads image URLs and prompts from structured input directories and produces a formatted review document with 2-column tables, per-shot prompts, and blank critique blocks for human annotators.

## Overview

This tool processes image URLs stored in subdirectories under `04.1.IMAGE_URL/` and matching prompts from `04.2.PROMPT/`, producing a single markdown review document. Each URL file is validated to ensure it points to an allowed image format (`.jpg`, `.jpeg`, `.png`). URLs that fail validation are replaced with `[No image]` placeholders.

## Features

- **Multi-Folder URL Input**: Reads `.txt` URL files from subdirectories inside `04.1.IMAGE_URL/`, matching files by position across folders
- **URL Validation**: Rejects URLs that don't end in `.jpg`, `.jpeg`, or `.png` or don't start with `http`
- **2-Column Table Layout**: Generates image tables with two columns per row, supporting any number of folder columns
- **HTML Markers**: Inserts `<!--- REVIEW_START -->`, `<!--- PROMPT_START/END -->`, `<!--- USER_START/END -->`, and `<!--- REVIEW_END -->` markers for downstream tooling
- **Critique Section**: Each shot includes a blank `<!--- USER_START --> ... <!--- USER_END -->` block for human annotation
- **Prompt Embedding**: Embeds the corresponding prompt text from `04.2.PROMPT/` in a fenced code block
- **Timestamped Output**: Output directory uses `{timestamp}_IMG-ANNOTATION` format

## Input Structure

```
USER-FILES/04.INPUT/
├── 04.1.IMAGE_URL/
│   ├── folder_a/          # Each subfolder contains .txt files with image URLs
│   │   ├── 01.txt         # URL content: https://example.com/image1.jpg
│   │   ├── 02.txt
│   │   └── ...
│   ├── folder_b/
│   │   ├── 01.txt
│   │   ├── 02.txt
│   │   └── ...
│   └── ...
└── 04.2.PROMPT/
    ├── 01.txt             # Text content: the prompt for shot 1
    ├── 02.txt             # Text content: the prompt for shot 2
    └── ...
```

- **URL files**: `.txt` files containing a single image URL. Only URLs ending in `.jpg`, `.jpeg`, or `.png` are accepted.
- **Prompt files**: `.txt` files containing the image generation prompt text for each shot.

## URL Validation

The tool validates each URL with two checks:
1. Must start with `http`
2. Must end with `.jpg`, `.jpeg`, or `.png` (case-insensitive)

Invalid URLs are replaced with `[No image]` in the output table, and the filename is set to `[No file]`.

## Output Format

```
USER-FILES/05.OUTPUT/{timestamp}_IMG-ANNOTATION/
└── Image_Review_{timestamp}.md
```

The generated markdown document has the following structure:

- **Header metadata**: `REVIEW_START` marker, title, generation timestamp, column descriptions, total image count
- **Shot sections**: Each `## Shot N` contains:
  - **Image table**: 2-column rows with image markdown and file headers, each column representing one folder
  - **Prompt block**: `PROMPT_START/END` markers surrounding the prompt text in a fenced code block
  - **Critique block**: `USER_START/END` markers surrounding a blank code block for human annotators
- **Footer**: `REVIEW_END` marker

## HTML Markers

These markers are used by downstream tools for parsing the generated document:

| Marker | Purpose |
|--------|---------|
| `<!--- REVIEW_START -->` | Marks the beginning of the review document |
| `<!--- PROMPT_START -->` | Precedes each shot's prompt section |
| `<!--- PROMPT_END -->` | Closes each shot's prompt section |
| `<!--- USER_START -->` | Opens the blank critique block for human annotation |
| `<!--- USER_END -->` | Closes the critique block |
| `<!--- REVIEW_END -->` | Marks the end of the review document |
| `<!--- TOTAL_IMAGES: N -->` | Embedded total image count |

## Installation

```bash
# Navigate to project directory
cd img-annotation-tool

# Create virtual environment
python3 -m venv .venv

# Install dependencies
pip install -r requirements.txt
```

## Usage

1. **Organize input files** in `USER-FILES/04.INPUT/`:
   - Place URL `.txt` files in subdirectories under `04.1.IMAGE_URL/`
   - Place prompt `.txt` files in `04.2.PROMPT/`

2. **Run the tool**:
   ```bash
   python run.py
   ```

3. **Find the output** in `USER-FILES/05.OUTPUT/{timestamp}_IMG-ANNOTATION/Image_Review_{timestamp}.md`

## Project Structure

```
img-annotation-tool/
├── src/
│   └── main.py              # Main tool implementation (178 lines)
├── USER-FILES/
│   ├── 04.INPUT/
│   │   ├── 04.1.IMAGE_URL/  # Subdirectories of .txt URL files
│   │   └── 04.2.PROMPT/     # .txt prompt files
│   └── 05.OUTPUT/           # Timestamped review documents
├── run.py                    # Bootstrap script (creates venv, installs deps, runs)
└── requirements.txt          # Dependencies
```

## Dependencies

- `natsort==8.4.0` — Natural file sorting for deterministic ordering
- `loguru==0.7.2` — Structured console logging

## Exit Codes

- **0**: Success — review document generated
- **1**: Error — missing directories, no folders, no prompts, or write failure

## Example Output Structure

```
<!--- REVIEW_START -->
# Image Review 251005
---
- **Generated:** 251005_110257
- **Column 1:** [Generation notes]
- **Column 2:** [Generation notes]
- **Total Images:** 24
<!--- TOTAL_IMAGES: 24 -->
---

## Shot 1

| folder_a/01.jpeg | folder_b/01.jpeg |
| ----------------------------------------------------------- | ----------------------------------------------------------- |
| ![image](https://example.com/image1.jpg) | ![image](https://example.com/image2.jpg) |

<!--- PROMPT_START -->
**01.txt:**
```text
A serene landscape with mountains and a lake at sunset, photorealistic
```
<!--- PROMPT_END -->

<!--- USER_START -->
**User:**
```text

```
<!--- USER_END -->
---

...

<!--- REVIEW_END -->
```

## Limitations

- Requires subdirectory structure under `04.1.IMAGE_URL/` (no flat file mode)
- Only `.jpg`, `.jpeg`, `.png` URLs are accepted
- No critique section for video prompts (see video-annotation-tool for that workflow)
- No configuration file — all paths hardcoded
