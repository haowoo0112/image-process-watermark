import cv2
import numpy as np

class water_mark:
    """water mark operation

    Attributes:
        head_shot: a picture which we want to hide water mark in it
        living_photo: a water mark
        living_photo_r: how many rows in water mark
        living_photo_c: how many colums in water mark
        water_mark_bit: how many bits water mark we want
        result: the result of hiding water mark in the picture
    """
    def __init__(self, head_name, living_name):
        """read a head shot and a living photo"""
        self.head_shot = cv2.imread(head_name, cv2.IMREAD_GRAYSCALE)
        self.living_photo = cv2.imread(living_name, cv2.IMREAD_GRAYSCALE)
        self.living_photo_r, self.living_photo_c = self.living_photo.shape

    def generate_picture_with_water_mark(self, water_mark_bit):
        """remove several and generate a picture with water mark"""
        self.water_mark_bit = water_mark_bit;
        origin_bit = 8 - water_mark_bit

        # create 2-D array as mask which can obtain some bit we want
        origin_mask_number = ((2 ** 8)-1)-((2 ** (8-origin_bit))-1)
        water_mask_number = ((2 ** 8)-1)-((2 ** (8-water_mark_bit))-1)
        origin_mask = np.full((self.living_photo_r,self.living_photo_c), origin_mask_number, dtype = np.uint8)
        water_mask = np.full((self.living_photo_r,self.living_photo_c), water_mask_number, dtype = np.uint8)

        # obtain the water mark in living photo and right shift several bits
        water_mark = self.living_photo.copy()
        water_mark = cv2.bitwise_and(water_mark, water_mask) 
        water_mark = water_mark// (2**(8-water_mark_bit))

        # remove several bits which want to put water mark in their
        self.result = self.head_shot.copy()
        self.result = cv2.bitwise_and(self.result, origin_mask)

        # water mark is combined in the picture and store this picture
        self.result = cv2.bitwise_or(self.result, water_mark)
        cv2.imwrite('remove_'+str(water_mark_bit)+'bit.jpg', self.result)

    def obtain_water_mark_from_picture(self):
        """obtain water mark in a picture with water mark"""
        water_mask_number = (2 ** self.water_mark_bit)-1
        water_mask = np.full((self.living_photo_r,self.living_photo_c), water_mask_number, dtype = np.uint8)
        water_mark = cv2.bitwise_and(self.result, water_mask) 
        water_mark = water_mark * (2**(8-self.water_mark_bit));
        cv2.imwrite('water_mark_'+str(self.water_mark_bit)+'bit.jpg', water_mark)

if __name__ == "__main__":
    Water_Mark = water_mark('original.jpg', 'watermark.jpg')

    # generate a picture with one to three bits watermark, respectively, and take out the watermark in this picture
    for i in range(1, 4):
        Water_Mark.generate_picture_with_water_mark(i)
        Water_Mark.obtain_water_mark_from_picture()
