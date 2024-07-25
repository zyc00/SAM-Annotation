import numpy as np
import matplotlib.pyplot as plt
import argparse
from PIL import Image


def show_mask(mask, ax, random_color=False):
    print(mask.shape)
    if random_color:
        color = np.concatenate([np.random.random(3), np.array([0.6])], axis=0)
    else:
        color = np.array([30 / 255, 144 / 255, 255 / 255, 0.6])
    h, w = mask.shape[-2:]
    mask_image = mask.reshape(h, w, 1) * color.reshape(1, 1, -1)
    ax.imshow(mask_image)


def show_box(box, ax, name, color):
    x0, y0 = box[0], box[1]
    w, h = box[2] - box[0], box[3] - box[1]
    ax.add_patch(
        plt.Rectangle(
            (x0, y0),
            w,
            h,
            edgecolor=color,
            facecolor=(0, 0, 0, 0),
            lw=5,
        )
    )
    plt.text(x0, y0, name, fontsize=40, color=color)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--image_folder", type=str, default="./example")
    parser.add_argument("--image_name", type=str, default="./example")
    parser.add_argument("--plot_bbox", type=bool, default=False, action="store_true")
    return parser.parse_args()


def plot_on_image(image, mask, box, name, color):
    pass


def main():
    args = parse_args()

    # Load image and mask
    mask_name = args.image_name.split(".")[0] + ".npy"
    image = np.array(Image.open(args.image_folder + "/" + args.image_name))
    mask = np.load(args.image_folder + "/" + mask_name, allow_pickle=True)

    # Plot image
    plt.figure(figsize=(10, 10))
