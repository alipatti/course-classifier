# Carleton Course Classifier

## Making the model

The training script and an explanation of our process is outlined in the Jupyter notebook `training.ipynb`. If you want to run this yourself, you'll need to download some large word-embedding files by uncommenting a few lines in the notebook. We've also included a saved version of the model we trained ourselves, so **you don't need to run the training script if you don't wan't to**. We achieve about 60 percent department-classification accuracy on a subset of the catalog that our model did not see during training.

## Using the model

A short example of using the trained model is available in `testing.ipynb`. Feel free to play around with this, but for the full experience, install the dependencies with `pip install -r requirements.txt` (you might want to make a virtual environment first) and run the web app with `python3 app.py`. It might take a second to load the first time around, but when it boots, navigate to the provided link and enjoy!
