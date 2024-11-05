pipo = int(input("pls enter pipo total : "))
w = int(input("pls enter thung : "))
x = pipo//w
i = 0
while(i<x):
    pipo-=w #แบบ input
    i += 1 # i = i + 1

print("----------------------------------","\nถุงที่",i,"เหลือ",pipo)
