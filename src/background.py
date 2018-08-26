"""
Module supporting the Background class needed for generating a background
image for the Nuts Detect (ND) project.

class Background: Creates a cv2 image based on a .jpeg and allows object
merge and region of interest (ROI) definiton.
"""

from random import randint

import cv2


class Background:
    """Create and manage a background image.

    This is one of the main class of the ND project and is needed all the
    time. It creates a cv2 image based on a .jpeg image with no constraints
    on the size and channels. Also includes input object and ROI definition
    methods.

    Attributes:
        img_path: A string representing the background image location.
        image: A cv2 image (numpy array) representing the background image.
        selection: A string representing whether or not ROI definition
        is automatic or manuel. Currently unused attribute.
        rois: A list containing tuples representing different ROIS (row_start,
        row_end, col_start, col_end).
    """


    def __init__(self, img_path, selection="auto"):
        """Init background image with img_path and selection mode"""
        self.img_path = img_path
        self.image = cv2.imread(img_path)
        self.selection = selection
        self.rois = [(522, 1257, 1084, 193),
                     (413, 1151, 279, 209),
                     (1326, 1123, 316, 277)]


    def init_roi(self):
        """Allow new ROI creation.

        This will override default ROI list and only populate the self.rois
        attribute with one element. Dependency on cv2.selectROI function.

        Args:
            None

        Returns:
            None
        """
        if self.rois is not None:

            if input("ROI already present. Override? (Y/N)") == 'Y':
                rois = cv2.selectROI(self.img_path)
                k = cv2.waitKey(0)
                if k == 27:
                    cv2.destroyAllWindows()
                self.rois = []
                self.rois = self.rois.append(rois)

            else:
                print("Aborting ROI creation..")


    def get_nut_placer(self):
        """Randomly select a ROI and a position in this ROI for nut placement.

        Args:
            None

        Returns:
            A tuple representing the row and the column in the background
            image matrix for the object to be input.
        """
        selected_delimiter = self.rois[randint(0, len(self.rois) - 1)]
        delim_row_b = selected_delimiter[1]
        delim_row_e = selected_delimiter[1] + selected_delimiter[3]
        delim_col_b = selected_delimiter[0]
        delim_col_e = selected_delimiter[0] + selected_delimiter[2]

        nut_placer_row = randint(delim_row_b, delim_row_e)
        nut_placer_col = randint(delim_col_b, delim_col_e)

        return (nut_placer_row, nut_placer_col)


    def input_nut(self, nut, threshold=50):
        """Take one object and merge it with the background image.

        Args:
            nut: A nut object representing the object to merge.
            threshold: An int representing the threshold when creating
            object mask.

        Returns:
            None
        """

        rows, cols, _channels = nut.image.shape

        nut_placer_row, nut_placer_col = self.get_nut_placer()

        roi = self.image[nut_placer_row:nut_placer_row + rows,
                         nut_placer_col:nut_placer_col + cols]

        mask, mask_inv = nut.get_mask(threshold)

        background_bg = cv2.bitwise_and(roi, roi, mask=mask_inv)
        nut_fg = cv2.bitwise_and(nut.image, nut.image, mask=mask)

        dst = cv2.add(background_bg, nut_fg)
        self.image[nut_placer_row:nut_placer_row + rows,
                   nut_placer_col:nut_placer_col + cols] = dst


    def save_background(self, save_path):
        """Save the background image.

        Args:
            save_path: A string representing the filename and location to
            save to.

        Returns:
            None
        """
        cv2.imwrite(save_path, self.image)
