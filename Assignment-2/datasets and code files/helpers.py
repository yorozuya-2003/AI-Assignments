# module imports
import numpy as np
import pandas as pd
import math
from datetime import datetime
import matplotlib.pyplot as plt

import warnings
warnings.filterwarnings('ignore')

# taking input for the number of students per TA
students_per_ta = int(input('1 TA per credit per approximately how many students = '))


def credit(LTP):
    ''''
    Calculates the number of credits for a course
    '''
    l,t,p = map(int, LTP.split('-'))
    return l + t + p/2


def min_TA(num_students, LTP=None, credits=None, studs_per_TA=students_per_ta):
    '''
    Calculates the minimum number of TAs required for a course
    '''
    if num_students < 20:
        return 0
    
    if credits is not None:
        res = math.ceil((num_students * credits) / studs_per_TA)
        return max(res, math.ceil(num_students/100))

    res = math.ceil((num_students * credit(LTP)) / studs_per_TA)   
    return max(res, math.ceil(num_students/100))


def offered_for(s):
    '''
    Splits the string of programs offered for a course into a list
    '''
    return list(s.split(', '))


def generate_combinations(l, n):
    '''
    Generates all possible combinations of length n from list l
    '''
    from itertools import combinations as c
    res = list(map(list, c(l, n)))

    return res

# priority of programs
program_comparison = {
    'UG-1': 0,
    'UG-2': 0,
    'UG-3': 1,
    'UG-4': 2,
    'MTech-1': 3,
    'PhD-1': 3,
    'MTech-PhD-1': 3,
    'MTech-2': 4,
    'PhD-2': 5,
    'MTech-PhD-2': 5,
    'PhD-3': 5,
    'MTech-PhD-3': 5,
    'MTech-4': 5,
    'PhD-4': 5,
    'MTech-PhD-4': 5,
    'MTech-5': 5,
    'PhD-5': 5,
}


def check_offered_for(ta_rollno, offer):
    '''
    Checks if the TA is eligible for the course by comparing the program priority
    '''
    for each in offer:
        if program_comparison[each] >= get_program_preference(ta_rollno):
            return False
    return True


def get_program_preference(rollno):
    '''
    Checks the program of the TA and returns the priority
    '''
    code = rollno[:3]
    if code == 'B21':
        return 1
    elif code == 'B20':
        return 2
    elif code == 'M23' or code == 'P23' or code == 'D23':
        return 3
    elif code == 'M22':
        return 4
    return 5


def check_ug(combo):
    '''
    Checks if the combination has more than 60% UG students
    '''
    if len(combo) == 0:
        return True
    num = 0
    for each in combo:
        if each[2][0] == 'B':
            num += 1
    if num / len(combo) > 0.6:
        return False
    
    return True


def check_pg(combo, num_students):
    '''
    Checks if the combination has satisfies the required number of PG students
    '''
    if len(combo) == 0:
        return True
    
    num_students /= 100
    num = 0
    for each in combo:
        if each[2][0] != 'B' and each[2][0] != 'M':
            num += 1
            if num >= num_students:
                return True
    return False


def check_grade(combo):
    '''
    Checks if the combination has only A, A- and B grades
    '''
    for each in combo:
        grade = each[3]
        if grade not in ['A', 'A-', 'B']:
            return False
    return True
