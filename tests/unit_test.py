import unittest
import sys,os
sys.path.append(r'C:\Users\MaaD\Desktop\pythonCode\sportsBettingProjects')
import sportsBetAlertor_v1
#import chromedriver.exe
from sportsBetAlertor_v1 import  check_is_surebet,get_surebet_factor



class Testing(unittest.TestCase):

    # def test_string(self):
    #     a = 'some'
    #     b = 'some'
    #     self.assertEqual(a, b)

    # def test_boolean(self):
    #     a = True
    #     b = True
    #     self.assertEqual(a, b)

    def test_check_is_actual_surebet(self):

        teamA_win_odds = 1.5
        teamB_win_odds = 6.0
        draw_odds      = 8.1

        retVal_test = check_is_surebet(teamA_win_odds,teamB_win_odds,draw_odds)

        exected_return_bool = True

        self.assertEqual(retVal_test, exected_return_bool)

    def test_check_is_actual_surebet_value(self):

        teamA_win_odds = 1.5
        teamB_win_odds = 6.0
        draw_odds      = 8.1

        retVal_test = get_surebet_factor(teamA_win_odds,teamB_win_odds,draw_odds)

        exected_return_float = 0.9567

        self.assertAlmostEquals(retVal_test, exected_return_float,places=3)


    def test_check_is_non_surebet(self):

        teamA_win_odds = 2.5
        teamB_win_odds = 1.25
        draw_odds      = 3.37

        # this three-wat is not a surebet as the formula should return 1.49673
        retVal_test = check_is_surebet(teamA_win_odds,teamB_win_odds,draw_odds)

        exected_return_bool = False

        self.assertEqual(retVal_test, exected_return_bool)


    def test_check_is_non_surebet_value(self):

        teamA_win_odds = 2.5
        teamB_win_odds = 1.25
        draw_odds      = 3.37

        # this three-wat is not a surebet as the formula should return 1.49673
        retVal_test = get_surebet_factor(teamA_win_odds,teamB_win_odds,draw_odds)

        exected_return_float = 1.497

        self.assertAlmostEquals(retVal_test, exected_return_float,places=3)


#test 2 :

#    def test_unit_test2(self):


#         a = True
#         b = True
#         self.assertEqual(a, b)


# #test 3 :

#     def unit_test3(self):

#         a = True
#         b = True
#         self.assertEqual(a, b)


if __name__ == '__main__':
    print('Running unit tests on sportsbetting applicationb version 1....')
    unittest.main()








