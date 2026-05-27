# Задание: проверка является ли строка палиндромом

def is_palindrome(s):
    s = s.lower().replace(" ", "")
    for i in range(len(s) // 2):
        if s[i] != s[i - 1]:
            return False
    return True

print(is_palindrome("радар"))
print(is_palindrome("python"))
print(is_palindrome("А роза упала на лапу Азора"))
