# pixel-thresholder

By following the steps below, you can perform thresholding on image files.

## Setting
Install dependencies:
```
pip install -r requirements.txt
```

## Thresholding
Execute by specifying the source path, save destination, pixel value for thresholding, threshold type, and whether your image file has an alpha channel:
```
python src/threshold_pixel.py input/image.png \
    output/image_binary_alpha.png 127 binary --alpha
```

## Result
Before executing the command above:

![before](https://github.com/mozu-dev/pixel-thresholder/blob/main/input/image.png)

After executing the command above:

![after](https://github.com/mozu-dev/pixel-thresholder/blob/main/output/image_binary_alpha.png)

## License
[MIT license](https://github.com/mozu-dev/pixel-thresholder/blob/main/LICENSE)

## Credit
Illustration by ziro_