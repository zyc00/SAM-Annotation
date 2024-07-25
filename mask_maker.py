import numpy as np
import matplotlib.pyplot as plt
import argparse
from PIL import Image


def show_mask(mask, ax, random_color=False, color=None):
    if random_color:
        color = np.concatenate([np.random.random(3), np.array([0.6])], axis=0)
    elif color is not None:
        color = np.array(color)
        color[-1] = 0.6
    else:
        color = np.array([30 / 255, 144 / 255, 255 / 255, 0.6])
    h, w = mask.shape[-2:]
    mask_image = mask.reshape(h, w, 1) * color.reshape(1, 1, -1)
    ax.imshow(mask_image)


def show_box(box, ax, name, index, color, plt_name=False, plt_index=False):
    x0, y0 = box[0], box[1]
    x1, y1 = box[2], box[3]
    w, h = box[2] - box[0], box[3] - box[1]
    ax.add_patch(
        plt.Rectangle(
            (x0, y0),
            w,
            h,
            edgecolor=color,
            facecolor=(0, 0, 0, 0),
            lw=2,
        )
    )
    if plt_name:
        plt.text(x0, y0, name, fontsize=10, color=color)
    if plt_index:
        plt.text((x0 + x1) / 2, (y0 + y1) / 2, str(index), fontsize=10, color=color)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--image_folder", type=str, default="gaussian_jul_25")
    parser.add_argument("--image_name", type=str, default="color_0.png")
    parser.add_argument("--plot_bbox", default=False, action="store_true")
    parser.add_argument("--plot_cat", default=False, action="store_true")
    parser.add_argument("--plot_index", default=False, action="store_true")
    parser.add_argument("--save", default=False, action="store_true")
    return parser.parse_args()


def plot_on_image(image, masks, cats, args, show_bbox=False):
    cmap = plt.get_cmap("hsv", 1000)
    plt.imshow(image)
    for i in range(len(masks)):
        mask = masks[i]
        rand_color_index = np.random.randint(0, 1000)
        show_mask(mask, plt.gca(), random_color=False, color=cmap(rand_color_index))
        if show_bbox:
            mask_points = np.where(mask > 0)
            x0, x1 = mask_points[1].min(), mask_points[1].max()
            y0, y1 = mask_points[0].min(), mask_points[0].max()
            show_box(
                [x0, y0, x1, y1],
                plt.gca(),
                cats[i],
                i,
                color=cmap(rand_color_index),
                plt_name=args.plot_cat,
                plt_index=args.plot_index,
            )
    return


def main():
    args = parse_args()

    # Load image and mask
    mask_name = args.image_name.split(".")[0] + ".npy"
    image = np.array(Image.open(args.image_folder + "/" + args.image_name))
    mask = np.load(args.image_folder + "/" + mask_name, allow_pickle=True).item()
    print(mask.keys())

    # Plot image
    plt.figure(figsize=(10, 10))
    plot_on_image(image, mask["masks"], mask["labels"], args, show_bbox=args.plot_bbox)
    plt.axis("off")
    if args.save:
        plt.margins(x=0, y=0)
        plt.savefig("./annotation.png", bbox_inches="tight", pad_inches=0)
    else:
        plt.show()


if __name__ == "__main__":
    main()
