import re

#krabbor e goa
def luhn(card_number):
    sum = 0
    for i, char in enumerate(card_number[::-1]):
        if re.search(r'\d', char):
            num = (1 + (i%2)) * int(char)
            if num > 9:
                sum += int(str(num)[0]) + int(str(num)[1])
            else:
                sum += num
        else:
            xpos = i

    rest = (10 - (sum%10))%10

    if xpos%2 == 1 and rest%2 == 1:
        rest = int("1" + str(rest - 1))
        
    return str(int(rest / (1 + (xpos%2))))

if __name__ == "__main__":
    f = open("data", "r")
    data = f.read().split()
    f.close()

    output = ""
    for row in data:
        output += luhn(row)
    print("Output:", output)