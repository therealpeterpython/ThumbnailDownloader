# ThumbnailDownloader
A simple script to download a small amount (<21) of low resolution thumbnails from the google image search. 

# Example
Note: For a full overview of the parameters of `download()` and `download_one()` see the (short) source code.
```python
import thumbnail_downloader as td

path = tf.download_one("google logo")  # relative path to the image file
print(path)
```
