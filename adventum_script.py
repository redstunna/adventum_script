import sys
import csv

if (len(sys.argv) < 2 or len(sys.argv) > 3):
    print("Argument error")
    print("Usage: python adventum_script.py <path_to_csv>")
    print("Usage: python adventum_script.py <path_to_csv> <budget_value>")
    print("Example: python adventum_script.py my_data.csv 15")
    sys.exit()

if (sys.argv[1] == "--help" or sys.argv[1] == "-h"):
    print("Usage: python adventum_script.py <path_to_csv>")
    print("Usage: python adventum_script.py <path_to_csv> <budget_value>")
    print("Example: python adventum_script.py my_data.csv 15")
    sys.exit()

def check_source_in_dict(dict,source_name):
    if (source_name in dict):
        dict[source_name] = dict[source_name] + 1
    else:
        dict[source_name] = 1

def add_to_source_dict(in_dict, out_dict):
    for in_key in in_dict:
        if (in_key in out_dict):
            out_dict[in_key] = out_dict[in_key] + in_dict[in_key]
        else:
            out_dict[in_key] = in_dict[in_key]

#------check cpc,cpm,aff values-----
def source_count(lst, conv_value):
    cpc_count = 0
    cpm_count = 0
    aff_count = 0
    out_dict = {}
    for str in lst:
        if('cpc' in str):
            cpc_count = cpc_count + 1
            check_source_in_dict(out_dict, str)

        if ('cpm' in str):
            cpm_count = cpm_count + 1
            check_source_in_dict(out_dict, str)

        if ('affiliate' in str):
            aff_count = aff_count + 1
            check_source_in_dict(out_dict, str)

    sum = cpc_count + cpm_count + aff_count

    for key in out_dict:
        out_dict[key] = conv_value/sum*out_dict[key]

    return out_dict

sources_dict = {}
lst = []
with open(sys.argv[1], 'rt') as csvfile:
    data = csv.reader(filter(lambda row: row[0] != '#',
                                   csvfile))
    #-------skip header-------
    next(data,None)

    for row in data:
        if ("cpc" in row[0]
            or "cpm"in row[0]
            or "affiliate" in row[0]):
            lst.append(row)

    for row in lst:
        source_medium_lst = row[0].split(" > ")
        conv_value = float(row[2].replace('$', '').replace(',', ''))
        count_dict = source_count(source_medium_lst, conv_value)
        add_to_source_dict(count_dict, sources_dict)


    sum_conv_value = 0
    for key in sources_dict:
        sum_conv_value = sum_conv_value + sources_dict[key]

    if (len(sys.argv)==2):
        print("Source/Medium Path : Conversion Value / Part Conversion Value")
        for key in sources_dict:
            print(key,":", sources_dict[key], "/", sources_dict[key]/sum_conv_value*100,"%")
    else:
        print("Source/Medium Path : Conversion Value / Part Conversion Value | Budget Part")
        for key in sources_dict:
            print(key,":", sources_dict[key], "/", sources_dict[key]/sum_conv_value*100,"%","|", sources_dict[key]/sum_conv_value*float(sys.argv[2]))

