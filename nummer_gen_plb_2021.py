""""Nummer Generator PLB2021"""

import PySimpleGUI as sg
import os
import pandas as pd
import sys
from icecream import ic
from data.data_definitions import *
from calculations.calculations import dataframe_cutter, combinaties_over_totale_order, combinaties
from calculations.character_template import *

from pathlib import Path


# from summary_code import html_sum_form_writer, summary_rol, lege_summary_rollen
# from rollen import rest_uitrekenen, rol_num_dikt, df_lege_csv_rol_builder_met_rolnummer

# todo checkbox rechtstreeks lijst invoeren lijst


def main():
    sg.change_look_and_feel("SystemDefault")

    layout = [
        # [sg.Text("VDP"), sg.Checkbox('nummers', default=True), sg.Checkbox('beelden')],
        # [sg.Text('Nummer Generator PLB2021', text_color="black")],
        [sg.Text("Ordernummer", size=(15, 1)), sg.InputText(202129657, key="order_number")],
        [sg.Text("Aantal VDP's", size=(15, 1)), sg.InputText(2, key="aantal_vdps")],
        [sg.Text("VDP map voor csv's")],
        [sg.In(key="folder_voor_vdp_map", size=(60, 10))],
        [sg.FolderBrowse(target="folder_voor_vdp_map")],
        # [sg.In(key="CSV file", size=(60, 10))],
        [sg.Text("CSV_file")],
        [
            sg.Checkbox(
                "gebruik een aangeleverde en bewerkte file.",
                key="csv_file_checkbox",
                default=False,
            )
        ],
        [sg.In(key="csv_file_in_pad", size=(60, 10))],
        [sg.FileBrowse(target="csv_file_in_pad")],
        [sg.Text()],
        [sg.CalendarButton("Datum", target=(1, 0), key='datum')],







        [sg.Frame(layout=[
            [sg.Checkbox("gebruik template", key="gebruik_template", default=False)],
            [sg.Text("template", size=(15, 1)), sg.Input("??????????????", key="template")],
            [sg.Checkbox("gebruik slice rechts", key="slice_rechts_check", default=False)],
            [sg.Text("slice rechts", size=(15, 1)), sg.Input(3, key="slice_rechts")],
            [sg.Checkbox("gebruik slice links", key="slice_links_check", default=False)],
            [sg.Text("slice links", size=(15, 1)), sg.Input(3, key="slice_links")],
            [sg.Text()],
            [sg.Checkbox("SSCC18", key="sscc18", default=False, size=(10, 1)),
             sg.Checkbox("mod10 (ean13 - ean8)", key = "ean13", default=False)],

            [sg.Radio('Nederlands', "RADIO1",key="radio", default=True, size=(10, 1)),
             sg.Radio('Duits', "RADIO1")]], title='Options', title_color='red', relief=sg.RELIEF_SUNKEN,
            tooltip='taal voor sluitetiket')],


        [sg.Text()],
        # [
        #     sg.Checkbox("gebruik template", key="gebruik_template", default=False),
        #     sg.Checkbox(),
        #     sg.Checkbox(),
        # ],
        # [sg.Text()],
        # [sg.Text("template", size=(15, 1)), sg.Input("??????????????", key="template")],
        # [sg.Checkbox("gebruik slice rechts", key="slice_rechts_check", default=False)],
        # [sg.Text("slice rechts", size=(5, 1)), sg.Input(3, key="slice_rechts")],
        # [sg.Checkbox("gebruik slice links", key="slice_links_check", default=False)],
        # [sg.Text("slice links", size=(5, 1)), sg.Input(3, key="slice_links")],
        # [sg.Text()],
        # [
        [sg.Text("Totaal aantal", size=(15, 1)),
            sg.Input(361_000, key="totaal_aantal"),
        ],

        [sg.Text("Beginnummer", size=(15, 1)), sg.InputText(1, key="begin_nummer")],
        [sg.Text("Veelvoud", size=(15, 1)), sg.InputText(1, key="veelvoud")],
        [sg.Text("posities", size=(15, 1)), sg.InputText(18, key="posities")],
        [sg.Text("voorloop getal", size=(15, 1)), sg.InputText(0, key="vlg0")],
        [
            sg.Text("Aantal_per_rol", size=(15, 1)),
            sg.InputText(9500, key="aantal_per_rol"),
        ],
        [sg.Text("Mes", size=(15, 1)), sg.InputText(6, key="mes")],
        [sg.Text("Y_waarde", size=(15, 1)), sg.InputText(11, key="Y_waarde")],
        [sg.Text("Wikkel", size=(15, 1)), sg.InputText(8, key="wikkel")],
        [sg.Text("prefix", size=(15, 1)), sg.InputText("", key="prefix")],
        [sg.Text("postfix", size=(15, 1)), sg.InputText("", key="postfix")],
        [sg.Text("hoogte etiket", size=(15, 1)), sg.InputText(80, key="hoogte")],
        [sg.Text("kern", size=(15, 1)), sg.InputText(76, key="kern")],
        [
            sg.Text("opmerkingen", size=(15, 1)),
            sg.InputText("Nabewerken NEE", key="opmerkingen"),
        ],
        [sg.Button("Ok"), sg.Cancel()],
        [sg.Text("_" * 80)],
        [sg.Text("SAVE of LOAD inputform", size=(35, 1))],
        # [sg.Text('Your Folder', size=(15, 1), justification='right'),
        #  sg.InputText('Default Folder', key='folder'), sg.FolderBrowse()],
        [
            sg.Button("Exit"),
            sg.Text(" " * 40),
            sg.Button("SaveSettings"),
            sg.Button("LoadSettings"),
        ],
    ]

    window = sg.Window("Nummer Generator PLB2021").Layout(layout)

    while True:
        event, values = window.Read()

        if event in ("Exit", None):
            break

        elif event == "SaveSettings":
            filename = sg.popup_get_file("Save Settings", save_as=True, no_window=True)
            # todo False in mac OS otherwise it will crash
            # todo save met ordernummer en tijd datum

            window.SaveToDisk(filename)
            # save(values)
        elif event == "LoadSettings":
            filename = sg.popup_get_file("Load Settings", no_window=True)
            # todo try except False in mac OS otherwise it will crash
            window.LoadFromDisk(filename)
            # load(form)

        elif event == "Ok":

            ic("ok")

            # print(button, values["order_number"], values["begin_nummer"], values["posities"])

            # datum = values["Datum"]
            # todo datetime    maken
            aantal_vdps = int(values['aantal_vdps'])
            ordernummer = values["order_number"]
            totaal_aantal = int(values["totaal_aantal"])
            begin_nummer = int(values["begin_nummer"])

            veelvoud = int(values["veelvoud"])
            posities = int(values["posities"])
            vlg = int(values["vlg0"])

            begin_nummer_to_check = f'{begin_nummer:>{vlg}{posities}}'
            ic(begin_nummer_to_check)
            aantal_per_rol = int(values["aantal_per_rol"])
            Y_waarde = int(values["Y_waarde"])
            wikkel = int(values["wikkel"])
            hoogte = int(values["hoogte"])
            kern = int(values["kern"])
            prefix = values["prefix"]
            postfix = values["postfix"]
            mes = int(values["mes"])
            opmerkingen = values["opmerkingen"]

            checkbox_slice_rechts = values["slice_rechts_check"]
            aantal_posities_uit_rechts = int(values["slice_rechts"])

            checkbox_slice_links = values["slice_links_check"]
            aantal_posities_uit_links = int(values["slice_links"])

            check_template = values["gebruik_template"]
            template10 = values["template"]
            naar_folder_pad = Path(values["folder_voor_vdp_map"])
            ic(f"naar_folder_pad: {naar_folder_pad}")
            inloop = Y_waarde * 10 - Y_waarde

            ic(values)

            # if not checkbox sscc __> hier komt lijstmaker sscc of komt in def lijstmaker

            eerste_lijst_uit_input = nummer_lijst_bouwer(
                begin_nummer,
                totaal_aantal,
                "leeg.pdf",
                posities,
                mes,
                aantal_per_rol,
                0,
                prefix,
                postfix
            )
            # eerst bekijken of checkboxes aan staan dan aantal vpds

            te_bewerken_dataframe_voor_plb_2020 = pd.DataFrame(
                eerste_lijst_uit_input,
                columns=["Kolom", "pdf", "omschrijving"],
                dtype="str",
            )

            ic(te_bewerken_dataframe_voor_plb_2020.head())
            ic(te_bewerken_dataframe_voor_plb_2020.tail())

            if checkbox_slice_links:
                te_bewerken_dataframe_voor_plb_2020[
                    "slice_links"
                ] = te_bewerken_dataframe_voor_plb_2020["Kolom"].apply(
                    lambda x: x[:aantal_posities_uit_links]
                )

            if checkbox_slice_rechts:
                te_bewerken_dataframe_voor_plb_2020[
                    "slice_rechts"
                ] = te_bewerken_dataframe_voor_plb_2020["Kolom"].apply(
                    lambda x: x[-aantal_posities_uit_rechts:]
                )

            ic(te_bewerken_dataframe_voor_plb_2020.head())

            template_length_checker = check_length_string_and_template_truths()

            temp_reader = sign_to_bool_translater()
            template_array = [temp_reader(x) for x in template10]
            template_array_truths = len([temp_reader(x) for x in template10 if temp_reader(x) is True])

            nieuw_nummer = number_translated_to_template()

            # als de check box aanstaat en het aantal tekens is gelijk aan de vraagtekens
            # (misschien een teller maken voor het aantal vraagtekens.

            # LET OP met het SSCC18 verhaal 17 18 (00) etc...

            # dit in een def zetten zodat erook een uitkomst kan komen
            # voor een negative uitslag posities of try except?

            if check_template:
                if not template_length_checker(begin_nummer_to_check, template_array_truths):
                    print(f'nummer is {len(begin_nummer_to_check)} tekens lang, template is {template_array_truths} tekens lang en dus zijn niet gelijk.')

            if check_template and template_length_checker(begin_nummer_to_check, template_array_truths):
                te_bewerken_dataframe_voor_plb_2020['hr_template']=\
                    te_bewerken_dataframe_voor_plb_2020["Kolom"].apply(lambda x: nieuw_nummer(x,
                                                                                    template10,
                                                                                    template_array,
                                                                                    compare_template_with_number_list()))
            ic(te_bewerken_dataframe_voor_plb_2020.head())

            #todo columnnames for endresult

            #############################################

            # space for other checkboxes

            #############################################


            # todo make all dataframe rolls

            # main dataframe wordt hier verdeeld
            totaal_aantal_in_dataframe = len(te_bewerken_dataframe_voor_plb_2020)
            ic(totaal_aantal_in_dataframe)

            lijst_met_alle_dataframe_rollen = dataframe_cutter(te_bewerken_dataframe_voor_plb_2020, aantal_per_rol)

            rol = roll()

            rollen = [rol(df, de_uitgerekenende_wikkel(aantal_per_rol, hoogte, kern), index)
                      for index, df in enumerate(lijst_met_alle_dataframe_rollen)]
            # list of tuples

            # ic(rollen)
            ic(rollen[0][:10])
            ic(rollen[1][:10])








            ###########################################

            # ic(rollen_per_vdp)
            # if lengte blok = n , dan uit lijst vdp aantal pak n aantal als blok lengte.
            #  nee verdeling is van klein naar groot nu ik moet of de laatste waarde eerst zetten.
            # HET MOET per rollen per vdp worden !per rollen gaan doen
            # wel even controleren

            # dataframe opdelen in rollen

            # rollen maken

            totaal_aan_rollen = dataframe_cutter(te_bewerken_dataframe_voor_plb_2020,aantal_per_rol)

            ic(len(totaal_aan_rollen))

            kollom_namen = headers_for_totaal_kolommen(te_bewerken_dataframe_voor_plb_2020, mes)
            ic(kollom_namen)

            ##########################################

            if aantal_vdps == 1:
                print("verwerk de lijst zoals ie nu is")
                # lijst in lijst maken

                combi = len(totaal_aan_rollen)//mes
                ic(combi)
                lijst_van_lijst_van_alle_rollen = lijst_opbreker(rollen, mes, combi)

                ic(len(lijst_van_lijst_van_alle_rollen))

                VDP = stapel_df_baan(lijst_van_lijst_van_alle_rollen)
                VDP.columns=kollom_namen
                # ic(VDP.shape)
                # ic(vdp_blok.head())
                VDP.to_csv("gtest1.csv")

            else:
                tot_comb_ = combinaties_over_totale_order(len(te_bewerken_dataframe_voor_plb_2020),
                                                          aantal_per_rol,
                                                          mes)
                ic(tot_comb_)

                combinatie_verdeling = combinaties(tot_comb_,aantal_vdps, mes)

                ic(combinatie_verdeling)

                ##################################

                # values from gUI
                ic(values)
                ###################################


if __name__ == "__main__":
    main()
