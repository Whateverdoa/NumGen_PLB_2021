"""Nummer Generator PLB2021"""

import json
import os
import pickle
import sys

import pandas as pd
from loguru import logger
from openpyxl import load_workbook
import xlrd
import xlwt
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QFormLayout,
    QLabel, QLineEdit, QPushButton, QCheckBox, QRadioButton,
    QGroupBox, QFileDialog, QButtonGroup, QMessageBox,
)

from data.data_definitions import *
from calculations.calculations import (
    dataframe_cutter,
    combinaties_over_totale_order,
    combinaties,
)
from calculations.character_template import *

from pathlib import Path


class NummerGeneratorWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Nummer Generator PLB2021")
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout()

        # --- Top form fields ---
        form = QFormLayout()

        self.order_number = QLineEdit("202129657")
        form.addRow("Ordernummer", self.order_number)

        self.aantal_vdps = QLineEdit("2")
        form.addRow("Aantal VDP's", self.aantal_vdps)

        main_layout.addLayout(form)

        # --- Folder browse ---
        main_layout.addWidget(QLabel("VDP map voor csv's"))
        folder_layout = QHBoxLayout()
        self.folder_voor_vdp_map = QLineEdit()
        folder_layout.addWidget(self.folder_voor_vdp_map)
        browse_folder_btn = QPushButton("Browse...")
        browse_folder_btn.clicked.connect(self.browse_folder)
        folder_layout.addWidget(browse_folder_btn)
        main_layout.addLayout(folder_layout)

        # --- More form fields ---
        form2 = QFormLayout()

        self.totaal_aantal = QLineEdit("100000")
        form2.addRow("Totaal aantal", self.totaal_aantal)

        self.begin_nummer = QLineEdit("1")
        form2.addRow("Beginnummer", self.begin_nummer)

        self.veelvoud = QLineEdit("1")
        form2.addRow("Veelvoud", self.veelvoud)

        self.posities = QLineEdit("18")
        form2.addRow("posities", self.posities)

        self.aantal_per_rol = QLineEdit("1000")
        form2.addRow("Aantal_per_rol", self.aantal_per_rol)

        self.mes = QLineEdit("4")
        form2.addRow("Mes", self.mes)

        self.Y_waarde = QLineEdit("10")
        form2.addRow("Y_waarde", self.Y_waarde)

        self.prefix = QLineEdit("")
        form2.addRow("prefix", self.prefix)

        self.postfix = QLineEdit("")
        form2.addRow("postfix", self.postfix)

        self.hoogte = QLineEdit("80")
        form2.addRow("hoogte etiket", self.hoogte)

        self.kern = QLineEdit("76")
        form2.addRow("kern", self.kern)

        self.opmerkingen = QLineEdit("")
        form2.addRow("opmerkingen", self.opmerkingen)

        main_layout.addLayout(form2)

        # --- Separator ---
        main_layout.addWidget(QLabel("_" * 60))
        main_layout.addWidget(QLabel("Werken met aangeleverde of zelfgemaakte CSV_file of xlxs file"))

        # --- CSV file checkbox and browse ---
        self.csv_file_checkbox = QCheckBox("file met headers: kolom1,pdf,omschrijving, etc...")
        main_layout.addWidget(self.csv_file_checkbox)

        file_layout = QHBoxLayout()
        self.csv_file_in_pad = QLineEdit()
        file_layout.addWidget(self.csv_file_in_pad)
        browse_file_btn = QPushButton("Browse...")
        browse_file_btn.clicked.connect(self.browse_file)
        file_layout.addWidget(browse_file_btn)
        main_layout.addLayout(file_layout)

        # --- Options frame ---
        options_group = QGroupBox("Options")
        options_layout = QVBoxLayout()

        self.gebruik_template = QCheckBox(
            "gebruik template bij sscc, 1 extra '?' toevoegen voor de cd"
        )
        options_layout.addWidget(self.gebruik_template)

        template_layout = QHBoxLayout()
        template_layout.addWidget(QLabel("template"))
        self.template = QLineEdit("??????????????")
        template_layout.addWidget(self.template)
        options_layout.addLayout(template_layout)

        self.slice_rechts_check = QCheckBox("gebruik slice rechts")
        options_layout.addWidget(self.slice_rechts_check)

        slice_r_layout = QHBoxLayout()
        slice_r_layout.addWidget(QLabel("slice rechts"))
        self.slice_rechts = QLineEdit("3")
        slice_r_layout.addWidget(self.slice_rechts)
        options_layout.addLayout(slice_r_layout)

        self.slice_links_check = QCheckBox("gebruik slice links")
        options_layout.addWidget(self.slice_links_check)

        slice_l_layout = QHBoxLayout()
        slice_l_layout.addWidget(QLabel("slice links"))
        self.slice_links = QLineEdit("3")
        slice_l_layout.addWidget(self.slice_links)
        options_layout.addLayout(slice_l_layout)

        self.wikkel_handmatig = QCheckBox("Wikkel handmatig")
        options_layout.addWidget(self.wikkel_handmatig)

        wikkel_layout = QHBoxLayout()
        wikkel_layout.addWidget(QLabel("Wikkel"))
        self.wikkel_handmatige_invoer = QLineEdit("3")
        wikkel_layout.addWidget(self.wikkel_handmatige_invoer)
        options_layout.addLayout(wikkel_layout)

        # SSCC18 and null checkboxes
        sscc_null_layout = QHBoxLayout()
        self.sscc18 = QCheckBox("SSCC18")
        sscc_null_layout.addWidget(self.sscc18)
        self.null = QCheckBox("null")
        sscc_null_layout.addWidget(self.null)
        options_layout.addLayout(sscc_null_layout)

        # Radio buttons
        radio_layout = QHBoxLayout()
        self.radio_nl = QRadioButton("Nederlands")
        self.radio_nl.setChecked(True)
        self.radio_de = QRadioButton("Duits")
        self.radio_group = QButtonGroup()
        self.radio_group.addButton(self.radio_nl)
        self.radio_group.addButton(self.radio_de)
        radio_layout.addWidget(self.radio_nl)
        radio_layout.addWidget(self.radio_de)
        options_layout.addLayout(radio_layout)

        options_group.setLayout(options_layout)
        main_layout.addWidget(options_group)

        # --- Ok / Cancel buttons ---
        btn_layout = QHBoxLayout()
        ok_btn = QPushButton("Ok")
        ok_btn.clicked.connect(self.on_ok)
        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.close)
        btn_layout.addWidget(ok_btn)
        btn_layout.addWidget(cancel_btn)
        main_layout.addLayout(btn_layout)

        # --- Separator ---
        main_layout.addWidget(QLabel("_" * 60))
        main_layout.addWidget(QLabel("SAVE of LOAD inputform"))

        # --- Exit / Save / Load buttons ---
        bottom_layout = QHBoxLayout()
        exit_btn = QPushButton("Exit")
        exit_btn.clicked.connect(self.close)
        bottom_layout.addWidget(exit_btn)
        bottom_layout.addStretch()
        save_btn = QPushButton("SaveSettings")
        save_btn.clicked.connect(self.on_save_settings)
        bottom_layout.addWidget(save_btn)
        load_btn = QPushButton("LoadSettings")
        load_btn.clicked.connect(self.on_load_settings)
        bottom_layout.addWidget(load_btn)
        main_layout.addLayout(bottom_layout)

        self.setLayout(main_layout)

    def get_values(self):
        """Return a dict of all widget values, mirroring the PySimpleGUI values dict."""
        return {
            "order_number": self.order_number.text(),
            "aantal_vdps": self.aantal_vdps.text(),
            "folder_voor_vdp_map": self.folder_voor_vdp_map.text(),
            "totaal_aantal": self.totaal_aantal.text(),
            "begin_nummer": self.begin_nummer.text(),
            "veelvoud": self.veelvoud.text(),
            "posities": self.posities.text(),
            "aantal_per_rol": self.aantal_per_rol.text(),
            "mes": self.mes.text(),
            "Y_waarde": self.Y_waarde.text(),
            "prefix": self.prefix.text(),
            "postfix": self.postfix.text(),
            "hoogte": self.hoogte.text(),
            "kern": self.kern.text(),
            "opmerkingen": self.opmerkingen.text(),
            "csv_file_checkbox": self.csv_file_checkbox.isChecked(),
            "csv_file_in_pad": self.csv_file_in_pad.text(),
            "gebruik_template": self.gebruik_template.isChecked(),
            "template": self.template.text(),
            "slice_rechts_check": self.slice_rechts_check.isChecked(),
            "slice_rechts": self.slice_rechts.text(),
            "slice_links_check": self.slice_links_check.isChecked(),
            "slice_links": self.slice_links.text(),
            "wikkel_handmatig": self.wikkel_handmatig.isChecked(),
            "wikkel_handmatige_invoer": self.wikkel_handmatige_invoer.text(),
            "sscc18": self.sscc18.isChecked(),
            "null": self.null.isChecked(),
            "radio": self.radio_nl.isChecked(),
        }

    def set_values(self, values):
        """Set all widget values from a dict."""
        if "order_number" in values:
            self.order_number.setText(str(values["order_number"]))
        if "aantal_vdps" in values:
            self.aantal_vdps.setText(str(values["aantal_vdps"]))
        if "folder_voor_vdp_map" in values:
            self.folder_voor_vdp_map.setText(str(values["folder_voor_vdp_map"]))
        if "totaal_aantal" in values:
            self.totaal_aantal.setText(str(values["totaal_aantal"]))
        if "begin_nummer" in values:
            self.begin_nummer.setText(str(values["begin_nummer"]))
        if "veelvoud" in values:
            self.veelvoud.setText(str(values["veelvoud"]))
        if "posities" in values:
            self.posities.setText(str(values["posities"]))
        if "aantal_per_rol" in values:
            self.aantal_per_rol.setText(str(values["aantal_per_rol"]))
        if "mes" in values:
            self.mes.setText(str(values["mes"]))
        if "Y_waarde" in values:
            self.Y_waarde.setText(str(values["Y_waarde"]))
        if "prefix" in values:
            self.prefix.setText(str(values["prefix"]))
        if "postfix" in values:
            self.postfix.setText(str(values["postfix"]))
        if "hoogte" in values:
            self.hoogte.setText(str(values["hoogte"]))
        if "kern" in values:
            self.kern.setText(str(values["kern"]))
        if "opmerkingen" in values:
            self.opmerkingen.setText(str(values["opmerkingen"]))
        if "csv_file_checkbox" in values:
            self.csv_file_checkbox.setChecked(bool(values["csv_file_checkbox"]))
        if "csv_file_in_pad" in values:
            self.csv_file_in_pad.setText(str(values["csv_file_in_pad"]))
        if "gebruik_template" in values:
            self.gebruik_template.setChecked(bool(values["gebruik_template"]))
        if "template" in values:
            self.template.setText(str(values["template"]))
        if "slice_rechts_check" in values:
            self.slice_rechts_check.setChecked(bool(values["slice_rechts_check"]))
        if "slice_rechts" in values:
            self.slice_rechts.setText(str(values["slice_rechts"]))
        if "slice_links_check" in values:
            self.slice_links_check.setChecked(bool(values["slice_links_check"]))
        if "slice_links" in values:
            self.slice_links.setText(str(values["slice_links"]))
        if "wikkel_handmatig" in values:
            self.wikkel_handmatig.setChecked(bool(values["wikkel_handmatig"]))
        if "wikkel_handmatige_invoer" in values:
            self.wikkel_handmatige_invoer.setText(str(values["wikkel_handmatige_invoer"]))
        if "sscc18" in values:
            self.sscc18.setChecked(bool(values["sscc18"]))
        if "null" in values:
            self.null.setChecked(bool(values["null"]))
        if "radio" in values:
            if values["radio"]:
                self.radio_nl.setChecked(True)
            else:
                self.radio_de.setChecked(True)

    def browse_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Folder")
        if folder:
            self.folder_voor_vdp_map.setText(folder)

    def browse_file(self):
        file, _ = QFileDialog.getOpenFileName(self, "Select File")
        if file:
            self.csv_file_in_pad.setText(file)

    def on_save_settings(self):
        filename, _ = QFileDialog.getSaveFileName(self, "Save Settings")
        if filename:
            values = self.get_values()
            with open(filename, "w") as f:
                json.dump(values, f, indent=2)

    def _load_settings_file(self, filename):
        with open(filename, "rb") as f:
            raw = f.read()

        try:
            values = json.loads(raw.decode("utf-8"))
            if not isinstance(values, dict):
                raise ValueError("JSON settings must be an object")
            return values
        except (UnicodeDecodeError, json.JSONDecodeError):
            pass

        try:
            values = pickle.loads(raw)
            if not isinstance(values, dict):
                raise ValueError("Pickle settings must contain a dictionary")
            return values
        except Exception as exc:
            raise ValueError("Could not read settings as JSON or pickle") from exc

    def on_load_settings(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Load Settings")
        if filename:
            try:
                values = self._load_settings_file(filename)
            except Exception as exc:
                logger.exception(f"Failed to load settings from {filename}")
                QMessageBox.critical(
                    self,
                    "Load Settings Error",
                    f"Could not load settings file:\n{filename}\n\n{exc}",
                )
                return
            self.set_values(values)

    def on_ok(self):
        values = self.get_values()

        logger.debug("ok")

        pad = Path(values["folder_voor_vdp_map"])
        pad_file = Path(values["csv_file_in_pad"])
        aantal_vdps = int(values["aantal_vdps"])
        ordernummer = values["order_number"]
        totaal_aantal = int(values["totaal_aantal"])
        begin_nummer = int(values["begin_nummer"])

        veelvoud = int(values["veelvoud"])
        posities = int(values["posities"])
        vlg = 0

        begin_nummer_to_check = f"{begin_nummer:>{vlg}{posities}}"
        logger.debug(f"begin_nummer_to_check: {begin_nummer_to_check}")
        aantal_per_rol = int(values["aantal_per_rol"])
        Y_waarde = int(values["Y_waarde"])

        hoogte = int(values["hoogte"])
        kern = int(values["kern"])
        prefix = values["prefix"]
        postfix = values["postfix"]
        mes = int(values["mes"])
        opmerkingen = values["opmerkingen"]

        ##### Wikkel #####

        wikkel_handmatig = values["wikkel_handmatig"]
        if wikkel_handmatig:
            wikkel = int(values["wikkel_handmatige_invoer"])  # handmatige wikkel
        else:
            wikkel = de_uitgerekenende_wikkel(aantal_per_rol, hoogte, kern)

        ###############

        checkbox_slice_rechts = values["slice_rechts_check"]
        aantal_posities_uit_rechts = int(values["slice_rechts"])

        checkbox_slice_links = values["slice_links_check"]
        aantal_posities_uit_links = int(values["slice_links"])

        check_template = values["gebruik_template"]
        template10 = values["template"]
        naar_folder_pad = Path(values["folder_voor_vdp_map"])
        logger.debug(f"naar_folder_pad: {naar_folder_pad}")
        inloop = Y_waarde * 10 - Y_waarde

        sscc = values["sscc18"]
        logger.debug(f"sscc: {sscc}")

        if values["radio"] == True:
            taal_var = "nl"
        else:
            taal_var = "de"

        logger.info(f"radio={taal_var}")

        # todo let op identieke benaming denk dat als er een file in staat dat het altijd true is! csv_file_checkbox
        if values["csv_file_checkbox"]:
            ...
            # todo functie om excel en of csv omte zetten naar dataframe na
            # todo check of headers kloppen

            te_bewerken_dataframe_voor_plb_2020 = maak_csv_naar_dataframe(pad_file)
            logger.info(f"type(te_bewerken_dataframe_voor_plb_2020)={type(te_bewerken_dataframe_voor_plb_2020)}")

        else:

            # if not checkbox sscc __>
            # hier komt lijstmaker sscc of komt in def lijstmaker
            # of input zelf gemaakte lijst

            eerste_lijst_uit_input = nummer_lijst_bouwer(
                begin_nummer,
                totaal_aantal,
                "leeg.pdf",
                posities,
                mes,
                aantal_per_rol,
                0,
                prefix,
                postfix,
                sscc,
                veelvoud
            )
            # eerst bekijken of checkboxes aan staan dan aantal vpds

            te_bewerken_dataframe_voor_plb_2020 = pd.DataFrame(
                eerste_lijst_uit_input,
                columns=["Kolom", "pdf", "omschrijving"],
                dtype="str",
            )

            logger.debug(f"te_bewerken_dataframe_voor_plb_2020.head():\n{te_bewerken_dataframe_voor_plb_2020.head()}")
            logger.debug(f"te_bewerken_dataframe_voor_plb_2020.tail():\n{te_bewerken_dataframe_voor_plb_2020.tail()}")

        te_bewerken_dataframe_voor_plb_2020 = normalize_input_dataframe_for_numgen(
            te_bewerken_dataframe_voor_plb_2020
        )
        logger.debug(
            f"input kolommen na normalisatie: {te_bewerken_dataframe_voor_plb_2020.columns.to_list()}"
        )

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

        logger.debug(f"te_bewerken_dataframe_voor_plb_2020.head():\n{te_bewerken_dataframe_voor_plb_2020.head()}")

        template_length_checker = check_length_string_and_template_truths()

        temp_reader = sign_to_bool_translater()
        template_array = [temp_reader(x) for x in template10]
        template_array_truths = len(
            [temp_reader(x) for x in template10 if temp_reader(x) is True]
        )

        nieuw_nummer = number_translated_to_template()

        # als de check box aanstaat en het aantal tekens is gelijk aan de vraagtekens
        # (misschien een teller maken voor het aantal vraagtekens.

        # LET OP met het SSCC18 verhaal 17 18 (00) etc...

        # dit in een def zetten zodat erook een uitkomst kan komen
        # voor een negative uitslag posities of try except?

        if check_template:
            if not template_length_checker(
                begin_nummer_to_check, template_array_truths, sscc
            ):
                logger.info(
                    f"nummer is {len(begin_nummer_to_check)} tekens lang, template is {template_array_truths} tekens lang en dus zijn niet gelijk."
                )

        if check_template and template_length_checker(
            begin_nummer_to_check, template_array_truths, sscc
        ):
            te_bewerken_dataframe_voor_plb_2020[
                "hr_template"
            ] = te_bewerken_dataframe_voor_plb_2020["Kolom"].apply(
                lambda x: nieuw_nummer(
                    x,
                    template10,
                    template_array,
                    compare_template_with_number_list(),
                )
            )
        logger.debug(f"te_bewerken_dataframe_voor_plb_2020.head():\n{te_bewerken_dataframe_voor_plb_2020.head()}")

        #############################################

        # space for other checkboxes

        #############################################

        # main dataframe wordt hier verdeeld
        totaal_aantal_in_dataframe = len(te_bewerken_dataframe_voor_plb_2020)
        logger.debug(f"totaal_aantal_in_dataframe: {totaal_aantal_in_dataframe}")

        lijst_met_alle_dataframe_rollen = dataframe_cutter(
            te_bewerken_dataframe_voor_plb_2020, aantal_per_rol
        )
        tot_rol = len(lijst_met_alle_dataframe_rollen)
        tot_rol_pos = len(str(tot_rol))
        logger.debug(f"tot_rol_pos: {tot_rol_pos}")

        # eerste manier om rollen te maken door slice van dataframe
        rol = roll()

        #
        # rollen = [rol(df, wikkel, index)
        #           for index, df in enumerate(lijst_met_alle_dataframe_rollen)]
        # # list of tuples
        #
        ### dataframe_rol, functiewikkel, rolnum, posities, taal

        rollen = [
            rol_van_generators(df, wikkel, index, tot_rol_pos, taal_var)
            for index, df in enumerate(lijst_met_alle_dataframe_rollen)
        ]

        summary_rollen = [
            sum_begin_eind(rol_df, rolnum, wikkel)
            for rolnum, rol_df in enumerate(lijst_met_alle_dataframe_rollen)
        ]

        logger.debug(f"summary_rollen: {summary_rollen}")

        ###########################################

        # if lengte blok = n , dan uit lijst vdp aantal pak n aantal als blok lengte.
        #  nee verdeling is van klein naar groot nu ik moet of de laatste waarde eerst zetten.
        # HET MOET per rollen per vdp worden !per rollen gaan doen
        # wel even controleren

        # dataframe opdelen in rollen

        # rollen maken

        totaal_aan_rollen = dataframe_cutter(
            te_bewerken_dataframe_voor_plb_2020, aantal_per_rol
        )

        logger.debug(f"len(totaal_aan_rollen): {len(totaal_aan_rollen)}")

        kolom_namen = headers_for_totaal_kolommen(
            te_bewerken_dataframe_voor_plb_2020, mes
        )
        logger.debug(f"kolom_namen: {kolom_namen}")

        sum_kol = filter_kolommen_pdf(mes, "baan")
        kolom_vervang_waarde_pdf = filter_kolommen_pdf(mes, "pdf")

        ##########################################



        ######################################

        if aantal_vdps == 1:
            logger.info("verwerk de lijst zoals ie nu is")
            # lijst in lijst maken

            vdp_alle_combinaties = len(totaal_aan_rollen) // mes
            logger.debug(f"vdp_alle_combinaties: {vdp_alle_combinaties}")

            lijst_van_lijst_van_alle_rollen = lijst_opbreker(
                rollen, mes, vdp_alle_combinaties
            )

            logger.debug(f"len(lijst_van_lijst_van_alle_rollen): {len(lijst_van_lijst_van_alle_rollen)}")

            # dit maakt een 'vdpblok' van de combinaties en rollen zonder in uitloop
            VDP = stapel_df_baan(lijst_van_lijst_van_alle_rollen)

            VDP, kolom_namen = assign_vdp_kolom_namen(
                VDP,
                te_bewerken_dataframe_voor_plb_2020,
                mes,
                "single-vdp",
            )
            logger.debug(f"kolom_namen: {kolom_namen}")
            logger.debug(f"VDP.dtypes: {VDP.dtypes}")
            ################################################
            # naamgeving vdp csv zonder index alles als string

            vdp_bestandsnaam = pad.joinpath(f"{ordernummer} VDP.csv")
            vdp_bestandsnaamexcel = pad.joinpath(f"{ordernummer} VDP.xlsx")


            vdp_1_df= inloop_uitloop_stans(
                VDP, wikkel, Y_waarde, kolom_vervang_waarde_pdf, aantal_per_rol
            )
            meterlijst = vdp_meters_uit_df_shape(vdp_1_df,hoogte)
            vdp_1_df.to_csv(vdp_bestandsnaam, index=0)
            vdp_1_df.to_excel(vdp_bestandsnaamexcel)


            ### summary
            lijst_alle_summary_rollen = lijst_opbreker(
                summary_rollen, mes, vdp_alle_combinaties
            )
            summary_vdp_1 = stapel_df_baan(lijst_alle_summary_rollen)
            summary_vdp_1.columns = sum_kol
            summary_vdp_1_bestandsnaam = pad.joinpath(f"{ordernummer} summary.xlsx")
            summary_vdp_1_html_bestandsnaam = pad.joinpath(
                f"{ordernummer} summary.html"
            )
            summary_vdp_1.to_excel(summary_vdp_1_bestandsnaam, index=0)
            summary_vdp_1.to_html(summary_vdp_1_html_bestandsnaam, index=0)

            keywordargs = {
                "Ordernummer: ": ordernummer,
                "Aantal VDP's": aantal_vdps,
                "vdp meters: ": f'{meterlijst} m',
                "Totaal aantal ": str(f"{totaal_aantal* veelvoud:,} etiketten").replace(",", "."),
                "begin_nummer": f"{prefix}{begin_nummer:>{0}{posities}}{postfix}",
                "eind_nummer": f"{prefix}{begin_nummer + totaal_aantal - 1:>{0}{posities}}{postfix}",
                "Aantal Rollen": f"{totaal_aantal * veelvoud // aantal_per_rol} rol(len) van {aantal_per_rol}",
                "Mes ": mes,
                "Wikkel": f"{wikkel + 3} etiketten inclusief sluitetiket",
                "Inloop en uitloop": f"{Y_waarde} x 10 sheets.",
                "Opmerkingen": opmerkingen,
            }

            html_sum_form_writer(pad, ordernummer, **keywordargs)



        else:
            lengte_df = len(te_bewerken_dataframe_voor_plb_2020)

            tot_comb_ = combinaties_over_totale_order(
                lengte_df, aantal_per_rol, mes
            )
            logger.debug(f"tot_comb_: {tot_comb_}")

            combinatie_verdeling = combinaties(tot_comb_, aantal_vdps, mes)

            logger.debug(f"combinatie_verdeling: {combinatie_verdeling}")

            vdp_alle_combinaties = len(totaal_aan_rollen) // mes
            logger.debug(f"vdp_alle_combinaties: {vdp_alle_combinaties}")

            lijst_van_lijst_van_alle_rollen = lijst_opbreker(
                rollen, mes, vdp_alle_combinaties
            )

            logger.debug(f"len(lijst_van_lijst_van_alle_rollen): {len(lijst_van_lijst_van_alle_rollen)}")

            verdeelde_lijst_van_vdps = verdeling_met_slice(
                lijst_van_lijst_van_alle_rollen, combinatie_verdeling
            )
            logger.debug(f"pad: {pad}")

            pdf_kol = filter_kolommen_pdf(mes, "pdf")

            meterlijst=[]

            for count, vdp in enumerate(verdeelde_lijst_van_vdps):
                bestandsnaam = pad.joinpath(f"{ordernummer} VDP")
                naam = vdpnaam(bestandsnaam, count + 1)

                htmlnaam = pad.joinpath(f"{ordernummer} VDP", ".html")
                logger.debug(f"htmlnaam: {htmlnaam}")

                verwerkte_vdp = stapel_df_baan(vdp)
                verwerkte_vdp, kolom_namen = assign_vdp_kolom_namen(
                    verwerkte_vdp,
                    te_bewerken_dataframe_voor_plb_2020,
                    mes,
                    f"multi-vdp-{count + 1}",
                )
                logger.debug(f"kolom_namen: {kolom_namen}")
                meterlijst.append(vdp_meters_uit_df_shape(verwerkte_vdp,hoogte))

                inloop_uitloop_stans(
                    verwerkte_vdp, wikkel, Y_waarde, pdf_kol, aantal_per_rol
                ).to_csv(naam, index=0)

                ######################## summary #########################
                # TODO PUT SUMMARY IN MODULE EN FORLOOPS IN DEF

                summary_lijst_van_lijst = lijst_opbreker(
                    summary_rollen, mes, vdp_alle_combinaties
                )

                verdeelde_summary_lijst = verdeling_met_slice(
                    summary_lijst_van_lijst, combinatie_verdeling
                )
                sum_df_lijst = []
                for count, sum_roll in enumerate(verdeelde_summary_lijst):
                    bestandsnaam = pad.joinpath(f"{ordernummer} Summary")

                    naam = vdpnaam(bestandsnaam, count + 1, ".xlsx")
                    htmlnaam = vdpnaam(bestandsnaam, count + 1, ".html")

                    verwerkte_summary = stapel_df_baan(sum_roll)
                    verwerkte_summary.columns = sum_kol
                    scheiding = pd.DataFrame(
                        [f"vdp {count + 1}"], columns=["VDP"]
                    )  # todo zet hier wikkel en andere informatie in svp
                    sum_vdp = pd.concat(
                        [scheiding, verwerkte_summary, scheiding], axis=0
                    )

                    sum_df_lijst.append(sum_vdp)

                pd.concat(sum_df_lijst).fillna(" ").to_html(
                    pad.joinpath(f"{ordernummer} Summary.html"), index=False
                )
                pd.concat(sum_df_lijst).to_excel(
                    pad.joinpath(f"{ordernummer} Summary.xlsx"), index=False
                )

                ######################## einde summary #########################

                ##################################


            # values from GUI
            logger.debug(f"meterlijst: {meterlijst}")
            meters = [f'VDP {vdp+1} : {str(meters)} m' for vdp, meters in enumerate(meterlijst)]
            logger.debug(f"meters: {meters}")
            logger.debug(f"values: {values}")

            keywordargs = {
                "Ordernummer: ": ordernummer,
                "Aantal VDP's": aantal_vdps,
                "vdp meters: ": ', '.join(meters),
                'lijstmeters': meterlijst,
                "Totaal aantal ": str(f"{totaal_aantal*veelvoud:,} etiketten").replace(",", "."),
                "begin_nummer": f"{prefix}{begin_nummer:>{0}{posities}}{postfix}",
                "eind_nummer": f"{prefix}{begin_nummer + totaal_aantal - 1:>{0}{posities}}{postfix}",
                "Aantal Rollen": f"{totaal_aantal * veelvoud// aantal_per_rol} rol(len) van {aantal_per_rol}",
                "Mes ": mes,
                "Wikkel": f"{wikkel + 3} etiketten inclusief sluitetiket",
                "Inloop en uitloop": f"{Y_waarde} x 10 sheets.",
                "Opmerkingen": opmerkingen,
            }

            html_sum_form_writer(pad, ordernummer, **keywordargs)

            ###################################
            for val in values:
                logger.info(val)


def main():
    app = QApplication(sys.argv)
    window = NummerGeneratorWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
