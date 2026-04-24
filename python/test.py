import ToyBlockCipher as TBC

K1 = 0
K2 = 65535

M1 = K1
M2 = K2

C1 = 12827
C2 = 8893
C3 = 28133
C4 = 3189

error = False

if TBC.ToyBlock(K1, M1) != C1:
    print("error in the first computation\n M = ", M1, "K = ", K1, "C = ", C1, "Result = ", TBC.ToyBlock(K1,M1))
    error = True
    
if TBC.ToyBlock(K1, M2) != C2:
    print("error in the second computation\n M = ", M2, "K = ", K1, "C = ", C2, "Result = ", TBC.ToyBlock(K1,M2))
    error = True
    
if TBC.ToyBlock(K2, M1) != C3:
    print("error in the third computation\n M = ", M1, "K = ", K2, "C = ", C3, "Result = ", TBC.ToyBlock(K2,M1))
    error = True
    
if TBC.ToyBlock(K2, M2) != C4:
    print("error in the fourth computation\n M = ", M2, "K = ", K2, "C = ", C4, "Result = ", TBC.ToyBlock(K2,M2))
    error = True

if error != True: 
    print("Correct!\n")
    
error = False

if TBC.ToyBlockDecipher(K1,C1) != M1:
    print("error in first decryption")
    error = True

if TBC.ToyBlockDecipher(K1,C2) != M2:
    print("error in second decryption")
    error = True
    
if TBC.ToyBlockDecipher(K2,C3) != M1:
    print("error in third decryption")
    error = True

if TBC.ToyBlockDecipher(K2,C4) != M2:
    print("error in fourth decryption")
    error = True

if error != True: 
    print("Correct!\n")