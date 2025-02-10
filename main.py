import math
import string as s
import re

ALPHABET = list(s.printable)


def has_cyrillic(text):
    return bool(re.search('[\u0400-\u04FF]', text))


def afina_choice(typ):
    print("""You must enter your key and the message. Note that \
is not supported yet. Also note that the first digit of the key must\
follow the rule: gcd(digit, length of alphabet) = 1 and must be less than the\
length of the alphabet. The second can be selected at random but must be less\
than the length of the alphabet -1 and more than -1. Enter your key like\
that: 5, 12""")

    while True:
        key = input("Enter your key [default: 99, 4]: ") or "99, 4"
        key_list = key.split(",")

        if len(key_list) > 2 or len(key_list) < 2:
            print("Nuh uh! Not allowed!")
            continue

        try:
            key = tuple(map(int, key_list))

            if math.gcd(key[0], len(ALPHABET)) != 1:
                print("First digit of the key doesnt match the gcd")
                continue
            if key[0] > len(ALPHABET):
                print(len(ALPHABET))
                print("First digit of the key can't be more than alph")
                continue
            if key[1] > len(ALPHABET) - 1 or key[1] < 0:
                print("Second digit of the key is incorrect")
                continue
        except ValueError:
            print("You know what number is?")
            continue
        except Exception:
            print("???")
            continue

        message = input("Enter your message: ")

        if has_cyrillic(message):
            print("Nuh uh!")
            continue

        if typ == "cipher":
            print("Your encrypted message is:")
            print(afina_cipher(key, message))
            break
        elif typ == "decipher":
            print("Your decrypted message is:")
            print(afina_decipher(key, message))
            break
        else:
            print("error")
            break


def afina_cipher(key, message):
    def afina_cipher_formula(num):
        return (num * key[0] + key[1]) % len(ALPHABET)

    message_listed = list(message)
    message_numerated = list(map(lambda char: ALPHABET.index(char),
                             message_listed))
    message_encrypted_numerated = list(map(afina_cipher_formula,
                                           message_numerated))
    message_encrypted = list(map(lambda num: ALPHABET[num],
                                 message_encrypted_numerated))
    return "".join(message_encrypted)


def afina_decipher(key, message):
    def afina_decipher_formula(num):
        alpha = pow(key[0], -1, len(ALPHABET))
        return (alpha * (num - key[1])) % len(ALPHABET)

    message_encrypted = list(message)
    message_encrypted_numerated = list(map(lambda char: ALPHABET.index(char),
                                       message_encrypted))
    message_decrypted_numerated = list(map(afina_decipher_formula,
                                           message_encrypted_numerated))
    message_decrypted = list(map(lambda num: ALPHABET[num],
                                 message_decrypted_numerated))
    return "".join(message_decrypted)


def afina_recurrent_choice(typ):
    pass


def afina(typ="basic"):
    while True:
        print("""Afina{}
[1] Cipher
[2] Decipher
[0] Back to main menu""".format(" recurrent" if typ == "recurrent" else ""))

        try:
            choice = int(input("Enter your choice: "))
        except ValueError:
            print("Looks like you don't understand what number is. Try again!")
            continue

        if choice == 0:
            break
        elif choice == 1:
            afina_choice("cipher") if typ == "basic" else \
                afina_recurrent_choice("cipher")
        elif choice == 2:
            afina_choice("decipher") if typ == "basic" else \
                afina_recurrent_choice("decipher")
        else:
            print("No such option!")
            continue

    return


while True:
    print("""Cipher/Decipher
[1] Affina cipher
[2] Affina recurrent cipher
[3] Replacement cipher
[0] Exit""")

    try:
        choice = int(input("Enter your choice: "))
    except ValueError:
        print("Looks like you don't understand what number is. Try again!")
        continue

    if choice == 0:
        break
    elif choice == 1:
        afina("basic")
    elif choice == 2:
        afina("recurrent")
    else:
        print("No such option!")
        continue
