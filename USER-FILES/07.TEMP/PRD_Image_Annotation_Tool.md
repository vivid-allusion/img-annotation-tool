# PRD - AI Image Generation Annotation Tool

## 01. Project Definition

### 01.1 Project Description

A Python script that generates markdown files for annotating AI-generated images by creating side-by-side comparisons with prompts, supporting multiple image folders from different AI models.

### 01.2 Core Features

- Discover image folders in `USER-FILES/04.INPUT/04.1.IMAGE_URL`
- Read prompts from `USER-FILES/04.INPUT/04.2.PROMPT/`
- Generate markdown with dynamic column layout (1-3+ columns based on folders)
- Create timestamped output in `USER-FILES/05.OUTPUT/`
- Include HTML comment markers for programmatic parsing
- Match images across folders by filename for side-by-side comparison

### 01.3 Specific Requirements

- Support 1 to N image folders (dynamically adapt table columns)
- Use natural sorting for consistent image ordering
- Preserve folder names as column headers
- Include prompt text for each image set
- Add critique sections with placeholder text
- Generate parseable HTML comments for automation
- Fill timestamp and image count automatically

### 01.4 Project Context

**Option A: Personal Tool (LLM-Operated)**

- **Users**: Just me (developer/owner)
- **Operation**: Claude Code or other LLM operates on my behalf
- **Documentation**: LLM-readable (clear docstrings and comments)
- **Testing**: Manual verification only, no automated test suite
- **CI/CD**: Not needed (no team, no external deployment)
- **Simplification Impact**:
  - No user documentation needed
  - No automated testing framework
  - No release management
  - No external integrations
  - Focus on core functionality only

### 01.5 Error Handling Strategy

- **No image folders**: Exit with clear message "No image folders found in USER-FILES/04.INPUT/04.1.IMAGE_URL"
- **No prompt files**: Exit with clear message "No prompt files found in USER-FILES/04.INPUT/04.2.PROMPT"
- **Mismatched images**: Log warning, continue with available images
- **Output exists**: Create new timestamped folder (never overwrite)
- **Missing images**: Skip that row, log in summary

---

## 02. Minimalist Architecture Philosophy

### Core Principles

**Simplicity First**

- One script, one purpose: generate annotation markdown
- No configuration files needed
- No user interaction required
- Deterministic output based on input structure
- Under 250 lines total

### Python Implementation Standards

**Code Structure**

- Single `main.py` file
- Type hints for all functions
- pathlib.Path for all file operations
- Functions under 50 lines each
- Natural sorting with natsort

**Error Handling**

- Fail fast with clear messages
- No silent failures
- Exit codes: 0 (success), 1 (error)
- Use loguru for structured logging

**Dependencies**

- pathlib (standard library)
- datetime (standard library)
- natsort (for natural sorting)
- loguru (for logging)

**File Processing**

- Read-only from USER-FILES/04.INPUT
- Write-only to USER-FILES/05.OUTPUT
- Never modify input files
- Process all images in memory

---

## 03. Dependencies

### Folder Structure

```plaintext
annotation_tool/
├── src/
│   └── main.py                # Single script file
├── requirements.txt            # Python dependencies
├── .env.example               # Not needed for this tool
└── USER-FILES/
    ├── 00.KB/                 # Knowledge base
    │   └── few_shots/         # Example outputs
    ├── 04.INPUT/              # Active input
    │   ├── 04.1.IMAGE_URL/    # Image folders
    │   │   ├── folder1/       # First model output
    │   │   ├── folder2/       # Second model output
    │   │   └── folder3/       # Third model output
    │   └── 04.2.PROMPT/       # Prompt files
    │       ├── prompt01.txt
    │       ├── prompt02.txt
    │       └── prompt03.txt
    └── 05.OUTPUT/             # Generated outputs
        └── {YYMMDD_HHMMSS}/   # Timestamped output
            └── Image_Review_{YYMMDD_HHMMSS}.md
```

---

## 04. Input/Output Pattern

### 04.1 Input Structure

**Image Folders** (`USER-FILES/04.INPUT/04.1.IMAGE_URL/`)

- Each subfolder represents one AI model's output
- Images must have matching filenames across folders
- Supported formats: .jpg, .jpeg, .png, .webp
- Natural sort order applied to filenames

**Prompt Files** (`USER-FILES/04.INPUT/04.2.PROMPT/`)

- Text files containing prompts (.txt)
- One prompt per file
- Files matched to images by sort order
- First prompt → first image set, etc.

### 04.2 Output Structure

**Markdown File** (`USER-FILES/05.OUTPUT/{timestamp}/`)

- Filename: `Image_Review_{YYMMDD_HHMMSS}.md`
- Dynamic column layout based on folder count
- HTML comments for parsing markers
- Critique sections with placeholders

### 04.3 Processing Flow

```plaintext
1. Discover image folders in 04.1.IMAGE_URL/
2. Discover prompt files in 04.2.PROMPT/
3. Match images across folders by filename
4. Generate markdown with appropriate column layout
5. Write to timestamped output directory
```

### 04.4 Template Selection Logic

- 1 folder → Single column table (like few_shot_1.md)
- 2 folders → Two column table (like few_shot_2.md)
- 3+ folders → N column table (like few_shot_3.md)

---

## 05. Implementation Details

### 05.1 Core Functions

```python
def discover_image_folders() -> List[Path]
    """Find all subdirectories in 04.1.IMAGE_URL"""

def discover_prompts() -> List[Path]
    """Find all .txt files in 04.2.PROMPT"""

def match_images_across_folders(folders: List[Path]) -> Dict[str, List[Path]]
    """Group images by filename across folders"""

def generate_markdown(folders, images, prompts) -> str
    """Create the annotation markdown content"""

def main() -> None
    """Orchestrate the entire process"""
```

### 05.2 Markdown Generation Rules

**Header Section**

```markdown
<!--- REVIEW_START -->
# Image Review {YYMMDD}
---
- **Generated:** {YYMMDD_HHMMSS}
- **Column 1:** [Generation notes filled out manually by user]
- **Column 2:** [Generation notes filled out manually by user]
- **Total Images:** {count}
<!--- TOTAL_IMAGES: {count} -->
---
```

**Image Section (per shot)**

```markdown
## Shot {n}

| folder1/image.jpeg | folder2/image.jpeg | folder3/image.jpeg |
| ------------------ | ------------------ | ------------------ |
| ![image](path)     | ![image](path)     | ![image](path)     |

<!--- PROMPT_START -->
**{prompt_filename}:**
```text
{prompt_content}
```

<!--- PROMPT_END -->

<!--- CRITIQUE_START -->

**Critique:**

```text
[To be filled by user]
```

<!--- CRITIQUE_END -->

---

```
### 05.3 Natural Sorting

- Use natsort for all file operations
- Ensures image1, image2, image10 sort correctly
- Applied to both folder names and image files

### 05.4 Logging Strategy

- Info: Processing steps and counts
- Warning: Mismatched images, missing files
- Error: Critical failures requiring exit
- Success: Final summary with output path

---

## 06. Execution

### Command
```bash
python3 -m src.main
```

### Expected Behavior

1. **Startup**: Log discovery of folders and prompts
2. **Processing**: Match images, generate markdown
3. **Output**: Save to timestamped directory
4. **Completion**: Log success with file path

### Exit Codes

- `0`: Success - markdown generated
- `1`: Error - missing inputs or write failure

---

## 07. Key Principles (Aligned with Manifesto)

1. **One Tool, One Purpose**: Generate annotation markdown, nothing else
2. **Fail Fast, Fail Loud**: Clear errors when inputs are missing
3. **File System Respect**: Never modify inputs, timestamped outputs
4. **Sequential by Default**: Process deterministically with natural sorting
5. **Minimalism Above All**: Single file, under 250 lines, no config needed

---

## 08. Success Criteria

- Correctly discovers all image folders
- Matches images across folders by name
- Generates proper column layout (1, 2, 3+ columns)
- Includes all prompts in order
- Creates parseable HTML comments
- Outputs to correct timestamped location
- Clear error messages when inputs missing