import numpy as np
import pandas as pd
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy.orm import aliased
from sqlalchemy import create_engine
from sqlalchemy import func

def sql_password(file):

    with open(file, 'r') as f1:
        for line in f1:
            idb, iuser, ipass = line.split()

    return idb, iuser, ipass

def query(file,group,filter_type,codes):

    idb,iuser,ipass = sql_password(file)
    engine = create_engine('mysql://'+iuser+':'+ipass+'@localhost/'+idb, echo=False)
    session = Session(engine)
    Base = automap_base()
    Base.prepare(engine, reflect=True)

    mort = Base.classes.mortality
    pop = Base.classes.population

    if group == 'year':
        poptype = [1]
        row = 21 #number of years
    if group == 'county':
        poptype = 3
        row = 0 #number of counties
    if filter_type == 'sex':
        field = 'race'
        type_1 = [1,3,5]
        type_2 = [2,4,6]
        col = 4 #year,pop,men,women
    if filter_type == 'race':
        field = 'race'
        type_1 = [1,2]
        type_2 = [3,4]
        type_3 = [5,6]
        col = 5 #year,pop,white,black,other

    if col >= 3:
        q1 = session.query(getattr(mort,group),func.sum(mort.number).label('type_1')).\
            group_by(getattr(mort,group)).filter(getattr(mort,field).in_(type_1))
    if col >= 4:
        q2 = session.query(getattr(mort,group),func.sum(mort.number).label('type_2')).\
            group_by(getattr(mort,group)).filter(getattr(mort,field).in_(type_2))
    if col >= 5:
        q3 = session.query(getattr(mort,group),func.sum(mort.number).label('type_3')).\
            group_by(getattr(mort,group)).filter(getattr(mort,field).in_(type_3))

    totalpop = session.query(getattr(pop,group),func.sum(pop.live_births + pop.age_1_4 + \
                    pop.age_5_9 + pop.age_10_14 + pop.age_15_19 + pop.age_20_24 + pop.age_25_34 + \
                    pop.age_35_44 + pop.age_45_54 + pop.age_55_64 + pop.age_65_74 + pop.age_75_84 + \
                    pop.age_85_above).label('population')).group_by(getattr(pop,group)).filter(pop.type.in_(poptype))

    table = [[0 for j in range(row)] for i in range(col)]
    for j,d in enumerate(q1):
        table[0][j] = getattr(d,group)
        table[2][j] = d.type_1
    for j,d in enumerate(totalpop):
        table[1][j] = d.population
    if col >= 4:
        for j,d in enumerate(q2):
            table[3][j] = d.type_2
    if col >= 5:
        for j,d in enumerate(q3):
            table[4][j] = d.type_3

    return table


