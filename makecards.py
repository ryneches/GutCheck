#!/usr/bin/env python
import csv

BASENAME = 'effluence'
CSVFILE  = 'microbiomecardsv2.csv'

header   = open('header.tex').read()
template = open('card_template.tex').read()
footer   = open('footer.tex').read()

f = open( 'effluence_cards.tex', 'w' )

f.write( header )

page = []

for n,record in enumerate(csv.reader(open(CSVFILE))) :
    if n == 0 : continue
   
    cardtype,cardclass,name,description,resistance,flavor = record
    
    if cardtype == 'Microbe'    : color = 'green'
    if cardtype == 'Event'      : color = 'red'
    if cardtype == 'Infection'  : color = 'yellow'
    if cardtype == 'Plasmid'    : color = 'cyan'
    
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

    page.append(template.replace( '__COLOR__',         color ) \
                        .replace( '__CARDTITLE__',  cardtype ) \
                        .replace( '__TOPTITLE__',  cardclass ) \
                        .replace( '__NAME__',           name ) \
                        .replace( '__DESC__',    description ) \
                        .replace( '__RESISTANCE__', drugtext ) \
                        .replace( '__FLAVOR__',       flavor ) )

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
