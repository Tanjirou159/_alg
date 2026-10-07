# Custom map without loops
def my_map(func, lst):
    if not lst:
        return []
    return [func(lst[0])] + my_map(func, lst[1:])


# Custom filter without loops
def my_filter(func, lst):
    if not lst:
        return []
    head, tail = lst[0], lst[1:]
    if func(head):
        return [head] + my_filter(func, tail)
    return my_filter(func, tail)


# Custom reduce without loops
def my_reduce(func, lst, initial=None):
    if not lst:
        if initial is None:
            raise TypeError("my_reduce() of empty sequence with no initial value")
        return initial
    if initial is None:
        return my_reduce(func, lst[1:], lst[0])
    return my_reduce(func, lst[1:], func(initial, lst[0]))


# One pass of Bubble Sort implemented via custom my_reduce
def bubble_pass(lst):
    def step(acc, x):
        if not acc:
            return [x]
        # Compare adjacent elements; swap if unsorted
        if acc[-1] > x:
            return acc[:-1] + [x, acc[-1]]
        return acc + [x]
    
    return my_reduce(step, lst, [])


# Bubble Sort without loops
def bubble_sort(lst):
    def _sort(arr, steps_left):
        if steps_left <= 1 or not arr:
            return arr
        return _sort(bubble_pass(arr), steps_left - 1)
    
    return _sort(lst, len(lst))


# Execution Test
data = [64, 34, 25, 12, 22, 11, 90]
sorted_data = bubble_sort(data)

print("Original Data:", data)
print("Sorted Data:  ", sorted_data)

# Verifying custom my_filter and my_map
evens = my_filter(lambda x: x % 2 == 0, sorted_data)
doubled = my_map(lambda x: x * 2, sorted_data)

print("Filtered Evens:", evens)
print("Mapped Doubled:", doubled)