import unittest 
from src.equipment import * 

class TestEquimentGetWeight(unittest.TestCase):
    def test_red_plate_get_weight(self):
        """
        TC5.1: Test RedPlate = 25kg
        """
        plate = RedPlate()
        expected_value = 25 
        self.assertEqual(expected_value, plate.get_weight())

    def test_blue_plate_get_weight(self):
        """
        TC5.2: Test BluePlate = 20kg
        """
        plate = BluePlate()
        expected_value = 20 
        self.assertEqual(expected_value, plate.get_weight())

    def test_yellow_plate_get_weight(self):
        """
        TC5.3: Test YellowPlate = 15kg
        """
        plate = YellowPlate()
        expected_value = 15
        self.assertEqual(expected_value, plate.get_weight())

    def test_green_plate_get_weight(self):
        """
        TC5.4: Test GreenPlate = 10kg
        """
        plate = GreenPlate()
        expected_value = 10 
        self.assertEqual(expected_value, plate.get_weight())

    def test_white_plate_get_weight(self):
        """
        TC5.5: Test WhitePlate = 5kg
        """
        plate = WhitePlate()
        expected_value = 5
        self.assertEqual(expected_value, plate.get_weight())

    def test_small_red_plate_get_weight(self):
        """
        TC5.6: Test SmallRedPlate = 2.5kg
        """
        plate = SmallRedPlate()
        expected_value = 2.5
        self.assertEqual(expected_value, plate.get_weight())

    def test_small_blue_plate_get_weight(self):
        """
        TC5.7: Test SmallBluePlate = 2kg
        """
        plate = SmallBluePlate()
        expected_value = 2
        self.assertEqual(expected_value, plate.get_weight())

    def test_small_yellow_plate_get_weight(self):
        """
        TC5.8: Test SmallYellowPlate = 1.5kg
        """
        plate = SmallYellowPlate()
        expected_value = 1.5
        self.assertEqual(expected_value, plate.get_weight())

    def test_small_white_plate_get_weight(self):
        """
        TC5.9: Test SmallWhitePlate = 0.5kg
        """
        plate = SmallWhitePlate()
        expected_value = 0.5 
        self.assertEqual(expected_value, plate.get_weight())

    def test_clip_get_weight(self):
        """
        TC5.10: Test Clip = 2.5kg
        """
        plate = Clip()
        expected_value = 2.5 
        self.assertEqual(expected_value, plate.get_weight())

    def test_female_bar_get_weight(self):
        """
        TC5.11: Test Female = 15kg
        """
        plate = FemaleBar()
        expected_value = 15
        self.assertEqual(expected_value, plate.get_weight())

    def test_male_bar_get_weight(self):
        """
        TC5.12: Test Female = 20kg
        """
        plate = MaleBar()
        expected_value = 20
        self.assertEqual(expected_value, plate.get_weight())


# type into terminal:
# python -m unittest tests.test_equipment_get_weight -v