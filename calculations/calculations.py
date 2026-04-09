""" the calculations represent decisions or planning.
They don't affect the world when they run"""
import math
from loguru import logger
from openpyxl import load_workbook
import xlrd
import xlwt
import itertools
import pandas as pd
from pathlib import Path


def delen(totaal_file_lengte, kolommen):
    return totaal_file_lengte // kolommen


def lengte_dataframe(df_in):
    lengte_van_dataframe, b = df_in.shape
    return lengte_van_dataframe


def lijst_begin_eind_voor_slice(df_lengte, block_length):
    return list(range(0, df_lengte, block_length))


def dataframe_cutter(df, blok_lengte):
    """cuts dataframe on length . ready made to concat because of reset_index
    blok_lengte =  de lengte van een VDP of een gedeelte van een VDP"""
    list_of_df = [
        df.loc[i: i + blok_lengte - 1, :].reset_index(drop=True)
        for i in range(0, len(df), blok_lengte)
    ]
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
        logger.debug(f"per deel rest {combinaties_per_deel_rest}")

        combinaties_per_deel = totaal_aantal_combinaties / aantal_vdps

        logger.debug(f"per deel  {combinaties_per_deel}")

        eerste_combinatie = math.ceil(combinaties_per_deel)
        logger.debug(f"per deel ceil {eerste_combinatie}")

        if (
                combinaties_per_deel_rest == 0
                or totaal_aantal_combinaties % aantal_vdps == 0
        ):

            volgende_waardes = [int(combinaties_per_deel) for x in range(aantal_vdps)]

            return volgende_waardes

        else:

            if aantal_vdps > 2:
                volgende_waardes = [
                    eerste_combinatie
                    for x in range(aantal_vdps - 1)
                    if aantal_vdps - 1 != 1
                ]
                logger.debug(f"volgende_waardes: {volgende_waardes}")
                laatste_waarde = abs(
                    totaal_aantal_combinaties - (sum(volgende_waardes))
                )
                logger.debug(f"laatste_waarde absoluut =  {laatste_waarde}")
                return volgende_waardes + [laatste_waarde]

            if aantal_vdps == 2:
                laatste_waarde = abs(totaal_aantal_combinaties - eerste_combinatie)
                logger.debug(f"laatste_waarde absoluut =  {laatste_waarde}")
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
            logger.error("error message aantal vdps en lijst komt niet overeen")
            return False

    return check


def combinaties_uit_rollen():
    def check(functie_lijst, mes):
        return [x // mes for x in functie_lijst]

    return check


def dataframe_copy_met_stans():
    def inloop_uitloop(dataframe_in, functiewikkel):
        dfwikkel_a = dataframe_in.copy()
        dfwikkel_a["pdf"] = "stans.pdf"

        inloop_uitloop_slice = dfwikkel_a[:functiewikkel]

        return inloop_uitloop_slice

    return inloop_uitloop


def wikkel_formule():
    def wikkel(Aantalperrol, formaat_hoogte, kern=76):
        """importing in a function?"""
        import math

        pi = math.pi
        # kern = 76  # global andere is 40
        materiaal = 145  # global var
        var_1 = int(
            math.sqrt(
                (4 / pi) * ((Aantalperrol * formaat_hoogte) / 1000) * materiaal
                + pow(kern, 2)
            )
        )
        wikkel = int(2 * pi * (var_1 / 2) / formaat_hoogte + 2)
        return wikkel

    return wikkel


de_uitgerekenende_wikkel = wikkel_formule()


def headers_for_totaal_kolommen(dataframe_rol, mes):
    df_rol_kolommen_lijst = dataframe_rol.columns.to_list()
    count = 1
    kolom_naam_lijst_naar_mes = []
    for _ in range(mes):
        for kolomnaam in df_rol_kolommen_lijst:
            # print(kolomnaam, count)
            header = f"{kolomnaam}_{count}"
            kolom_naam_lijst_naar_mes.append(header)
        count += 1

    return kolom_naam_lijst_naar_mes


def _find_column_case_insensitive(columns, target_name):
    for kolom in columns:
        if str(kolom).strip().lower() == target_name.lower():
            return kolom
    return None


def normalize_input_dataframe_for_numgen(dataframe_in):
    dataframe_uit = dataframe_in.copy()
    dataframe_uit.columns = [str(kolom).strip() for kolom in dataframe_uit.columns]

    kolom_name = _find_column_case_insensitive(dataframe_uit.columns, "Kolom")
    if kolom_name is None:
        kolom1_name = _find_column_case_insensitive(dataframe_uit.columns, "kolom1")
        if kolom1_name is not None:
            dataframe_uit = dataframe_uit.rename(columns={kolom1_name: "Kolom"})
        elif len(dataframe_uit.columns) > 0:
            eerste_kolom = dataframe_uit.columns[0]
            logger.warning(
                f"Kolom header ontbreekt. Gebruik eerste kolom '{eerste_kolom}' als 'Kolom'."
            )
            dataframe_uit = dataframe_uit.rename(columns={eerste_kolom: "Kolom"})
        else:
            raise ValueError("Inputbestand bevat geen kolommen.")
    elif kolom_name != "Kolom":
        dataframe_uit = dataframe_uit.rename(columns={kolom_name: "Kolom"})

    pdf_name = _find_column_case_insensitive(dataframe_uit.columns, "pdf")
    if pdf_name is not None and pdf_name != "pdf":
        dataframe_uit = dataframe_uit.rename(columns={pdf_name: "pdf"})
    if "pdf" not in dataframe_uit.columns:
        dataframe_uit["pdf"] = "leeg.pdf"

    omschrijving_name = _find_column_case_insensitive(
        dataframe_uit.columns, "omschrijving"
    )
    if omschrijving_name is not None and omschrijving_name != "omschrijving":
        dataframe_uit = dataframe_uit.rename(
            columns={omschrijving_name: "omschrijving"}
        )
    if "omschrijving" not in dataframe_uit.columns:
        dataframe_uit["omschrijving"] = ""

    return dataframe_uit.fillna("").astype("str")


def pad_csv_dataframe_to_full_mes_rollen(dataframe_in, mes, aantal_per_rol):
    if mes <= 0:
        raise ValueError(f"mes moet groter dan 0 zijn, ontvangen: {mes}")
    if aantal_per_rol <= 0:
        raise ValueError(
            f"aantal_per_rol moet groter dan 0 zijn, ontvangen: {aantal_per_rol}"
        )

    totaal_rijen = len(dataframe_in)
    volledige_rollen, rest_rijen = divmod(totaal_rijen, aantal_per_rol)
    totaal_rollen = volledige_rollen + (1 if rest_rijen > 0 else 0)
    rest_rollen = (mes - (totaal_rollen % mes)) % mes if totaal_rollen > 0 else 0

    pad_partial = (aantal_per_rol - rest_rijen) % aantal_per_rol
    pad_full = rest_rollen * aantal_per_rol
    pad_total = pad_partial + pad_full

    if pad_total == 0:
        return dataframe_in, {
            "pad_total": 0,
            "pad_partial": 0,
            "pad_full": 0,
            "totaal_rollen_na_pad": totaal_rollen,
        }

    filler_rij = {kolom: "" for kolom in dataframe_in.columns}
    if "pdf" in filler_rij:
        filler_rij["pdf"] = "stans.pdf"

    pad_df = pd.DataFrame([filler_rij] * pad_total, columns=dataframe_in.columns)
    dataframe_uit = pd.concat([dataframe_in, pad_df], ignore_index=True)

    totaal_rollen_na_pad = len(dataframe_uit) // aantal_per_rol
    return dataframe_uit.fillna("").astype("str"), {
        "pad_total": pad_total,
        "pad_partial": pad_partial,
        "pad_full": pad_full,
        "totaal_rollen_na_pad": totaal_rollen_na_pad,
    }


def assign_vdp_kolom_namen(vdp_dataframe, bron_dataframe, mes, context="VDP"):
    kolom_namen = headers_for_totaal_kolommen(bron_dataframe, mes)
    werkelijke_kolommen = vdp_dataframe.shape[1]

    if len(kolom_namen) != werkelijke_kolommen:
        logger.warning(
            f"{context}: kolom mismatch verwacht={len(kolom_namen)} werkelijk={werkelijke_kolommen}. "
            f"Herleid kolommen op basis van VDP-layout."
        )

        if mes <= 0:
            raise ValueError(f"{context}: mes moet groter dan 0 zijn, ontvangen: {mes}")

        if werkelijke_kolommen % mes != 0:
            raise ValueError(
                f"{context}: aantal kolommen ({werkelijke_kolommen}) is niet deelbaar door mes ({mes})."
            )

        kolommen_per_baan = werkelijke_kolommen // mes
        basis_kolommen = vdp_dataframe.columns.to_list()[:kolommen_per_baan]
        fallback_df = pd.DataFrame(columns=basis_kolommen)
        kolom_namen = headers_for_totaal_kolommen(fallback_df, mes)

        if len(kolom_namen) != werkelijke_kolommen:
            raise ValueError(
                f"{context}: kolomnamen mismatch blijft bestaan. "
                f"verwacht={werkelijke_kolommen}, opgebouwd={len(kolom_namen)}"
            )

    vdp_dataframe = vdp_dataframe.copy()
    vdp_dataframe.columns = kolom_namen
    return vdp_dataframe, kolom_namen


def verdeling_met_slice(funclijst, funcverddeellijst):
    """te verdelen lijst en een lijst met verdeelwaardes in
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


def filter_kolommen_pdf(mes, de_kolomnaam):
    # defenitie gekopieerd van
    # headers_for_totaal_kolommen()
    df_rol_kolommen_lijst = [de_kolomnaam]
    count = 1
    kolomnaam_vervang_waarde = []
    for _ in range(mes):
        for kolomnaam in df_rol_kolommen_lijst:
            # print(kolomnaam, count)
            header = f"{kolomnaam}_{count}"
            kolomnaam_vervang_waarde.append(header)
        count += 1
    return kolomnaam_vervang_waarde


def inloop_uitloop_stans(df, wikkel, etiket_y, kolomnaam_vervang_waarde, apr):
    # todo transform with list comprehensions

    loop = (etiket_y * 10) - wikkel
    logger.debug(f"wikkel: {wikkel}")
    logger.debug(f"loop: {loop}")
    generator = df.itertuples(index=0)

    einde_df = len(df)
    logger.debug(f"einde_df: {einde_df}")
    data_df = []
    nieuwe_df = []

    for seq in itertools.islice(generator, 2, 3):
        data_df.append(seq)

    data_df1 = pd.DataFrame(data_df)

    data2 = pd.DataFrame(
        [x for x in itertools.islice(generator, wikkel, wikkel + etiket_y)]
    )
    logger.debug(f"data2.head(): {data2.head()}")

    generator = df.itertuples(index=0)
    data3 = pd.DataFrame(
        [x for x in itertools.islice(generator, (einde_df - etiket_y), einde_df)]
    )
    logger.debug(f"data3.head(): {data3.head()}")

    generator = df.itertuples(index=0)
    # moved 0ne line for double sluitetiket
    for seq in itertools.islice(generator, 4, loop):
        nieuwe_df.append(seq)
    inloopDF = pd.DataFrame(nieuwe_df)
    inloopDF[kolomnaam_vervang_waarde] = "stans.pdf"

    generator = df.itertuples(index=0)

    begin_laatste_sluit = einde_df - (apr + (wikkel + 1))
    logger.debug(f"begin_laatste_sluit: {begin_laatste_sluit}")
    laatste_sluit = pd.DataFrame(
        [
            x
            for x in itertools.islice(
            generator, begin_laatste_sluit, begin_laatste_sluit + 1
        )
        ]
    )

    # inloopDF.reset_index()

    # in en uitloop kunnen hier gegenereerd worden als laatste stans eroverheen

    indat = pd.concat(
        [
            data2,
            data_df1,
            laatste_sluit,
            inloopDF,
            df,
            inloopDF,
            data_df1,
            laatste_sluit,
            data3,
        ]
    )
    indat.reset_index()
    return indat


def csv_name_giver():
    def naming_a_csv(name, count, exp=".csv"):
        csv_name = f"{name}_{count}{exp}"
        return csv_name

    return naming_a_csv


vdpnaam = csv_name_giver()


def dataframe_from_csv():
    def file_to_dataframe(file_in):
        """Builds a Dataframe from a workable csv or excel file
        on which we can Generate with itertuples"""

        if Path(file_in).suffix == ".csv":
            # extra arg = ";"or ","
            logger.debug(f"suffix: {Path(file_in).suffix}")
            file_to_generate_on = pd.read_csv(
                file_in, sep=";", encoding="utf-8", dtype="str"
            )
            if (
                len(file_to_generate_on.columns) == 1
                and "," in str(file_to_generate_on.columns[0])
            ):
                file_to_generate_on = pd.read_csv(
                    file_in, sep=",", encoding="utf-8", dtype="str"
                )

        elif Path(file_in).suffix == ".xlsx":
            logger.debug(f"suffix: {Path(file_in).suffix}")
            file_to_generate_on = pd.read_excel(file_in, dtype=str, engine="openpyxl")

        elif Path(file_in).suffix == ".xls":
            logger.debug(f"suffix: {Path(file_in).suffix}")
            file_to_generate_on = pd.read_excel(file_in, dtype=str)

        return file_to_generate_on

    return file_to_dataframe


maak_csv_naar_dataframe = dataframe_from_csv()


def vdp_meters_uit_df_shape(df, formaat_hoogte):
    totaal, kolommen = df.shape
    meters = totaal * (formaat_hoogte + 3) / 1000
    return meters
