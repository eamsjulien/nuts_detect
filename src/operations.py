"""
Module supporting the operations functions needed for various file operations
for the Nuts Detect (ND) project.

function get_file_number: Get the number of files in a folder.
"""

import os

import cv2

def get_file_number(path):
    """Get file number for a folder.

    Args:
        path: A string representing the folder path.

    Returns:
        An int representing the number of files in a folder.
    """

    nbr = [n for n in os.listdir(path) if os.path.isfile(os.path.join(path, n))]
    return len(nbr)


def resize_image(img, resize_fact):
    """Resize an image with factor resize_fact.

    Args:
        img: A numpy array representing the image to resize.
        resize_fact: A float representing the scaling factor.

    Returns:
        An numpy array representing the resized image.
    """

    return cv2.resize(img, resize_fact)

def get_resize_prop(in_col, in_row, out_col, out_row):
    """Get the resize proportions.

    Args:
        in_col: An integer representing the column in.
        in_row: An integer representing the row in.
        out_col: An integer representing the column out.
        out_row: An integer representing the row out.

    Returns:
        A tuple representing the proportion between in and out.
    """

    col_prop = out_col / in_col
    row_prop = out_row / in_row

    return (col_prop, row_prop)

def write_item_info_file(cls, placer, itemshape, backshape, path):
    """Write item position to file.

    Args:
        cls: An integer representing the class number.
        placer: A tuple representing the obj topleft row and col.
        itemshape: A tuple representing the obj row and column size.
        backshape: A tuple representing the image height and width.
        path: A string representing the file path.

    Returns:
        None
    """

    new_x = (float(placer[1]) + (itemshape[1] / 2.0)) / float(backshape[1])
    new_y = (float(placer[0]) + (itemshape[0] / 2.0)) / float(backshape[0])
    new_wid = float(itemshape[1] / backshape[1])
    new_hgt = float(itemshape[0] / backshape[0])

    line = "{} {} {} {} {}\n".format(cls, new_x, new_y, new_wid, new_hgt)
    with open(path, 'a') as filen:
        filen.write(line)

def validate_img_number(path, nbr):
    """Validate if files are in sufficient number.

    Args:
        path: A string representing the folder to check.
        nbr: An int representing the number to compare with.

    Returns:
        A boolean True if files in path are in number nbr. Else, False.
    """

    if get_file_number(path) == nbr:
        return True
    return False
