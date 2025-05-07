from DesFunctions import *
 
Message_Claire ="F883D6C1C2790E64"

Message_Chiffré="40C802AABF23AC0F" 

Message_chiffré_fauté = [
 "408A02A8AF22AC0F",
"498816ABAF33A40E",
"004812BABF63E946",
"509842EAAD228C0F",
"00C912AABFE3AD42",
"409882EAAC22E80F",
"008816A2FF75AC0E",
"60C832AABF63AD0E",
"404D023ABE23A80B",
"439906EAAF22AE1B",
"40A806ABEB27BD0D",
"40CC12BA3E23E41A",
"548807ABEF07AC0D",
"40CC22BA3A23EC5B",
"409902E8AFA3AC0B",
"49880EABEF37AC0F",
"44E8438ABF23AC4F",
"D4CD03BABE23681F",
"40C502EEFF26AC8B",
"558847AA8B23AF4F",
"00CD02EEBF6AAC8B",
"54C84BAADB33AD4F",
"54CD033ABF03EC0B",
"42C900AEBF22AC1B",
"00C012A3BF63AC0E",
"70C852AABF639D4E",
"44DA03AEBF22E82F",
"40CD12AAF7672C1E",
"448807AABF21E82F",
"40C810EAF766AC0E",
"04C8438ABB6BBC0F",
"D4C883BABF23AC0F"
]

possible_keys = [[] for _ in range(8)] 



def findPossibleKeys(bits, Edr_array, Er_array, A_array):
    possible_keys = [[] for _ in range(8)]
    
    for j in range(8):
        for sk in bits: 
            B = xorthensbox(Edr_array[j], sk, j)
            C = xorthensbox(Er_array[j], sk, j)
            x = xor(B, C)
            if A_array[j] == x:
                possible_keys[j].append(sk)
    
    return possible_keys


def getLandD(Message_Chiffré, initial_perm):
    # Convertir le texte chiffré hexadécimal en binaire
    ct_binary = hex2bin(Message_Chiffré)
    
    # Appliquer la permutation initiale
    ct_permuted = permute(ct_binary, initial_perm, 64)
    
    # Diviser le texte permuté en L16 et R16
    l16 = ct_permuted[:32]
    r16 = ct_permuted[32:64]
    
    return l16, r16


def filter_possible_keys(Message_chiffré_fauté, l16, r16, initial_perm, inverse_per, exp_d, possible_keys):
    for i in Message_chiffré_fauté:
        # Refaire les étapes initiales avec le nouveau texte chiffré
        dct = i

        dl, dr = getLandD(dct, initial_perm)
        xor_l_dl = xor(l16, dl)
        A = permute(xor_l_dl, inverse_per, 32)
        A_array = split_binary_into_segments(A, 4)
        Er = permute(r16, exp_d, 48)
        Edr = permute(dr, exp_d, 48)
        Er_array = split_binary_into_segments(Er)
        Edr_array = split_binary_into_segments(Edr)
        
        # Itérer sur les clés possibles et supprimer celles qui ne correspondent pas
        for j in range(0, 8):
            for s in possible_keys[j]:
                B = xorthensbox(Edr_array[j], s, j)
                C = xorthensbox(Er_array[j], s, j)
                x = xor(B, C)
                if A_array[j] != x:
                    possible_keys[j].remove(s)


def find_key(Message_Claire , Message_Chiffré, permuted_key):
    all_combinations = generate_combinations(permuted_key)
    final_key = ""
    for combination in all_combinations:
        key = ''.join(combination)
        cipher = DES(Message_Claire , key)
        if cipher == Message_Chiffré:
            final_key = key
            break
    return final_key


if __name__ == "__main__":
    #Texte chiffré sans la faute
    l16, r16 = getLandD(Message_Chiffré, initial_perm)
    #Texte chiffré avec la faute
    dct = Message_chiffré_fauté[0]
    dl16, dr16 = getLandD(dct, initial_perm)
    #XOR de la partie gauche du texte chiffré et de la partie gauche du texte chiffré avec la faute
    xor_l_dl = xor(l16,dl16)
    # Permuter le résultat XOR des moitiés gauche et droite avec la permutation inverse P^-1
    A = permute(xor_l_dl, inverse_per, 32)
    # Permuter la moitié droite avec la permutation d'expansion pour obtenir un résultat de 48 bits
    Er = permute(r16, exp_d, 48)
    # Permuter la moitié droite fautive avec la permutation d'expansion pour obtenir un résultat de 48 bits
    Edr = permute(dr16, exp_d, 48)
    # Diviser le résultat de la permutation A en segments de 4 bits
    A_array = split_binary_into_segments(A, 4)
    # Diviser le résultat de la permutation Er en segments de 6 bits
    Er_array = split_binary_into_segments(Er)
    # Diviser le résultat de la permutation Edr en segments de 6 bits
    Edr_array = split_binary_into_segments(Edr)
     # Générer toutes les combinaisons possibles de 6 bits
    bits = generate_bit_combinations(6)

    possible_keys = findPossibleKeys(bits, Edr_array, Er_array, A_array)

    #Afficher le nombre de solutions possibles pour chaque équation
    for i,line in enumerate(possible_keys):
        print("S-box ",i+1, " : ", len(line)," solutions possible avant filtrage")

    #Itérer sur les différents textes chiffrés avec fautes
    filter_possible_keys(Message_chiffré_fauté, l16, r16, initial_perm, inverse_per, exp_d, possible_keys)

    #Afficher le nombre de solutions possibles pour chaque équation après le filtrage
    for i,line in enumerate(possible_keys):
        print("S-box ",i+1, " : ", len(line), "solution après filtrage")
    # Joindre les tableaux internes en chaînes
    inner_strings = [''.join(inner) for inner in possible_keys]
    # Joindre les chaînes internes en une chaîne finale
    k16 = ''.join(inner_strings)
    # Afficher le résultat

    print(f"K16 retrouvée (binaire) : {k16} ({len(k16)} bits)")
    print(f"K16 retrouvée (hexadécimal) : {bin2hex(k16)}")

    permuted_key = permuteArray(k16,inverse_pc2,56)
    #Force brute sur les 9 derniers bits de la clé
    final_key = find_key(Message_Claire , Message_Chiffré, permuted_key)

    print("Clé K' (56 bits sans parité) :" , final_key)
    print("Clé K' (hexadécimal) :" , bin2hex(final_key))

    final_key = permuteArray(final_key,inverse_pc1,64)
    final_key = ''.join(final_key)

    print("Clé (avant ajout des bits de parité): " , bin2hex(final_key))


    final_key = add_parity_bits(final_key)
    print("Clé complète avec bits de parité (binaire) : " , final_key)
    print("Clé complète avec bits de parité (hexadécimal) : " , bin2hex(final_key))


    # obtenir la clé de 56 bits à partir de 64 bits en utilisant les bits de parité
    key = permute(final_key, pc1, 56)
    #Chiffrement
    cypher = DES(Message_Claire ,key)
    #Affichage du résultat
    print("Chiffrement obtenu : " , cypher)
    print("Chiffrement attendu : " , Message_Chiffré)

    if cypher == Message_Chiffré:
        print("la clé est correcte")