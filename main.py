import math
import string as s
import random
import re

ALPHABET_RU = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ "
ALPHABET_EN = s.ascii_uppercase + " "


def ALPHABET(t):
    if t == "ru":
        return ALPHABET_RU
    elif t == "en":
        return ALPHABET_EN


def key_formula(k1, k2, alphabet):
    return ((k1[0] * k2[0]) % len(alphabet),
            (k1[1] + k2[1]) % len(alphabet))


def key_maker(message_length, alphabet):
    keys_chain = []
    for i in range(0, len(alphabet)):
        for j in range(0, len(alphabet)):
            keys_chain.append([(i, 1), (j, 1)])

    for keys in keys_chain:
        keys_temp_chain = keys

        for i in range(0, message_length):
            if len(keys_temp_chain) >= i + 1:
                continue

            k1 = keys_temp_chain[i-1]
            k2 = keys_temp_chain[i-2]
            if math.gcd(key_formula(k1, k2, alphabet)[0], len(alphabet)) != 1:
                break
            keys_temp_chain.append(key_formula(k1, k2, alphabet))

        if len(keys_temp_chain) == message_length:
            return keys_temp_chain

    return None


def afina_recurrent_cipher(key1, key2, message, alphabet):
    key_chain = [key1, key2]
    message_listed = list(message)

    for i in range(0, len(message_listed)):
        if len(key_chain) >= i + 1:
            continue

        k1 = key_chain[i-1]
        k2 = key_chain[i-2]
        if math.gcd(key_formula(k1, k2, alphabet)[0], len(alphabet)) != 1:
            print("""Given keys will make the message undecryptable. \
    Use other keys""")
            if not key_maker(len(message), alphabet):
                print("Looks like we can't make keys for this")
                return False
            sug_keys = [key_maker(len(message), alphabet)[0],
                        key_maker(len(message), alphabet)[1]]
            print("""We would souggest you to use these keys:""", sug_keys)
            return False
        key_chain.append(key_formula(k1, k2, alphabet))

    message_numerated = list(map(lambda char: alphabet.index(char),
                                 message_listed))
    message_encrypted_numerated = []
    for i in range(0, len(key_chain)):
        enc = (key_chain[i][0] * message_numerated[i] + key_chain[i][1]) %\
            len(alphabet)
        message_encrypted_numerated.append(enc)
    message_encrypted = list(map(lambda num: alphabet[num],
                                 message_encrypted_numerated))
    return "".join(message_encrypted)


def afina_recurrent_decipher(key1, key2, message, alphabet):
    key_chain = [key1, key2]
    message_listed = list(message)

    for i in range(0, len(message_listed)):
        if len(key_chain) >= i + 1:
            continue

        k1 = key_chain[i-1]
        k2 = key_chain[i-2]
        if math.gcd(key_formula(k1, k2, alphabet)[0], len(alphabet)) != 1:
            print("""These keys are unacceptable. If keys are right, the text\
 is undecryptable""")
            return False
        key_chain.append(key_formula(k1, k2, alphabet))

    key_chain = list(map(lambda key: (pow(key[0], -1, len(alphabet)), key[1]),
                         key_chain))

    message_numerated = list(map(lambda char: alphabet.index(char),
                                 message_listed))
    message_decrypted_numerated = []
    for i in range(0, len(key_chain)):
        dec = (key_chain[i][0] * (message_numerated[i] - key_chain[i][1])) % \
            len(alphabet)
        message_decrypted_numerated.append(dec)
    message_decrypted = list(map(lambda num: alphabet[num],
                                 message_decrypted_numerated))
    return "".join(message_decrypted)


def lang_choice():
    print("Choose alphabet RU or EN")

    while True:
        choice = input("Your input: ")
        choice_en = re.search("EN", choice, re.IGNORECASE)
        choice_ru = re.search("RU", choice, re.IGNORECASE)

        if choice_en:
            return "en"
        elif choice_ru:
            return "ru"
        else:
            continue


def afina_recurrent_choice(typ):
    lang = lang_choice()

    print("""You must enter your keys and the message. Also note that the\
first digit of the key must follow the rule: gcd(digit, length of alphabet) =\
1 and must be less than the length of the alphabet. The second\
can be selected at random but must be less than the length of the alphabet -1\
and more than -1. Enter your key like that: 5, 12""")

    while True:
        key = input("Enter your key [default: 99, 4]: ") or "99, 4"
        key2 = input("Enter your key2 [default: 99, 4]: ") or "99, 4"
        key_list1 = key.split(",")
        key_list2 = key2.split(",")

        if len(key_list1) > 2 or len(key_list1) < 2 or \
           len(key_list2) > 2 or len(key_list2) < 2:
            print("Nuh uh! Not allowed!")
            continue

        try:
            key1 = tuple(map(int, key_list1))
            key2 = tuple(map(int, key_list2))

            if math.gcd(key1[0], len(ALPHABET(lang))) != 1 or\
               math.gcd(key1[0], len(ALPHABET(lang))) != 1:
                print("First digit of the key doesnt match the gcd")
                continue
            if key1[0] > len(ALPHABET(lang)) or key2[0] > len(ALPHABET(lang)):
                print("Alphabet length:", len(ALPHABET(lang)))
                print("First digit of the key can't be more than alph")
                continue
            if key1[1] > len(ALPHABET(lang)) - 1 or key1[1] < 0 or\
               key2[1] > len(ALPHABET(lang)) - 1 or key2[1] < 0:
                print("Second digit of the key is incorrect")
                continue
        except ValueError:
            print("You know what number is?")
            continue
        except Exception as e:
            print("???", e)
            continue

        message = input("Enter your message: ")

        if not message:
            print("stup")
            continue

        if typ == "cipher":
            print("Your encrypted message is:")
            if afina_recurrent_cipher(key1, key2, message, ALPHABET(lang)):
                print("--------------------------------------------------------")
                print(afina_recurrent_cipher(key1, key2, message, ALPHABET(lang)))
                print("--------------------------------------------------------")
            else:
                print("No text")
            break
        elif typ == "decipher":
            print("Your decrypted message is:")
            if afina_recurrent_decipher(key1, key2, message, ALPHABET(lang)):
                print("--------------------------------------------------------")
                print(afina_recurrent_decipher(key1, key2, message, ALPHABET(lang)))
                print("--------------------------------------------------------")
            else:
                print("No text")
            break
        else:
            print("error")
            break


def afina_choice(typ):
    lang = lang_choice()

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

            if math.gcd(key[0], len(ALPHABET(lang))) != 1:
                print("First digit of the key doesnt match the gcd")
                continue
            if key[0] > len(ALPHABET(lang)):
                print(len(ALPHABET(lang)))
                print("First digit of the key can't be more than alph")
                continue
            if key[1] > len(ALPHABET(lang)) - 1 or key[1] < 0:
                print("Second digit of the key is incorrect")
                continue
        except ValueError:
            print("You know what number is?")
            continue
        except Exception:
            print("???")
            continue

        message = input("Enter your message: ")

        if not message:
            print("stup")
            continue

        if typ == "cipher":
            print("Your encrypted message is:")
            print("--------------------------------------------------------")
            print(afina_cipher(key, message, ALPHABET(lang)))
            print("--------------------------------------------------------")
            break
        elif typ == "decipher":
            print("Your decrypted message is:")
            print("--------------------------------------------------------")
            print(afina_decipher(key, message, ALPHABET(lang)))
            print("--------------------------------------------------------")
            break
        else:
            print("error")
            break


def replacement_cd(message, key, alphabet):
    cd = ""
    for i in range(0, len(message)):
        cd += key[alphabet.index(message[i])]

    return cd


def replacement_choice(typ):
    while True:
        print("""First, chose alphabet to use.
[1] English
[2] Russian
[0] Exit""")

        try:
            choice = int(input("Enter your choice: "))
        except ValueError:
            print("Number please!")
            continue

        if choice == 0:
            break
        elif choice == 1:
            eng_alphabet_default = ALPHABET("en")
            print("""Enter your alphabet in one string. Make sure to list all\
characters and do not repeat characters. If you want to create randomly\
generated alphabet, type random""")

            while True:
                user_input = input("Enter your alphabet: ")

                if user_input == "random":
                    alphabet = list(eng_alphabet_default)
                    random.shuffle(alphabet)
                    print("----------------------------------------------------")
                    print("".join(alphabet))
                    print("----------------------------------------------------")

                    if typ == "cipher":
                        print("""Enter message to cipher without any dots and
etc. Also write it uppercase. Program is case sensitive yet.""")
                        message = input("Message: ")
                        print("--------------------------------------------------------")
                        print(replacement_cd(message, alphabet, eng_alphabet_default))
                        print("--------------------------------------------------------")
                        return
                    else:
                        print("""Enter message to decipher without any dots and
etc. Also write it uppercase. Program is case sensitive yet.""")
                        message = input("Message: ")
                        print("--------------------------------------------------------")
                        print(replacement_cd(message, eng_alphabet_default, alphabet))
                        print("--------------------------------------------------------")
                        return
                elif len(eng_alphabet_default) > len(user_input):
                    print("Alphabet is not full.")
                    continue
                elif len(eng_alphabet_default) == len(user_input):
                    if typ == "cipher":
                        print("""Enter message to cipher without any dots and
etc. Also write it uppercase. Program is case sensitive yet.""")
                        message = input("Message: ")
                        print("--------------------------------------------------------")
                        print(replacement_cd(message, user_input, eng_alphabet_default))
                        print("--------------------------------------------------------")
                        return
                    else:
                        print("""Enter message to decipher without any dots and
etc. Also write it uppercase. Program is case sensitive yet.""")
                        message = input("Message: ")
                        print("--------------------------------------------------------")
                        print(replacement_cd(message, eng_alphabet_default, user_input))
                        print("--------------------------------------------------------")
                        return

        elif choice == 2:
            ru_alphabet_default = ALPHABET("ru")
            print("""Enter your alphabet in one string. Make sure to list all\
characters and do not repeat characters. If you want to create randomly\
generated alphabet, type random""")

            while True:
                user_input = input("Enter your alphabet: ")

                if user_input == "random":
                    alphabet = list(ru_alphabet_default)
                    random.shuffle(alphabet)
                    print("----------------------------------------------------")
                    print("".join(alphabet))
                    print("----------------------------------------------------")

                    if typ == "cipher":
                        print("""Enter message to cipher without any dots and
etc. Also write it uppercase. Program is case sensitive yet.""")
                        message = input("Message: ")
                        print("--------------------------------------------------------")
                        print(replacement_cd(message, alphabet, ru_alphabet_default))
                        print("--------------------------------------------------------")
                        return
                    else:
                        print("""Enter message to decipher without any dots and
etc. Also write it uppercase. Program is case sensitive yet.""")
                        message = input("Message: ")
                        print("--------------------------------------------------------")
                        print(replacement_cd(message, ru_alphabet_default, alphabet))
                        print("--------------------------------------------------------")
                        return
                elif len(ru_alphabet_default) > len(user_input):
                    print("Alphabet is not full.")
                    continue
                elif len(ru_alphabet_default) == len(user_input):
                    if typ == "cipher":
                        print("""Enter message to cipher without any dots and
etc. Also write it uppercase. Program is case sensitive yet.""")
                        message = input("Message: ")
                        print("--------------------------------------------------------")
                        print(replacement_cd(message, user_input, ru_alphabet_default))
                        print("--------------------------------------------------------")
                        return
                    else:
                        print("""Enter message to decipher without any dots and
etc. Also write it uppercase. Program is case sensitive yet.""")
                        message = input("Message: ")
                        print("--------------------------------------------------------")
                        print(replacement_cd(message, ru_alphabet_default, user_input))
                        print("--------------------------------------------------------")
                        return
        else:
            print("No such option!")
            continue


def afina_cipher(key, message, alphabet):
    def afina_cipher_formula(num):
        return (num * key[0] + key[1]) % len(alphabet)
    message_listed = list(message)
    message_numerated = list(map(lambda char: alphabet.index(char),
                                 message_listed))
    message_encrypted_numerated = list(map(afina_cipher_formula,
                                           message_numerated))
    message_encrypted = list(map(lambda num: alphabet[num],
                                 message_encrypted_numerated))
    return "".join(message_encrypted)


def afina_decipher(key, message, alphabet):
    def afina_decipher_formula(num):
        alpha = pow(key[0], -1, len(alphabet))
        return (alpha * (num - key[1])) % len(alphabet)

    message_encrypted = list(message)
    message_encrypted_numerated = list(map(lambda char: alphabet.index(char),
                                           message_encrypted))
    message_decrypted_numerated = list(map(afina_decipher_formula,
                                           message_encrypted_numerated))
    message_decrypted = list(map(lambda num: alphabet[num],
                                 message_decrypted_numerated))
    return "".join(message_decrypted)


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


def replacement():
    while True:
        print("""Replacement
[1] Cipher
[2] Decipher
[0] Back to main menu""")

        try:
            choice = int(input("Enter your choice: "))
        except ValueError:
            print("Looks like you don't understand what number is. Try again!")
            continue

        if choice == 0:
            break
        elif choice == 1:
            replacement_choice("cipher")
        elif choice == 2:
            replacement_choice("decipher")
        else:
            print("No such option")
            continue


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
    elif choice == 3:
        replacement()
    else:
        print("No such option!")
        continue
