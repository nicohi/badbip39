# Translates arbitrary ascii data into bip39-formatted word list.
# Wordlist: https://github.com/bitcoin/bips/blob/master/bip-0039/english.txt
import sys


def printHelp():
    print("Usage:")
    print("\t--      |read stdin (ASCII) and output BIP39 encoding of data|")
    print(
        "\t--text  |read arguments (ASCII) for data and output BIP39 encoding of data|"
    )
    print("\t--bip39 |read arguments BIP39 words separated by space. output data|")


def readWords():
    with open("words.txt") as file:
        return [line.strip() for line in file]


def numberToBase(n, b):
    if n == 0:
        return [0]
    digits = []
    while n:
        digits.append(int(n % b))
        n //= b
    return digits[::-1]

def toInteger(numbers, base):
    r = 0
    for i,n in enumerate(numbers):
        r = r * base + n
    return r

def toBIP(text):
    words = readWords()
    bs = bytes(text, "ascii")
    data = int.from_bytes(bs, "little")
    bip39 = [words[d] for d in numberToBase(data, len(words))]
    print(f"{len(bip39)} words")
    return bip39

def fromBIP(phrase):
    wordmap = {w:n for n,w in enumerate(readWords())}
    dint = toInteger([wordmap[w] for w in phrase], len(wordmap))
    bs = dint.to_bytes((dint.bit_length() + 7) // 8, 'little')
    return bs.decode('ascii')

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("No arguments")
    elif sys.argv[1] == "--bip39":
        phrase = sys.argv[2:]
        # print(f"'{phrase}'")
        print(fromBIP(phrase))
        sys.exit()
    elif sys.argv[1] == "--text":
        text = " ".join(sys.argv[2:])
        # print(f"'{text}'")
        print(toBIP(text))
        sys.exit()
    elif sys.argv[1] == "--":
        text = sys.stdin.read()
        # print(f"'{text}'")
        print(toBIP(text))
        sys.exit()

    printHelp()
    sys.exit()
