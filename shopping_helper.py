#!/usr/bin/env python
'''
Shopping Helper

Given a list of store inventories and a shopping list, return the minimum number of
store visits required to satisfy the shopping list.

For example, given the following stores & shopping list:

  Shopping List: 10 apples, 4 pears, 3 avocados, 1 peach

  Kroger: 4 apples, 5 pears, 10 peaches
  CostCo: 3 oranges, 4 apples, 4 pears, 3 avocados
  ALDI: 1 avocado, 10 apples
  Meijer: 2 apples

The minimum number of stores to satisfy this shopping list would be 3:
Kroger, CostCo and ALDI.
or
Kroger, CostCo and Meijer.

Shopping lists and store inventories will be passed in JSON format,
an example of which will be attached in the email.  Sample outputs for the
given inputs should also be attached as well.

Use the helper provided to print.

Usage: shopping_helper.py (shopping_list.json) (inventories.json)
'''

import argparse
import copy
import json

# to help you get started, we have provided some boiler plate code

# Hello, I struggled on the logic to get the overall shortest path to fill the shopping cart.
# I'm comfortable with my logic otherwise and I would appreciate it if you would send me
# an approximate way to fulfill the requirement for this exercise. brent.allen.foster@outlook.com

def satisfy_shopping_list(shopping_list_json, inventory_json):
    # find out minimum combination of stores that would satisfy shopping list
    shopping_list_dict = json.loads(json.dumps(shopping_list_json))
    store_inv_dict = json.loads(json.dumps(inventory_json))
    inventory_dictionary = {}

    shopping_list_val_zero = []
    # Only look for items that are in the shopping list, ignore other inventory
    for x in shopping_list_dict:
        if shopping_list_dict.get(x) > 0: # No need to check inventory if list is zero
             for e in store_inv_dict:
                for p in store_inv_dict[e]:
                     # No need to add item from inventory if zero
                    if x in p['inventory'] and p['inventory'].get(x) > 0:
                        store_name = p['name']
                        inv_qty = p['inventory'].get(x)
                        inner_dict = {store_name : inv_qty}
                        # Break up the logic into another method
                        inventory_dictionary = store_inventory_based_on_items_in_list(
                            inventory_dictionary, x, inner_dict)
        else:
            shopping_list_val_zero.append(x)

    for i in shopping_list_val_zero:
        shopping_list_dict.pop(i)

    # Find out here if whole shopping list is possible
    for x in shopping_list_dict:
        if x not in inventory_dictionary.keys():
            print("No store carries [" + x + "]")
            exit()           
    match_list_with_inventory(shopping_list_dict, inventory_dictionary)

def store_inventory_based_on_items_in_list(main_dictionary, item_name, item_store_inventory_dict):
    if main_dictionary.has_key(item_name):
        tmp_dict = main_dictionary.get(item_name)
        tmp_dict.update(item_store_inventory_dict)
        main_dictionary[item_name] = tmp_dict
    else:
        main_dictionary[item_name] = item_store_inventory_dict
    return main_dictionary

def match_list_with_inventory(shopping_list_dict, inventory_dictionary):
    compiled_dict = {}
    for i in shopping_list_dict:
        qty_needed = shopping_list_dict.get(i)
        x = inventory_dictionary.get(i)
        for p in x:
            inv_qty = x.get(p)
            adj_qty = 0
            if inv_qty >= qty_needed:
                adj_qty = qty_needed
            else:
                adj_qty = inv_qty
            if compiled_dict.has_key(i):
                temp_dict = compiled_dict.get(i)
                inner_var = 0
                for u in temp_dict:
                    inner_var += temp_dict.get(u)
                if inner_var == qty_needed:
                    break
                else:
                    tmp_var = qty_needed - inner_var
                    if inv_qty <= tmp_var:
                        adj_qty = inv_qty
                    else:
                        adj_qty = tmp_var
                temp_dict.update({p : adj_qty})
                compiled_dict[i] = temp_dict
                break
            else:
                compiled_dict[i] = {p : adj_qty}
    if shopping_list_go_no_go(shopping_list_dict, compiled_dict):
        for u in compiled_dict:
            pass_dict = compiled_dict.get(u)
            print("For [" + u + "]")
            for e in pass_dict:
                print("Go to {" + e + "} and get (" +
                                    str(pass_dict.get(e)) + ")")
        print("Shopping list can be completed (Pass)")
    else:
        print("Shopping list cannot be completed (Fail)")

def shopping_list_go_no_go(shopping_list_dict, compiled_dict):
    is_list_complete = True
    for i in shopping_list_dict:
        qty_needed = shopping_list_dict.get(i)
        x = compiled_dict.get(i)
        qty = 0
        for p in x:
            qty += x.get(p)
        if qty != qty_needed:
            print("Need to get (" + str(qty_needed) + ") [" + i +
            "] but could only find (" + str(qty) + ")")
            is_list_complete = False
    return is_list_complete

def main():
    args = parse_args()
    with open(args.shopping_list_json_path) as shopping_list_json_file, open(args.inventory_json_path) as inventory_json_file:
        shopping_list_json = json.load(shopping_list_json_file)
        inventory_json = json.load(inventory_json_file)
        satisfy_shopping_list(shopping_list_json, inventory_json)

def parse_args():
    p = argparse.ArgumentParser()

    p.add_argument('shopping_list_json_path')
    p.add_argument('inventory_json_path')

    args = p.parse_args()
    return args

if __name__ == '__main__':
    main()
