# Idea brief

## What I Want

I want you to create a python script that can generate markdown files for annotation of AI generated images. 

## Images

The script should run with the command `python3 -m src.main` and then it will go into this folder `USER-FILES/04.INPUT/04.1.IMAGE_URL` and look for folders with images.The script should be able to adapt to multiple folders of images.

If there's just one image folder in USER-FILES/04.INPUT Then the markdown should look like this USER-FILES/00.KB/few_shots/few_shot_1.md

If there's two image folder in USER-FILES/04.INPUT Then the markdown should look like this USER-FILES/00.KB/few_shots/few_shot_2.md


If there's three image folder in USER-FILES/04.INPUT Then the markdown should look like this USER-FILES/00.KB/few_shots/few_shot_3.md


## Prompt

There can be multiple folders with images, but the images are always generated with the same image prompt. Just using different modules and settings. That's why all the rows in the table with the images should have the same prompt. The prompt can be found in this path as text files.

USER-FILES/04.INPUT/04.2.PROMPT/


These inputs are synthesized into a markdown file that is generated and saved to /Users/ruben/08_-_DEVELOPMENT/ISOF_TOOLS/annotation_tool/USER-FILES/05.OUTPUT/{yymmdd_hhmmss}/Image_Review{yymmdd_hhmmss}.md. 

