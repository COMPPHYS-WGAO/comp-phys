import random
import numpy as np
import re
import urllib
import matplotlib.pyplot as plt
import os.path


# initialize the directory path
boy_dir = '/Users/gaowenyi/comp-phys/'
boynames_file = boy_dir + 'boynames.txt'
girl_dir = '/Users/gaowenyi/comp-phys/'
girlnames_file = girl_dir + 'girlnames.txt'

boynames = []               # set the list of names as global
girlnames = []              # will later be iterated through and add names to them


def pullnames(text, gender):                # pullnames() operates on the two empty name lists i.e. boynames
                                            # and gives them name elements
    matchstring = 'nameDetails">.*</span>'
    for items in text:
        x = re.findall(matchstring, items)
        if len(x) > 0:
            if gender == 'Male':
                boynames.append(x[0].lstrip('nameDetails">').rstrip('</span>'))
            else:
                girlnames.append(x[0].lstrip('nameDetails">').rstrip('</span>'))
                

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


# to check if the file exists on the computer
# so that after the first call, we can extract it from our own machine --> much faster
if os.path.isfile(boynames_file):
    ''
else:          
    i = 1
    j = 1
    boyurl = 'http://www.prokerala.com/kids/baby-names/boy/page-1.html'
    girlurl = 'http://www.prokerala.com/kids/baby-names/girl/page-1.html'

    while len(boynames) < 7880:      # 7880 is the total number of the boys' names
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
        
    with open(boynames_file, 'w') as f:        # to write the list of names into a local file
        f.write(str(boynames))
    with open(girlnames_file, 'w') as f:
        f.write(str(girlnames))

    # open(boynames_file, 'w').write(str(boynames))
    # open(girlnames_file, 'w').write(str(girlnames))


class Dolphins:        ### basic dolphin class

    def __init__(self, name, sex, mom, dad):
        self.name = name
        self.sex = sex
        self.age = 0
        self.mom = mom
        self.dad = dad
        self.death = random.gauss(35, 5)
        self.refracperiod = 0

    def update(self):
        self.age += 1
        self.refracperiod += 1

    def legal(self, partner):        # all the conditions checking if its legal for the two dolphins mating
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



def nextgen(partner1, partner2, dict1, dict2, malegen, femalegen, prob):
    
    if partner1.legal(partner2):         # .legal() returns boolean
    
        if partner1.sex == 'Male':       # we decide the parent's role
            father = partner1.name       # if they are legal
        else:
            mother = partner1.name

        if partner2.sex == 'Male':
            father = partner2.name
        else:
            mother = partner2.name
                    
        p = random.random()          # generates random numbers from 0-1
        if p <= prob:                 # ideally prob should be 0.5 
            child_name = malegen.next()
            while child_name in dict1 or child_name in dict2:    # to check if the name is repeated
                child_name = malegen.next()
            dict1[child_name] = Dolphins(child_name, 'Male', mother, father)
            # this is where we create new dolphins (male)
        else:
            child_name = femalegen.next()
            while child_name in dict1 or child_name in dict2:    # to check if the name is repeated
                child_name = femalegen.next()
            dict2[child_name] = Dolphins(child_name, 'Female', mother, father)
        partner1.refracperiod = 0     # make sure the refraction period is kept tracking
        partner2.refracperiod = 0


####################################################################################

# initialize a bunch of list to collect demading data for later use
m_dolphinlist = []
f_dolphinlist = []
living_dolphins = []
min_prob_list = []
for i in range(1, 11):        #the length/range of the list should be the same as the trials we are going to have, which is 10
    m_dolphinlist.append('dolphinherd'+str(i))
    f_dolphinlist.append('dolphinherd'+str(i))
    living_dolphins.append(i)                       # each element will be overwritten/given a meaningful value later


for trial in range(10):       # to have 10 different trials, we use a giant for loop
    probability = 0           # at the begining of each trial, set prob back to 0 !
    while probability <= 0.5:
        
        malegenerator = namegenerator('Male')
        femalegenerator = namegenerator('Female')
        
        # to avoid unecessary addition into the dictionary 
        # m_dolphinlist[trial]/f_dolphinlist[trial] are going to be unique for each trial
        
        m_dolphinlist[trial] = {'Alex': Dolphins('Alex', 'Male', 'Jane', 'Irvine'),\
                                  'Chris': Dolphins('Chris', 'Male', 'Jean', 'Alen'),}
        f_dolphinlist[trial] = {'Becca': Dolphins('Becca', 'Female', 'Kate', 'Kyrie'),\
                                  'Dennis': Dolphins('Dennis', 'Female', 'Kim', 'Mike')}

        years = 0
        deaths = []
        living_dolphins[trial] = []
        while years < 150:
            mkeys = m_dolphinlist[trial].keys()
            fkeys = f_dolphinlist[trial].keys()# temp1 is the list entering the year
            breeding = 0
            #two nested for loops to check if the two are able to have baby
            for dolphin in mkeys:
                for partner in fkeys:
                    cool = nextgen(m_dolphinlist[trial][dolphin], f_dolphinlist[trial][partner], m_dolphinlist[trial], f_dolphinlist[trial], malegenerator, femalegenerator, probability)
                    # nextgen() takes 3 arguments: partner1, partner2, and current dolphin dictionary
                    if cool == 1:
                        breeding += cool
            # check if any is too old
            for elder in mkeys:
                m_dolphinlist[trial][elder].update()
                if m_dolphinlist[trial][elder].age >= m_dolphinlist[trial][elder].death:
                    if elder not in deaths:
                        deaths.append(elder)
            for elder in fkeys:
                f_dolphinlist[trial][elder].update()# check if any is too old
                if f_dolphinlist[trial][elder].age >= f_dolphinlist[trial][elder].death:
                    if elder not in deaths:
                        deaths.append(elder)

            # set_trace()
            mkeys2 = m_dolphinlist[trial].keys()  #keys2 are the list of dolphins at the end of the year, does not include deaths
            fkeys2 = f_dolphinlist[trial].keys()
            living_dolphins[trial].append(len(mkeys2) + len(fkeys2)-len(deaths)) # net number of dolphins at the end of the year
            # living_dolphins[trial] is the list of number of dolphins of each year for each trial
            # print len(temp2)
            if years == 25:
                year25 = (years, len(mkeys2) + len(fkeys2)-len(deaths), abs(len(mkeys2) + len(fkeys2)-len(mkeys)-len(fkeys)))
            if years == 50:
                year50 = (years, len(mkeys2) + len(fkeys2)-len(deaths), abs(len(mkeys2) + len(fkeys2)-len(mkeys)-len(fkeys)))
            if years == 75:
                year75 = (years, len(mkeys2) + len(fkeys2)-len(deaths), abs(len(mkeys2) + len(fkeys2)-len(mkeys)-len(fkeys)))
            if years == 100:
                year100 = (years, len(mkeys2) + len(fkeys2)-len(deaths), len(mkeys2)+len(fkeys2)-4)
            if years == 125:
                year125 = (years, len(mkeys2) + len(fkeys2)-len(deaths), abs(len(mkeys2) + len(fkeys2)-len(mkeys)-len(fkeys)))
            if years == 149:
                year149 = (years, len(mkeys2) + len(fkeys2)-len(deaths))
                min_prob_list.append(probability)
                probability = 1
                break
            years += 1
            if len(mkeys2) + len(fkeys2)-len(deaths) == 0:
                probability += 0.01
                break
        if years == 149:
            print('Trial No.', trial+1)
            print '#'*50 
            print("Entering year {:d} with {:d} dolphins, with {:d} breeding.".format(*year25))
            print('#'*50)
            print("Entering year {:d} with {:d} dolphins, with {:d} breeding.".format(*year50))
            print('#'*50)
            print("Entering year {:d} with {:d} dolphins, with {:d} breeding.".format(*year75))
            print('#'*50)
            print("At year {:d}, there are {:d} living dolphins.\nthere have been {:d} births, in total.".format(*year100))
            print("#"*50)
            print("At year {:d}, there are {:d} living dolphins.".format(*year149))

            
print '\n'
avg_min = np.mean(min_prob_list)
print 'The minimum probability of producing males is about', avg_min*100., '%'

avg_std = []
for i in range(years):
    avg_std.append((np.mean([j[i] for j in living_dolphins]), np.std([j[i] for j in living_dolphins])))
    # it gives a list of tuples
std_above = [i+j for i, j in avg_std]
std_below = [i-j for i, j in avg_std]
avg = [i[0] for i in avg_std]

x = np.arange(0, 149, 1)
plt.plot(x, avg, 'r')

plt.fill_between(x, std_above, std_below)
plt.show()


