import hashlib
import timeit

def read_file(file_path):
    try:
        with open(file_path, 'r') as file:
            return file.read()
    except FileNotFoundError:
        print(f"File not found: {file_path}")
    except Exception as e:
        print(f"Error reading file {file_path}: {str(e)}")
    return ""

# Example usage
file_path_1 = 'article_1.txt'
file_path_2 = 'article_2.txt'

# Reading files
article_1 = read_file(file_path_1)
article_2 = read_file(file_path_2)

# Function Knuth-Morris-Pratt (KMP) algorithm
def kmp_search(text, pattern):
    n, m = len(text), len(pattern)
  
    prefix = [0] * m
    j = 0
    for i in range(1, m):
        while (j > 0 and pattern[j] != pattern[i]):
            j = prefix[j-1]
        if pattern[j] == pattern[i]:
            j += 1
        prefix[i] = j
    
    # Search for substring
    j = 0
    for i in range(n):
        while (j > 0 and pattern[j] != text[i]):
            j = prefix[j-1]
        if pattern[j] == text[i]:
            j += 1
        if j == m:
            return i - m + 1  
    return -1  

# Function Boyer-Moore algorithm
def boyer_moore_search(text, pattern):
    n, m = len(text), len(pattern)
    if m == 0: return 0
    last = {}
    for i in range(m):
        last[pattern[i]] = i
    
    # Boyer-Moore algorithm
    i = m - 1
    j = m - 1
    while i < n:
        if text[i] == pattern[j]:
            if j == 0:
                return i
            else:
                i -= 1
                j -= 1
        else:
            l = last.get(text[i], -1)
            i += m - min(j, 1 + l)
            j = m - 1
    return -1

# Function Rabin-Karp algorithm
def rabin_karp_search(text, pattern):
    n, m = len(text), len(pattern)
    hpattern = hashlib.sha1(pattern.encode()).hexdigest()
    for i in range(n - m + 1):
        hs = hashlib.sha1(text[i:i+m].encode()).hexdigest()
        if hs == hpattern:
            return i  
    return -1  

# Selecting substrings for search
existing_substring = "алгоритми"  # Existing substring
non_existing_substring = "щаслива людина" # Non-existing substring

# Testing algorithms
print("Testing KMP:")
print(kmp_search(article_1, existing_substring))
print(kmp_search(article_1, non_existing_substring))

print("\nTesting Boyer-Moore:")
print(boyer_moore_search(article_1, existing_substring))
print(boyer_moore_search(article_1, non_existing_substring))

print("\nTesting Rabin-Karp:")
print(rabin_karp_search(article_1, existing_substring))
print(rabin_karp_search(article_1, non_existing_substring))

# Setup for timeit to measure execution time
setup = '''
from __main__ import kmp_search, boyer_moore_search, rabin_karp_search, article_1, article_2, existing_substring, non_existing_substring
'''

# Number of repetitions
number = 10

# Measure time for KMP algorithm
kmp_existing = timeit.timeit('kmp_search(article_1, existing_substring)', setup=setup, number=number)
kmp_non_existing = timeit.timeit('kmp_search(article_1, non_existing_substring)', setup=setup, number=number)

# Measure time for Boyer-Moore algorithm
bm_existing = timeit.timeit('boyer_moore_search(article_1, existing_substring)', setup=setup, number=number)
bm_non_existing = timeit.timeit('boyer_moore_search(article_1, non_existing_substring)', setup=setup, number=number)

# Measure time for Rabin-Karp algorithm
rk_existing = timeit.timeit('rabin_karp_search(article_1, existing_substring)', setup=setup, number=number)
rk_non_existing = timeit.timeit('rabin_karp_search(article_1, non_existing_substring)', setup=setup, number=number)

print("\nTime measurements for KMP algorithm:")
print(f"Existing substring: {kmp_existing:.6f} seconds")
print(f"Non-existing substring: {kmp_non_existing:.6f} seconds")

print("\nTime measurements for Boyer-Moore algorithm:")
print(f"Existing substring: {bm_existing:.6f} seconds")
print(f"Non-existing substring: {bm_non_existing:.6f} seconds")

print("\nTime measurements for Rabin-Karp algorithm:")
print(f"Existing substring: {rk_existing:.6f} seconds")
print(f"Non-existing substring: {rk_non_existing:.6f} seconds")
