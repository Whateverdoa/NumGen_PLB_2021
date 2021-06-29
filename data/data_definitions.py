from typing import Union

import pandas as pd
from pandas import DataFrame, Series

from calculations.calculations import *

# todo toevoegen ean13  etc en sscc18
def nummer_lijst_bouwer(begin_nummer, totaal, pdf, posities, mes, aantal_per_rol, vlg=0, prefix="", postfix=""):
    """
    met de lijst output word een dataframe gemaakt"""
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

# todo summary
def roll_summary():
    # maak een dataframe als in num gen 2.0
    def summary_rol_van_dataframe(dataframe_rol, functie_taal_rolnum):
        begin, eind, aantal = begin_eind_dataframe(dataframe_rol)
        sluitetiket = f"Rol {functie_taal_rolnum + 1} | {begin} - {eind} | {aantal} etiketten"

