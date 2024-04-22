from skimage import io, exposure
from skimage.color import rgb2gray
from skimage.filters import gaussian, sobel, unsharp_mask
from skimage.exposure import rescale_intensity 


pipeline_steps = {
    "Grayscale": {
        "function": "rgb2gray"
        },
    "Gaussian Blur": {
        "function": "gaussian", 
        "params": {"sigma": 4.0}
        },
    "Edge Detection": {
        "function": "sobel"
        },
    "Sharpen": {
        "function": "unsharp_mask",
        "params": {"radius": 2.0, "amount": 2.0}
        },
    "Contrast Adjustment": {
        "function": "rescale_intensity"
        }
}

class ImageProcessing:
    def __init__(self, image_path):
        self.image_path = image_path
        self.image = io.imread(image_path)
        self.processed_images = [self.image]

    def process_image(self, steps):
        for step in steps:
            print(globals())
            function = globals()[step['function']]
            if step.get('params'):
                self.image = function(self.image, **step.get('params'))
            else:
                self.image = function(self.image)
            self.processed_images.append(self.image)
