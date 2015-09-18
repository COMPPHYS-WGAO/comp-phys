'''
   >>> di[0][1]<=di[8][0]
   True
   >>> ap[0][1]>=di[8][0]
   False
   

'''


from pprint import pprint

#        name                   dist. app.b      abs.b

data = [('Alpha Centauri A',    4.3,  0.26,      1.56), 
        ('ALpha Centauri B',    4.3,  0.77,      0.45),
        ('Alpha Centauri C',    4.2,  0.00001,   0.00006),
        ("Barnard's Star",      6.0,  0.00004,   0.0005),
        ('Wolf 359',            7.7,  0.000001,  0.00002),
        ('BD +36 degrees 2147', 8.2,  0.0003,    0.006), 
        ('Luyten 726-8 A',      8.4,  0.000003,  0.00006),
        ('Luyten 726-8 B',      8.4,  0.000002,  0.00004),
        ('Sirius A',            8.6,  1.00,      23.6),
        ('Sirius B',            8.6,  0.001,     0.003),
        ('Ross 154',            9.4,  0.00002,   0.0005)]

di = [(di[1], di[0]) for di in sorted([(d[1], d[0]) for d in data])]
ap = [(ap[1], ap[0]) for ap in sorted([(p[2], p[0]) for p in data])]
ab = [(ab[1], ab[0]) for ab in sorted([(b[3], b[0]) for b in data])]

if __name__ == "__main__":

    import doctest
    
    print '\n'
    print 'Ranked by Distance:', '\n'
    for a, b in di:
        print "{:19}, {:4}".format(a, b)
    print '\n'
    print 'Ranked by Apparent Brightness:', '\n'
    for a, b in ap:
        print "{:19}, {:4}".format(a, b)
    print '\n'
    print 'Ranked by Absolute Brightness:', '\n'
    for a, b in ab:
        print "{:19}, {:4}".format(a, b)
    print '\n'