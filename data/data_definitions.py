from typing import Union
import itertools

import pandas as pd
from pandas import DataFrame, Series

from calculations.calculations import *

# todo toevoegen ean13  etc en sscc18
def nummer_lijst_bouwer(begin_nummer, totaal, pdf, posities, mes, aantal_per_rol, vlg=0, prefix="", postfix=""):
    """met de lijst output word een dataframe gemaakt
    #todo plaats andere zoals sscc en ean 13 ook in deze def?"""

    num_lijst = []
    rest_lijst = []

    def maak_simpele_lijst(begin_nummer, totaal, pdf):
        '''list comp voor maken nummer lijst, 3 kolommen
        kijk voor benamingen in project lijst bewerken'''
        eind = begin_nummer + totaal
        nummers = [(f'{prefix}{x:>{vlg}{posities}}{postfix}', f'{pdf}', '') for x in range(begin_nummer, eind)]
        nummers_df = pd.DataFrame(nummers, columns=["kolom1", "pdf", "omschrijving"], dtype="str")
        return nummers



    def rest_rollen_uitrekenen(mes, totaal, aantal_per_rol):
        """het totaal delen door de aantal per rol:

        de restwaarde hier van geeft het aantal rollen dat te kort is"""
        if totaal % mes * aantal_per_rol == 0:
            return 0

        if totaal <= mes * aantal_per_rol:

            print(f'aantal rest rollen = {abs((mes * aantal_per_rol - totaal) // aantal_per_rol)} uit if')
            return abs((mes * aantal_per_rol - totaal) // aantal_per_rol)

        else:

            rest_rollen = mes - totaal // aantal_per_rol % mes
            print(f'aantal rest rollen = {rest_rollen} uit else')
            return rest_rollen

    num_lijst = maak_simpele_lijst(begin_nummer, totaal, pdf)
    rest = rest_rollen_uitrekenen(mes, totaal, aantal_per_rol)
    rest_lijst = maak_simpele_lijst(1, (rest * aantal_per_rol), "stans.pdf")

    if rest != 0:
        rest_lijst = maak_simpele_lijst(1, (rest * aantal_per_rol), "stans.pdf")

        totlijst = num_lijst + rest_lijst
        return totlijst

    else:
        return num_lijst

# dit is een functie die in lijstmaker zit
def rest_rollen_uitrekenen(mes, totaal, aantal_per_rol):
    """het totaal delen door de aantal per rol:

    de restwaarde hier van geeft het aantal rollen dat te kort is"""
    if totaal % mes * aantal_per_rol == 0:
        return 0

    if totaal <= mes * aantal_per_rol:

        print(f'aantal rest rollen = {abs((mes * aantal_per_rol - totaal) // aantal_per_rol)} uit if')
        return abs((mes * aantal_per_rol - totaal) // aantal_per_rol)



    else:

        rest_rollen = mes - (totaal // aantal_per_rol) % mes
        print(f'aantal rest rollen = {rest_rollen} uit else')
        return rest_rollen

# gebruikt bij 1 vdp vooralsnog
def roll():
    
    def rol_van_dataframe(dataframe_rol, functiewikkel, functie_taal_rolnum):
        begin, eind, aantal = begin_eind_dataframe(dataframe_rol)
        sluitetiket = f"Rol {functie_taal_rolnum + 1} | {begin} - {eind} | {aantal} etiketten"

        dfwikkel = dataframe_rol.copy()
        dfwikkel['pdf'] = "stans.pdf"
        sluit = dfwikkel[:1]
        sluit['omschrijving'] = sluitetiket

        # def maken want zo maak je ook gewoon de inloop en uitloop in de laatste stap.
        dfwikkel_a = dataframe_rol.copy()
        dfwikkel_a['pdf'] = "stans.pdf"
        dfwikkel1 = dfwikkel_a[:2]
        dfwikkel2 = dfwikkel_a[:functiewikkel]

        rol_met_wikkel_en_sluit: Union[DataFrame, Series] = pd.concat([dfwikkel1, sluit, dfwikkel2, dataframe_rol]).reset_index(drop=True)

        ic(rol_met_wikkel_en_sluit.head(20))

        return rol_met_wikkel_en_sluit

    return rol_van_dataframe


def rol_uit_generator():

    def rol_gen(dataframe_rol, functiewikkel, rolnum, posities, taal):
        """taal komt uit een keuze lijst kan 1 van twee zijn nl en de"""
        begin, eind, aantal = begin_eind_dataframe(dataframe_rol)

        # sluitetiket = f"Rol {functie_taal_rolnum + 1} | {begin} - {eind} | {aantal} etiketten"

        def taal_sluitetiket():
            # rolnummer komt uit enumarate
            # nummer omzetten in string
            def taal(dataframe_rol, taal, rolnummer, posities):
                # posities if  len(lijst)>= 10 dan 2 100 = 3 etc zie plb2020 of num generator

                rol_nummer = f'{rolnummer + 1:>{0}{posities}}'
                begin, eind, aantal = begin_eind_dataframe(dataframe_rol)

                if taal == "nl":
                    sluitetiket = f"Rol {rol_nummer} | {begin} - {eind} | {aantal} etiketten"
                    return sluitetiket
                if taal == "de":
                    sluitetiket = f"Rolle {rol_nummer} | {begin} - {eind} | {aantal} stück"
                    return sluitetiket

            return taal

        language = taal_sluitetiket()

        sluitetiket = language(dataframe_rol, taal, rolnum, posities)
        #print(f'{sluitetiket=}') werkt als ic in python 3.9

        generator = dataframe_rol.itertuples(index=0)

        inloop_rol = pd.DataFrame([x for x in itertools.islice(generator, 0, 2)])
        print(inloop_rol)
        inloop_rol['pdf'] = 'stans.pdf'

        generator = dataframe_rol.itertuples(index=0)

        sluit = pd.DataFrame([x for x in itertools.islice(generator, 0, 1)])
        sluit['pdf'] = 'stans.pdf'
        sluit['omschrijving'] = sluitetiket

        generator = dataframe_rol.itertuples(index=0)

        inloop_rol2 = pd.DataFrame([x for x in itertools.islice(generator, 0, functiewikkel)])
        inloop_rol2['pdf'] = 'stans.pdf'

        rol_met_wikkel_en_sluit: Union[DataFrame, Series] = pd.concat(
            [inloop_rol, sluit, inloop_rol2, dataframe_rol]).reset_index(drop=True)

        return rol_met_wikkel_en_sluit

    return rol_gen

rol_van_generators = rol_uit_generator()


#todo summary naar pdf via html
def roll_summary():
    # maak een dataframe als in num gen 2.0
    # haal de data uit de VDP dataframe met begin en eind slice wikkel combi
    def summary_rol_van_dataframe(dataframe_rol, rolnum):
        begin, eind, aantal = begin_eind_dataframe(dataframe_rol)

        sluitetiket = f"Rol {rolnum + 1} | {begin} - {eind} | {aantal} etiketten"

        begin = pd.DataFrame([begin])
        eind = pd.DataFrame([eind])

        rol_sum=pd.concat([begin,eind])

        return rol_sum
    return summary_rol_van_dataframe


sum_begin_eind = roll_summary()