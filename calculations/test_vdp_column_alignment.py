import pandas as pd

from calculations.calculations import (
    assign_vdp_kolom_namen,
    dataframe_cutter,
    lijst_opbreker,
    maak_csv_naar_dataframe,
    normalize_input_dataframe_for_numgen,
    pad_csv_dataframe_to_full_mes_rollen,
    stapel_df_baan,
)
from data.data_definitions import rol_van_generators


def _build_vdp(df_in, mes=4, aantal_per_rol=25, wikkel=5):
    rollen_dataframes = dataframe_cutter(df_in, aantal_per_rol)
    tot_rol_posities = len(str(len(rollen_dataframes)))
    rollen = [
        rol_van_generators(df, wikkel, index, tot_rol_posities, "nl")
        for index, df in enumerate(rollen_dataframes)
    ]
    vdp_alle_combinaties = len(rollen_dataframes) // mes
    lijst_van_lijst = lijst_opbreker(rollen, mes, vdp_alle_combinaties)
    return stapel_df_baan(lijst_van_lijst)


def test_normalize_input_dataframe_for_numgen_adds_required_columns():
    bron = pd.DataFrame({"kolom1": ["1001", "1002"]}, dtype="str")

    uit = normalize_input_dataframe_for_numgen(bron)

    assert "Kolom" in uit.columns
    assert "pdf" in uit.columns
    assert "omschrijving" in uit.columns
    assert uit["Kolom"].tolist() == ["1001", "1002"]
    assert uit["pdf"].tolist() == ["leeg.pdf", "leeg.pdf"]
    assert uit["omschrijving"].tolist() == ["", ""]


def test_assign_vdp_kolom_namen_recovers_from_mismatch():
    bron = pd.DataFrame(
        {f"c{index}": [f"{index}_{x}" for x in range(100)] for index in range(10)},
        dtype="str",
    )
    vdp = _build_vdp(bron)

    vdp_uit, kolom_namen = assign_vdp_kolom_namen(vdp, bron, 4, "pytest-mismatch")

    assert len(kolom_namen) == vdp_uit.shape[1] == 48
    assert "pdf_1" in kolom_namen
    assert "omschrijving_1" in kolom_namen


def test_assign_vdp_kolom_namen_with_aligned_schema():
    bron = pd.DataFrame(
        {
            "Kolom": [f"{x:04d}" for x in range(100)],
            "pdf": ["leeg.pdf"] * 100,
            "omschrijving": [""] * 100,
            "extra": [f"waarde{x}" for x in range(100)],
        },
        dtype="str",
    )
    vdp = _build_vdp(bron)

    vdp_uit, kolom_namen = assign_vdp_kolom_namen(vdp, bron, 4, "pytest-aligned")

    assert len(kolom_namen) == vdp_uit.shape[1]
    assert kolom_namen[0] == "Kolom_1"
    assert kolom_namen[-1] == "extra_4"


def test_dataframe_from_csv_handles_semicolon_and_comma(tmp_path):
    semicolon_csv = tmp_path / "semicolon.csv"
    semicolon_csv.write_text(
        "Kolom;pdf;omschrijving\n1001;leeg.pdf;\n1002;leeg.pdf;\n",
        encoding="utf-8",
    )

    comma_csv = tmp_path / "comma.csv"
    comma_csv.write_text(
        "Kolom,pdf,omschrijving\n1001,leeg.pdf,\n1002,leeg.pdf,\n",
        encoding="utf-8",
    )

    semicolon_df = maak_csv_naar_dataframe(semicolon_csv)
    comma_df = maak_csv_naar_dataframe(comma_csv)

    assert semicolon_df.shape == (2, 3)
    assert comma_df.shape == (2, 3)
    assert semicolon_df.columns.to_list() == ["Kolom", "pdf", "omschrijving"]
    assert comma_df.columns.to_list() == ["Kolom", "pdf", "omschrijving"]


def test_pad_csv_dataframe_partial_roll_only():
    bron = pd.DataFrame(
        {
            "Kolom": [str(x) for x in range(10)],
            "pdf": ["leeg.pdf"] * 10,
            "omschrijving": [""] * 10,
        },
        dtype="str",
    )

    uit, info = pad_csv_dataframe_to_full_mes_rollen(bron, mes=4, aantal_per_rol=3)

    assert info == {
        "pad_total": 2,
        "pad_partial": 2,
        "pad_full": 0,
        "totaal_rollen_na_pad": 4,
    }
    assert len(uit) == 12
    assert uit.iloc[-1]["pdf"] == "stans.pdf"


def test_pad_csv_dataframe_partial_and_full_rolls():
    bron = pd.DataFrame(
        {
            "Kolom": [str(x) for x in range(13)],
            "pdf": ["leeg.pdf"] * 13,
            "omschrijving": [""] * 13,
        },
        dtype="str",
    )

    uit, info = pad_csv_dataframe_to_full_mes_rollen(bron, mes=4, aantal_per_rol=3)

    assert info == {
        "pad_total": 11,
        "pad_partial": 2,
        "pad_full": 9,
        "totaal_rollen_na_pad": 8,
    }
    assert len(uit) == 24
    assert (uit.iloc[-11:]["pdf"] == "stans.pdf").all()
