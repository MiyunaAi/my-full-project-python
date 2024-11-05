'''def combined(pos_only,/,standard,*,kwd_only):
    print(pos_only,standard,kwd_only)
#combined(1,2,3)
#combined(1,2,kwd_only=3)
combined(1,standard=2,kwd_only=3)'''

'''def keyword_only(*,arg):
    print (arg)
keyword_only(arg=1)
#keyword_only(1)'''

'''def exponents(base,power) :
    return base**power ;
print (exponents(2,30))'''

'''expo = lambda n,p : n**p
print (expo(3,3))'''

def expo(n):
    return lambda p : n**p
power2 = expo(2)
power3 = expo(3)
print(power2(5))
print(power3(5))