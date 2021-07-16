""""function with gui for exporting custom input from string
1 make number, make numberstring
2 make template string in to a list
3 make bool list
4
 original from project lijstmaker 2021_1
"""

from collections import Counter


def sign_to_bool_translater():
    '''takes 1 character from a string iterable
    and changes it into True if it is a template sign'''
    def change_one_sign(mark):
        if mark == "?":
            return True
        else:
            return False
    return change_one_sign


def check_num_template():
    """checks if template is equal in positions with number
           returns bool"""

    def check_nummer_met_template(number, template):
        c = Counter(template)
        vraagtekens = c["?"]
        if vraagtekens == len(number):
            # message in simple py GUI
            print("ok")
            return True

        else:
            # message in simple py GUI
            print(f"vraagtekens(?) in template == {vraagtekens} en getal == {len(number)}!! maak waardes svp gelijk")
            return False

    return check_nummer_met_template


def compare_template_with_number_list():
    """walks through the two lists and compares them, unfinished only works if len list == equal :
    run after check_num_template"""
    def two_lists_use_on_true(templatelijst, nummerstring, input, i):

        if input == False:
            nummerstring.insert(0, " ")
            return templatelijst[i]
        else:
            return nummerstring[i]
    return two_lists_use_on_true



# ct = sign_to_bool_translater()
#
# ct("0")
# sscc = "00350504067240000013"
# sscc18_HR = "(00) 3 5050406 724000001 3"
# templatesscc18 = "(??) ? ???????  ????????? ?"
#
# array_bool_1 = [ct(x) for x in templatesscc18]
#
# ctt = sign_to_bool_translater()
# array_bool = [ctt(x) for x in templatesscc18]
# # todo check deze 1
# testlijst = compare_template_with_number_list()
# newnumber = []
# l1 = list(templatesscc18)
# l2 = list(sscc)
# for index in range(len(l1)):
#     newnumber.append(testlijst(l1,l2,array_bool[index],index))
# print(('').join(newnumber))
# newnumber=[]


def check_length_string_and_template_truths():
    '''takes the string and the template and only returns TRUE or FALSE
    if length is equal or != to length
    I dont want program to run  and will use try etc... to break program    and let user fix the error'''
    def check_lengtes_bool(number_string, counted_truths):
        if not len(number_string)+1 == counted_truths:
            print(counted_truths)
            return False
        else:
            return True

    return check_lengtes_bool


def template_translate_2_bool_list():
    """enter a template string made of ????
    to show how the user wants to convert a number
    to a human readable or needed form"""
    def temp_translate(functiebool,template_string):
        """if it is a function dont use the parenthesis in the definition"""
        truth = functiebool
        array_bool_list = [truth(str(x)) for x in template_string]
        return array_bool_list
    return temp_translate


def number_translated_to_template():
    """ 1 input number as string (to list)
        2 a template
        3 bool  list of template"""

    def translated_number(number_to_list, template_string, array_bool_, func):
        """"func = compare_template_with_number_list()
        ik denk dat hier een decorator zou moeten komen"""
        functie_compare_t_w_n = func
        new_number = []
        list_number = list(number_to_list)
        template_list = list(template_string)

        for i in range(len(template_list)):
            new_number.append(functie_compare_t_w_n(template_list, list_number, array_bool_[i], i))

        return ('').join(new_number)

    return translated_number


#todo build function to accomadate all these function:)


def checking_box_template(a,b):
    if a and b == True:
        pass







