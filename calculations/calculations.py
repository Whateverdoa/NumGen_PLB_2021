""" the calculations represent decisions or planning.
They don't affect the world when they run"""
import math
from openpyxl import load_workbook
import xlrd
import xlwt
import itertools
import pandas as pd
from pathlib import Path
from icecream import ic


def delen(totaal_file_lengte, kolommen):
    return totaal_file_lengte // kolommen


def lengte_dataframe(df_in):
    lengte_van_dataframe, b = df_in.shape
    return lengte_van_dataframe


def lijst_begin_eind_voor_slice(df_lengte, block_length):
    return list(range(0, df_lengte, block_length))


def dataframe_cutter(df, blok_lengte):
    """ cuts dataframe on length . ready made to concat because of reset_index
        blok_lengte =  de lengte van een VDP of een gedeelte van een VDP"""
    list_of_df = [df.loc[i:i + blok_lengte - 1, :].reset_index(drop=True) for i in range(0, len(df), blok_lengte)]
    return list_of_df


def begin_eind_dataframe(df_rol):
    """geeft begin van file, eind van file en aantal van file in tuple format"""

    begin = df_rol.iat[0, 0]
    beg = df_rol.iloc[0, 0]
    einde, kolommen = df_rol.shape
    eind_positie_rol = einde - 1
    eind = df_rol.iat[eind_positie_rol, 0]

    return (begin, eind, einde)


def combinaties_berekenen():
    def combinaties(totaal_met_restrollen, apr, mes):
        return (totaal_met_restrollen // apr) // mes

    return combinaties


combinaties_over_totale_order = combinaties_berekenen()


def combinaties_per_vdp_berekenen():

    def lijst_combinaties(totaal_aantal_combinaties, aantal_vdps, mes):

        combinatie_lijst = []

        combinaties_per_deel_rest = totaal_aantal_combinaties / aantal_vdps % mes
        print(f'per deel rest {combinaties_per_deel_rest}')

        combinaties_per_deel = totaal_aantal_combinaties / aantal_vdps

        print(f'per deel  {combinaties_per_deel}')

        eerste_combinatie = math.ceil(combinaties_per_deel)
        print(f'per deel ceil {eerste_combinatie}')

        if combinaties_per_deel_rest == 0 or totaal_aantal_combinaties % aantal_vdps == 0:

            volgende_waardes = [int(combinaties_per_deel) for x in range(aantal_vdps)]

            return volgende_waardes

        else:

            if aantal_vdps > 2:
                volgende_waardes = [eerste_combinatie for x in range(aantal_vdps - 1) if aantal_vdps - 1 != 1]
                print(volgende_waardes)
                laatste_waarde = abs(totaal_aantal_combinaties - (sum(volgende_waardes)))
                print(f'laatste_waarde absoluut =  {laatste_waarde}')
                return volgende_waardes + [laatste_waarde]

            if aantal_vdps == 2:
                laatste_waarde = abs(totaal_aantal_combinaties - eerste_combinatie)
                print(f'laatste_waarde absoluut =  {laatste_waarde}')
                return [eerste_combinatie] + [laatste_waarde]

        # als het blok een restwaarde heeft van 0
        # dan kan je deze combinatie waarde gebruiken voor alle n vdp's(denk ik)

    return lijst_combinaties


combinaties = combinaties_per_vdp_berekenen()


def rollen_uit_aantallen():
    "len(lijst)controleren op aantal_vdp's"

    def check(lijst_functie, vdps, aantal_per_rol):
        if len(lijst_functie) == vdps:
            rollen = [x // aantal_per_rol for x in lijst_functie]
            return rollen
        else:
            print("ërror message aantal vdps en lijst komt niet overeen")
            return False

    return check


def combinaties_uit_rollen():
    def check(functie_lijst, mes):
        return [x // mes for x in functie_lijst]

    return check


def dataframe_copy_met_stans():
    def inloop_uitloop(dataframe_in, functiewikkel):
        dfwikkel_a = dataframe_in.copy()
        dfwikkel_a['pdf'] = "stans.pdf"

        inloop_uitloop_slice = dfwikkel_a[:functiewikkel]

        return inloop_uitloop_slice

    return inloop_uitloop


def wikkel_formule():
    def wikkel(Aantalperrol, formaat_hoogte, kern=76):
        """ importing in a function?"""
        import math

        pi = math.pi
        # kern = 76  # global andere is 40
        materiaal = 145  # global var
        var_1 = int(math.sqrt((4 / pi) * ((Aantalperrol * formaat_hoogte) / 1000) * materiaal + pow(kern, 2)))
        wikkel = int(2 * pi * (var_1 / 2) / formaat_hoogte + 2)
        return wikkel - 2

    return wikkel


de_uitgerekenende_wikkel = wikkel_formule()


def headers_for_totaal_kolommen(dataframe_rol, mes):
    df_rol_kolommen_lijst = dataframe_rol.columns.to_list()
    count = 1
    kolom_naam_lijst_naar_mes = []
    for _ in range(mes):
        for kolomnaam in df_rol_kolommen_lijst:
            # print(kolomnaam, count)
            header = f'{kolomnaam}_{count}'
            kolom_naam_lijst_naar_mes.append(header)
        count += 1

    return kolom_naam_lijst_naar_mes


def verdeling_met_slice(funclijst, funcverddeellijst):
    """ te verdelen lijst en een lijst met verdeelwaardes in
    uit => lijsten in lijst verdeeld
    """
    verdeelde_lijst = []
    begin = 0
    einde = funcverddeellijst[0]
    for index, einde in enumerate(funcverddeellijst):
        einde += begin
        # print(index,begin,einde)
        # print(tot_comb_lijst[begin:einde])
        verdeelde_lijst.append(funclijst[begin:einde])
        begin = einde

    return verdeelde_lijst


def lijst_opbreker(lijst_in, mes_waarde, combi):
    start = 0
    end = mes_waarde
    combinatie_binnen_mes = []

    for combinatie in range(combi):
        # print(combinatie)
        combinatie_binnen_mes.append(lijst_in[start:end])
        start += mes_waarde
        end += mes_waarde
    return combinatie_binnen_mes


# dit bouwt een vdp!
def stapel_df_baan(lijst_in):
    # lijst= [df1,df2,df3etc]
    # axis = 0 stapeld verticaal
    # axis = 1 stapeld horizontaal
    vdp_stapel = []
    for lijst_combi_df in lijst_in:
        vdp_stapel.append(pd.concat(lijst_combi_df, axis=1))

    vdp = pd.concat(vdp_stapel, axis=0)


    return vdp.reset_index(drop=True)

#deprecated
def VDP_inloop_uitloop():

    def filter_kolommen_pdf(mes):
        # defenitie gekopieerd van
        # headers_for_totaal_kolommen()
        df_rol_kolommen_lijst = ["pdf"]
        count = 1
        kolomnaam_vervang_waarde = []
        for _ in range(mes):
            for kolomnaam in df_rol_kolommen_lijst:
                # print(kolomnaam, count)
                header = f'{kolomnaam}_{count}'
                kolomnaam_vervang_waarde.append(header)
            count += 1
        return kolomnaam_vervang_waarde

    def vdp_met_in_en__uit(vdp_dataframe, mes, etiket_y,aantal_per_rol, wikkel):
        """voegt in en uitloop toe aan de vdp,

        voor de inloop sluit en uitloop sluit etiketten"""

        kolomnaam_vervang_waarde = filter_kolommen_pdf(mes)
        inloop = (etiket_y * 10) - wikkel
        print(vdp_dataframe.columns)

        # kopieer de dataframe
        # 1 keer voor echte data en 1 keer voor de in  uitloop
        # begin_inloop = vdp_dataframe.copy()
        df_voor_roldata = vdp_dataframe.copy()


        # selecteer sluit etiket
        begin_inloop_sluit = df_voor_roldata.iloc[2:3]

        roldata_begin = wikkel + 3
        roldata_eind = roldata_begin + etiket_y

        # echte begin data
        roldata = df_voor_roldata.iloc[roldata_begin:roldata_eind]

        # verander leeg naar stans.pdf voor inloop en uitloop

        begin_inloop = vdp_dataframe.copy()
        # begin_inloop.loc[~begin_inloop.index.duplicated(), :]
        ic(begin_inloop.index.is_unique)
        # begin_inloop[kolomnaam_vervang_waarde] = "stans.pdf"  # #todo werkt bij 1 maar niet bij meerdere
        begin_inloop.replace("leeg.pdf", "stans.pdf")

        inloop_df = begin_inloop.iloc[4:inloop]
        print(inloop_df.columns)
        inloop_df[kolomnaam_vervang_waarde] = "stans.pdf"

        # echte uitloop data
        data_uitloop = df_voor_roldata[-etiket_y:]
        uitloop = (etiket_y * 10) - wikkel
        uitloop_df = begin_inloop.iloc[-uitloop:]
        uitloop_df[kolomnaam_vervang_waarde] = "stans.pdf"


        # todo berekenen ish met rol
        b_eindsluit = -(aantal_per_rol + wikkel+1)
        eindsluit = -(aantal_per_rol + wikkel)
        uitloopsluit = begin_inloop.iloc[b_eindsluit: eindsluit]

        # voeg alles samen voor een vdp
        vdp_met_in_en_uitloop = pd.concat([
            roldata,
            begin_inloop_sluit,
            uitloopsluit,
            inloop_df,

            vdp_dataframe,

            uitloop_df,

            begin_inloop_sluit,
            uitloopsluit,
            data_uitloop
        ])

        return vdp_met_in_en_uitloop

    return vdp_met_in_en__uit


vdp_maker = VDP_inloop_uitloop()


def filter_kolommen_pdf(mes, de_kolomnaam):
    # defenitie gekopieerd van
    # headers_for_totaal_kolommen()
    df_rol_kolommen_lijst = [de_kolomnaam]
    count = 1
    kolomnaam_vervang_waarde = []
    for _ in range(mes):
        for kolomnaam in df_rol_kolommen_lijst:
            # print(kolomnaam, count)
            header = f'{kolomnaam}_{count}'
            kolomnaam_vervang_waarde.append(header)
        count += 1
    return kolomnaam_vervang_waarde


def inloop_uitloop_stans(df, wikkel, etiket_y, kolomnaam_vervang_waarde, apr):
    #todo transform with list comprehensions

    loop = (etiket_y * 10) - wikkel
    ic(wikkel)
    ic(loop)
    generator = df.itertuples(index=0)

    einde_df = len(df)
    ic(einde_df)
    data_df = []
    nieuwe_df = []
    
    for seq in itertools.islice(generator, 2, 3):
        data_df.append(seq)

    data_df1 = pd.DataFrame(data_df)

    data2 = pd.DataFrame([x for x in itertools.islice(generator, wikkel, wikkel + etiket_y)])
    ic(data2.head())

    generator = df.itertuples(index=0)
    data3 = pd.DataFrame([x for x in itertools.islice(generator, (einde_df - etiket_y), einde_df)])
    ic(data3.head())

    generator = df.itertuples(index=0)

    for seq in itertools.islice(generator,3,loop):
        nieuwe_df.append(seq)
    inloopDF = pd.DataFrame(nieuwe_df)
    inloopDF[kolomnaam_vervang_waarde] ='stans.pdf'

    generator = df.itertuples(index=0)

    begin_laatste_sluit = einde_df - (apr + (wikkel+1))
    ic(begin_laatste_sluit)
    laatste_sluit = pd.DataFrame([x for x in itertools.islice(generator,begin_laatste_sluit,begin_laatste_sluit+1)])
    
    
    
    # inloopDF.reset_index()

    #in en uitloop kunnen hier gegenereerd worden als laatse stans eroverheen

    indat = pd.concat([data2,

                       data_df1,
                       laatste_sluit,

                       inloopDF,
                       
                       df,
                       
                       inloopDF,

                       data_df1,
                       laatste_sluit,

                       data3

                       ])
    indat.reset_index()
    return indat



def csv_name_giver():

    def naming_a_csv(name, count, exp=".csv"):
        csv_name = f'{name}_{count}{exp}'
        return csv_name

    return naming_a_csv

vdpnaam= csv_name_giver()

def dataframe_from_csv():

    def file_to_dataframe(file_in):
        """Builds a Dataframe from a workable csv or excel file
         on which we can Generate with itertuples"""

        if Path(file_in).suffix == ".csv":
            # extra arg = ";"or ","
            ic(Path(file_in).suffix)
            file_to_generate_on = pd.read_csv(file_in, ";", encoding='utf-8', dtype="str")

        elif Path(file_in).suffix == ".xlsx":
            ic(Path(file_in).suffix)
            file_to_generate_on = pd.read_excel(file_in, engine='openpyxl')

        elif Path(file_in).suffix == ".xls":
            ic(Path(file_in).suffix)
            file_to_generate_on = pd.read_excel(file_in)

        return file_to_generate_on

    return file_to_dataframe

maak_csv_naar_dataframe = dataframe_from_csv()



