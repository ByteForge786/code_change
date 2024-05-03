def check_matching_lists(list1, list2):
    set1 = set(list1)
    for item in list2:
        if item not in set1:
            print("Not all values in the second list match with the first list.")
            return
    print("All values in the second list match with the first list.")

# Sample lists
list1 = ['apple', 'banana', 'orange', 'pear']
list2 = ['banana', 'orange']

# Check if all values in list2 match with list1
check_matching_lists(list1, list2)
