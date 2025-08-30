#!/usr/bin/env python3
"""AI Image Generation Annotation Tool - Generate markdown for image review."""

import sys
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional
from collections import defaultdict

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


def match_urls_across_folders(folders: List[Path]) -> Dict[str, List[Optional[str]]]:
    """Read URLs from text files and group by filename across folders."""
    all_urls = defaultdict(lambda: [None] * len(folders))
    
    for idx, folder in enumerate(folders):
        # Read all .txt files in the folder
        txt_files = natsorted([f for f in folder.iterdir() if f.suffix == '.txt'])
        
        for txt_file in txt_files:
            # Read the URL from the text file
            try:
                url = txt_file.read_text().strip()
                if url:
                    # Use the text file name as the key (e.g., "image1.txt")
                    all_urls[txt_file.name][idx] = url
            except Exception as e:
                logger.warning(f"Failed to read URL from {txt_file}: {e}")
    
    # Sort by filename naturally
    sorted_urls = {k: all_urls[k] for k in natsorted(all_urls.keys())}
    
    logger.info(f"Matched {len(sorted_urls)} URL file(s) across folders")
    return sorted_urls


def generate_markdown(folders: List[Path], urls: Dict[str, List[Optional[str]]], 
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
    
    total_images = len(urls)
    lines.append(f"- **Total Images:** {total_images}")
    lines.append(f"<!--- TOTAL_IMAGES: {total_images} -->")
    lines.append("---")
    
    # Generate shots
    shot_num = 0
    for txt_name, url_list in urls.items():
        shot_num += 1
        lines.append(f"## Shot {shot_num}")
        lines.append("")
        
        # Convert txt filename to image filename (e.g., "image1.txt" -> "image1.jpeg")
        img_name = txt_name.replace('.txt', '.jpeg')
        
        # Table header
        headers = []
        separators = []
        for folder in folders:
            header_path = f"{folder.name}/{img_name}"
            headers.append(f"{header_path:30}")
            separators.append("-" * 29)
        
        lines.append("| " + " | ".join(headers) + " |")
        lines.append("| " + " | ".join(separators) + " |")
        
        # Table content with images using URLs
        img_cells = []
        for url in url_list:
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
        urls = match_urls_across_folders(folders)
        
        if not urls:
            logger.error("No URL files found to process")
            sys.exit(1)
        
        # Generate markdown
        markdown_content = generate_markdown(folders, urls, prompts)
        
        # Create output directory
        now = datetime.now()
        timestamp = now.strftime("%y%m%d_%H%M%S")
        output_dir = Path(f"USER-FILES/05.OUTPUT/{timestamp}")
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Write output file
        output_file = output_dir / f"Image_Review_{timestamp}.md"
        output_file.write_text(markdown_content)
        
        logger.success(f"✓ Markdown generated successfully: {output_file}")
        logger.info(f"Total URL files processed: {len(urls)}")
        
    except Exception as e:
        logger.error(f"Failed to generate markdown: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()