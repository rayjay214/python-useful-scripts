#!/usr/bin/env python
# coding=utf-8

g_dict={}

with open('csv_to_dict.csv', 'r') as record_list:
    for line in record_list:
        line = line.strip()
        col_list = line.split(',')
        try:
            key = col_list[0]
            value = col_list[1]
            g_dict[key] = value
        except Exception as e:
		    print(line)
		    print(e)

for key in g_dict:
    print("key:{}, value:{}".format(key, g_dict[key]))
