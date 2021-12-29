import math

def find_percentile(a, b, p=50):
    small_arr = a if len(a) < len(b) else b
    big_arr = a if len(a) > len(b) else b

    sum_len = len(a) + len(b)
    half_len = (sum_len) // 2
    is_odd_arr = bool(sum_len % 2)

    midpoint = half_len if is_odd_arr else half_len - 1
    # to find a median we need to find no more than midpoint elements
    # we use 2-pointers approach
    # we divide the smallest array on 2, and getting the pointer pointing on the half of it
    # so to find another part of the array we need to look for the first midpoint - smallest part,
    # in total the nessesary amount of elements

    left_pointer = len(small_arr) // 2
    right_pointer = half_len - left_pointer

    # now we need to check if the pointers don't overlap each other:
    # right_pointer <= then next to the left_pointer element,
    # and left_pointer <= then next to the right_pointer element - as they were in the same array.
    # if they overlap, we need to move pointer and recompute anoter and repeat it until they don't overlap.

    while right_pointer > small_arr[left_pointer] and left_pointer > big_arr[right_pointer]:
        left_pointer += 1
        right_pointer = half_len - left_pointer

    if is_odd_arr:
        midpoint = min(small_arr[left_pointer], big_arr[right_pointer])
    else:
        midpoint = min(small_arr[left_pointer], big_arr[right_pointer]) - 1

    return midpoint
