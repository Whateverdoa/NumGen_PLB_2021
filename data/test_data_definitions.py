from data.data_definitions import *

totaal = 102_000
aantal_vdps = 2
mes = 3

apr = 1000
# bepaal = vdp_aantal_bepalen()
# arg = bepaal(totaal, aantal_vdps, apr, mes)


# def test_vdp_aantalen_berekenen():
#     test = aantallen_per_vdp_lijst(363000, 5, 1000, mes)
#     print(sum([72600, 72600, 72600, 72600, 72600]))
#     assert test == [72600, 72600, 72600, 72600, 72600]


def test_rest_rollen_uitrekenen():
    """gedeelte van lijstmaker"""
    mes, totaal, apr = 4, 1_000_000, 1000
    test = rest_rollen_uitrekenen(mes, totaal, apr)
    assert test == 0


# def test_vdp_aantal_bepalen():
#     bepaal = vdp_aantal_bepalen()
#     test = bepaal(totaal, aantal_vdps, apr, mes)
#     assert test == [51000, 50000]


# def test_rollen_uit_aantallen():
#     bepaal = vdp_aantal_bepalen()
#     arg = bepaal(totaal, aantal_vdps, apr, mes)
#     omgezette_lijst = rollen_uit_aantallen()
#     test = omgezette_lijst(arg, aantal_vdps, apr)
#
#     assert test == [51, 51]


def test_combinaties_uit_rollen():
    combinaties = combinaties_uit_rollen()
    test = combinaties([51, 51], mes)

    assert test == [17, 17]


def test_combinaties_berekenen():
    test = combinaties_over_totale_order(380000,9500,5)
    assert test == 8
