# Testing Roboflow Pipeline

## Objective
The goal is to read images from Google Photos, figure out which ones were taken by an analog camera, and sort those into their own album.
Unfortunately, it's not possible to organize photos using the google photos API, so for now, we download a copy of lower resolution.

## Model
Trained a model on a reasonably small (67 images) sample of images using a *ViT* model. Split into train, test, and validation sets. 


## Roboflow Versions
* Version 1: Tested out resized 640x640 images with some data augmentations
* Version 2: Reduced size to 400x400
* Version 3: Used different augmentations 
* Version 4: Add more images to the dataset


## Results

First three versions failed to accurately predict analog images. Adding additional samples improved the predictions.