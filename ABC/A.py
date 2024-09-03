N = int(input())
H = list(map(int,input().split()))

T = 0

for life in H:
    num = life // 5
    T += num * 3
    life -= num * 5
    while life > 0:
        T += 1
        if T % 3 == 0:
            life -= 3
        else:
            life -= 1

print(T)