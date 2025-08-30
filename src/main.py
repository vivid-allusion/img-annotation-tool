#!/usr/bin/env python3
"""AI Image Generation Annotation Tool - Generate markdown for image review."""

import sys
import re
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional
from collections import defaultdict
from urllib.parse import quote, unquote

from natsort import natsorted
from loguru import logger


def discover_url_folders() -> List[Path]:
    """Find all subdirectories containing URL text files in 04.1.IMAGE_URL."""
    base_path = Path("USER-FILES/04.INPUT/04.1.IMAGE_URL")
    
    if not base_path.exists():
        logger.error(f"URL folder path does not exist: {base_path}")
        sys.exit(1)
    
    folders = [f for f in base_path.iterdir() if f.is_dir() and not f.name.startswith('.')]
    folders = natsorted(folders, key=lambda x: x.name)
    
    if not folders:
        logger.error("No URL folders found in USER-FILES/04.INPUT/04.1.IMAGE_URL")
        sys.exit(1)
    
    logger.info(f"Found {len(folders)} URL folder(s): {[f.name for f in folders]}")
    return folders


def discover_prompts() -> List[Path]:
    """Find all .txt files in 04.2.PROMPT."""
    base_path = Path("USER-FILES/04.INPUT/04.2.PROMPT")
    
    if not base_path.exists():
        logger.error(f"Prompt folder path does not exist: {base_path}")
        sys.exit(1)
    
    prompts = list(base_path.glob("*.txt"))
    prompts = natsorted(prompts, key=lambda x: x.name)
    
    if not prompts:
        logger.error("No prompt files found in USER-FILES/04.INPUT/04.2.PROMPT")
        sys.exit(1)
    
    logger.info(f"Found {len(prompts)} prompt file(s): {[p.name for p in prompts]}")
    return prompts


def clean_url(url: str) -> str:
    """Clean and validate URL, handling special characters."""
    # Strip all whitespace including tabs, newlines, etc.
    url = url.strip()
    
    # Remove any trailing/leading whitespace characters that might be invisible
    url = re.sub(r'^\s+|\s+$', '', url)
    
    # Check if URL needs encoding for special characters
    # Split URL into parts to handle the path separately
    if url.startswith('http'):
        # Don't encode the whole URL, just ensure it's clean
        # The URL should already be properly encoded from the source
        return url
    
    return url


def match_urls_across_folders(folders: List[Path]) -> List[Dict[str, Optional[str]]]:
    """Read URLs from text files and group by position/order in each folder."""
    # Get all txt files from each folder, sorted
    folder_files = []
    max_files = 0
    
    for folder in folders:
        txt_files = natsorted([f for f in folder.iterdir() if f.suffix == '.txt'])
        folder_files.append(txt_files)
        max_files = max(max_files, len(txt_files))
        logger.info(f"Found {len(txt_files)} files in {folder.name}")
    
    # Create list of dictionaries, one per "shot"
    all_urls = []
    
    for shot_idx in range(max_files):
        shot_data = {
            'urls': [],
            'filenames': []
        }
        
        for folder_idx, files in enumerate(folder_files):
            if shot_idx < len(files):
                txt_file = files[shot_idx]
                try:
                    raw_content = txt_file.read_text()
                    url = clean_url(raw_content)
                    
                    if url and url.startswith('http'):
                        shot_data['urls'].append(url)
                        shot_data['filenames'].append(txt_file.name)
                        logger.debug(f"Shot {shot_idx+1}, Folder {folder_idx}: {txt_file.name}")
                    else:
                        shot_data['urls'].append(None)
                        shot_data['filenames'].append(None)
                        if url:
                            logger.warning(f"Invalid URL format in {txt_file}: {url[:50]}...")
                except Exception as e:
                    shot_data['urls'].append(None)
                    shot_data['filenames'].append(None)
                    logger.warning(f"Failed to read URL from {txt_file}: {e}")
            else:
                shot_data['urls'].append(None)
                shot_data['filenames'].append(None)
        
        all_urls.append(shot_data)
    
    logger.info(f"Created {len(all_urls)} shots from {len(folders)} folders")
    return all_urls


def generate_markdown(folders: List[Path], shots: List[Dict[str, Optional[str]]], 
                     prompts: List[Path]) -> str:
    """Create the annotation markdown content."""
    now = datetime.now()
    timestamp = now.strftime("%y%m%d_%H%M%S")
    date_str = now.strftime("%y%m%d")
    
    # Start markdown content
    lines = ["<!--- REVIEW_START -->"]
    lines.append(f"# Image Review {date_str}")
    lines.append("---")
    lines.append(f"- **Generated:** {timestamp}")
    
    # Add column metadata
    for i, folder in enumerate(folders, 1):
        lines.append(f"- **Column {i}:** [Generation notes filled out manually by user]")
    
    total_images = len(shots)
    lines.append(f"- **Total Images:** {total_images}")
    lines.append(f"<!--- TOTAL_IMAGES: {total_images} -->")
    lines.append("---")
    
    # Generate shots
    for shot_num, shot_data in enumerate(shots, 1):
        lines.append(f"## Shot {shot_num}")
        lines.append("")
        
        # Split folders into groups of 3 for table rows
        max_cols = 3
        for row_start in range(0, len(folders), max_cols):
            row_end = min(row_start + max_cols, len(folders))
            row_folders = folders[row_start:row_end]
            
            # Table header for this row
            headers = []
            separators = []
            for folder_idx in range(row_start, row_end):
                folder = folders[folder_idx]
                if shot_data['filenames'][folder_idx]:
                    # Use actual filename for header
                    filename = shot_data['filenames'][folder_idx]
                    # Convert .txt to .jpeg for display
                    display_name = filename.replace('.txt', '.jpeg')
                    headers.append(f"{folder.name}/{display_name:30}"[:60])
                else:
                    headers.append(f"{folder.name}/[No file]                      "[:60])
                separators.append("-" * 59)
            
            lines.append("| " + " | ".join(headers) + " |")
            lines.append("| " + " | ".join(separators) + " |")
            
            # Table content with images using URLs
            img_cells = []
            for folder_idx in range(row_start, row_end):
                url = shot_data['urls'][folder_idx]
                if url:
                    img_cells.append(f"![image]({url})")
                else:
                    img_cells.append("[No image]")
            
            lines.append("| " + " | ".join(img_cells) + " |")
            lines.append("")
        
        # Add prompt if available
        prompt_idx = shot_num - 1
        if prompt_idx < len(prompts):
            prompt_file = prompts[prompt_idx]
            prompt_content = prompt_file.read_text().strip()
            
            lines.append("<!--- PROMPT_START -->")
            lines.append(f"**{prompt_file.name}:**")
            lines.append("```text")
            lines.append(prompt_content)
            lines.append("```")
            lines.append("")
            lines.append("<!--- PROMPT_END -->")
        else:
            lines.append("<!--- PROMPT_START -->")
            lines.append("**Prompt:**")
            lines.append("```text")
            lines.append("[No prompt available]")
            lines.append("```")
            lines.append("")
            lines.append("<!--- PROMPT_END -->")
        
        lines.append("")
        lines.append("<!--- CRITIQUE_START -->")
        lines.append("**Critique:**")
        lines.append("```text")
        lines.append("[To be filled by user]")
        lines.append("```")
        lines.append("<!--- CRITIQUE_END -->")
        lines.append("---")
    
    lines.append("")
    lines.append("<!--- REVIEW_END -->")
    
    return "\n".join(lines)


def main() -> None:
    """Orchestrate the entire process."""
    logger.info("Starting AI Image Generation Annotation Tool (URL mode)")
    
    try:
        # Discover inputs
        folders = discover_url_folders()
        prompts = discover_prompts()
        
        # Match URLs from text files
        shots = match_urls_across_folders(folders)
        
        if not shots:
            logger.error("No URL files found to process")
            sys.exit(1)
        
        # Generate markdown
        markdown_content = generate_markdown(folders, shots, prompts)
        
        # Create output directory
        now = datetime.now()
        timestamp = now.strftime("%y%m%d_%H%M%S")
        output_dir = Path(f"USER-FILES/05.OUTPUT/{timestamp}")
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Write output file
        output_file = output_dir / f"Image_Review_{timestamp}.md"
        output_file.write_text(markdown_content)
        
        logger.success(f"✓ Markdown generated successfully: {output_file}")
        logger.info(f"Total shots created: {len(shots)}")
        
    except Exception as e:
        logger.error(f"Failed to generate markdown: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()