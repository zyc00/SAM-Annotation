# SAM_Annotation

# Image Annotation with SegmenAnything (SAM)
## Key Features

- **Point Annotation**: Utilize minimal points to define complex structures in tight sandstone image pores.
- **Data Masking**: Accurately generate masks that are crucial for further analysis or machine learning applications.
- **Efficiency**: Expedite the annotation process without compromising on precision.
- **Customizable**: Flexible tool design to suit various annotation needs.

## Visualization of SAM Annotation

   ![Annotation GIF](Demonstration/1.gif)  

## Model Usage Instructions

**Step 1**: Download the pre-trained weights of the SAM model and place them in the `checkpoints` folder. [Download Link](https://github.com/facebookresearch/segment-anything)

For `ViT-H` checkpoint: 
```
cd checkpoints && wget https://dl.fbaipublicfiles.com/segment_anything/sam_vit_h_4b8939.pth && cd ..
```

**Step 2**: Modify the following lines in `utils\file_functions.py` according to the chosen weight type:
```python
   sam_checkpoint = "checkpoints\sam_vit_h_4b8939.pth"
   model_type = "vit_h"
```

For detailed instructions, refer to the [SAM Official Website](https://github.com/facebookresearch/segment-anything).

**Step 3**: For fine-tuning the SAM model, you can refer to my other article: [Link to Article](https://github.com/wudi-ldd/Fine-Tuning-SAM)


## Installation
Prerequest: `torch`, `segment_anything`
```
pip install omegaconf
pip install pyqt5
pip install -U pillow=9.2.0
pip uninstall opencv-python && pip install opencv-python-headless
```

## Quick Start
Set `SAM's checkpoint`, `Image Folder` and `Annotation Categories` in the [config](./configs/config_vit_h.yaml).

Start GUI:
```
python main.py
```

Use `E` to end annotation for a mask. Use `S` to save annotation results after finishing annotating all instances.
The annotation results will be saved as a `.npy` file in the image folder.

## Shortcuts

- **Left Mouse Click**: Click on areas of interest.
- **Right Mouse Click**: Click on areas not of interest to complete the data annotation without manually drawing mask boxes.
- **Z**: Undo to the previous mouse click state.
- **E**: Finish annotation and save the current mask state.
- **S**: Save annotation to a `.npy` file.

## TODO:
- Segmentation proposals with text prompts.
- Mask & label visualization.




