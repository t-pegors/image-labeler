# Image Labeler

A quick and easy way to manually assign binary labels to image files. Using cv2, each image is displayed and then labeled with a keypress. Labels are either 1 (key "f") or 0 (key "j"). Labels are stored in a "labels.csv" file within the image folder. Each column is a label category. 

Give this class a folder location with all your images, use the class methods to add labels.  (for ML classification or general "Did I find what I was looking for?" questions.)

Any images that error out on imread will be marked, and on save, will be removed from the csv file and moved to a "bad_images" folder.

### Define the Class:

`c = Labels(path='YOUR_PATH_HERE')`

If there is no label csv file, one will be created that holds the current list of filenames as rows.

### Create a series of Labels:

`c.create_label(label_name='Face_Present', counter=True)`

Each image will pop up, use the following keystrokes:
* "f" = 1
* "j" = 0
* esc = exit labeling (will save progress upon exit)

If counter = True, a command line counter will show you how many labels out of the total you have completed.
When labeling is complete, the label csv file will automatically be updated and save to the image folder as "labels.csv"

### Resume labeling:

`c.resume_label(label_name='Face_Present', counter=True)`

Will pick up where you left off labeling and feed you just the images that haven't yet been labeled.

### Delete label:

`c.delete_label(label_name=['Face_Present', 'Dog_Present']`

Pass a list of column names to remove from the labels.csv file.
