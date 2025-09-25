print("Hello, formal language project!")

def is_in_language (s):
    if len(s) == 0:
        return False
    
    for ch in s:
        if ch not in ("a", "b"):
            return False
    
    i = 0
    n = len(s)
    while i < n and s[i] == 'a':
        i+=1
    
    count_a = i

    if count_a == 0:
        return False
    
    while i < n and s[i] == 'b':
        i+=1

    count_b = n - count_a

    if i != n:
        return False
    
    if count_b != count_a:
        return False
    
    return True