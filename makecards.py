#!/usr/bin/env python
import csv

BASENAME = 'gut_check'
CSVFILE  = 'microbiomecardsv8.csv'

header   = open('header.tex').read()
template = open('card_template.tex').read()
footer   = open('footer.tex').read()

f = open( 'gut_check_cards.tex', 'w' )

f.write( header )

page = []

for n,record in enumerate(csv.reader(open(CSVFILE))) :
    if n == 0 : continue
   
    cardtype,cardclass,name,description,resistance,flavor,pos,neg,other = record
    
    if cardtype == 'Microbe'    : color = 'orange'
    if cardtype == 'Event'      : color = 'pink'
    if cardtype == 'Infection'  : color = 'yellow'
    if cardtype == 'Plasmid'    : color = 'magenta'
    if cardtype == 'Checkup'    : color = 'teal'
    
    
    drugs = []
    for drug in resistance.strip().split(',') :
        if len(drug) <= 1 : continue
        drugs.append(drug.strip())
    
    if len(drugs) == 0 and cardtype == 'Microbe' : drugtext = 'Not resistant\n'
    if len(drugs) >  0 and cardtype == 'Microbe' :
        drugtext = 'Resistance: \\begin{itemize}\n'
        for drug in drugs :
            drugtext = drugtext + '\\item ' + drug + '\n'
        drugtext = drugtext + '\\end{itemize}\n'

    if cardtype == 'Event' : drugtext = ''
    
    # This creates a list containing the attributes that don't need to be modified by conditional statements
      
    conditions = [('__COLOR__', color),('__CARDTITLE__', cardtype),('__TOPTITLE__', cardclass),('__NAME__', name), 
    ('__DESC__', description), ('__RESISTANCE__', drugtext), ('__FLAVOR__', flavor)]
    
    #this appends the conditions list as required for values in pos and neg fields (__CIRCLE__ in template)
    
    circle = "no"
    
    if pos !="0" and neg !="0" :
        circle = "yes"
        conditions.append(( '__CIRCLE__', '\\draw[green,fill=green] (3.7,.75) circle (4ex); \\node at (3.7,0.75) {\\LARGE \\bfseries __POS__}; \\draw[red,fill=red] (5.2,.75) circle (4ex); \\node at (5.2,0.75) {\\LARGE \\bfseries __NEG__};'))
        conditions.append(('__POS__', pos))
        conditions.append(('__NEG__', neg))
        
    if pos !="0" and neg =="0" :
        circle = "yes"
        conditions.append(( '__CIRCLE__', '\\draw[green,fill=green] (3.7,.75) circle (4ex); \\node at (3.7,0.75) {\\LARGE \\bfseries __POS__};'))
        conditions.append(('__POS__', pos))
        
    if neg !="0" and pos =="0" :
        circle = "yes"
        conditions.append(('__CIRCLE__', '\\draw[red,fill=red] (5.2,.75) circle (4ex); \\node at (5.2,0.75) {\\LARGE \\bfseries __NEG__};'))
        conditions.append(('__NEG__', neg))   
    
    if circle == "no":
        conditions.append(('__CIRCLE__', ""))  
    
    #this puts values from the "other" column in csv file into the __FOOD__ part of template
     
    food = "no"
    
    if other !="0" :
        food = "yes"
        conditions.append(( '__FOOD__', '\\draw[pink,fill=pink] (2.15,.75) circle (4ex); \\node at (2.15,0.75) {\\LARGE \\bfseries __OTHER__};'))
        conditions.append(('__OTHER__', other))
    
    if food == "no":
        conditions.append(('__FOOD__', ""))
    
    
    
    thiscard = template.replace(conditions[0][0],conditions[0][1])
    
    for i in conditions[1:]:
        thiscard = thiscard.replace(i[0],i[1])
        
    page.append(thiscard)
    
   # print thiscard
#     
#     page.append(template.replace( '__COLOR__',         color ) \
#                         .replace( '__CARDTITLE__',  cardtype ) \
#                         .replace( '__TOPTITLE__',  cardclass ) \
#                         .replace( '__NAME__',           name ) \
#                         .replace( '__DESC__',    description ) \
#                         .replace( '__RESISTANCE__', drugtext ) \
#                         .replace( '__FLAVOR__',       flavor ) \
#                         .replace( '__POS__',       pos ) \
#                         .replace( '__NEG__',       neg ) )
# 
#     
#     thiscard = template.replace( '__COLOR__',  color )
#     thiscard1 = thiscard.replace( '__CARDTITLE__', cardtype )
#     thiscard2 = thiscard1.replace( '__TOPTITLE__', cardclass)
#     thiscard3 = thiscard2.replace( '__NAME__',  name)
#     thiscard4 = thiscard3.replace( '__DESC__',  description) 
#     thiscard5 = thiscard4.replace( '__RESISTANCE__',  drugtext) 
#     thiscard6 = thiscard5.replace( '__FLAVOR__',  flavor)
#     
#     
#     if pos !="0" :   
#         thiscard7=thiscard6.replace( '__CIRCLE__', '\\draw[green,fill=green] (3.7,.9) circle (4ex); \\node at (3.7,0.9) {\\LARGE \\bfseries __POS__}; \\node at (5.2,0.9) {\\LARGE \\bfseries __NEG__};`')
#     
#         thiscard8 = thiscard7.replace( '__POS__',  pos)
#         
#     if neg !="0" :    
#         
#         thiscard7=thiscard6.replace( '__CIRCLE__', '\\draw[red,fill=red] (5.2,.9) circle (4ex); \\node at (5.2,0.9) {\\LARGE \\bfseries __NEG__};`')
#         
#         thiscard9 = thiscard8.replace( '__NEG__',  neg)
#     
#     else:
#  	    thiscard9=thiscard6.replace( '__CIRCLE__', " " )
        
    
    
   # page.append(thiscard9)
    
  
    
    print 'card ' + str(n) + ' : ' + name
    
    if len(page) == 9 :
        f.write( '\\begin{tabular}{c c c}\n')
        f.write( '\n&\n'.join(page[0:3]) )
        f.write( '\n\\\\\n' )
        f.write( '\n&\n'.join(page[3:6]) )
        f.write( '\n\\\\\n' )
        f.write( '\n&\n'.join(page[6:9]) )
        f.write( '\n\\end{tabular}\n\\cleardoublepage' )
        print '----'

        page = []


f.write( footer )
f.close()
