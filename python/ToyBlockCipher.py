def Substitution(m):
    # m is 4 bits
    S_Box = [14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7]
    
    return S_Box[m]

def InverseSubstitution(m):
    S_BoxInv = [14, 3, 4, 8, 1, 12, 10, 15, 7, 13, 9, 6, 11, 2, 0, 5]
    
    return S_BoxInv[m]
    
def Permutation(m):
    # m is 16 bits
    perm =  [0, 4, 8, 12, 1, 5, 9, 13, 2, 6, 10, 14, 3, 7, 11, 15]
    c = 0
    
    for i in range(16):
        bit = (m>>(15-i)) & 1
        new_pos = perm[i]
        c |= (bit<<(15-new_pos))
        
    return c

def InversePermutation(m):
    return Permutation(m)

def KSchedule(K):
    # K is 16 bits
    S1 = [0, 13, 1, 10, 8, 11, 3, 2, 4, 7, 15, 9, 12, 5, 6, 14]
    S2 = [13, 2, 6, 5, 1, 12, 11, 3, 10, 4, 8, 7, 14, 15, 0, 9]
    
    Ks = [K]
    for i in range(4):
        s1 = (Ks[i]>>12) & 0xf
        s2 = (Ks[i]>>8) & 0x0f
        s3 = (Ks[i]>>4) & 0x00f
        s4 = Ks[i] & 0x000f
        
        s1 = S1[s1]
        s2 = S2[s2]
        s3 = S1[s3]
        s4 = S2[s4]
        
        S = (s2<<12) | (s1<<8) | (s4<<4) | (s3)
        Ks.append(S)
        
    return Ks

def ToyBlock(K, M):
    # K and M are 16 bits
    Ks = KSchedule(K)
    C = M
    
    for i in range(4):
        C ^= Ks[i]
        sb1 = Substitution((C>>12) & 0xf)
        sb2 = Substitution((C>>8) & 0x0f)
        sb3 = Substitution((C>>4) & 0x00f)
        sb4 = Substitution(C & 0x000f)
        
        C = (sb1<<12) | (sb2<<8) | (sb3<<4) | (sb4)
        
        if i != 3:
            C = Permutation(C)
    
    C ^=Ks[4]
    
    return C

def ToyBlockDecipher(K, C):
    Ks = KSchedule(K)
    
    M = C
    for i in range(4):
        M ^= Ks[4-i]
        if i != 0:
            M = InversePermutation(M)
        
        sb1 = InverseSubstitution((M>>12) & 0xf)
        sb2 = InverseSubstitution((M>>8) & 0x0f)
        sb3 = InverseSubstitution((M>>4) & 0x00f)
        sb4 = InverseSubstitution(M & 0x000f)
    
        M = (sb1<<12) | (sb2<<8) | (sb3<<4) | (sb4)
    
    M ^= Ks[0]
    
    return M