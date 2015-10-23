import random
import numpy as np
import re
import urllib
import matplotlib.pyplot as plt
import os.path
import networkx as nx


boy_dir = '/Users/gaowenyi/comp-phys/'
boynames_file = boy_dir + 'boynames.txt'
girl_dir = '/Users/gaowenyi/comp-phys/'
girlnames_file = girl_dir + 'girlnames.txt'

boynames = []               # set the list of names as global
girlnames = []              # will later be iterated through and add names to them


def pullnames(text, gender):                # pullnames() operates on the two empty name lists i.e. boynames
                                            # and gives them name elements
    matchstring = 'nameDetails">.*</span>'
    if gender == 'Male':
        namelist = []
        for items in text:
            x = re.findall(matchstring, items)
            if len(x) > 0:
                namelist.append(x[0])
        for stuff in namelist:
            new_stuff = stuff.lstrip('nameDetails">').rstrip('</span>')
            boynames.append(new_stuff)
    else:
        namelist = []
        for items in text:
            x = re.findall(matchstring, items)
            if len(x) > 0:
                namelist.append(x[0])
        for stuff in namelist:
            new_stuff = stuff.lstrip('nameDetails">').rstrip('</span>')
            girlnames.append(new_stuff)
                

def namegenerator(sex):
    x = 0
    y = 0
    if sex == 'Male':
        with open(boynames_file, 'r') as f:
            boynames = eval(f.read())               # though boynames is repeatedly used
        while x < len(boynames)-1:              # it gets overwritten inside of the function
            yield boynames[x]                   # it only refers to a value
            x += 1
    else:
        with open(girlnames_file, 'r') as f:
            girlnames = eval(f.read())       
        while y < len(girlnames)-1:
            yield girlnames[y]
            y += 1



if os.path.isfile(boynames_file):
    ''
else:
            
    i = 1
    j = 1
    boyurl = 'http://www.prokerala.com/kids/baby-names/boy/page-1.html'
    girlurl = 'http://www.prokerala.com/kids/baby-names/girl/page-1.html'

    while len(boynames) < 7880:
        x = boyurl.replace('1', str(i))
        xinfile = urllib.urlopen(x)
        xlines = xinfile.readlines()  # xlines is a list of lines that can be iterated through by pullnames()
        xinfile.close()
        pullnames(xlines, 'Male')
        i += 1
        print i

    while len(girlnames) < 5974:
        y = girlurl.replace('1', str(j))
        yinfile = urllib.urlopen(y)
        ylines = yinfile.readlines()  # xlines is a list of lines that can be iterated through by pullnames()
        yinfile.close()
        pullnames(ylines, 'Female')
        j += 1
        print j
    with open(boynames_file, 'w') as f:
        f.write(str(boynames))
    with open(girlnames_file, 'w') as f:
        f.write(str(girlnames))

    # open(boynames_file, 'w').write(str(boynames))
    # open(girlnames_file, 'w').write(str(girlnames))


class Dolphins:        ### basic dolphin class

    def __init__(self, name, sex, mom, dad):
        self.name = name
        # self.sex = random.sample(['Female', 'Male'], 1)[0]
        self.sex = sex
        self.age = 0
        self.mom = mom
        self.dad = dad
        self.death = random.gauss(35, 5)
        self.refracperiod = 0

    def update(self):
        self.age += 1
        self.refracperiod += 1

    def legal(self, partner):
        if partner.sex != self.sex\
        and self.age >= 8 \
        and partner.age >= 8\
        and np.abs(self.age - partner.age) <= 10\
        and self.mom != partner.mom \
        and self.dad != partner.dad\
        and self.refracperiod > 5 \
        and partner.refracperiod > 5\
        and self.age <= self.death\
        and partner.age <= partner.death:
            return True
        else:
            return False



def nextgen(partner1, partner2, dict1, dict2, malegen, femalegen):

    if partner1.sex == 'Male':
        father = partner1.name
    else:
        mother = partner1.name

    if partner2.sex == 'Male':
        father = partner2.name
    else:
        mother = partner2.name

    if partner1.legal(partner2):                # .legal() returns boolean
        child_sex = random.sample(['Male', 'Female'], 1)[0]
        if child_sex == 'Male':
            child_name = malegen.next()
            dict1[child_name] = Dolphins(child_name, child_sex, mother, father)
        if child_sex == 'Female':
            child_name = femalegen.next()
            dict2[child_name] = Dolphins(child_name, child_sex, mother, father)
        partner1.refracperiod = 0
        partner2.refracperiod = 0
        # return 'A {:s} baby dolphin named {:s} is bron!'.format(child_sex, child_name)
        return 1


####################################################################################

m_dolphinlist = []
f_dolphinlist = []# initialize to track dictionary at the end of each trial
living_dolphins = []
dolphin_pop_75 = []
for i in range(1, 11):
    m_dolphinlist.append('dolphinherd'+str(i))
    f_dolphinlist.append('dolphinherd'+str(i))
    living_dolphins.append(i)                       # each element will be overwritten/given a meaningful value later


for trial in range(10):
    print('Trial No.', trial+1)

    malegenerator = namegenerator('Male')
    femalegenerator = namegenerator('Female')

    m_dolphinlist[trial] = {'Alex': Dolphins('Alex', 'Male', 'Jane', 'Irvine'),\
                              'Chris': Dolphins('Chris', 'Male', 'Jean', 'Alen'),}
    f_dolphinlist[trial] = {'Becca': Dolphins('Becca', 'Female', 'Kate', 'Kyrie'),\
                              'Dennis': Dolphins('Dennis', 'Female', 'Kim', 'Mike')}

    years = 0
    breeding = 0
    deaths = []
    living_dolphins[trial] = []
    while years < 150:
        mkeys = m_dolphinlist[trial].keys()
        fkeys = f_dolphinlist[trial].keys()# temp1 is the list entering the year
        # print len(temp1)
        breeding = 0
        for dolphin in mkeys:
            for partner in fkeys:
                cool = nextgen(m_dolphinlist[trial][dolphin], f_dolphinlist[trial][partner], m_dolphinlist[trial], f_dolphinlist[trial], malegenerator, femalegenerator)
                # nextgen() takes 3 arguments: partner1, partner2, and current dolphin dictionary
                if cool == 1:
                    breeding += cool
        for elder in mkeys:
            m_dolphinlist[trial][elder].update()# check if any is too old
            if m_dolphinlist[trial][elder].age >= m_dolphinlist[trial][elder].death:
                if elder not in deaths:
                    deaths.append(elder)
        for elder in fkeys:
            f_dolphinlist[trial][elder].update()# check if any is too old
            if f_dolphinlist[trial][elder].age >= f_dolphinlist[trial][elder].death:
                if elder not in deaths:
                    deaths.append(elder)

        # set_trace()
        mkeys2 = m_dolphinlist[trial].keys()
        fkeys2 = f_dolphinlist[trial].keys()
        living_dolphins[trial].append(len(mkeys2) + len(fkeys2)-len(deaths))
        # living_dolphins[trial] is the list of number of dolphins of each year for each trial
        # print len(temp2)
        if years % 25 == 0:
            print("#"*50)
            print("Entering year {:d} with {:d} dolphins, with {:d} breeding.".format(years, len(mkeys) + len(fkeys)-len(deaths), abs(len(mkeys2) + len(fkeys2)-len(mkeys)-len(fkeys))))
        if years == 75:
            m_copy = m_dolphinlist[trial].copy()
            f_copy = f_dolphinlist[trial].copy()
            m_copy.update(f_copy)
            map(m_copy.pop, deaths)
            dolphin_pop_75.append(m_copy)
        if years == 100:
            print("At year {:d}, there are {:d} living dolphins.\nthere have been {:d} births, in total.".format(years, len(mkeys2) + len(fkeys2)-len(deaths), len(mkeys2)+len(fkeys2)-4))
        if years == 149:
            print("#"*50)
            print("At year {:d}, there are {:d} living dolphins.".format(years, len(mkeys2) + len(fkeys2)-len(deaths)))
        years += 1

    print('\n'*2)

rand = random.randrange(0, 10)

dolphin_pop = {}
dolphin_pop.update(dolphin_pop_75[rand])


main_char = (random.sample(dolphin_pop, 1))[0]
main_mom = dolphin_pop[main_char].mom
main_dad = dolphin_pop[main_char].dad

# full_sib_dad = [(main_char, main_dad)]
# full_sib_mom = [(main_char, main_mom)]
full_sib = []
mom_half = []
dad_half = []

for dolph in dolphin_pop:
    if dolphin_pop[dolph].mom == main_mom and dolphin_pop[dolph].dad == main_dad:
#         full_sib_mom.append((main_mom, dolph))
#         full_sib_dad.append((main_dad, dolph))
        full_sib.append(dolph)
    elif dolphin_pop[dolph].mom == main_mom:
#         mom_half.append((main_mom, dolph))
        mom_half.append(dolph)
    elif dolphin_pop[dolph].dad == main_dad:
#         dad_half.append((main_dad, dolph))
        dad_half.append(dolph)
        
# print full_sib_dad, full_sib_mom, mom_half, dad_half
print full_sib, mom_half, dad_half

G = nx.Graph()

G.add_node(main_mom, pos=(0, 3))
G.add_node(main_dad, pos=(1, 3))

xh = 0.5
xf = 0

for i in dolphin_pop:
    if i in mom_half:
        G.add_node(i, pos=(xh, 1))
        G.add_edge(i, main_mom)
        xh += 1
    if i in dad_half:
        G.add_node(i, pos=(xh, 1))
        G.add_edge(i, main_dad)
        xh += 1
    if i in full_sib:
        G.add_node(i, pos=(xh, 2))
        G.add_edge(i, main_mom)
        G.add_edge(i, main_dad)
        xf += 1
        
pos = nx.get_node_attributes(G, 'pos')

nx.draw(G, pos)

plt.show()
    

