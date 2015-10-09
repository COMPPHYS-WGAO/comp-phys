import random
import numpy as np


class Dolphins:

    def __init__(self, name, mom, dad):
        self.name = name
        self.sex = random.sample(['Female', 'Male'], 1)[0]
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


names = ['a', 'b', 'c', 'd']
childs = {}
def nextgen(partner1, partner2):

    if partner1.sex == 'Male':
        male = partner1.name
    else:
        female = partner1.name

    if partner2.sex == 'Male':
        male = partner2.name
    else:
        female = partner2.name

    if partner1.legal(partner2) == True:
        child_name = random.sample(names, 1)[0]
        dolphinherd[child_name] = Dolphins(child_name, random.sample(["Male", "Female"], 1)[0], female, male)
        names.remove(child_name)
        partner1.refracperiod = 0
        partner2.refracperiod = 0


dolphinherd = {'Alex': Dolphins('Alex', 'male', 'Jane', 'Irvine'),\
               'Becca': Dolphins('Becca', 'female', 'Kate', 'Kyrie'),\
               'Chris': Dolphins('Chris', 'male', 'Jean', 'Alen'),\
               'Dennis': Dolphins('Dennis', 'female', 'Kim', 'Mike')}


r_sex = random.sample(['Female', 'Male'], 1)[0]