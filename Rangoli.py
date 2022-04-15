def rangoli(n, alphabet = 'abcdefghijklmnopqrstuvwxyz', i = 0):    
    middle = (4*n)+1
    if i == 0:
        print(" Here comes the magic! ".center(middle,"#"))
    
    if i <= n:
        print("-".join(alphabet[n:n-i:-1]+alphabet[n-i:n+1]).center(middle,"-"))

    elif i > n & i < 2*n:
        print("-".join(alphabet[n:-(n-i):-1]+alphabet[-(n-i):n+1]).center(middle,"-"))
        
    if i == 2*n:
        return(print(" Enjoy, your pattern! ".center(middle, "#")))

    return rangoli(n=n, i = i+1)