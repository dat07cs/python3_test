import random
import string
from contextlib import contextmanager

if __name__ == '__main__':
    def explain(fruits, summary):
        map = {fruit[:2]: fruit for fruit in fruits}
        quantity = ''
        fruit = ''
        result = ''
        for i in range(len(summary)):
            if summary[i].isdigit() and fruit:
                if result:
                    result += ' + '
                result += quantity + ' x ' + (map[fruit] if fruit in map else 'NA')
                quantity = ''
                fruit = ''
            if summary[i].isdigit():
                quantity += summary[i]
            else:
                fruit += summary[i]

        if result:
            result += ' + '
        result += quantity + ' x ' + (map[fruit] if fruit in map else 'NA')

        return result

    fruits = ['orange', 'apple', 'pear']
    # print(explain(fruits, '1or10ap12pe'))
    # print(explain(fruits, '1or10ap12xx'))

    class Rect(object):
        def __init__(self, x, y, w, h):
            self.x = x
            self.y = y
            self.w = w
            self.h = h

    def is_intersect(r1, r2):
        """
        :type r1: Rect
        :type r2: Rect
        """

    def find_longest_palindrome(text):
        n = len(text)
        if n == 0:
            return
        n = 2 * n + 1  # Position count
        l = [0] * n
        l[0] = 0
        l[1] = 1
        c = 1  # center position
        r = 2  # center right position
        max_lps_length = 0
        max_lps_center_position = 0

        # Uncomment it to print LPS length array
        # print('%d %d' % (L[0], L[1]))
        for i in range(2, n):  # current right position

            # get current left position i_mirror for current right position i
            i_mirror = 2 * c - i  # current left position
            l[i] = 0
            diff = r - i
            # If current right position i is within current right position r
            if diff > 0:
                l[i] = min(l[i_mirror], diff)

            # Attempt to expand palindrome centered at current right position i
            # Here for odd positions, we compare characters and if match then increment LPS length by ONE
            # If even position, we just increment LPS by ONE without any character comparison
            try:
                while ((i + l[i]) < n and (i - l[i]) > 0) and \
                        (((i + l[i] + 1) % 2 == 0) or (text[(i + l[i] + 1) // 2] == text[(i - l[i] - 1) // 2])):
                    l[i] += 1
            except Exception:
                pass

            if l[i] > max_lps_length:  # Track maxLPSLength
                max_lps_length = l[i]
                max_lps_center_position = i

            # If palindrome centered at current right position i expand beyond current right position r,
            # adjust current position c based on expanded palindrome.
            if i + l[i] > r:
                c = i
                r = i + l[i]

            # print('i=%s, c=%s, r=%s, l=%s' % (i, c, r, l))

        # Uncomment it to print LPS length array
        # print('%d' % (L[i],))
        start = (max_lps_center_position - max_lps_length) / 2
        end = start + max_lps_length - 1
        print('LPS of string is %s : %s' % (text, text[start:end + 1]))

    # find_longest_palindrome('babcbabcbaccba')
    # find_longest_palindrome('ababcbcbc')


    def multiply_strings(str1, str2):
        negative = False
        if str1[0] == '-':
            str1 = str1[1:]
            if str2[0] == '-':
                str2 = str2[1:]
            else:
                negative = True
        elif str2[0] == '-':
            str2 = str2[1:]
            negative = True

        str1 = trim_string_number(str1)
        str2 = trim_string_number(str2)

        result = '0'
        for i in range(len(str2) - 1, -1, -1):
            t = multiply_string_and_digit(str1, str2[i])
            if t != '0':
                t += '0' * (len(str2) - i - 1)
                result = add_strings(result, t)

        return result if not negative else '-' + result


    def multiply_string_and_digit(s, d):
        d = int(d)
        if d == 0:
            return '0'
        if d == 1:
            return s

        result = ''
        c = 0
        for i in range(len(s) - 1, -1, -1):
            x = int(s[i])
            c, v = divmod(x * d + c, 10)
            result = str(v) + result
        if c > 0:
            result = str(c) + result

        return result


    def add_strings(str1, str2):
        str1 = trim_string_number(str1)
        str2 = trim_string_number(str2)

        length = max(len(str1), len(str2))
        str1 = '0' * (length - len(str1)) + str1
        str2 = '0' * (length - len(str2)) + str2

        result = ''
        c = 0
        for i in range(length - 1, -1, -1):
            x, y = int(str1[i]), int(str2[i])
            c, v = divmod(x + y + c, 10)
            result = str(v) + result
        if c > 0:
            result = '1' + result

        return result

    def trim_string_number(s):
        # non-negative string number only
        i = 0
        while i < len(s) - 1 and s[i] == '0':
            i += 1
        return s[i:]

    # print(multiply_strings('-12631824123172498123124612837102371923', '0000000123712312461298461238127031273912649128'))
    # print(multiply_strings('-999999999999', '999999999999'))

    def area_of_rectangles_one(rectangles):
        pass

    def alphanumeric(length):
        array = []
        for i in range(length):
            array.append(random.choice(string.ascii_lowercase + (3*string.digits)))
        return array

    counter = 0

    def swap(array, x, y, count=True):
        if count:
            global counter
            counter += 1
        tmp = array[x]
        array[x] = array[y]
        array[y] = tmp
        return array

    def swap_equal_block(array, index, length):
        for i in range(length):
            swap(array, index + i, index + length + i)
        return array

    def swap_block(array, low, high, pos):
        l1 = pos - low
        l2 = high - pos + 1
        if l1 == 0 or l2 == 0:
            return array

        while l1 != l2:
            if l1 > l2:
                l1 -= l2
                pos -= l2
                swap_equal_block(array, pos, l2)
            else:
                l2 -= l1
                swap_equal_block(array, low, l1)
                low += l1
                pos += l1
        swap_equal_block(array, low, l1)
        return array

    def segment_characters(array):
        start, pos = -1, -1
        for i in range(len(array)):
            value = array[i]
            # noinspection PyTypeChecker
            if '0' <= value <= '9':  # number
                if start >= 0 and pos < start:  # has alphabet block before number block
                    pos = i
            else:  # alphabet
                if start < 0:  # first alphabet block
                    start = i
                else:
                    if pos > start:  # end number block, swap alphabet block and number block
                        swap_block(array, start, i - 1, pos)
                        start += i - pos
                        pos = -1
        # last swap if needed
        if pos > start:
            swap_block(array, start, len(array) - 1, pos)
        return array

    def participle(array):
        swap = 0
        faci = 0
        for i in range(len(array)):
            value = array[i]
            # noinspection PyTypeChecker
            if '0' <= value <= '9':
                current = array[faci]
                for j in range(faci, i):
                    next = array[j + 1]
                    array[j + 1] = current
                    current = next
                    swap += 1
                array[faci] = value
                faci += 1
        return array, swap

    # array = alphanumeric(10)
    # r1 = segment_characters(list(array))
    # print('%010d' % counter, r1)
    # r2, c2 = participle(list(array))
    # print('%010d' % c2, r2)

    def binary_search(array, x, l=0, r=-1):
        if array is None or len(array) == 0:
            return -1

        if r < 0:
            r = len(array) - 1

        if x < array[l] or x > array[r]:
            return -1

        if l == r:
            return l if array[l] == x else -1

        mid = (l + r) // 2

        if x < array[mid]:
            return binary_search(array, x, l=l, r=mid)
        elif x == array[mid]:
            if mid - 1 < l or array[mid-1] < x:
                return mid
            else:
                return binary_search(array, x, l=l, r=mid-1)
        else:
            return binary_search(array, x, l=mid+1, r=r)

    def index_rotated_sorted_array(array, x, l=0, r=-1):
        if array is None or len(array) == 0:
            return -1

        if r < 0:
            r = len(array) - 1

        if l == r:
            return l if array[l] == x else -1

        mid = (l + r) // 2

        if array[l] == array[mid] and array[mid+1] == array[r]:
            if array[l] == array[r]:
                if array[l] == x:
                    left_index = index_rotated_sorted_array(array, x, l=l, r=mid)
                    if left_index > l:
                        return left_index
                    else:
                        right_index = index_rotated_sorted_array(array, x, l=mid+1, r=r)
                        if right_index > mid + 1:
                            return max(left_index, right_index)
                        else:
                            return min(left_index, right_index)
                else:
                    left_index = index_rotated_sorted_array(array, x, l=l, r=mid)
                    if left_index > -1:
                        return left_index
                    else:
                        return index_rotated_sorted_array(array, x, l=mid+1, r=r)
            else:
                if array[l] == x:
                    return l
                elif array[mid+1] == x:
                    return mid + 1
                else:
                    return -1
        elif array[l] == array[mid]:
            if array[l] == x:
                pass

    def max_heap(array):
        n = len(array)
        for i in range(n//2, -1, -1):
            down_heap(array, i)
        return array

    def down_heap(array, index):
        n = len(array)
        left_child = 2 * index + 1
        right_child = left_child + 1
        if left_child < n:
            tmp = right_child if right_child < n and array[left_child] <= array[right_child] else left_child
            if array[tmp] > array[index]:
                swap(array, tmp, index, count=False)
                down_heap(array, tmp)

    # print(max_heap([i for i in range(10)]))

    def max_heap_pop(array):
        last = array.pop(len(array)-1)
        largest = array[0]
        array[0] = last
        down_heap(array, 0)
        return largest

    def select_k_largest_elements(array, k):
        array = max_heap(list(array))
        print(array)
        result = []
        for i in range(min(k, len(array))):
            result.append(max_heap_pop(array))
        return result

    # print(select_k_largest_elements([1, 23, 12, 9, 30, 2, 50], 3))

    def index_rotated_sorted_array2(array, x):
        n = len(array)

        if array[0] == x:
            return 0

        l = 0
        r = n - 1
        if x >= array[0]:
            while r > l:
                mid = (l + r) // 2
                if array[mid] == x:
                    return mid
                if array[mid] < array[0] or array[mid] > x:
                    r = mid
                else:
                    l = mid + 1
        else:
            while r > l:
                mid = (l + r) // 2
                if array[mid] == x:
                    return mid
                if array[0] > array[mid] > x:
                    r = mid
                else:
                    l = mid + 1
        if array[r] == x:
            return r

        return -1

    # print(index_rotated_sorted_array2([5, 6, 7, 8, 9, 1, 2, 3, 4], 3))

    def sum_of_pair(sorted_arr, sum):
        if len(sorted_arr) < 2:
            return -1, -1
        if len(sorted_arr) == 2:
            return 0, 1 if sorted_arr[0] + sorted_arr[1] == sum else -1, -1

        l = 0
        r = len(sorted_arr) - 1
        while l < r:
            s = sorted_arr[l] + sorted_arr[r]
            if s == sum:
                return l, r
            if s < sum:
                l += 1
            else:
                r -= 1

        return -1, -1

    print(sum_of_pair([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11], 10))

    def palindrome_dynamic_programming(input):
        size = len(input)

        matrix = [[0]*size for _ in range(size)]

        low = 0
        length = 1
        for i in range(size):
            matrix[i][i] = 1

        for i in range(size - 1):
            if input[i] == input[i+1]:
                matrix[i][i+1] = 1
                if length == 1:
                    low = i
                    length = 2

        for gap in range(2, size):
            for i in range(0, size - gap):
                j = i + gap
                if matrix[i+1][j-1] == 1 and input[i] == input[j]:
                    matrix[i][j] = 1
                    if gap + 1 > length:
                        low = i
                        length = gap + 1

        return input[low:low+length]

    print(palindrome_dynamic_programming('qwqwertyuioppoiuytrewqqw'))

    @contextmanager
    def log_context_manager():
        print('enter')
        yield None
        print('exit')

    # with log_context_manager():
    #     print('run')


