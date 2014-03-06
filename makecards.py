#!/usr/bin/env python
import csv

BASENAME = 'effluence'

header   = open('header.tex').read()
template = open('card_template.tex').read()
footer   = open('footer.tex').read()

f = open( 'effluence_cards.tex', 'w' )

f.write( header )

for n,record in enumerate(csv.reader(open('microbiomecardsv1.csv'))) :
    if n == 0 : continue
   
    cardtype,cardclass,name,description,resistance,flavor = record
    
    if cardtype == 'Microbe' : color = 'green'
    if cardtype == 'Event'   : color = 'red'
    
    drugs = []
    for drug in resistance.strip().split(',') :
        drugs.append(drug.strip())
    
    if len(drugs) == 0 and cardtype == 'Microbe' : drugtext = 'Not resistant'
    if len(drugs) >  0 and cardtype == 'Microbe' :
        drugtext = 'Resistance: \\begin{itemize}\n'
        for drug in drugs :
            drugtext = drugtext + '\\item ' + drug + '\n'
        drugtext = drugtext + '\\end{itemize}\n'

    if cardtype == 'Event' : drugtext = ''

    f.write(template.replace( '__COLOR__',         color ) \
                    .replace( '__CARDTITLE__',  cardtype ) \
                    .replace( '__TOPTITLE__',  cardclass ) \
                    .replace( '__NAME__',           name ) \
                    .replace( '__DESC__',    description ) \
                    .replace( '__RESISTANCE__', drugtext ) \
                    .replace( '__FLAVOR__',       flavor ) )
f.write( footer )
f.close()
