import random
import numpy as np


class Dolphins:        ### basic dolphin class

    def __init__(self, name, sex, mom, dad):
        self.name = name
        # self.sex = random.sample(['Female', 'Male'], 1)[0]
        self.sex = sex
        self.age = 0
        self.mom = mom
        self.dad = dad
        self.death = random.gauss(35.5)
        self.refracperiod = 0

    def update(self):
        self.age += 1
        self.refracperiod += 1

    def legal(self, partner):
        if partner.sex != self.sex\
        and self.age <= 8 and partner.age <= 8\
        and np.abs(self.age - partner.age) <= 10\
        and self.mom != partner.mom and self.dad != partner.dad\
        and self.refracperiod > 5 and partner.refracperiod > 5:
            return True
        else:
            return False


# names = ['a', 'b', 'c', 'd']

# boynames = ['andy', 'joe', 'cole']
# girlnames = ['vicky', 'terra', 'gina']
#
# def name_and_sex(boys, girls):      # 'boys' and 'girls' are lists of names
#     # how about return a tuple
#     random_boys = random.sample(boys, len(boys))
#     random_girls = random.sample(girls, len(girls))
#     random_name = random.sample([boys, girls], 1)[0][0]
#
#     if random_name in boys:
#         sex = 'Male'
# #         boys.remove(random_name)  # to avoid repeating
#     elif random_name in girls:
#         sex = 'Female'
# #         girls.remove(random_name)
#     return (random_name, sex)
#
#
# ns_tuple = name_and_sex(boynames, girlnames)
# if ns_tuple[0] in boynames:
#     boynames.remove(ns_tuple[0])
# else:
#     girlnames.remove(ns_tuple[0])

# def nextgen(partner1, partner2, name_sex):  # name_sex is the returned value from function name_and_sex
#                                             # so it is a tuple
#
#     if partner1.sex == 'Male':              # both partner1 and partner2 are class objects
#         male = partner1.name                # obtained from the dictionary dolphinherds
#     else:
#         female = partner1.name
#
#     if partner2.sex == 'Male':
#         male = partner2.name
#     else:
#         female = partner2.name
#
#     if partner1.legal(partner2) == True:
#         # child_name = random.sample(names, 1)[0]
#         child_name = name_sex[0]
#         child_sex = name_sex[1]
#         dolphinherd[child_name] = Dolphins(child_name, child_sex, female, male)
#         # names.remove(child_name)
#
#         partner1.refracperiod = 0
#         partner2.refracperiod = 0

def select_name(boys, girls):
    sex = random.sample(['Male', 'Female'], 1)[0]
    if sex == 'Male':
        childname = random.sample(boys, 1)[0]
    else:
        childname = random.sample(girls, 1)[0]

    return (childname, sex)             # it returns a tuple


def nextgen(partner1, partner2, name_sex):

    if partner1.sex == 'Male':
        male = partner1.name
    else:
        female = partner1.name

    if partner2.sex == 'Male':
        male = partner2.name
    else:
        female = partner2.name

    while partner1.legal(partner2):
        child_name = name_sex[0]
        child_sex = name_sex[1]
        dolphinherd[child_name] = Dolphins(child_name, child_sex, female, male)

        partner1.refracperiod = 0
        partner2.refracperiod = 0
        break
# to initialize the very first four dolphins
# two males two females each with different parents
dolphinherd = {'Alex': Dolphins('Alex', 'Male', 'Jane', 'Irvine'),\
               'Becca': Dolphins('Becca', 'Female', 'Kate', 'Kyrie'),\
               'Chris': Dolphins('Chris', 'Male', 'Jean', 'Alen'),\
               'Dennis': Dolphins('Dennis', 'Female', 'Kim', 'Mike')}

# def generation(dict, ngen):
#     names = []
#     for i in dict:
#         names.append(i)

# r_sex = random.sample(['Female', 'Male'], 1)[0]