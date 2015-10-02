
import random
import datetime as dt


class whale:
    
    def __init__(self, name):
        self.name = name
        self.sex = random.sample(['female', 'male'], 1)[0]
        self.born = dt.datetime.now()
        print 'A {:s} whale named {:s} is born!'.format(self.sex, self.name)

    def age(self):
        present = dt.datetime.now()
        return present - self.born
    
    def sing(self):
        return '\a'*5
        
    def __str__(self):
        return 'A whale named {:s} (age {:s})'.format(self.name, str(self.age()))

names = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'i', 'j', 'k', 'l', 'm', 'n', 'o'\
        'p', 'q', 'r', 's', 't', 'u']
whales = []

for i in names:
    whales.append(whale(i))

print whales

w = whale('Splash')
print w.age()
print w.sing()

