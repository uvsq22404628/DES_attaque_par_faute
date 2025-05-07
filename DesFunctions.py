shift_table = [1, 1, 2, 2,
			2, 2, 2, 2,
			1, 2, 2, 2,
			2, 2, 2, 1]

# Table de position des 64 bits au niveau initial : Table de permutation initiale
initial_perm = [58, 50, 42, 34, 26, 18, 10, 2,
				60, 52, 44, 36, 28, 20, 12, 4,
				62, 54, 46, 38, 30, 22, 14, 6,
				64, 56, 48, 40, 32, 24, 16, 8,
				57, 49, 41, 33, 25, 17, 9, 1,
				59, 51, 43, 35, 27, 19, 11, 3,
				61, 53, 45, 37, 29, 21, 13, 5,
				63, 55, 47, 39, 31, 23, 15, 7]

# Table de permutation finale
final_perm = [40, 8, 48, 16, 56, 24, 64, 32,
			39, 7, 47, 15, 55, 23, 63, 31,
			38, 6, 46, 14, 54, 22, 62, 30,
			37, 5, 45, 13, 53, 21, 61, 29,
			36, 4, 44, 12, 52, 20, 60, 28,
			35, 3, 43, 11, 51, 19, 59, 27,
			34, 2, 42, 10, 50, 18, 58, 26,
			33, 1, 41, 9, 49, 17, 57, 25]

# Table S-box
sbox = [[[14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7],
		[0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8],
		[4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0],
		[15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13]],

		[[15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10],
		[3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5],
		[0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15],
		[13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9]],

		[[10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8],
		[13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1],
		[13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7],
		[1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12]],

		[[7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15],
		[13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9],
		[10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4],
		[3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14]],

		[[2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9],
		[14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6],
		[4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14],
		[11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3]],

		[[12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11],
		[10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8],
		[9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6],
		[4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13]],

		[[4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1],
		[13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6],
		[1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2],
		[6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12]],

		[[13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7],
		[1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2],
		[7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8],
		[2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11]]]

# Table D-box d'expansion
exp_d = [32, 1, 2, 3, 4, 5, 4, 5,
		6, 7, 8, 9, 8, 9, 10, 11,
		12, 13, 12, 13, 14, 15, 16, 17,
		16, 17, 18, 19, 20, 21, 20, 21,
		22, 23, 24, 25, 24, 25, 26, 27,
		28, 29, 28, 29, 30, 31, 32, 1]

# Table de permutation directe
per = [16, 7, 20, 21,
	29, 12, 28, 17,
	1, 15, 23, 26,
	5, 18, 31, 10,
	2, 8, 24, 14,
	32, 27, 3, 9,
	19, 13, 30, 6,
	22, 11, 4, 25]

keys = set()

def hex2bin(s):
	mp = {'0': "0000",
		'1': "0001",
		'2': "0010",
		'3': "0011",
		'4': "0100",
		'5': "0101",
		'6': "0110",
		'7': "0111",
		'8': "1000",
		'9': "1001",
		'A': "1010",
		'B': "1011",
		'C': "1100",
		'D': "1101",
		'E': "1110",
		'F': "1111"}
	bin = ""
	for i in range(len(s)):
		bin = bin + mp[s[i]]
	return bin

# Conversion binaire vers hexadécimal
def bin2hex(s):
	mp = {"0000": '0',
		"0001": '1',
		"0010": '2',
		"0011": '3',
		"0100": '4',
		"0101": '5',
		"0110": '6',
		"0111": '7',
		"1000": '8',
		"1001": '9',
		"1010": 'A',
		"1011": 'B',
		"1100": 'C',
		"1101": 'D',
		"1110": 'E',
		"1111": 'F'}
	hex = ""
	for i in range(0, len(s), 4):
		ch = ""
		ch = ch + s[i]
		ch = ch + s[i + 1]
		ch = ch + s[i + 2]
		ch = ch + s[i + 3]
		hex = hex + mp[ch]
	return hex

# Conversion binaire vers décimal
def bin2dec(binary):
	binary1 = binary
	decimal, i, n = 0, 0, 0
	while(binary != 0):
		dec = binary % 10
		decimal = decimal + dec * pow(2, i)
		binary = binary//10
		i += 1
	return decimal

# Conversion décimal vers binaire
def dec2bin(num):
	res = bin(num).replace("0b", "")
	if(len(res) % 4 != 0):
		div = len(res) / 4
		div = int(div)
		counter = (4 * (div + 1)) - len(res)
		for i in range(0, counter):
			res = '0' + res
	return res

# Fonction de permutation pour réorganiser les bits
def permute(k, arr, n):
	permutation = ""
	for i in range(0, n):
		permutation = permutation + k[arr[i] - 1]
	return permutation

def xor(a, b):
	ans = ""
	for i in range(len(a)):
		if a[i] == b[i]:
			ans = ans + "0"
		else:
			ans = ans + "1"
	return ans

# Permutation inverse
inverse_per = [0] * len(per)
for i, num in enumerate(per):
    inverse_per[num - 1] = i + 1

# Test de la permutation et de son inverse
test = all(inverse_per[per[i] - 1] == i + 1 for i in range(len(per)))

pc2 = [14, 17, 11, 24, 1, 5,
			3, 28, 15, 6, 21, 10,
			23, 19, 12, 4, 26, 8,
			16, 7, 27, 20, 13, 2,
			41, 52, 31, 37, 47, 55,
			30, 40, 51, 45, 33, 48,
			44, 49, 39, 56, 34, 53,
			46, 42, 50, 36, 29, 32]

pc1 = [57, 49, 41, 33, 25, 17, 9,
		1, 58, 50, 42, 34, 26, 18,
		10, 2, 59, 51, 43, 35, 27,
		19, 11, 3, 60, 52, 44, 36,
		63, 55, 47, 39, 31, 23, 15,
		7, 62, 54, 46, 38, 30, 22,
		14, 6, 61, 53, 45, 37, 29,
		21, 13, 5, 28, 20, 12, 4]

inverse_pc2 = [0] * 56
for i, num in enumerate(pc2):
	inverse_pc2[num - 1] = i + 1

inverse_pc1 = [0] * 64
for i, num in enumerate(pc1):
	inverse_pc1[num - 1] = i + 1

def permuteArray(k, arr, n):
    permutation = []
    for i in range(n):
        if arr[i] == 0:
            permutation.append('')
        else:
            permutation.append(k[arr[i] - 1])
    return permutation

def generate_combinations(key, index=0, combination=[], combinations=[]):
    if index == len(key):
        combinations.append(combination.copy())
        return
    
    if key[index] == '':
        combination.append('0')
        generate_combinations(key, index + 1, combination, combinations)
        combination.pop()  # Retour arrière
        combination.append('1')
        generate_combinations(key, index + 1, combination, combinations)
        combination.pop()  # Retour arrière
    else:
        combination.append(key[index])
        generate_combinations(key, index + 1, combination, combinations)
        combination.pop()  # Retour arrière
    return combinations

def encrypt(Message_Claire, rkb, rk):
	Message_Claire = hex2bin(Message_Claire)
	# Permutation initiale
	Message_Claire = permute(Message_Claire, initial_perm, 64)
	# Division
	left = Message_Claire[0:32]
	right = Message_Claire[32:64]
	for i in range(0, 16):
		# D-box d'expansion : Expansion des 32 bits de données en 48 bits
		right_expanded = permute(right, exp_d, 48)
		# XOR RoundKey[i] et right_expanded
		xor_x = xor(right_expanded, rkb[i])
		# S-boxes : substitution de la valeur de la table s-box en calculant la ligne et la colonne
		sbox_str = ""
		for j in range(0, 8):
			row = bin2dec(int(xor_x[j * 6] + xor_x[j * 6 + 5]))
			col = bin2dec(int(xor_x[j * 6 + 1] + xor_x[j * 6 + 2] + xor_x[j * 6 + 3] + xor_x[j * 6 + 4]))
			val = sbox[j][row][col]
			sbox_str = sbox_str + dec2bin(val)
		# D-box directe : Réorganisation des bits après substitution
		sbox_str = permute(sbox_str, per, 32)
		# XOR left et sbox_str
		result = xor(left, sbox_str)
		left = result
		# Échange
		if(i != 15):
			left, right = right, left
	# Combinaison
	combine = left + right
	# Permutation finale : réorganisation finale des bits pour obtenir le texte chiffré
	cipher_text = permute(combine, final_perm, 64)
	return cipher_text

def shift_left(k, nth_shifts):
	s = ""
	for i in range(nth_shifts):
		for j in range(1, len(k)):
			s = s + k[j]
		s = s + k[0]
		k = s
		s = ""
	return k

def DES(Message_Claire, key):
	left = key[0:28]  # rkb pour les RoundKeys en binaire
	right = key[28:56]  # rk pour les RoundKeys en hexadécimal
	rkb = []
	rk = []
	for i in range(0, 16):
		# Décalage des bits selon le nombre de décalages en vérifiant la table de décalage
		left = shift_left(left, shift_table[i])
		right = shift_left(right, shift_table[i])
		# Combinaison des chaînes gauche et droite
		combine_str = left + right
		# Compression de la clé de 56 à 48 bits
		round_key = permute(combine_str, pc2, 48)
		rkb.append(round_key)
		rk.append(bin2hex(round_key))
	cipher_text = bin2hex(encrypt(Message_Claire, rkb, rk))
	return cipher_text

def generate_combinations_fixed_length(key, index=0, combination=[], combinations=[], fixed_length=0):
    if len(combination) == fixed_length:
        combinations.append(combination.copy())
        return
    
    if index == len(key):
        return
    
    if key[index] == '':
        combination.append('0')
        generate_combinations_fixed_length(key, index + 1, combination, combinations, fixed_length)
        combination.pop()  # Retour arrière
        combination.append('1')
        generate_combinations_fixed_length(key, index + 1, combination, combinations, fixed_length)
        combination.pop()  # Retour arrière
    else:
        combination.append(key[index])
        generate_combinations_fixed_length(key, index + 1, combination, combinations, fixed_length)
        combination.pop()  # Retour arrière
    return combinations

def xorthensbox(s, sK, i):
    x = xor(s, sK)
    row = bin2dec(int(x[0] + x[5]))
    col = bin2dec(int(x[1] + x[2] + x[3] + x[4]))
    val = sbox[i][row][col]
    return dec2bin(val)

def split_binary_into_segments(binary_string, segment_length=6):
    segments = []
    for i in range(0, len(binary_string), segment_length):
        segment = binary_string[i:i+segment_length]
        segments.append(segment)
    return segments

def generate_bit_combinations(num_bits):
    combinations = []
    for i in range(2 ** num_bits):
        binary = bin(i)[2:].zfill(num_bits)
        combinations.append(binary)
    return combinations

def add_parity_bits(key_56bit):
    if len(key_56bit) != 56:
        raise ValueError("La clé doit faire 56 bits")
    key_64bit = []
    for i in range(8):
        # Extraire les 7 bits pour cet octet
        byte = key_56bit[i*7:(i+1)*7]
        # Calculer le bit de parité (parité impaire)
        parity_bit = '1' if byte.count('1') % 2 == 0 else '0'
        # Ajouter les 7 bits et le bit de parité pour former l'octet de 8 bits
        key_64bit.append(byte + parity_bit)
    return ''.join(key_64bit)
