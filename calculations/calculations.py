""" the calculations represent decisions or planning.
They don't affect the world when they run"""
import math
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
    def combinaties(totaal_met_restrollen,apr,mes):
        return (totaal_met_restrollen//apr)//mes
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
        return [x//mes for x in functie_lijst]

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
        return wikkel-2
    return wikkel

de_uitgerekenende_wikkel = wikkel_formule()

def headers_for_totaal_kolommen(dataframe_rol):
    aantal, kolommen = dataframe_rol.shape
    df_rol_kolommen_lijst = dataframe_rol.columns.to_list()
    count = 1
    kolom_naam_lijst_naar_mes = []
    for _ in range(kolommen):
        for kolomnaam in df_rol_kolommen_lijst:
            # print(kolomnaam, count)
            header = f'{kolomnaam}_{count}'
            kolom_naam_lijst_naar_mes.append(header)
        count += 1

    return kolom_naam_lijst_naar_mes




