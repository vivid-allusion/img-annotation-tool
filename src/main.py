#!/usr/bin/env python3
"""AI Image Generation Annotation Tool - Generate markdown for image review."""

import sys
from pathlib import Path
from datetime import datetime
from typing import List
from dataclasses import dataclass

from natsort import natsorted
from loguru import logger


@dataclass
class Shot:
    """Single shot with URLs from multiple folders."""
    urls: List[str | None]
    filenames: List[str | None]


def main() -> None:
    """Generate markdown for image annotation."""
    logger.info("Starting AI Image Generation Annotation Tool")
    
    # Discover URL folders
    url_base = Path("USER-FILES/04.INPUT/04.1.IMAGE_URL")
    if not url_base.exists():
        logger.error(f"URL folder does not exist: {url_base}")
        sys.exit(1)
    
    folders = natsorted([f for f in url_base.iterdir() if f.is_dir()])
    if not folders:
        logger.error("No URL folders found")
        sys.exit(1)
    logger.info(f"Found {len(folders)} folders")
    
    # Discover prompts
    prompt_base = Path("USER-FILES/04.INPUT/04.2.PROMPT")
    if not prompt_base.exists():
        logger.error(f"Prompt folder does not exist: {prompt_base}")
        sys.exit(1)
    
    prompts = natsorted(list(prompt_base.glob("*.txt")))
    if not prompts:
        logger.error("No prompt files found")
        sys.exit(1)
    logger.info(f"Found {len(prompts)} prompts")
    
    # Match URLs by position across folders
    all_files = []
    max_files = 0
    for folder in folders:
        txt_files = natsorted([f for f in folder.iterdir() if f.suffix == '.txt'])
        all_files.append(txt_files)
        max_files = max(max_files, len(txt_files))
        logger.info(f"{folder.name}: {len(txt_files)} files")
    
    # Create shots by matching files at same position
    shots = []
    for idx in range(max_files):
        urls = []
        filenames = []
        
        for folder_files in all_files:
            if idx < len(folder_files):
                try:
                    url = folder_files[idx].read_text().strip()
                    valid_ext = url.lower().endswith(('.jpg', '.jpeg', '.png'))
                    if url.startswith('http') and valid_ext:
                        urls.append(url)
                        filenames.append(folder_files[idx].name)
                    else:
                        urls.append(None)
                        filenames.append(None)
                except Exception as e:
                    logger.warning(f"Failed to read {folder_files[idx]}: {e}")
                    urls.append(None)
                    filenames.append(None)
            else:
                urls.append(None)
                filenames.append(None)
        
        if any(u is not None for u in urls):
            shots.append(Shot(urls, filenames))
    
    logger.info(f"Created {len(shots)} shots")
    
    # Generate markdown
    now = datetime.now()
    timestamp = now.strftime("%y%m%d_%H%M%S")
    date_str = now.strftime("%y%m%d")
    
    lines = ["<!--- REVIEW_START -->"]
    lines.append(f"# Image Review {date_str}")
    lines.append("---")
    lines.append(f"- **Generated:** {timestamp}")
    
    for i, folder in enumerate(folders, 1):
        lines.append(f"- **Column {i}:** [Generation notes]")
    
    lines.append(f"- **Total Images:** {len(shots)}")
    lines.append(f"<!--- TOTAL_IMAGES: {len(shots)} -->")
    lines.append("---")
    
    # Generate each shot
    for shot_num, shot in enumerate(shots, 1):
        lines.append(f"## Shot {shot_num}")
        lines.append("")
        
        # Create tables with max 2 columns per row
        for row_start in range(0, len(folders), 2):
            row_end = min(row_start + 2, len(folders))
            
            # Headers
            headers = []
            for i in range(row_start, row_end):
                if shot.filenames[i]:
                    name = shot.filenames[i].replace('.txt', '.jpeg')
                    headers.append(f"{folders[i].name}/{name}"[:60])
                else:
                    headers.append(f"{folders[i].name}/[No file]")
            
            lines.append("| " + " | ".join(headers) + " |")
            lines.append("| " + " | ".join(["-" * 59] * len(headers)) + " |")
            
            # Images
            imgs = []
            for i in range(row_start, row_end):
                if shot.urls[i]:
                    imgs.append(f"![image]({shot.urls[i]})")
                else:
                    imgs.append("[No image]")
            
            lines.append("| " + " | ".join(imgs) + " |")
            lines.append("")
        
        # Add prompt
        lines.append("<!--- PROMPT_START -->")
        if shot_num - 1 < len(prompts):
            prompt_file = prompts[shot_num - 1]
            lines.append(f"**{prompt_file.name}:**")
            lines.append("```text")
            lines.append(prompt_file.read_text().strip())
            lines.append("```")
        else:
            lines.append("**Prompt:**")
            lines.append("```text")
            lines.append("[No prompt available]")
            lines.append("```")
        lines.append("")
        lines.append("<!--- PROMPT_END -->")
        
        # Add critique section
        lines.append("")
        lines.append("<!--- USER_START -->")
        lines.append("**User:**")
        lines.append("```text")
        lines.append("")
        lines.append("```")
        lines.append("<!--- USER_END -->")
        lines.append("---")
    
    lines.append("")
    lines.append("<!--- REVIEW_END -->")
    
    # Write output
    output_dir = Path(f"USER-FILES/05.OUTPUT/{timestamp}_IMG-ANNOTATION")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    output_file = output_dir / f"Image_Review_{timestamp}.md"
    output_file.write_text("\n".join(lines))
    
    logger.success(f"✓ Generated: {output_file}")
    logger.info(f"Total shots: {len(shots)}")


if __name__ == "__main__":
    main()