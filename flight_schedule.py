airports = {'DCA': 'Washington, D.C.', 'IAD': 'Dulles', \
            'LHR': 'London-Heathrow', 'SVO': 'Moscow', \
            'CDA': 'Chicago-Midway', 'SBA': 'Santa Barbara', \
            'LAX': 'Los Angeles','JFK': 'New York City', \
            'MIA': 'Miami', 'AUM': 'Austin, Minnesota'}

# airline, number, heading to, gate, time (decimal hours) 
flights = [('Southwest',145,'DCA',1,6.00),\
           ('United',31,'IAD',1,7.1),('United',302,'LHR',5,6.5),\
           ('Aeroflot',34,'SVO',5,9.00),('Southwest',146,'CDA',1,9.60),\
           ('United',46,'LAX',5,6.5), ('Southwest',23,'SBA',6,12.5), ('United',2,'LAX',10,12.5),\
           ('Southwest',59,"LAX",11,14.5),\
           ('American', 1,'JFK',12,11.3),('USAirways', 8,'MIA',20,13.1),\
           ('United',2032,'MIA',21,15.1),('SpamAir',1,'AUM',42,14.4)]

# Part I

print 'Flight', '\t'+'\t', 'Destination', '\t'+'\t', 'Gate', '\t', 'Time'
print '-'*57
for i in flights:
    a = airports[i[2]]
    if len(a)<=6:
        a += '\t'*2
    elif len(a)>6 and len(a)<=15:
        a += '\t'
    print i[0]+' '+str(i[1]), '\t', a, '\t', i[3], '\t', i[4]


#Part II

bl = []


for i in flights:
    sl = list(i)
    sl.insert(0,i[4])
    bl.append(sl)
new_flights = sorted(bl)


print 'Flight', '\t'+'\t', 'Destination', '\t'+'\t', 'Gate', '\t', 'Time'
print '-'*57
for i in new_flights:
    a = airports[i[3]]
    if len(a)<=6:
        a += '\t'*2
    elif len(a)>6 and len(a)<=15:
        a += '\t'
    print i[1]+' '+str(i[2]), '\t', a, '\t', i[4], '\t', i[5]

#Part III

n_flights = sorted(flights, key=lambda tup: tup[4])

print 'Flight', '\t'+'\t', 'Destination', '\t'+'\t', 'Gate', '\t', 'Time'
print '-'*57
for i in n_flights:
    a = airports[i[2]]
    if len(a)<=6:
        a += '\t'*2
    elif len(a)>6 and len(a)<=15:
        a += '\t'
    print i[0]+' '+str(i[1]), '\t', a, '\t', i[3], '\t', i[4]


