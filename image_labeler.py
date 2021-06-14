import cv2
import os
import pandas as pd
import numpy as np
import warnings


class Labels:

    label_filename = "labels.csv"

    def __init__(self, path):

        self.path = path
        self.valid_images = [".jpg", ".jpeg", ".gif", ".png"]
        self.label_file_exist = False

        if os.path.isdir(path):
            os.chdir(path)
            if os.path.isfile(Labels.label_filename):
                print("Label file exists.")
                self.label_file_exist = True
                self.df = pd.read_csv(Labels.label_filename)
                self.image_filenames = list(self.df['filename'])
                self.num_images = len(self.df)
                if len(self.df.columns) > 1:
                    for column in self.df.columns:
                        if column == 'filename':
                            print(f"... { self.num_images } total images in directory")
                        else:
                            num_completed_labels = self.df[column].notnull().sum()
                            if num_completed_labels == self.num_images:
                                complete_tag = 'COMPLETE'
                            else:
                                complete_tag = 'INCOMPLETE'
                            print(f"...... { column } is { complete_tag }. ({ num_completed_labels }/{ self.num_images })")

            else:
                print("Label file does not exist... creating CSV of filenames now.")
                self.image_filenames = self.get_filenames()
                self.df = self.create_label_file()
                self.label_file_exist = True
                print("...", len(self.image_filenames), "images found in folder.")
        else:
            warnings.warn("Error: directory not found.")

    def get_filenames(self):
        imgs = []
        for f in os.listdir(self.path):
            ext = os.path.splitext(f)[1]
            if ext.lower() not in self.valid_images:
                continue
            imgs.append(f)
        return imgs

    def create_label(self, label_name,counter):

        if not self.label_file_exist:  # make sure the label csv file exists in the folder
            self.df = self.create_label_file()

        if label_name in self.df.columns:  # make sure the label column does NOT exist
            warnings.warn("Error: label file already exists. Either delete, or resume label.")
            return

        label_df = self.df[['filename']].copy()
        label_df[label_name] = np.nan
        label_df = self.display_images_for_labeling(label_df,counter)
        self.df[label_name] = label_df[label_name]
        self.remove_bad_images(label_name)
        self.save_label_file()

        print(f"Label { label_name } saved.")

    def resume_label(self, label_name, counter=False):

        if self.label_file_exist:
            label_df = self.df[['filename', label_name]].copy()
            self.df[label_name] = self.display_images_for_labeling(label_df,counter)[label_name]
            self.remove_bad_images(label_name)
            self.save_label_file()

        else:
            print("Error: no label file exists.")

    def create_label_file(self):

        return pd.DataFrame(self.image_filenames, columns=['filename'])

    def display_images_for_labeling(self, labels_df, counter):

        end_loop = False
        label_column = labels_df.columns[1]
        total_imgs = len(labels_df)

        print("f: TRUE, j: FALSE, esc: EXIT AND SAVE")

        rows_with_nan = [index for index, row in labels_df.iterrows() if row.isnull().any()]
        for row in rows_with_nan:

            try:
                I = cv2.imread(os.path.join(self.path, self.df['filename'][row]))
            except:
                labels_df.at[row, label_column] = 5  # mark for removal
                continue  # skip to the next iteration

            filename = self.df['filename'][row]

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
                    labels_df.at[row, label_column] = 1
                    keep_image_displayed = False
                    if counter:
                        print(f"... { str(labels_df[label_column].notnull().sum()) } / { str(total_imgs) } images given { label_column } label.")
                elif k == 106:  # j
                    labels_df.at[row, label_column] = 0
                    keep_image_displayed = False
                    if counter:
                        print(f"... { str(labels_df[label_column].notnull().sum()) } / { str(total_imgs) } images given { label_column } label.")
                elif k == -1:
                    keep_image_displayed = True
                else:
                    keep_image_displayed = True
                    print('invalid key', k)

            cv2.destroyAllWindows()
            if end_loop:
                return labels_df

        return labels_df

    def delete_label(self, label_name=[]):

        val = input(f"Are you sure you want to delete the { ', '.join(label_name)} label columns? (Y/N): ")
        if val == "Y":
            self.df = self.df.drop(columns=label_name)
            self.save_label_file()
        else:
            pass

    def save_label_file(self):

        self.df.to_csv(Labels.label_filename, index=False)

    def remove_bad_images(self, label_file):

        bad_files = list(self.df.loc[self.df[label_file] == 5, 'filename'])
        if bad_files:
            idxs = self.df[self.df[label_file] == 5].index  # bad images
            self.df.drop(idxs, inplace=True)  # remove bad images from csv

            if not os.path.isdir('bad_images'):
                os.mkdir('bad_images')

            for file in bad_files:
                print(os.path.join(self.path, 'bad_images', file))
                os.replace(os.path.join(self.path, file), os.path.join(self.path, 'bad_images', file))


if __name__ == '__main__':
    c = Labels(path='YOUR_PATH_HERE')
    c.create_label('Face', counter=True)
    #c.resume_label('Face', counter=True)
    #print(c.df)
