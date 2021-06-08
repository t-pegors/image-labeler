import cv2
import os
import pandas as pd


class Labels:
    """
    path: give the class a full path to the folder containing your image files
    """

    label_filename = "labels.csv"

    def __init__(self, path):

        self.path = path
        self.valid_images = [".jpg", ".gif", ".png"]
        self.label_file_exist = False

        if os.path.isdir(path):
            os.chdir(path)
            if os.path.isfile(Labels.label_filename):
                print("Label file exists.")
                self.label_file_exist = False
            else:
                print("Label file does not exist... creating CSV of filenames now.")
                self.image_filenames = self.get_filenames()
                self.label_df = self.create_label_file()
                print("...", len(self.image_filenames), "images found in folder.")
        else:
            print("Error: directory not found.")

    def get_filenames(self):
        imgs = []
        for f in os.listdir(self.path):
            ext = os.path.splitext(f)[1]
            if ext.lower() not in self.valid_images:
                continue
            imgs.append(f)
        return imgs

    def create_label(self, label_name):

        if self.label_file_exist:
            pass
        else:
            self.label_df = self.create_label_file()
            self.label_df[label_name] = self.display_images_for_labeling()
            self.save_label_file()

    def create_label_file(self):

        return pd.DataFrame(self.image_filenames, columns=['filename'])

    def display_images_for_labeling(self):

        labels = []
        end_loop = False
        for row in range(0, len(self.label_df)):

            I = cv2.imread(os.path.join(self.path, self.label_df['filename'][row]))
            filename = self.label_df['filename'][row]

            if I.shape[0] > 600:
                percent_redux = round(600 / I.shape[0], 2)
                width = int(I.shape[1] * percent_redux)
                height = int(I.shape[0] * percent_redux)
                I = cv2.resize(I, (width, height))

            keep_image_displayed = True
            while keep_image_displayed:
                cv2.imshow(filename, I)
                k = cv2.waitKey(33)
                if k == 27:  # escape
                    keep_image_displayed = False
                    end_loop = True
                elif k == 102:  # f
                    labels.append(1)
                    keep_image_displayed = False
                elif k == 106:  # j
                    labels.append(0)
                    keep_image_displayed = False
                elif k == -1:
                    keep_image_displayed = True
                else:
                    keep_image_displayed = True
                    print('invalid key', k)

            cv2.destroyAllWindows()
            if end_loop:
                break

        return labels

    def save_label_file(self):

        self.label_df.to_csv(Labels.label_filename, index=False)

    # df = pd.dataFrame(imgs_filenames, columns=['filename'])
    #
    #
    # def add_label_column(df, label):



if __name__ == '__main__':
    c = Labels(path='/Users/pegors/Documents/Logos/APU/')
    c.create_label(label_name='Color')
    print(c.label_df)
