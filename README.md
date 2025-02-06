# Make black/dark edges of high-quality scans transparent

### What the script does
This simple script (partially LLM-generated) removes black borders around relatively light-coloured documents in high-quality scans, such as library digitisations. The image is not cropped, but the dark border becomes transparent, so that the document is cropped with its natural borders at best. Dark areas are only cropped if they touch the edge of the image at at least two points in order to prevent dark content in the centre of the image from being deleted. 

![example](https://github.com/user-attachments/assets/467d84f3-38b5-4ed3-b9b0-b93a26c3ea82)

For simple cropping of scans with dark edges, please refer to [remove_black_borders](https://github.com/loglux/remove_black_borders/) by [loglux](https://github.com/loglux). 

### Limits of the script
Darker image content, such as brown leather bindings, is currently deleted as it is identified as a dark area. It is planned to adapt the code so that dark areas are always defined in relation to the brightness threshold in the centre of the image. A makeshift solution is to experiment with the threshold values in the script. It is also planned to smooth the edges of the document, as the dark areas will be removed pixel by pixel. 

## Prerequisites

Before using this script, you need to have the following dependencies installed:

- opencv-python
- numpy
- Pillow

```bash
pip install opencv-python
pip install numpy
pip install pillow
```

## Usage

1. Clone or download this repository to your local machine.

2. Place the images you want to process in a folder of your choice. You can set the input folder by modifying the `input_dir` variable in the script.

3. Secondly specify the output folder where the cropped images will be saved by modifying the `output_dir` variable in the script. If not provided, it defaults to a folder with the same name as the input folder but prefixed with "op_".

```python
input_dir = "path/to/input"
output_dir = "path/to/output"
```

4. Run the script:
```bash
python removeBlackEdges.py
```

- The script will now process all the supported files in the input folder, detect borders and make them transparent, and save the cropped images in the output folder.
