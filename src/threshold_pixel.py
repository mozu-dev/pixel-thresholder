import cv2
import argparse


def parse_arguments():
    parser = argparse.ArgumentParser(
        description='Convert an image to binary using various thresholding methods, with optional alpha channel consideration.')
    parser.add_argument(
        'input_image',
        type=str,
        help='Path to the input image.')
    parser.add_argument(
        'output_image',
        type=str,
        help='Path to the output image.')
    parser.add_argument(
        'threshold_value',
        type=int,
        help='Threshold value for non-adaptive methods. Ignored for Otsu and adaptive methods.')
    parser.add_argument(
        'threshold_type',
        type=str,
        help='Threshold type (ex. binary, binary_inv, trunc, tozero, tozero_inv, adaptive_mean, adaptive_gaussian, otsu).')
    parser.add_argument(
        '--block_size',
        type=int,
        default=11,
        help='Block size for adaptive methods. Default is 11.')
    parser.add_argument(
        '--C',
        type=int,
        default=2,
        help='Constant subtracted from the mean or weighted mean for adaptive methods. Default is 2.')
    parser.add_argument(
        '--alpha',
        action='store_true',
        help='Consider the alpha channel if present.')
    return parser.parse_args()


def apply_threshold(image, args, threshold_methods):
    if args.threshold_type in ['adaptive_mean', 'adaptive_gaussian']:
        method = threshold_methods[args.threshold_type]
        return cv2.adaptiveThreshold(
            image,
            255,
            method,
            cv2.THRESH_BINARY,
            args.block_size,
            args.C)
    elif args.threshold_type == 'otsu':
        _, binary_image = cv2.threshold(
            image, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    else:
        method = threshold_methods[args.threshold_type]
        _, binary_image = cv2.threshold(
            image, args.threshold_value, 255, method)
    return binary_image


def main():
    args = parse_arguments()

    threshold_methods = {
        'binary': cv2.THRESH_BINARY,
        'binary_inv': cv2.THRESH_BINARY_INV,
        'trunc': cv2.THRESH_TRUNC,
        'tozero': cv2.THRESH_TOZERO,
        'tozero_inv': cv2.THRESH_TOZERO_INV,
        'adaptive_mean': cv2.ADAPTIVE_THRESH_MEAN_C,
        'adaptive_gaussian': cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        'otsu': cv2.THRESH_OTSU
    }

    if args.alpha:
        image = cv2.imread(args.input_image, cv2.IMREAD_UNCHANGED)
        if image.shape[-1] == 4:
            rgb_channels = image[:, :, :3]
            alpha_channel = image[:, :, 3]
            gray_image = cv2.cvtColor(rgb_channels, cv2.COLOR_BGR2GRAY)
            binary_image = apply_threshold(gray_image, args, threshold_methods)
            final_image = cv2.merge(
                (binary_image, binary_image, binary_image, alpha_channel))
        else:
            final_image = apply_threshold(image, args, threshold_methods)
    else:
        image = cv2.imread(args.input_image, cv2.IMREAD_GRAYSCALE)
        final_image = apply_threshold(image, args, threshold_methods)

    cv2.imwrite(args.output_image, final_image)


if __name__ == "__main__":
    main()
