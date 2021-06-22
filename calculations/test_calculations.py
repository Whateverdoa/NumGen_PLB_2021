from .calculations import *
from data.data_definitions import *


def test_delen():
    test = delen(1000, 3)
    assert test == 333


def test_lengte_dataframe():
    test = lengte_dataframe(test_df)
    assert test == 195354


def test_lijst_begin_eind_voor_slice():
    blok_lengte = delen(lengte_dataframe(test_df), 3)
    test = lijst_begin_eind_voor_slice(lengte_dataframe(test_df), blok_lengte)
    assert test == [0, 65118, 130236, 195354]


def test_begin_eind_dataframe():
    test = begin_eind_dataframe(test_df)

    assert test == ('MH376MP6', 'MHJ688V8', 195354)


def test_combinaties_per_vdp_berekenen():
    comp = combinaties_per_vdp_berekenen()
    test = comp(9, 2, 3)

    assert test == [5, 4]
