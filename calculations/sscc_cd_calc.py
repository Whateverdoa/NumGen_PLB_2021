import pandas as pd
from checkdigit._data import cleanse, convert
from checkdigit import gs1
from icecream import ic

def calculate(data: str) -> str:
    """Calculates the luhn check digit.

    Args:
        data: A block of data without the check digit

    Returns:
        str: A string representing the missing check digit

    """
    data = cleanse(data)
    position_counter = 1  # 1-based indexing
    total_sum = 0
    for item in data[::-1]:  # Reverses String
        digit = int(item)
        if position_counter % 2:  # If position number is odd with reversed string
            add_value = digit * 3
            total_sum += add_value
        else:

            total_sum += digit

        # ic(total_sum)
        position_counter += 1
    return convert(10 - (total_sum % 10), "luhn")


sscc = 8717496330005000
# ic(calculate(sscc))
ic(gs1.calculate("08717496330005005"))




def maak_sscc_lijst(begin_nummer, totaal, pdf='leeg.pdf'):
    '''list comp voor maken nummer lijst, 3 kolommen
    kijk voor benamingen in project lijst bewerken'''
    eind = begin_nummer + totaal
    nummers = [[f'{x:>{0}{17}}{gs1.calculate(str(x))}',f'{pdf}'," "] for x in range(begin_nummer,eind)]


    return nummers

print(maak_sscc_lijst(sscc, 10))

df = pd.DataFrame(maak_sscc_lijst(sscc, 51000), columns=["kolom1", "pdf", "omschrijving"], dtype="str")
ic(df.head(50))
df.to_csv('check.csv',sep=";", encoding="utf-8",index=0)