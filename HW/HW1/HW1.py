import time
from typing import Union, List

import numpy as np
import random
from itertools import product

# ~~~~~~~~~~~~~~~ Problem 2 ~~~~~~~~~~~~~~~
# Consider a set of four six-sided dice. Describe the ensemble of outcomes of a roll of
# these dice in the case where a) they are ordered, and b) they are unordered. What is
# the probability of rolling four fair six-sided dice and obtaining a sum which is equal to
# 17? You can do this either analytically (dif cult but not impossible; perhaps a table?) or
# empirically (write a little Monte Carlo program and estimate it?)


def problem_2_method_1():
    unordered_combinations = []
    ordered_combinations = []
    all_ordered_combinations = []
    total_combinations = 0
    total_ordered_combinations = 0

    for a in range(1, 7):  # [1, 2, 3, 4, 5, 6]
        for b in range(1, 7):
            for c in range(1, 7):
                for d in range(1, 7):
                    total_combinations += 1
                    combination = [a, b, c, d]
                    ordered = sorted(combination)
                    if ordered not in all_ordered_combinations:
                        all_ordered_combinations.append(ordered)
                    if a + b + c + d == 17:
                        unordered_combinations.append(combination)
                        if ordered not in ordered_combinations:
                            ordered_combinations.append(ordered)
    problem_2_print_results(unordered_combinations, ordered_combinations, all_ordered_combinations, total_combinations)


def problem_2_method_2():
    unordered_combinations = []
    ordered_combinations = []
    all_ordered_combinations = []
    total_combinations = 0

    for combination in product(range(1, 7), repeat=4):
        total_combinations += 1
        ordered = sorted(combination)
        if ordered not in all_ordered_combinations:
            all_ordered_combinations.append(ordered)
        if sum(combination) == 17:
            unordered_combinations.append(combination)
            if ordered not in ordered_combinations:
                ordered_combinations.append(ordered)
    problem_2_print_results(unordered_combinations, ordered_combinations, all_ordered_combinations, total_combinations)


def problem_2_print_results(unordered_combinations, ordered_combinations, all_ordered_combinations, total_combinations):
    print(f"Total number of combinations: {total_combinations}")
    print(f"Total number of ordered combinations: {len(all_ordered_combinations)}")
    print(f"Total number of combinations that add to 17: {len(unordered_combinations)}")
    print(f"Total number of ordered combinations that add to 17: {len(ordered_combinations)}")
    probability_unordered = round(len(unordered_combinations) / total_combinations, 3)
    probability_ordered = round(len(ordered_combinations) / len(all_ordered_combinations), 3)
    print(f"Probability of getting 17: {probability_unordered}")
    print(f"Probability of getting 17 out of ordered combinations: {probability_ordered}")
    print(f"The ordered solutions: {' '.join(str(ordered_combinations))}")


# problem_2_method_1()
# problem_2_method_2()
"""Results: 
Total number of combinations: 1296
Total number of ordered combinations: 126
Total number of combinations that add to 17: 104
Total number of ordered combinations that add to 17: 9
Probability of getting 17: 0.08
Probability of getting 17 out of ordered combinations: 0.071
The ordered solutions: [1, 4, 6, 6], [1, 5, 5, 6], [2, 3, 6, 6], 
                       [2, 4, 5, 6], [2, 5, 5, 5], [3, 3, 5, 6], 
                       [3, 4, 4, 6], [3, 4, 5, 5], [4, 4, 4, 5]
"""


# ~~~~~~~~~~~~~~~ Problem 3 ~~~~~~~~~~~~~~~
# In the production of a top-antitop event in a hadron collider, assume that the top and
# antitop quarks each decay to a W and a b quark. One W decays to two quarks, and the
# other one decays to a lepton (e or mu) plus a neutrino. Thus the nal observed state is
# a lepton, missing transverse momentum from the neutrino, and four jets (two of which
# are b jets). You would like to properly assign the observed objects to their parent top or
# antitop quark (the charge of the lepton determines which is which), but there are clearly
# many combinations. If we know which jets are from b quarks (“b-tagged”) we can re-
# duce the number of combinations. However, the efficiency for tagging b quark jets as
# such is not 100%. How many combinations are there, in fact, when you have a) zero b-
# tagged jets, b) one b-tagged jet, and c) two b-tagged jets? Assume that when you tag a
# jet, you are in fact tagging a real b jet.


def problem_3_method_1():
    """Brute force method for specifically 4 jets and 0, 1, or 2 b-jets"""
    possible_number_of_b_jets = list(range(2))
    number_of_jets = 4
    possible_jet_combinations = []  # will be a list of lists indexed by how many b-jets

    for number_of_b_jets in possible_number_of_b_jets:
        if number_of_b_jets == 0:
            print(f"For the case with zero b-jets, the only option is to have all four jets be ordinary quark jets.")
            possible_jet_combinations.append([[False, False, False, False]])
        elif number_of_b_jets == 1:
            one_jet_combinations_list = []
            for jet in list(range(4)):
                combination = [True if i == jet else False for i in list(range(4))]
                one_jet_combinations_list.append(combination)
            possible_jet_combinations.append(one_jet_combinations_list)
        else:
            two_jet_combinations_list = []
            for jet_1 in list(range(4)):
                for jet_2 in list(range(4)):
                    combination = [True if i in [jet_1, jet_2] and jet_1 != jet_2 else False for i in list(range(4))]
                    if True in combination and combination not in two_jet_combinations_list:
                        two_jet_combinations_list.append(combination)
            possible_jet_combinations.append(two_jet_combinations_list)
    problem_3_print_results(possible_jet_combinations)


def problem_3_method_2():
    """A general function for any number of jets and b-jets"""
    possible_number_of_b_jets = list(range(3))  # [0, 1, 2]
    number_of_jets = 4
    possible_jet_combinations = []  # will be a list of lists indexed by how many b-jets

    for number_of_b_jets in possible_number_of_b_jets:
        if number_of_b_jets == 0:
            print(
                f"For the case with zero b-jets, the only option is to have all four jets be ordinary quark jets.")
            possible_jet_combinations.append([[False, False, False, False]])
        elif number_of_b_jets == 1:
            one_jet_combinations_list = []
            for jet in list(range(4)):
                combination = [True if i == jet else False for i in list(range(4))]
                one_jet_combinations_list.append(combination)
            possible_jet_combinations.append(one_jet_combinations_list)
        else:
            jet_combinations_list = []
            for combination in product(list(range(number_of_jets)), repeat=number_of_b_jets):
                # iteritems.product gives tuples like (0, 0), (0, 1), .... (3, 3) with a number of elements
                # equal to the value of the "repeat" field
                def condition(i):
                    # i is an integer
                    # sets contain only unique elements, so second conditions checks for duplicates like (3, 3)
                    return i in combination and len(combination) == len(set(combination))
                # sets the elements of the list equal to the index of list(range()) to be True
                b_jets = [True if condition(i) else False for i in list(range(number_of_jets))]
                if True in b_jets and b_jets not in jet_combinations_list:
                    jet_combinations_list.append(b_jets)
            possible_jet_combinations.append(jet_combinations_list)
    problem_3_print_results(possible_jet_combinations)


def problem_3_print_results(possible_jet_combinations):
    for i in possible_jet_combinations:
        print(f"Possible combinations for {possible_jet_combinations.index(i)} jets:")
        for count, j in enumerate(i):
            print(f"{j}", end=" ")
            if possible_jet_combinations.index(i) > 0:
                if count > 1 and (count + 1) % 3 == 0:
                    print('')
        print('\n')


# problem_3_method_2()

"""Result
For the case with zero b-jets, the only option is to have all four jets be ordinary quark jets.
Possible combinations for 0 jets:
[False, False, False, False] 

Possible combinations for 1 jets:
[True, False, False, False] [False, True, False, False] [False, False, True, False] 
[False, False, False, True] 

Possible combinations for 2 jets:
[True, True, False, False] [True, False, True, False] [True, False, False, True] 
[False, True, True, False] [False, True, False, True] [False, False, True, True] 

"""


# ~~~~~~~~~~~~~~~ Problem 4 ~~~~~~~~~~~~~~~
# An isolated island practices a strange form of birth control where couples have chil-
# dren until they have a boy, and then they stop. If 52% of all live births are girls, then af-
# ter many generations what will the male/female ratio on the island be? Assume males
# and females have equal life expectancy. You may answer this either using pure logic or
# perhaps you might perform a simple computer simulation.


def problem_4():
    year = 0  # I don't know how far we are required to go with the realism here but I'll have some fun
    end_of_the_world = 1000  # This is the year the world will end.
    gender_ratio_log = []  # Gender ratio per year
    population_log = []  # Population count per year
    chance_of_girl = 0.52

    class Community:
        def __init__(self):
            self.citizen_counter = 1
            self.citizens: List[Citizen] = []
            self.marriage_pool = []
            self.want_children = []
            self.birth_record = {}

    community = Community()  # Every citizen in the country will live together in this list

    class Citizen:
        def __init__(self, community):
            self.citizen_id = community.citizen_counter
            community.citizens.append(self)
            community.citizen_counter += 1
            if random.random() <= chance_of_girl:
                self.gender = "Female"
                self.male = False
                self.female = True
            else:
                self.gender = "Male"
                self.male = True
                self.female = False
            community.birth_record.setdefault(year, [self]).append(self)
            self.birthyear = year
            self.partner = None
            self.marriage_year = None
            self.children = []

        def age(self):
            age = year - self.birthyear
            return age

    def get_citizen(citizen_id):
        for citizen in community.citizens:
            if citizen.citizen_id == citizen_id:
                return citizen

    def get_married(citizen):
        for potential_match in community.marriage_pool:
            if citizen == potential_match:
                continue  # apparently getting married to yourself is called "sologamy"
            if citizen.gender == potential_match.gender:
                continue  # I'm sorry we don't allow same-gender marriage either
            community.marriage_pool.remove(citizen)
            community.marriage_pool.remove(potential_match)
            citizen.partner = potential_match
            potential_match.partner = citizen
            citizen.marriage_year = potential_match.marriage_year = year
            if citizen.female:
                community.want_children.append(citizen)
            else:
                community.want_children.append(potential_match)
            # print(citizen.age(), potential_match.age())
            # print(f"[{year}] Citizens {citizen.citizen_id} and {potential_match.citizen_id} got married!")
            return

    def have_a_child(community, citizen):
        if year - citizen.marriage_year < 1:
            return  # Slow down a bit! Wait at least a year to have a child
        new_baby = Citizen(community)
        if new_baby.male:
            community.want_children.remove(citizen)
        community.citizens.append(new_baby)
        citizen.children.append(new_baby)
        citizen.partner.children.append(new_baby)
        # print(f"[{year}] A new baby {'boy' if new_baby.male else 'girl'} was born! Please welcome "
        #       f"citizen number {new_baby.citizen_id} to the community! "
        #       f"--> {[j.gender for j in citizen.children]}")

    def permanently_retire_from_life(community, citizen):
        # print(citizen.age())
        if citizen.age() == 80:  # At the age of 80 they permanently retire from the community (and life in general)
            # print(citizen.age() == 80)
            # print(year, citizen.birthyear, citizen.age())
            # print(year)
            community.citizens.remove(citizen)
            # print('dead')
            # print(f"[{year}] Citizen number {citizen.citizen_id} has permanently retired from the community.")

    print("Generating population")
    # Start off with 100 citizens
    for i in range(100):
        community.citizens.append(Citizen(community))
    initial_males = sum(i.male for i in community.citizens)
    initial_females = sum(i.female for i in community.citizens)
    print(f"Suddenly in the year zero, {initial_males} males and {initial_females} females popped into existence!")
    if not initial_males or not initial_females:
        print("Oh no! Your population is very lopsided and has only males or females. It has no chance of survival.")
        return

    year = 18
    while True:
        for citizen in community.birth_record.get(year-20, []):
            community.marriage_pool.append(citizen)
        for citizen in community.marriage_pool:
            get_married(citizen)
        for citizen in community.want_children:
            have_a_child(community, citizen)
        for citizen in community.birth_record.get(year-80, []):
            # print(citizen)
            permanently_retire_from_life(community, citizen)
        if not community.citizens:
            break
        number_of_females = sum(i.female for i in community.citizens)
        number_of_males = sum(i.male for i in community.citizens)
        gender_ratio_log.append(round(number_of_females / (number_of_males + number_of_females), 4))
        population_log.append(number_of_males + number_of_females)
        year += 1
        if year % 100 == 0:
            print(f"Year {year-1} --> Year {year}    {population_log[-1]} ({gender_ratio_log[-1]})")
    for citizen in community.citizens:
        print(citizen.age())




problem_4()




