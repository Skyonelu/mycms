import math

def su_us_hk(B, C, E, F, I1, stock_v):
    #E = [0] + [C[i] - C[i - 1] for i in range(1,len(E))]
    H = [0] + [1 if E[0] > 0 else 0] + [1 if E[i - 1] > 0 and E[i] > 0 else 0 for i in range(1,len(E))]
    I = [0] + [2 if E[0] < 0 else 0] + [2 if E[i - 1] < 0 and E[i] < 0 else 0 for i in range(1,len(E))]
    J = [0] + [H[i] + I[i] for i in range(1,len(E))]#J列第一个永远是0（之前忘记规定这个了）
    K = [0] + [J[:i+1:].count(0) for i in range(1,len(E))]
    L = [0] + [J[:i+1:].count(1) for i in range(1,len(E))]
    M = [0] + [J[:i+1:].count(2) for i in range(1,len(E))]
    N = [0] + [K[i] - L[i] - M[i] for i in range(1,len(E))]  # =K3-L3-M
    O = [0] + [L[i] - M[i] for i in range(1,len(E))]  # L3-M3
    P = [0] + [M[i] - L[i] for i in range(1,len(E))]  # =M3-L3
    Q = [0] + [abs(O[i]) + abs(P[i]) for i in range(1,len(E))]  # ABS(O3)+ABS(P3)
    R = [0] + [1 if Q[i - 1] > 0 and Q[i] == 0 else 0 for i in range(1,len(E))]  # IF(AND(Q3>0,Q4=0),1,0)    1
    R1 = [0]+[1 if Q[i - 1] == Q[i] else 0 for i in range(1,len(E))]  # =IF(Q4=Q3,1,0)
    S = [0] + [sum(R[:i+1:]) for i in range(1,len(E))]   # SUM($R$2:R3)
    T = [1] + [1 if O[i - 1] > N[i - 1] and O[i] < N[i] else (1 if O[i - 1] < N[i - 1] and O[i] > N[i] else (1 if O[i]==N[i] else 0)) for i in range(1,len(E))]# =IF(AND(O2>N2,O3<N3),1,IF(AND(O2<N2,O3>N3),1,IF(N3=O3,1,0))))
    U = [0] + [sum(T[:i+1:]) for i in range(len(E))]#=SUM(T$2:$T3)
    V = [1] + [1 if P[i - 1] > N[i - 1] and P[i] < N[i] else (1 if P[i - 1] < N[i - 1] and P[i] > N[i] else (1 if P[i]==N[i] else 0)) for i in range(1,len(E))]#=IF(AND(P2>N2,P3<N3),1,IF(AND(P2<N2,P3>N3),1,IF(N3=P3,1,0)))
    W = [0] + [sum(V[:i+1:]) for i in range(1,len(E))]#=SUM(V$2:$V3)
    X = [0] + [(N[i] - N[0])/(B[i] - B[0]) for i in range(1,len(E))]#=(N3-$N$2)/(B3-$B$2)
    Y = [0] + [sum(X[:i+1:])/B[i] for i in range(1,len(E))]#=SUM($X$2:X3)/B3
    Z = [0] + [X[i] - X[i-1] for i in range(1,len(E))]#=X3-X2
    AA = [0] + [(O[i] - O[0])/(B[i] - B[0]) for i in range(1,len(E))]#=(O3-$O$2)/(B3-$B$2)
    AB = [0] + [sum(AA[:i+1:])/B[i] for i in range(1,len(E))]#=SUM($AA$2:AA3)/B3
    AC = [0] + [AA[i] - AA[i-1] for i in range(1,len(E))]#=AA3-AA2
    AD = [0] + [(P[i] - P[0])/(B[i] - B[0]) for i in range(1,len(E))]#=(P3-$P$2)/(B3-$B$2)
    AE = [0] + [sum(AD[:i+1:])/B[i] for i in range(1,len(E))]#=SUM($AD$2:AD3)/B3
    AF = [0] + [AD[i] - AD[i-1] for i in range(1,len(E))]#=AD3-AD2
    AG = [0] + [1 if AA[i-1] == 0 and AA[i]> 0 else (1 if AC[i-1] < 0 and AC[i] >= 0 else 0) for i in range(1,len(E))]#=IF(AND(AA2=0,AA3>0),1,IF(AND(AC2<0,AC3>=0),1,0))
    AH = [0] + [1 if N[i] < O[i] and N[i] > P[i] and O[i] > P[i] and Z[i-1] > 0 and Z[i] < 0 else (1 if N[i] < P[i] and N[i] > O[i] and O[i] < P[i] and Z[i-1] < 0 and Z[i] > 0 else 0) for i in range(1,len(E))]#IF(AND(N3<O3,N3>P3,O3>P3,Z2>0,Z3<0),1,IF(AND(N3<P3,N3>O3,O3<P3,Z2<0,Z3>0),1,0))
    AI = [0 if AG[i] == 0 else AG[i] - AH[i] for i in range(1,len(E))]#IF(AG3=0,0,AG3-AH3)
    AJ = [0] + [1 if N[i] < P[i] and N[i] > O[i] and P[i] > O[i] and Z[i-1] > 0 and Z[i] < 0 else (1 if N[i] < O[i] and N[i] > P[i] and P[i] < O[i] and Z[i-1] < 0 and Z[i] > 0 else 0) for i in range(1,len(E))]#[IF(AND(N3<P3,N3>O3,P3>O3,Z2>0,Z3<0),1,IF(AND(N3<O3,N3>P3,P3<O3,Z2<0,Z3>0),1,0))
    AK = [0] + [1 if AD[i-1] == 0 and AD[i] > 0 else (1 if AF[i-1] < 0 and AF[i] >= 0 else 0) for i in range(1,len(E))]#IF(AND(AD2=0,AD3>0),1,IF(AND(AF2<0,AF3>=0),1,0))
    AL = [0 if AK[i] == 0 else AK[i] - AJ[i] for i in range(1,len(E))]#IF(AK3=0,0,AK3-AJ3)
    AW = [0] + [1 if N[i] > O[i] and O[i] > 0 and S[i-1] == S[i] else (1 if N[i] > P[i] and P[i] > 0 and S[i-1] == S[i] else 0) for i in range(1,len(E))]#IF(AND(N3 > O3, O3 > 0, S3=S2), 1, IF(AND(N3 > P3, P3 > 0, S3=S2), 2, 0))
    AX = [0] + [1 if AW[i-1] == 0 and AW[i] == 1 else (2 if AW[i-1] == 0 and AW[i] == 2 else 0) for i in range(1,len(E))]#IF(AND(AW2=0, AW3=1), 1, IF(AND(AW2=0, AW3=2), 2, 0))
    AY = [0] + [AX[:i+1:].count(1) for i in range(1,len(E))]#COUNTIF($AX$2: AX3, 1)
    AZ = [0] + [AX[:i+1:].count(2) for i in range(1,len(E))]#COUNTIF($AX$2: AX3, 2)
    BA = [0] + [AY[i] - AZ[i] for i in range(1,len(E))]#AY3 - AZ3
    BB = [0] + [AZ[i] - AY[i] for i in range(1,len(E))]#AZ3 - AY3
    BE = [0] + [1 if N[i] < P[i] and O[i] > 0 and AA[i] > 0 else (1 if N[i] < O[i] and AF[i-1] < 0 and AF[i] >= 0 else 0) for i in range(1,len(E))]#IF(AND(N3 < P3, O3 > 0, AA3 > 0), 1, IF(AND(N3 < O3, P3 > 0, AF2 < 0, AF3 >= 0), 1, 0))
    BF = [0] + [1 if N[i] < O[i] and P[i] > 0 and AD[i] > 0 else (1 if N[i] < P[i] and O[i] > 0 and AC[i-1] < 0 and AC[i] >= 0 else 0) for i in range(1,len(E))]#IF(AND(N3 < O3, P3 > 0, AD3 > 0), 1, IF(AND(N3 < P3, O3 > 0, AC2 < 0, AC3 >= 0), 1, 0))
    BG = [0] + [1 if N[i] < P[i] and O[i] > 0 and S[i-1] == S[i] else (2 if N[i] < O[i] and P[i] > 0 and S[i-1] == S[i] else 0) for i in range(1,len(E))]#IF(AND(N3 < P3, O3 > 0, S3=S2), 1, IF(AND(N3 < O3, P3 > 0, S3=S2), 2, 0))
    BH = [0] + [1 if BG[i-1] == 0 and BG[i] == 1 else (2 if BG[i-1] == 0 and BG[i] == 2 else 0) for i in range(1,len(E))]#IF(AND(BG2=0, BG3=1), 1, IF(AND(BG2=0, BG3=2), 2, 0))
    BI = [0] + [BH[:i+1:].count(1) for i in range(1,len(E))]#COUNTIF($BH$2: BH3, 1)
    BJ = [0] + [BH[:i+1:].count(2) for i in range(1,len(E))]#COUNTIF($BH$2: BH3, 2)
    BK = [0] + [BI[i] - BJ[i] for i in range(1,len(E))]#BI3 - BJ3
    BL = [0] + [BJ[i] - BI[i] for i in range(1,len(E))]#BJ3 - BI3
    BC = [0] + [1 if N[i] < O[i] and BL[i] >= 0 and P[i] > 0 and AF[i-1] > 0 and AF[i] <= 0 else 0 for i in range(1,len(E))]#IF(AND(N3 < O3, BL3 >= 0, P3 > 0, AF2 > 0, AF3 <= 0), 1, 0)
    BD = [0] + [1 if N[i] < P[i] and BK[i] >= 0 and O[i] > 0 and AC[i-1] > 0 and AC[i] <= 0 else 0 for i in range(1,len(E))]#IF(AND(N3 < P3, BK3 >= 0, O3 > 0, AC2 > 0, AC3 <= 0), 1, 0)
    AM = [0] + [1 if N[i] > P[i] and BB[i] >= 0 and P[i] > 0 and AF[i-1] >= 0 and AF[i] < 0 else (1 if N[i] > O[i] and BA[i] >= 0 and O[i] > 0 and AC[i-1] <= 0 and AC[i] > 0 else 0) for i in range(1,len(E))]#IF(AND(N3>P3,BB3>=0,P3>0,AF2>=0,AF3<0),1,IF(AND(N3>O3,BA3>=0,O3>0,AC2<=0,AC3>0),1,0))
    AN = [0] + [1 if N[i] > O[i] and BA[i] >= 0 and O[i] > 0 and AC[i-1] >= 0 and AC[i] < 0 else (1 if N[i] > P[i] and BB[i] >= 0 and P[i] > 0 and AF[i-1] <= 0 and AF[i] > 0 else 0) for i in range(1,len(E))]#IF(AND(N3>O3,BA3>=0,O3>0,AC2>=0,AC3<0),1,IF(AND(N3>P3,BB3>=0,P3>0,AF2<=0,AF3>0),1,0))
    AR = [0] + [1 if N[i] > O[i] and O[i] > 0 and AC[i-1] <= 0 and AC[i] > 0 else (1 if N[i] > P[i] and P[i] > 0 and AF[i-1] <= 0 and AF[i] > 0 else 0) for i in range(1,len(E))]#IF(AND(N3 > O3, O3 > 0, AC2 <= 0, AC3 > 0), 1, IF(AND(N3 > P3, P3 > 0, AF2 <= 0, AF3 > 0), 1, 0))
    AS = [0] + [1 if N[i] > P[i] and P[i] > 0 and AF[i-1] <= 0 and AF[i] > 0 else (1 if N[i] > O[i] and O[i] > 0 and AC[i-1] <= 0 and AC[i] > 0 else 0) for i in range(1,len(E))]#IF(AND(N3 > P3, P3 > 0, AF2 <= 0, AF3 > 0), 1, IF(AND(N3 > O3, O3 > 0, AC2 <= 0, AC3 > 0), 1, 0))
    AO = [0] + [0 if AM[i] == 0 else AM[i] - AR[i] for i in range(1,len(E))]#IF(AM3=0,0,AM3-AR3)
    AT = [0] + [0 if AN[i] == 0 else AN[i] - AS[i] for i in range(1,len(E))]#IF(AN3=0, 0, AN3 - AS3)
    AP = [0] + [AO[i] + AG[i] + BC[i] for i in range(1,len(E))]#AO3+AG3+BC3
    AQ = [0] + [AR[i] + AH[i] + BE[i] for i in range(1,len(E))]#AR3+AH3+BE3
    AU = [0] + [AS[i] + AJ[i] + BF[i] for i in range(1,len(E))]#AS3+AJ3+BF3
    AV = [0] + [AT[i] + AK[i] + BD[i] for i in range(1,len(E))]#AT3+AK3+BD3
    BM = ["-"] + ["BUY" if AP[i] > 0 else "-" for i in range(1,len(E))]#IF(AP2>0,"BUY","-")
    BN = ["-"] + ["SELL" if AV[i] > 0 else "-" for i in range(1,len(E))]#IF(AV2=1,"SELL","-")
    BO = [0]
    BP = [0]
    BQ = [0]
    BR = [0]
    BRA = [0]
    BRB = [0]
    BS = [0]
    BT = [0]
    for i in range(1,len(E)):
        BO.append((C[i] if BM[i] == "BUY" else BO[i-1]))#IF(BM3="BUY",VALUE(C3),BO2)
        BP.append((C[i] if BN[i] == "SELL" else BP[i-1]))#IF(BN3="SELL",VALUE(C3),BP2)
        BQ.append(10000000 if BO[i] == 0 else BO[i])#IF(BO3=0,10000000,VALUE(BO3))
        BR.append(10000000 if BQ[i] == 10000000 else (BQ[i] if BQ[i] < BQ[i-1] else BR[i-1]))#=IF(BQ3=10000000,10000000,IF(BQ3<BQ2,BQ3,BR2))
        BRA.append(1 if BR[i] < BR[i-1] else 0)#=IF(BR3<BR2,1,0)
        BRB.append(1 if BP[i] > BP[i-1] else 0)#=IF(BP3>BP2,1,0)
        BS.append(BRA)
        BT.append(1 if BN[i] == "SELL" and BRB[i] == 1 else (1 if BN[i] == "SELL" and BP[i-1] == 0 and BP[i] > 0 else 0))#IF(AND(BN3="SELL",BRB3=1),1,IF(AND(BN3="SELL",BP2=0,BP3>0),1,0))
    BU = [0] + [
        1 if BM[i - 2] == "BUY" and BM[i - 1] == "BUY" and BM[i] == "BUY" and BO[i - 2] < BO[i - 3] and BO[i - 1] < BO[
            i - 2] and BO[i] < BO[i - 1] else (1 if BN[i - 1] == "SELL" and BM[i] == "BUY" and BP[i - 1] > BO[i] else 0)
        for i in range(1,len(E))]
    # IF(AND(BM2="BUY",BM3="BUY",BM4="BUY",BO2<BO1,BO3<BO2,BO4<BO3),1,IF(AND(BN3="SELL",BM4="BUY",BP3>BO4),1,0))
    BV = [0] + [1 if BN[i - 2] == "SELL" and BN[i - 1] == "SELL" and BN[i] == "SELL" and BP[i - 2] < BP[i - 3] and BP[i - 1] <
               BP[i - 2] and BP[i] < BP[i - 1] else (
        1 if BM[i - 1] == "BUY" and BN[i] == "SELL" and BO[i - 1] < BP[i] else 0) for i in range(1,len(E))]
    # IF(AND(BN2="SELL",BN3="SELL",BN4="SELL",BP2>BP1,BP3>BP2,BP4>BP3),1,IF(AND(BM3="BUY",BN4="SELL",BO3<BP4),1,0))
    BW = [0]
    BX = [0]
    BY = [0]
    BZ = [0]
    CA = [0]
    CB = [0]
    CC = [0]
    CD = [0]
    CE = [0]
    CF = [0]
    for i in range(1,len(E)):
        BW.append("BUY" if BRA[i] - BU[i] == 1 else "-")#BW = ["BUY" if BS[i] - BU[i] == 1 else "-" for i in range(1,len(E))]#IF(BS3-BU3=1,"BUY","-")
        BX.append("SELL" if BT[i] - BV[i] == 1 else "-")#BX = ["SELL" if BT[i] - BV[i] == 1 else "-" for i in range(1,len(E))]#IF(BT3-BV3=1,"SELL","-")
        BY.append(BW[:i+1:].count("BUY"))#COUNTIF($BW$2:BW3,"BUY")
        BZ.append(BX[:i+1:].count("SELL"))#COUNTIF($BX$2:BX3,"SELL")
        CA.append(BY[i] + BZ[i])#BY2+BZ2
        CB.append(BY[i]/CA[i] if CA[i] > 0 else 0)#IF(CA3>0,BY3/CA3,0)
        CC.append(BZ[i]/CA[i] if CA[i] > 0 else 0)#=IF(CA3>0,BZ3/CA3,0)
        CD.append(math.log(1/CB[i],2) if CB[i] > 0 else 0)#=IF(CB3>0,LOG(1/CB3,2),0)
        CE.append(math.log(1/CC[i],2) if CC[i] > 0 else 0)#=IF(CC3>0,LOG(1/CC3,2),0)
        CF.append(CB[i]*CD[i] + CC[i]*CE[i])#=CB3*CD3+CC3*CE3
    CG = [0]
    CH = [0]
    for i in range(1,len(E)):
        CG.append(BW[i] if CD[i] == 0 or CD[i] > 0.3 else "-")
        CH.append(BX[i] if CE[i] == 0 or CE[i] > 0.3 else "-")
    #CG = [BW[i] if CD[i] == 0 or CD[i] > 0.3 else "-" for i in range(len(E))]#=IF(OR(CD3=0,CD3>0.3),BW3,"-")
    #CH = [BX[i] if CE[i] == 0 or CE[i] > 0.3 else "-" for i in range(len(E))]#=IF(OR(CE3=0,CE3>0.3),BX3,"-")
    CI = [0]
    CJ = [0]
    for i in range(1,len(E)):
        CI.append(C[i] if CG[i] == "BUY" else CI[i-1])#=IF(CG3="BUY",C3,CI2)
        CJ.append(CI[i] if CI[i-1] == 0 and CI[i] > 0 else CJ[i-1])#=IF(AND(CI2=0,CI3>0),CI3,CJ2)
    CK = [0] + [0 if CJ[i] == 0 else CJ[i] - C[i] for i in range(1,len(E))]#=IF(CJ3=0,0,CJ3-C3)
    CL = [0] + [sum(CK[:i+1:]) for i in range(1,len(E))]#=SUM($CK$3:CK3)
    CM = [0] + [0 if CL[i-1] == 0 else (CL[i] - CL[i-1])/CL[i-1] for i in range(1,len(E))]#=IF(CL4=0,0,(CL5-CL4)/CL4)
    CN = [0] + [CM[i] - CM[i-1] for i in range(1,len(E))]#=CM3-CM2
    CO = [0]
    CP = [0]
    for i in range(1,len(E)):
        CO.append(C[i] if CH[i] == "SELL" else CO[i-1])#=IF(CH3="SELL",C3,CO2)
        CP.append(CO[i] if CO[i-1] == 0 and CO[i] > 0 else CP[i-1])#=IF(AND(CO2=0,CO3>0),CO3,CP2)
    CQ = [0] + [0 if CO[i] == 0 else C[i] - CP[i] for i in range(1,len(E))]#=IF(CO3=0,0,(C3-CP3))
    CR = [0] + [sum(CQ[:i+1:]) for i in range(1,len(E))]#SUM($CQ$3:CQ3)
    CS = [0] + [CR[i]/B[i] for i in range(1,len(E))]#=SUM($CQ$3:CQ3)/B3
    CT = [0] + [CI[i]/2 + CO[i]/2 for i in range(1,len(E))]#=(CI3+CO3)/2
    CU = [0] + [CS[i] - CS[i-1] for i in range(1,len(E))]#=CS4-CS3
    CV = [0] + [1 if CL[i-1] > 0 and CL[i] > 0 else (2 if CL[i-1] < 0 and CL[i] < 0 else 0) for i in range(1,len(E))]#=IF(AND(CL2>0,CL3>0),1,IF(AND(CL2<0,CL3<0),2,0))
    CW = [0] + [1 if CR[i-1] > 0 and CR[i] > 0 else (2 if CR[i-1] < 0 and CR[i] < 0 else 0) for i in range(1,len(E))]#=IF(AND(CR2>0,CR3>0),1,IF(AND(CR2<0,CR3<0),2,0))
    CX = [0] + [1 if CU[i-1] > 0 and CU[i] > 0 and CS[i] > 0 else 0 for i in range(1,len(E))]#=IF(AND(CU3>0,CU4<0,CS4>0),1,0)
    CY = [0] + [1 if CU[i-1] < 0 and CU[i] > 0 and CS[i] < 0 else 0 for i in range(1,len(E))]#=IF(AND(CU3<0,CU4>0,CS4<0),1,0)
    CZ = [0] + [1 if CR[i-2] <= 0 and CR[i-1] > 0 and CR[i] > 0 else 0 for i in range(1,len(E))]#=IF(AND(CR2<=0,CR3>0,CR4>0),1,0)
    DA = [0] + [1 if CR[i-2] >= 0 and CR[i-1] < 0 and CR[i] < 0 else 0 for i in range(1,len(E))]#=IF(AND(CR2>=0,CR3<0,CR4<0),1,0)
    DB = [0] + [C[i] if CX[i] == 1 else 0 for i in range(1,len(E))]#=IF(CX4=1,VALUE(C4),0)
    DC = [0] + [1 if DB[i] > 0 else 0 for i in range(1,len(E))]#=IF(DB4>0,1,0)
    DD = [0] + [DC[:i+1:].count(1) for i in range(1,len(E))]#=COUNTIF($DC$4:DC4,1)
    DE = [0] + [C[i] if CY[i] == 1 else 0 for i in range(1,len(E))]#=IF(CY4=1,VALUE(C4),0)
    DF = [0] + [1 if DE[i] > 0 else 0 for i in range(1,len(E))]#=IF(DE4>0,1,0)
    DG = [0] + [DF[:i+1:].count(1) for i in range(1,len(E))]#=COUNTIF($DF$4:DF4,1)
    DH = [0] + [C[i] if CZ[i] == 1 else 0 for i in range(1,len(E))]#=IF(CZ4=1,VALUE(C4),0)
    DI = [0] + [1 if DH[i] > 0 else 0 for i in range(1,len(E))]#=IF(DH4>0,1,0)
    DJ = [0] + [DI[:i+1:].count(1) for i in range(1,len(E))]#=COUNTIF($DI$4:DI4,1)
    DK = [0] + [C[i] if DA[i] == 1 else 0 for i in range(1,len(E))]#=IF(DA4=1,VALUE(C4),0)
    DL = [0] + [1 if DK[i] > 0 else 0 for i in range(1,len(E))]#=IF(DK4>0,1,0)
    DM = [0] + [DL[:i+1:].count(1) for i in range(1,len(E))]#=COUNTIF($DL$4:DL4,1)
    DN = [0] + [0 if DD[i] == 0 else sum(DB[:i+1:])/DD[i] for i in range(1,len(E))]#=IF(DD4=0,0,SUM($DB$4:DB4)/DD4)
    DO = [0]
    for i in range(1,len(E)):
        DO.append(DN[i] if DN[i-1] == 0 and DN[i] > 0 else DO[i-1])#=IF(AND(DN3=0,DN4>0),DN4,DO3)
    DP = [0] + [DN[i] - DO[i] for i in range(1,len(E))]#=DN4-DO4
    DQ = [0] + [DP[i] - DP[i-1] for i in range(1,len(E))]#=DP4-DP3
    DR = [0] + [0 if DG[i] == 0 else sum(DE[:i+1:])/DG[i] for i in range(1,len(E))]#=IF(DG4=0,0,SUM($DE$4:DE4)/DG4)
    DS = [0]
    for i in range(1,len(E)):
        DS.append(DR[i] if DR[i-1] == 0 and DR[i] > 0 else DS[i-1])#=IF(AND(DR3=0,DR4>0),DR4,DS3)
    DT = [0] + [DR[i] - DS[i] for i in range(1,len(E))]#=DR4-DS4
    DU = [0] + [DT[i] - DT[i-1] for i in range(1,len(E))]#=DT4-DT3
    DV = [0] + [0 if DJ[i] == 0 else sum(DH[:i+1:])/DJ[i] for i in range(1,len(E))]#=IF(DJ4=0,0,SUM($DH$4:DH4)/DJ4)
    DW = [0]
    for i in range(1,len(E)):
        DW.append(DV[i] if DV[i-1] == 0 and DV[i] > 0 else DW[i-1])#=IF(AND(DV3=0,DV4>0),DV4,DW3)
    DX = [0] +  [DV[i] - DW[i] for i in range(1,len(E))]#=DV4-DW4
    DY = [0] + [DX[i] - DX[i-1] for i in range(1,len(E))]#=DX4-DX3
    DZ = [0] + [0 if DM[i] == 0 else sum(DK[:i+1])/DM[i] for i in range(1,len(E))]#=IF(DM4=0,0,SUM($DK$4:DK4)/DM4)
    EA = [0]
    EB = [0]
    EC = [0]
    for i in range(1,len(E)):
        EA.append(DZ[i] if DZ[i-1] == 0 and DZ[i] > 0 else EA[i-1])#=IF(AND(DZ3=0,DZ4>0),DZ4,EA3)
        EB.append(DZ[i] - EA[i])#=DZ4-EA4
        EC.append(EB[i] - EB[i-1])#=EB4-EB3
    ED = [0]
    EE = [0]
    EF = [0]
    EG = [0]
    EH = [0]
    EI = [0]
    EJ = [0]
    EK = [0]
    for i in range(1,len(E)):
        ED.append(CI[i] if CI[i-1] == 0 and CI[i] > 0 else ED[i-1])#=IF(AND(CI2=0,CI3>0),CI3,ED2)
        EE.append(CO[i] if CI[i-1] == 0 and CO[i] > 0 else EE[i-1])#=IF(AND(CO2=0,CO3>0),CO3,EE2)
        EF.append(ED[i] if ED[i-1] == 0 and ED[i] > 0 else (EE[i] if EE[i-1] == 0 and EE[i] >0 else EF[i-1]))#=IF(AND(ED2=0,ED3>0),ED3,IF(AND(EE2=0,EE3>0),EE3,EF2))
        EG.append(EF[i] if EF[i-1] == 0 and EF[i] > 0 else EG[i-1])#=IF(AND(EF2=0,EF3>0),EF3,EG2)
        EH.append(C[i] - EG[i] if EG[i] > 0 else 0)
        EI.append(EG[i] - C[i] if EG[i] > 0 else 0)
        EJ.append(sum(EH[:i+1:]))
        EK.append(sum(EI[:i+1:]))
    EL = [0] + [EJ[i]/B[i] for i in range(1,len(E))]#=EJ3/B3
    EM = [0] + [EL[i] - EL[i-1] for i in range(1,len(E))]#=EL3-EL2
    EN = [0] + [EK[i]/B[i] for i in range(1,len(E))]#=EK3/B3
    EO = [0] + [EN[i] - EN[i-1] for i in range(1,len(E))]#=EN3-EN2
    EP = [0] + [1 if EM[i-1] > 0 and EM[i] < 0 and EJ[i] > 0 else 0 for i in range(1,len(E))]#=IF(AND(EM2>0,EM3<0,EJ3>0),1,0)
    EQ = [0] + [1 if EN[i-1] < 0 and EN[i] > 0 and EK[i] > 0 else 0 for i in range(1,len(E))]#=IF(AND(EN2<0,EN3>0,EK3>0),1,0)
    ER = [0] + [1 if EJ[i-2] <= 0 and EJ[i-1] > 0 and EJ[i] > 0 else 0 for i in range(1,len(E))]#=IF(AND(EJ1<=0,EJ2>0,EJ3>0),1,0)
    ES = [0] + [1 if EK[i-2] <= 0 and EK[i-1] > 0 and EK[i] > 0 else 0 for i in range(1,len(E))]#=IF(AND(EK1<=0,EK2>0,EK3>0),1,0)
    ET = [0] + [C[i] if EP[i] == 1 else 0 for i in range(1,len(E))]#=IF(EP3=1,VALUE(C3),0)
    EU = [0] + [1 if ET[i] > 0 else 0 for i in range(1,len(E))]#=IF(ET3>0,1,0)
    EV = [0] + [EU[:i+1:].count(1) for i in range(1,len(E))]#=COUNTIF($EU3:EU$3,1)
    EW = [0] + [C[i] if EQ[i] == 1 else 0 for i in range(1,len(E))]#=IF(EQ3=1,VALUE(C3),0)
    EX = [0] + [1 if EW[i] > 0 else 0 for i in range(1,len(E))]#=IF(EW3>0,1,0)
    EY = [0] + [EX[:i+1:].count(1) for i in range(1,len(E))]#=COUNTIF($EX3:EX$3,1)
    EZ = [0] + [C[i] if ER[i] == 1 else 0 for i in range(1,len(E))]#=IF(ER3=1,VALUE(C3),0)
    FA = [0] + [1 if EZ[i] > 0 else 0 for i in range(1,len(E))]#=IF(EZ3>0,1,0)
    FB = [0] + [FA[:i+1:].count(1) for i in range(1,len(E))]#=COUNTIF($FA3:FA$3,1)
    FC = [0] + [C[i] if ES[i] == 1 else 0 for i in range(1,len(E))]#IF(ES3=1,VALUE(C3),0)
    FD = [0] + [1 if FC[i] > 0 else 0 for i in range(1,len(E))]#=IF(FC3>0,1,0)
    FE = [0] + [FD[:i+1:].count(1) for i in range(1,len(E))]#=COUNTIF($FD3:FD$3,1)
    FF = [0] + [0 if EV[i] == 0 else sum(ET[:i:])/EV[i] for i in range(1,len(E))]#=IF(EV3=0,0,SUM($ET3:ET$3)/EV3)
    FG = [0]
    for i in range(1,len(E)):
        FG.append(FF[i] if FF[i-1] == 0 and FF[i] > 0 else FG[i-1])#=IF(AND(FF2=0,FF3>0),FF3,FG2)
    FH = [0] + [FF[i] - FG[i] for i in range(1,len(E))]#=FF3-FG3
    FI = [0] + [FH[i] - FH[i-1] for i in range(1,len(E))]#=FH3-FH2
    FJ = [0] + [0 if EY[i] == 0 else sum(EW[:i+1:])/EY[i] for i in range(1,len(E))]#=IF(EY3=0,0,SUM($EW3:EW$4)/EY3)
    FK = [0]
    for i in range(1,len(E)):
        FK.append(FJ[i] if FJ[i-1] == 0 and FJ[i] > 0 else FK[i-1])#=IF(AND(FJ2=0,FJ3>0),FJ3,FK2)
    FL = [0] + [FJ[i] - FK[i] for i in range(1,len(E))]#=FJ3-FK3
    FM = [0] + [FL[i] - FL[i-1] for i in range(1,len(E))]#=FL3-FL2
    FN = [0] + [0 if FB[i] == 0 else sum(EZ[:i:])/FB[i] for i in range(1,len(E))]#=IF(FB3=0,0,SUM($EZ3:EZ$4)/FB3)
    FO = [0]
    for i in range(1,len(E)):
        FO.append(FN[i] if FN[i-1] == 0 and FB[i] > 0 else FO[i-1])#=IF(AND(FN2=0,FN3>0),FN3,FO2)
    FP = [0] + [FN[i] - FO[i] for i in range(1,len(E))]#=FN3-FO3
    FQ = [0] + [FP[i] - FP[i-1] for i in range(1,len(E))]#=FP3-FP2
    FR = [0] + [0 if FE[i] == 0 else sum(FC[:i:])/FE[i] for i in range(1,len(E))]#=IF(FE3=0,0,SUM($FC3:FC$4)/FE3)
    FS = [0]
    for i in range(1,len(E)):
        FS.append(FR[i] if FR[i-1] == 0 and FR[i] > 0 else FS[i-1])#=IF(AND(FR2=0,FR3>0),FR3,FS2)
    FT = [0] + [FR[i] - FS[i] for i in range(1,len(E))]#=FR3-FS3
    FU = [0] + [FT[i] - FT[i-1] for i in range(1,len(E))]#=FT3-FT2
    FV = [0] + [FF[i]/2 + DN[i]/2 if FF[i] > 0 and DN[i] > 0 else FF[i] + DN[i] for i in range(1,len(E))]#=IF(AND(FF3>0,DN3>0),(FF3+DN3)/2,(FF3+DN3))
    FW = [0]
    for i in range(1,len(E)):
        FW.append(FV[i] if FV[i-1] == 0 and FV[i] > 0 else FW[i-1])#=IF(AND(FV2=0,FV3>0),FV3,FW2)
    FX = [0] + [FV[i] - FW[i] for i in range(1,len(E))]#=FV3-FW3
    FY = [0] + [FX[i] - FX[i-1] for i in range(1,len(E))]#=FX3-FX2
    FZ = [0] + [FJ[i]/2 + DR[i]/2 if FJ[i] > 0 and DR[i] > 0 else FJ[i] + DR[i] for i in range(1,len(E))]#=IF(AND(FJ3>0,DR3>0),(FJ3+DR3)/2,(FJ3+DR3))
    GA = [0]
    for i in range(1,len(E)):
        GA.append(FZ[i] if FZ[i-1] == 0 and FZ[i] > 0 else GA[i-1])#=IF(AND(FZ2=0,FZ3>0),FZ3,GA2)
    GB = [0] + [FZ[i] - GA[i] for i in range(1,len(E))]#=FZ3-GA3
    GC = [0] + [GB[i] - GB[i-1] for i in range(1,len(E))]#=GB3-GB2
    GD = [0] + [DV[i]/2 + FN[i]/2 if DV[i] > 0 and FN[i] > 0 else DV[i] + FN[i] for i in range(1,len(E))]#=IF(AND(DV3>0,FN3>0),(DV3+FN3)/2,(DV3+FN3))
    GE = [0]
    for i in range(1,len(E)):
        GE.append(GD[i] if GD[i-1] == 0 and GD[i] > 0 else GE[i-1])
    #=IF(AND(GD2=0,GD3>0),GD3,GE2)
    GF = [0] + [GD[i] - GE[i] for i in range(1,len(E))]#=GD3-GE3
    GG = [0] + [GF[i] - GF[i-1] for i in range(1,len(E))]#=GF3-GF2
    GH = [0] + [FR[i]/2 + DZ[i]/2 if FR[i] > 0 and DZ[i] > 0 else FR[i] + DZ[i] for i in range(1,len(E))]#=IF(AND(FR3>0,DZ3>0),(FR3+DZ3)/2,(FR3+DZ3))
    GI = [0]
    for i in range(1,len(E)):
        GI.append(GH[i] if GH[i-1] == 0 and GH[i] > 0 else GI[i-1])#=IF(AND(GH2=0,GH3>0),GH3,GI2)
    GJ = [0] + [GH[i] - GI[i] for i in range(1,len(E))]#=GH3-GI3
    GK = [0] + [GJ[i] - GJ[i-1] for i in range(1,len(E))]#=GJ3-GJ2
    #剪刀确定
    IL = [0]
    IM = [0]
    IMA = [0]
    IMB = [0]
    IMC = [0]
    IN = [0]
    IO = [0]
    IP = [0]
    IQ = [0]
    IR = [0]
    IS = [0]
    ISA = [0]
    ISB = [0]
    IT = [0]
    IU = [0]
    IV = [0]
    IW = [0]
    IX = [0]
    IY = [0]
    IZ = [0]
    for i in range(1,len(E)):
        IL.append(1 if CG[i] == "BUY" else 0)  # =IF(CG3="BUY",1,0)
        IM.append(2 if CH[i] == "SELL" else 0)  # =IF(CH3="SELL",2,0)
        IMA.append(IL[:i+1:].count(1))#=COUNTIF(IL3:$IL$3,1)
        IMB.append(IM[:i+1:].count(2))#=COUNTIF(IM3:$IM$3,2)
        IMC.append(1 if IMB[i] > IMA[i] and IMA[i] > 0 else (2 if IMA[i] > IMB[i] and IMB[i] > 0 else (1 if IMB[i] >= 2 and IMB[i] > IMA[i] else (2 if IMA[i] >= 2 and IMA[i] > IMB[i] else IMC[i-1]))))
        #=IF(AND(IMB3>IMA3,IMA3>0),1,IF(AND(IMA3>IMB3,IMB3>0),2,IF(AND(IMB3>=2,IMB3>IMA3),1,IF(AND(IMA3>=2,IMA3>IMB3),2,IMC2))))#=IF(AND(IMB3>IMA3,IMA3>0),1,IF(AND(IMA3>IMB3,IMB3>0),2,IMC2))
        IN.append(1 if FB[i] > 0 and FB[i] > FE[i] else (1 if FB[i - 1] == 0 and FB[i] > 0 and FB[i] == FE[
            i - 1] else 0))  # =IF(AND(FB3>0,FB3>FE3),1,IF(AND(FB2=0,FB3>0,FB3=FE2),1,0))
        IO.append(2 if FE[i] > 0 and FE[i] > FB[i] else (2 if FE[i - 1] == 0 and FE[i] > 0 and FE[i] == FB[
            i - 1] else 0))  # =IF(AND(FE3>0,FE3>FB3),2,IF(AND(FE2=0,FE3>0,FE3=FB2),2,0))
        IP.append(1 if IN[i] == 1 else (2 if IO[i] == 2 else IP[i - 1]))  # =IF(IN3=1,1,IF(IO3=2,2,IP2))
        IQ.append(2 if IP[i] == 1 and IL[i] == 1 else (2 if IP[1] == 2 and IM[i] == 2 else (
            1 if IP[i] == 1 and IM[i] == 2 else (1 if IP[i] == 2 and IL[i] == 1 else IQ[i - 1]))))
        # =IF(AND(IP3=1,IL3=1),2,IF(AND(IP3=2,IM3=2),2,IF(AND(IP3=1,IM3=2),1,IF(AND(IP3=2,IL3=1),1,IQ2))))
        IR.append(1 if IT[i - 1] == 1 and IP[i] == 1 and IM[i] == 2 and IQ[i] == 1 else (
            1 if IP[i] == 2 and IM[i] == 2 else 0))  # =IF(AND(IT2=1,IP3=1,IM3=2,IQ3=1),1,IF(AND(IP3=2,IM3=2),1,0))
        IS.append(1 if IT[i - 1] == 2 and IP[i] == 2 and IL[i] == 1 and IQ[i] == 1 else (
            1 if IP[i] == 1 and IL[i] == 1 else 0))  # =IF(AND(IT2=2,IP3=2,IL3=1,IQ3=1),1,IF(AND(IP3=1,IL3=1),1,0))
        ISA.append(0 if IR[i] == 1 and IMC[i] == 1 and IP[i] == 1 else (1 if IR[i] == 0 and IMC[i] == 2 and IP[i] == 2 else IR[i]))#=IF(AND(IR3=1,IMC3=1,IP3=1),0,IF(AND(IR3=0,IMC3=2,IP3=2),1,IR3))
        ISB.append(0 if IS[i] == 1 and IMC[i] == 2 and IP[i] == 2 else (1 if IS[i] == 0 and IMC[i] == 1 and IP[i] == 1 else IS[i]))#=IF(AND(IS3=1,IMC3=2,IP3=2),0,IF(AND(IS3=0,IMC3=1,IP3=1),1,IS2))
        IT.append(1 if IMC[i - 1] == 0 and IMC[i] == 1 else (2 if IMC[i - 1] == 0 and IMC[i] == 2 else IT[
            i - 1]))  # =IF(AND(IMC2=0,IMC3=1),1,IF(AND(IMC2=0,IMC3=2),2,IT2))
        IU.append(C[i] if IT[i-1] == 0 and IT[i] == 1 else (C[i] if IT[i-1] == 0 and IT[i] == 2 else IU[i - 1]))  # =IF(and(IT2==0,IT3=1),EG3,IF(AND(IT2=0,IT3=2),EG3,IU2))
        IV.append(C[i] - IU[i] if IT[i] == 1 else 0)  # =IF(IT3=1,C3-IU3,0)
        IW.append(sum(IV[:i+1:]))  # =SUM($IV$3:IV3)
        IX.append(IU[i] - C[i] if IT[i] == 2 else 0)  # =IF(IT3=2,IU3-C3,0)
        IY.append(sum(IX[:i+1:]))  # =SUM($IX$3:IX3)
        IZ.append(IV[i] if IT[i] == 1 else (IX[i] if IT[i] == 2 else 0))  # =IF(IT3=1,IV3,IF(IT3=2,IX3,0))
    JA = [0]
    JB = [0]
    JC = [0]
    JD = [0]
    JE = [0]
    JF = [0]
    JG = [0]
    JH = [0]
    JI = [0]
    JJ = [0]
    JKA = [0]
    JKB = [0]
    JK = [0]
    JL = [0]
    JM = [0]
    JN = [0]
    JO = [0]
    JP = [0]
    JQ = [0]
    JR = [0]
    JS = [0]
    JT = [0]
    JU = [0]
    JV = [0]
    JW = [0]
    JX = [0]
    for i in range(1, len(E)):
        JA.append(1 if IT[i - 1] == 1 and ISA[i] == 1 else (2 if IT[i - 1] == 2 and ISB[i] == 1 else (
            1 if B[i] > 60 and IT[i - 1] == 1 and JE[i - 1] <= 0 else (
                2 if IT[i - 1] == 2 and B[i] > 60 and JE[i - 1] <= 0 else JA[i - 1]))))
        # =IF(AND(IT2=1,ISA3=1),1,IF(AND(IT2=2,ISB3=1),2,IF(AND(B3>60,IT2=1,JE2<=0),1,IF(AND(IT2=2,B3>60,JE2<=0),2,JA2))))*
        JB.append(IT[i] - JA[i])  # =IT3-JA3
        JC.append(IW[i] if JB[i] == 1 else (IY[i] if JB[i] == 2 else JC[i - 1]))  # =IF(JB3=1, IW3, IF(JB3=2, IY3, JC2))
        JD.append(IV[i] * (stock_v - B[i]) if JB[i - 1] == 1 and JA[i] == 1 else (
            IX[i] * (stock_v - B[i]) if JB[i - 1] == 2 and JA[i] == 2 else JD[
                i - 1]))  # =IF(AND(JB2=1,JA3=1),IV3*(390-B3),IF(AND(JB2=2,JA3=2),IX3*(390-B3),JD2))
        JE.append(JC[i] + JD[i])  # =JC3+JD3
        JF.append(1 if IT[i] == 1 and ISA[i] == 1 else (
            2 if IT[i] == 2 and ISB[i] == 2 else JF[i - 1]))  # =IF(AND(IT3=1,ISA3=1),1,IF(AND(IT3=2,ISB3=1),2,JF2))*
        JG.append(IT[i] - JF[i])  # =IT3-JF3
        JH.append(IW[i] if JG[i] == 1 else (IY[i] if JG[i] == 2 else JH[i - 1]))  # =IF(JG3=1,IW3,IF(JG3=2,IY3,JH2))
        JI.append(IV[i] * (stock_v - B[i]) if JG[i - 1] == 1 and JF[i] == 1 else (
            IX[i] * (stock_v - B[i]) if JG[i - 1] == 2 and JF[i] == 2 else JI[
                i - 1]))  # =IF(AND(JG2=1,JF3=1),IV3*(390-B3),IF(AND(JG2=2,JF3=2),IX3*(390-B3),JI2))
        JJ.append(JH[i] + JI[i])  # =(JH3+JI3)
        JKA.append(1 if JB[i] == 0 and IMC[i] == 1 and IP[i] == 1 else 0)  # =IF(AND(JB3=0,IMC3=1,IP3=1),1,0)*
        JKB.append(1 if JB[i] == 0 and IMC[i] == 2 and IP[i] == 2 else 0)  # =IF(AND(JB3=0,IMC3=2,IP3=2),1,0)*
        JK.append(1 if JM[i - 1] == 1 and IP[i] == 1 and IM[i] == 2 else 0)  # =IF(AND(JM2=1,IP3=1,IM3=2),1,0)
        JL.append(1 if JM[i - 1] == 2 and IP[i] == 2 and IL[i] == 1 else 0)  # =IF(AND(JM2=2,IP3=2,IL3=1),1,0)
        JM.append(1 if JKA[i - 1] == 0 and JKA[i] == 1 else (2 if JKB[i - 1] == 0 and JKB[i] == 1 else JM[
            i - 1]))  # =IF(AND(JKA2=0,JKA3=1),1,IF(AND(JKB2=0,JKB3=1),2,JM2))*
        JN.append(C[i] if JM[i - 1] == 0 and JM[i] == 1 else (C[i] if JM[i - 1] == 0 and JM[i] == 2 else JN[
            i - 1]))  # =IF(AND(JM2=0,JM3=1),C3,IF(AND(JM2=0,JM3=2),C3,JN2))
        JO.append(C[i] - JN[i] if JM[i] == 1 else 0)  # =IF(JM3=1,C3-JN3,0)
        JP.append(sum(JO[:i+1:]))  # =SUM($JO$3:JO3)
        JQ.append(JN[i] - C[i] if JM[i] == 2 else 0)  # =IF(JM3=2,JN3-C3,0)
        JR.append(sum(JQ[:i+1:]))  # =SUM($JQ$3:JQ3)
        JS.append(JP[i] if JM[i] == 1 else (JR[i] if JM[i] == 2 else 0))  # =IF(JM3=1,JP3,IF(JM3=2,JR3,0))
        JT.append(1 if JM[i - 1] == 1 and JK[i] == 1 else (2 if JM[i - 1] == 2 and JL[i] == 1 else (
            1 if JM[i - 1] == 1 and B[i] > 60 and JX[i - 1] <= 0 else (
                2 if JM[i - 1] == 2 and B[i] > 60 and JX[i - 1] <= 0 else JT[i - 1]))))
        # =IF(AND(JM2=1,JK3=1),1,IF(AND(JM2=2,JL3=1),2,IF(AND(JM2=1,B3>60,JX2<=0),1,IF(AND(JM2=2,B3>60,JX2<=0),2,JT2))))
        JU.append(JM[i] - JT[i])  # =JM3-JT3
        JV.append(JS[i] if JU[i] == 1 else (JS[i] if JU[i] == 2 else JV[i - 1]))  # =IF(JU3=1,JS3,IF(JU3=2,JS3,JV2))
        JW.append(JO[i] * (stock_v - B[i]) if JU[i - 1] == 1 and JT[i] == 1 else (
            JQ[i] * (stock_v - B[i]) if JU[i - 1] == 2 and JT[i] == 2 else JW[
                i - 1]))  # =IF(AND(JU2=1,JT3=1),JO3*(390-B3),IF(AND(JU2=2,JT3=2),JQ3*(390-B3),JW2))
        JX.append(JV[i] + JW[i])  # =JV3+JW3
    GL = [0]
    GM = [0]
    for i in range(1,len(E)):
        GL.append(1 if EJ[i-1] ==0 and EJ[i] > 0 else (2 if EK[i-1] == 0 and EK[i] > 0 else GL[i-1]))#=IF(AND(EJ2=0,EJ3>0),1,IF(AND(EK2=0,EK3>0),2,GL2))
        GM.append(C[i] if GL[i] == 1 else (C[i] if GL[i] == 2 else GM[i-1]))#=IF(GL3=1,EF3,IF(GL3=2,EG3,GM2))
    GN = [0] + [C[i] - GM[i] if GL[i] == 1 else 0 for i in range(1,len(E))]#=IF(GL3=1,C3-GM3,0)
    GO = [0] + [sum(GN[:i+1:]) for i in range(1,len(E))]#=SUM($GN$3:GN3)
    GP = [0] + [GM[i] - C[i] if GL[i] == 2 else 0 for i in range(1,len(E))]#=IF(GL3=2,GM3-C3,0)
    GQ = [0] + [sum(GP[:i+1:]) for i in range(1,len(E))]#=SUM($GP$3:GP3)
    GR = [0] + [EJ[i] if GL[i] == 1 else (EK[i] if GL[i] == 2 else 0) for i in range(1,len(E))]#=IF(GL3=1,EJ3,IF(GL3=2,EK3,0))
    GS = [0]
    GT = [0]
    GU = [0]
    GV = [0]
    GW = [0]
    GX = [0]
    GY = [0]
    GZ = [0]
    HA = [0]
    HB = [0]
    for i in range(1,len(E)):
        GS.append(1 if GL[i - 1] == 1 and FX[i] < 0 and FY[i] < 0 else (
            2 if GL[i - 1] == 2 and GB[i] > 0 and GC[i] > 0 else (2 if GL[i - 1] == 2 and FY[i] > 0 else (
                1 if GL[i - 1] == 1 and GC[i] < 0 else (1 if GL[i - 1] == 1 and B[i] > 60 and GW[i - 1] <= 0 else (
                    2 if GL[i - 1] == 2 and B[i] > 0 and GW[i - 1] <= 0 else GS[i - 1]))))))
        # IF(AND(GL2=1,FX3<0,FY3<0),1,IF(AND(GL2=2,GB3>0,GC3>0),2,IF(AND(GL2=2,FY3>0),2,IF(AND(GL2=1,GC3<0),1,IF(AND(GL2=1,B3>60,GW2<=0),1,IF(AND(GL2=2,B3>60,GW2<=0),2,GS2))))))
        GT.append(GL[i] - GS[i])#=GL3-GS3
        GU.append(GR[i] if GT[i] == 1 else (GR[i] if GT[i] == 2 else GU[i-1]))#=IF(GT3=1,GR3,IF(GT3=2,GR3,GU2))
        GV.append(EH[i]*(stock_v-B[i]) if GT[i-1] == 1 and GS[i] == 1 else (EI[i]*(stock_v-B[i]) if GT[i-1] == 2 and GS[i] == 2 else GV[i-1]))#=IF(AND(GT2=1,GS3=1),EH3*(390-B3),IF(AND(GT2=2,GS3=2),EI3*(390-B3),GV2))
        GW.append(GU[i] + GV[i])#=GU3+GV3
        GX.append(1 if GL[i - 1] == 1 and FX[i] < 0 and FY[i] > 0 else (
            2 if GL[i - 1] == 2 and GB[i] > 0 and GC[i] > 0 else (
                2 if GL[i - 1] == 2 and FY[i] > 0 else (1 if GL[i - 1] == 1 and GC[i] < 0 else GX[i - 1]))))
        # =IF(AND(GL2=1,FX3<0,FY3<0),1,IF(AND(GL2=2,GB3>0,GC3>0),2,IF(AND(GL2=2,FY3>0),2,IF(AND(GL2=1,GC3<0),1,GX2))))
        GY.append(GL[i] - GX[i])#=GL3-GX3
        GZ.append(GR[i] if GY[i] == 1 else (GR[i] if GY[i] == 2 else GZ[i-1]))#=IF(GY3=1,GR3,IF(GY3=2,GR3,GZ2))
        HA.append(EH[i]*(stock_v-B[i]) if GY[i-1] == 1 and GX[i] == 1 else (EI[i]*(stock_v-B[i]) if GY[i-1] == 2 and GX[i] == 2 else HA[i-1]))#=IF(AND(GY2=1,GX3=1),EH3*(390-B3),IF(AND(GY2=2,GX3=2),EI3*(390-B3),HA2))
        HB.append(GZ[i] + HA[i])#=(GZ3+HA3)
    HC = [0]
    HCA = [0]
    HD = [0]
    HE = [0]
    HF = [0]
    HG = [0]
    HH = [0]
    HI = [0]
    HJ = [0]
    HK = [0]
    HL = [0]
    HM = [0]
    HN = [0]
    HO = [0]
    HP = [0]
    HQ = [0]
    HR = [0]
    HS = [0]
    for i in range(1,len(E)):
        HC.append(1 if GT[i] == 0 and IP[i] == 1 else (2 if GT[i] == 0 and IP[i] == 2 else HC[i-1]))#=IF(AND(IP3=1,GT3=0),1,IF(AND(IP3=2,GT3=0),2,HC2))
        HCA.append(1 if HC[i-1] == 0 and HC[i] == 1 else (2 if HC[i-1] == 0 and HC[i] == 2 else HCA[i-1]))#=IF(AND(HC2=0,HC3=1),1,IF(AND(HC2=0,HC3=2),2,HD2))
        HD.append(C[i] if HCA[i-1] == 0 and HCA[i] == 1 else (C[i] if HCA[i-1] == 0 and HCA[i] == 2 else HD[i-1]))#=IF(AND(HC2=0,HC3=1),C3,IF(AND(HC2=0,HC3=2),C3,HD2))
        HE.append(C[i] - HD[i] if HCA[i] == 1 else 0)#=IF(HC3=1,C3-HD3,0)
        HF.append(sum(HE[:i+1:]))#=SUM($HE$3:HE3)
        HG.append(HD[i] - C[i] if HCA[i] == 2 else 0)#=IF(HC3=2,HD3-C3,0)
        HH.append(sum(HG[:i+1:]))#=SUM($HG$3:HG3)
        HI.append(HF[i] if HCA[i] == 1 else (HH[i] if HCA[i] == 2 else 0))#=IF(HC3=1,HF3,IF(HC3=2,HH3,0))
        HJ.append(1 if HCA[i-1] == 1 and FX[i] < 0 and FY[i] < 0 else (2 if HCA[i-1] == 2 and GB[i] > 0 and GC[i] > 0 else (1 if HCA[i-1] == 1 and B[i] > 60 and HN[i-1] <= 0 else (2 if HCA[i-1] == 2 and B[i] > 60 and HN[i-1] <= 0 else HJ[i-1]))))
        #=IF(AND(HCA2=1,FX3<0,FY3<0),1,IF(AND(HCA2=2,GB3>0,GC3>0),2,IF(AND(HCA2=1,B3>60,HN2<=0),1,IF(AND(HCA2=2,B3>60,HN2<=0),2,HJ2))))
        #=IF(AND(HC2=1,JK3=1),1,IF(AND(HC2=2,JL3=1),2,IF(AND(HC2=1,B3>60,HN2<=0),1,IF(AND(HC2=2,B3>60,HN2<=0),2,HJ2))))*
        HK.append(HCA[i] - HJ[i])#=HC3-HJ33
        HL.append(HI[i] if HK[i] == 1 else (HI[i] if HK[i] == 2 else HL[i-1]))#=IF(HK3=1,HI3,IF(HK3=2,HI3,HL2))
        HM.append(HE[i]*(stock_v-B[i]) if HK[i-1] ==1 and HJ[i] == 1 else (HG[i]*(stock_v-B[i]) if HK[i-1] == 2 and HJ[i] == 2 else HM[i-1]))#=IF(AND(HK2=1,HJ3=1),HE3*(390-B3),IF(AND(HK2=2,HJ3=2),HG3*(390-B3),HM2))
        HN.append(HL[i] + HM[i])#=HL3+HM3
        HO.append(1 if HCA[i-1] == 1 and FX[i] < 0 and FY[i] < 0 else (2 if HCA[i-1] ==2 and GB[i] > 0 and GC[i] > 0 else HO[i-1]))
        #=IF(AND(HCA2=1,FX3<0,FY3<0),1,IF(AND(HCA2=2,GB3>0,GC3>0),2,HO2))
        HP.append(HCA[i] - HO[i])#=HC3-HO3
        HQ.append(HI[i] if HP[i] == 1 else (HI[i] if HP[i] == 2 else HQ[i-1]))#=IF(HP3=1,HI3,IF(HP3=2,HI3,HQ2))
        HR.append(HE[i]*(stock_v-B[i]) if HP[i-1] ==1 and HO[i] == 1 else (HG[i]*(stock_v-B[i]) if HP[i-1] == 2 and HO[i] == 2 else HR[i-1]))#=IF(AND(HP2=1,HO3=1),HE3*(390-B3),IF(AND(HP2=2,HO3=2),HG3*(390-B3),HR2))
        HS.append(HQ[i] + HR[i])#=HQ3+HR3
    HT = [0]
    HU = [0]
    HV = [0]
    HW = [0]
    HX = [0]
    HY = [0]
    HZ = [0]
    IA = [0]
    IB = [0]
    IC = [0]
    ID = [0]
    IE = [0]
    IF = [0]
    IG = [0]
    IH = [0]
    II = [0]
    IJ = [0]
    IK = [0]
    for i in range(1,len(E)):
        HT.append(1 if GY[i-1] == 1 and GX[i] == 1 and HB[i-1] <= 0 and B[i] > 60 else (1 if GY[i-1] == 2 and GX[i] == 2 and HB[i-1] <= 0 and B[i] > 60 else HT[i-1]))
        #=IF(AND(GY2=1,GX3=1,HB2<=0,B3>60),1,IF(AND(GY2=2,GX3=2,HB2<=0,B3>60),1,HT2))
        HU.append("BUY" if GL[i-1] == 0 and GL[i] == 1 else ("SELL" if GL[i-1] == 0 and GL[i] == 2 else 0))#=IF(AND(GL2=0,GL3=1),"BUY",IF(AND(GL2=0,GL3=2),"SELL",0))
        HV.append("BUY" if HC[i-1] == 0 and HC[i] == 1 else ("SELL" if HC[i-1] == 0 and HC[i] == 2 else (0 if HT[i] == 1 else 0)))#=IF(AND(HC2=0,HC3=1),"BUY",IF(AND(HC2=0,HC3=2),"SELL",IF(HT3=1,0,0)))
        HW.append(GW[i] if HT[i] == 1 else GW[i] + HN[i])#=IF(HT3=1,GW3,GW3+HN3)
        HX.append(HB[i] + HS[i])#=HB3+HS3
        HY.append(GM[i])#=VALUE(GM3)
        HZ.append(HW[i] - HW[i-1])#=HW3-HW2
        IA.append(HX[i] - HX[i-1])#=HX3-HX2
        IB.append(0 if HY[i] == 0 else HZ[i]/HY[i])#=IF(HY3=0,0,HZ3/HY3)
        IC.append(0 if HY[i] == 0 else IA[i]/HY[i])#=IF(HY3=0,0,IA3/HY3)
        ID.append(1 if IB[i] > 0.01 else 0)#=IF(IB3>1%,1,0)
        IE.append(1 if IC[i] > 0.01 else 0)#=IF(IC3>1%,1,0)
        IF.append(ID[:i+1:].count(1))#=COUNTIF($ID$3:ID3,1)
        IG.append(IE[:i+1:].count(1))#=COUNTIF($IE$3:IE3,1)
        IH.append(IF[i]/B[i])#=IF3/B3
        II.append(IG[i]/B[i])#=IG3/B3
        IJ.append(1 if IH[i-1] > 0 and IH[i] > IH[i-1] else IJ[i-1])#=IF(AND(HY2=0,HY3>0,IH3>0,IH4>IH3),1,IJ3)change to =IF(AND(IH3>0,IH4>IH3),1,IJ3)
        IK.append(1 if II[i-1] > 0 and II[i] > II[i-1] else IK[i-1])#=IF(AND(HY2=0,HY3>0,II3>0,II4>II3),1,IK3)
    JY = [0]
    JZ = [0]
    KA = [0]
    KB = [0]
    KC = [0]
    KD = [0]
    KE = [0]
    KF = [0]
    KG = [0]
    KH = [0]
    for i in range(1,len(E)):
        JY.append(1 if JM[i] == 1 and JK[i] == 1 else (2 if JM[i] == 2 and JL[i] ==2 else (JY[i-1])))#=IF(AND(JM3=1,JK3=1),1,IF(AND(JM3=2,JL3=1),2,JY2))
        JZ.append(JM[i] - JY[i])#=JM3-JY3
        KA.append(JS[i] if JZ[i] == 1 else (JS[i] if JZ[i] == 2 else KA[i-1]))#=IF(JZ3=1,JS3,IF(JZ3=2,JS3,KA2))
        KB.append(JO[i]*(stock_v-B[i]) if JZ[i-1] == 1 and JY[i] == 1 else (JQ[i]*(stock_v-B[i]) if JZ[i-1] == 2 and JY[i] == 2 else KB[i-1]))#=IF(AND(JZ2=1,JY3=1),JO3*(390-B3),IF(AND(JZ2=2,JY3=2),JQ3*(390-B3),KB2))
        KC.append(KA[i] + KB[i])#=KA3+KB3
        KD.append(1 if JB[i-1] == 1 and JA[i] == 1 and JE[i-1] <= 0 and B[i] > 60 else (1 if JB[i-1] == 2 and JA[i] == 2 and JE[i-1] <= 0 and B[i] > 60 else KD[i-1]))
        #=IF(AND(JB2=1,JA3=1,JE2<=0,B3>60),1,IF(AND(JB2=2,JA3=2,JE2<=0,B3>60),1,KD2))
        KE.append("BUY" if IT[i-1] == 0 and IT[i] == 1 else ("SELL" if IT[i-1] == 0 and IT[i] == 2 else 0))#=IF(AND(IT2=0,IT3=1),"BUY",IF(AND(IT2=0,IT3=2),"SELL",0))
        KF.append("BUY" if JM[i-1] == 0 and JM[i] == 1 else ("SELL" if JM[i-1] == 0 and JM[i] == 2 else (0 if KD[i] == 0 else 0)))#=IF(AND(JM2=0,JM3=1),"BUY",IF(AND(JM2=0,JM3=2),"SELL",IF(KD3=1,0,0)))
        KG.append(JE[i] if KD[i] == 1 else JE[i] + JX[i])#=IF(KD3=1,JE3,JE3+JX3)
        KH.append(JJ[i] + KC[i])#=JJ3+KC3
    KI = [0]
    KJ = [0]
    KK = [0]
    KL = [0]
    KM = [0]
    KN = [0]
    KO = [0]
    KP = [0]
    KQ = [0]
    KR = [0]
    KS = [0]
    KT = [0]
    KU = [0]
    KV = [0]
    KW = [0]
    for i in range(1,len(E)):
        KI.append(1 if JG[i] == 1 else (2 if JZ[i] == 2 else (2 if JG[i] == 2 else (1 if JZ[i] == 1 else 0))))#=IF(JG3=1,1,IF(JZ3=2,2,IF(JG3=2,2,IF(JZ3=1,1,0))))
        KJ.append(1 if JB[i] == 1 else (2 if JU[i] == 2 else (2 if JB[i] == 2 else (1 if JU[i] == 1 else 0))))#=IF(JB3=1,1,IF(JU3=2,2,IF(JB3=2,2,IF(JU3=1,1,0))))
        KK.append(IU[i])#=VALUE(IU4)
        KL.append(KG[i] - KG[i-1])#=KG3-KG2
        KM.append(KH[i] - KH[i-1])#=KH3-KH2
        KN.append(0 if KK[i] == 0 else KL[i]/KK[i])#=IF(KK3=0,0,KL3/KK3)
        KO.append(0 if KK[i] == 0 else KM[i]/KK[i])#=IF(KK3=0,0,KM3/KK3)
        KP.append(1 if KN[i] > 0.01 else 0)#=IF(KN3>1%,1,0)
        KQ.append(1 if KO[i] > 0.01 else 0)#=IF(KO3>1%,1,0)
        KR.append(KP[:i+1:].count(1))#=COUNTIF($KP$3:KP3,1)
        KS.append(KQ[:i+1:].count(1))#=COUNTIF($KQ$3:KQ3,1)
        KT.append(KR[i]/B[i])#=KR3/B3
        KU.append(KS[i]/B[i])#=KS3/B3
        KV.append(1 if KT[i-1] > 0 and KT[i] > KT[i-1] else KV[i-1])#=IF(AND(KK1=0,KK2>0,KT2>0,KT3>KT2),1,KV2)change to =IF(AND(KT2>0,KT3>KT2),1,KV2)
        KW.append(1 if KU[i-1] > 0 and KU[i] > KU[i-1] else KW[i-1])#=IF(AND(KK1=0,KK2>0,KU2>0,KU3>KU2),1,KW2)

    KX = [1 if (B[i] >= 5 and B[i] <= stock_v and L[i-4] == 0 and L[i-3] > 0 and K[i-4] == K[i-3]) else 0 for i in range(len(E))]#=IF(AND(B6 >= 5, B6 <= 48, L2=0, L3 > 0, K2=K3), 1, 0)
    KY = [1 if (B[i] >= 5 and B[i] <= stock_v and M[i-4] == 0 and M[i-3] > 0 and K[i-4] == K[i-3]) else 0 for i in range(len(E))]#=IF(AND(B6 >= 5, B6 <= 48, M2=0, M3 > 0, K2=K3), 1, 0)
    KZ = [1 if (B[i] >= 7 and B[i] <= stock_v and K[i-2] == K[i-3] and L[i-3] == 0 and L[i-2] > 0 and M[i-2] == M[i-3]) else 0 for i in range(len(E))]#=IF(AND(B8 >= 7, B8 <= 48, K6=K5, L5=0, L6 > 0, M6=M5), 1, 0)
    LA = [1 if (B[i]  >= 7 and B[i] <= stock_v and K[i-2] == K[i-3] and M[i-3] == 0 and M[i-2] > 0 and L[i-2] == L[i-3]) else 0 for i in range(len(E))]#=IF(AND(B8 >= 7, B8 <= 48, K5=K6, L5=L6, M5=0, M6 > 0), 1, 0)
    LB = [1 if (B[i]  >= 6 and B[i] <= stock_v and K[i-2] == K[i-3] and L[i-2] > L[i-3] and M[i-2] == M[i-3]) else 0 for i in range(len(E))]#=IF(AND(K5=K4,L5>L4,M5=M4),1,0)
    LC = [1 if (B[i] >= 6 and B[i] <= stock_v and K[i-2] == K[i-3] and M[i-2] > M[i-3] and L[i-2] == L[i-3]) else 0 for i in range(len(E))]#=IF(AND(K5=K4,L5=L4,M5>M4),1,0)
    LD = [1 if (B[i] >= 11 and B[i] <= stock_v and K[i-1] == K[i-2] and L[i-1] > L[i-2] and M[i-1] == M[i-2]) else 0 for i in range(len(E))]#=IF(AND(K11=K10,L11>L10,M11=M10),1,0)
    LE = [1 if (B[i]  >= 11 and B[i] <= stock_v and K[i-1] == K[i-2] and L[i-1] == L[i-2] and M[i-1] > M[i-2]) else 0 for i in range(len(E))]#=IF(AND(K11=K10,L11=L10,M11>M10),1,0)
    LF = [1 if (B[i] >= 5 and B[i] <= stock_v and J[i-1] == 0 and J[i-2] == 2 and J[i-3] == 0 and J[i-4] == 1) else 0 for i in range(len(E))]#=IF(AND(J2=1, J3=0, J4=2, J5=0), 1, 0)
    LG = [1 if (B[i]  >= 6 and B[i] <= stock_v and J[i-2] == 0 and J[i-3] == 2 and J[i-4] == 0 and J[i-5] == 1) else 0 for i in range(len(E))]#=IF(AND(J2=1, J3=0, J4=2, J5=0), 1, 0)
    LH = [1 if (B[i] >= 5 and B[i] <= stock_v and J[i-2] == 0 and J[i-3] == 1 and J[i-4] == 0 and J[i-5] == 2) else 0 for i in range(len(E))]#=IF(AND(J2=2, J3=0, J4=1, J5=0), 1, 0)
    LI = [1 if (B[i] >= 6 and B[i] <= stock_v and J[i-1] == 0 and J[i-2] == 1 and J[i-3] == 0 and J[i-4] == 2) else 0 for i in range(len(E))]#=IF(AND(J2=2, J3=0, J4=1, J5=0), 1, 0)
    LJ = [1 if (B[i] >= 2 and B[i] <= stock_v and J[i-1] == 0 and J[i] == 1) else 0 for i in range(len(E))]#=IF(AND(J2=0, J3=1), 1, 0)
    LK = [1 if (B[i] >= 3 and B[i] <= stock_v and J[i-2] == 0 and J[i-1] == 2) else 0 for i in range(len(E))]#=IF(AND(J2=0, J3=2), 1, 0)
    LL = [1 if (B[i] >= 2 and B[i] <= stock_v and J[i-1] == 0 and J[i] == 2) else 0 for i in range(len(E))]#=IF(AND(J2=0, J3=2), 1, 0)
    LM = [1 if (B[i]   >= 3 and B[i] <= stock_v and J[i-2] == 0 and J[i-1] == 1) else 0 for i in range(len(E))]#=IF(AND(J2=0, J3=1), 1, 0)
    LN = [1 if (B[i]  >= 9 and B[i] <= stock_v and K[i-2] > K[i-3] and L[i-2] == L[i-3] and L[i-2] >= 3 and M[i-2] == M[i-3] and M[i-2] >= 2) else 0 for i in range(len(E))]
    #=IF(AND(K8 > K7, L8=L7, L8 >= 3, M8=M7, M8 >= 2), 1, 0)
    LO = [1 if (B[i]  >= 9 and B[i] <= stock_v and K[i-2] > K[i-3] and L[i-2] == L[i-3] and L[i-2] >= 2 and M[i-2] == M[i-3] and M[i-2] >= 3) else 0 for i in range(len(E))]
    #=IF(AND(K8 > K7, L8=L7, L8 >= 2, M8=M7, M8 >= 3), 1, 0)
    LP = [1 if (B[i]  >= 6 and B[i] <= stock_v and K[i-2] == K[i-3] and L[i-2] > L[i-3] and M[i-2] == M[i-3]) else 0 for i in range(len(E))]#=IF(AND(K5=K4, L5 > L4, M5=M4), 1, 0)
    LQ = [1 if (B[i]  >= 6 and B[i] <= stock_v and K[i-2] == K[i-3] and L[i-2] == L[i-3] and M[i-2] > M[i-3]) else 0 for i in range(len(E))]#=IF(AND(K5=K4, L5=L4, M5 > M4), 1, 0)

    #以下改列名称
    LR = [KY[i] + LA[i] + LC[i] + LE[i] + LJ[i] + LK[i] + LO[i] + LQ[i] for i in range(len(E))]#=KY3+LA3+LC3+LE3+LJ3+LK3+LO3+LQ3=T2 + V2 + X2 + Z2 + AF2 + AG2 + AJ2 + AL2
    LS = [KX[i] + KZ[i] + LB[i] + LD[i] + LL[i] + LM[i] + LN[i] + LP[i] for i in range(len(E))]#=KX3+KZ3+LB3+LD3+LL3+LM3+LN3+LP3# =U2 + W2 + Y2 + AA2 + AH2 + AI2 + AK2 + AM2
    LT = [1 if LR[i] > 1 else LR[i] for i in range(len(E))]#=IF(LR3>1,1,LR3)=IF(AN2 > 1, 1, AN2)
    LU = [1 if LS[i] > 1 else LS[i] for i in range(len(E))]#=IF(LS3>1,1,LS3)=IF(AO2 > 1, 1, AO2)
    LV = [LT[i] - LU[i] + LF[i] + LH[i] for i in range(len(E))]#=LT3-LU3+LF3+LH3=AP2 - AQ2 + AB2 + AD2
    LW = [LU[i] - LT[i] + LG[i] + LI[i] for i in range(len(E))]#=LU3-LT3+LG3+LI3=AQ2 - AP2 + AC2 + AE2
    LX = [1 if LV[i] >= 1 else 0 for i in range(len(E))]#=IF(LV3>=1,1,0)=IF(AR2 >= 1, 1, 0)
    LY = [1 if LW[i] >= 1 else 0 for i in range(len(E))]#=IF(LW3>=1,1,0)=IF(AS2 >= 1, 1, 0)
    LZ = [1 if O[i] > 0 else (2 if P[i] > 0 else 0) for i in range(len(E))]#=IF(O3>0,1,IF(P3>0,2,0))=IF(O2 > 0, 1, IF(P2 > 0, 2, 0))
    MA = ["BUY" if LX[i] == 1 else 0 for i in range(len(E))]#=IF(LX3=1,"BUY",0)=IF(AT2=1, "BUY", 0)
    MB = [C[i] if MA[i] == "BUY" else 0 for i in range(len(E))]#=IF(MA3="BUY",VALUE(C3),0)=IF(AW2="BUY", VALUE(C2), 0)
    MC = ["SELL" if LY[i] == 1 else 0 for i in range(len(E))]#=IF(LY3=1,"SELL",0)=IF(AU2=1, "SELL", 0)
    MD = [C[i] if MC[i] == "SELL" else 0 for i in range(len(E))]#=IF(MC3="SELL",VALUE(C3),0)=IF(AY2="SELL",VALUE(C2),0)
    ME = [0]
    MF = [0]
    MG = [0]
    MH = [0]
    MHA = [0]
    MHB = [0]
    MI = [0]
    MJ = [0]
    MK = [0]
    ML = [0]
    MM = [0]
    MN = [0]
    MO = [0]
    MOA = [0]
    MOB = [0]
    MP = [0]
    MQ = [0]
    MR = [0]
    MS = [0]
    MT = [0]
    MU = [0]
    for i in range(1,len(E)):
        ME.append("BUY" if MA[i] == "BUY" else ME[i - 1])#=IF(MA2="BUY","BUY",ME1)=IF(AW2="BUY", "BUY", BA1)
        MF.append(MB[i] if MB[i] > 0 else MF[i-1])#=IF(MB2>0,MB2,MF1)=IF(AX2 > 0, AX2, BB1)
        MG.append("SELL" if MC[i] == "SELL" else MG[i - 1])#=IF(MC2="SELL","SELL",MG1)=IF(AY2="SELL", "SELL", BC1)
        MH.append(MD[i] if MD[i] > 0 else MH[i-1])  #=IF(MD2>0,MD2,MH1) =IF(AZ2 > 0, AZ2, BD1)
        MHA.append(1 if MF[i-1] == 0 and MF[i] > 0 else (1 if MF[i] > MF[i-1] else 0))#=IF(AND(MF2=0,MF3>0),1,IF(MF3<MF2,1,0))
        MHB.append(1 if MH[i] > MH[i-1] else 0)#=IF(MH3>MH2,1,0)
        MI.append("BUY" if MA[i] == "BUY" and MHA[i] == 1 else "-")#=IF(AND(MA3="BUY",MHA3=1),"BUY","-")
        MJ.append("SELL" if MC[i] == "SELL" and MHB[i] == 1 else "-")#=IF(AND(MC3="SELL",MHB3=1),"SELL","-")
        #MI.append("BUY" if MA[i-1] == "BUY" and MA[i] == "BUY" and MB[i] < MB[i-1] else ("BUY" if MA[i] == "BUY" and MF[i] > 0 and MF[i] < min(MF[:i+1:]) else ("BUY" if ME[i-1] == 0 and ME[i] =="BUY" and MF[i] > 0 else "-")))
        #=IF(AND(MA2="BUY",MA3="BUY",MB3<MB2),"BUY",IF(AND(MA3="BUY",MF3>0,MF3<MIN($MF2:MF$2)),"BUY",IF(AND(ME2=0,ME3="BUY",MF3<>0),"BUY","-")))
        #MJ.append("SELL" if MG[i-1] == "SELL" and MG[i] == "SELL" and MH[i] > max(MH[:i+1:]) else ("SELL" if MG[i-1] == 0 and MG[i] =="SELL" and MH[i] > 0 else "-"))
        #=IF(AND(MG2="SELL",MG3="SELL",MH3>MAX($MH$2:MH2)),"SELL",IF(AND(MG2=0,MG3="SELL",MH3>0),"SELL","-"))==IF(AND(AY4="SELL",BD4>MAX($BD$2:BD3)),"SELL",IF(AND(BC3=0,BC4="SELL",BD4>0),"SELL","-")
        MK.append(C[i] if MI[i] == "BUY" else MK[i-1])#=IF(MI3="BUY",VALUE(C3),MK2)=IF(BP2="BUY",VALUE(C2),BG1)
        ML.append(C[i] if MJ[i] == "SELL" else ML[i-1])#=IF(MJ3="SELL",VALUE(C3),ML2)=IF(BQ2="SELL",VALUE(C2),BH1)
        MM.append(1 if MI[i] == "BUY" and MK[i] < ML[i-1] else 0)#=IF(AND(MI3="BUY",MK3<ML2),1,0)=IF(AND(BP3="BUY",BG3<BH2),1,0) =IF(AND(BP3="BUY",BG3<BH2),1,IF(AND(BP3="BUY",BG2=0),1,0))
        MN.append(100000000 if MF[i] == 0 else MK[i])#==IF(MF3=0,10000000,VALUE(MK3))=IF(BB2=0,10000000,VALUE(BG2))
        MO.append(100000000 if MN[i] == 100000000 else (MN[i] if MN[i] < MN[i-1] else MO[i-1]))#=IF(MN3=10000000,10000000,IF(MN3<MN2,MN3,MO2))
        MOA.append(1 if MO[i] < MO[i-1] else 0)#=IF(MO3<MO2,1,0)
        MOB.append(1 if ML[i] > ML[i-1] else 0)#=IF(ML3>ML2,1,0)
        MP.append(1 if MM[i] + MOA[i] == 2 else 0)#=IF(MM3+MOA3=2,1,0)=IF(BI3+BK3=2,1,0)
        MQ.append(1 if MJ[i] == "SELL" and MOB[i] == 1 else (1 if MJ[i] == "SELL" and ML[i-1] == 0 and ML[i] > 0 else 0))
        #=IF(AND(MJ3="SELL",MOB3=1),1,IF(AND(MJ3="SELL",ML2=0,ML3>0),1,0))=IF(AND(BQ3="SELL",BH3>MAX($BH$2:BH2)),1,IF(AND(BQ3="SELL",BH2=0,BH3>0),1,0))
        MR.append(1 if MI[i-2] == "BUY" and MI[i-1] ==  "BUY" and MI[i] == "BUY" and MK[i-2] < MK[i-3] and MK[i-1] < MK[1-2] and MK[i] < MK[i-1] else (1 if MJ[i-1] == "SELL" and MI[i] == "BUY" and ML[i-1] > MK[i] else 0))
        #=IF(AND(MI2="BUY",MI3="BUY",MI4="BUY",MK2<MK1,MK3<MK2,MK4<MK3),1,IF(AND(MJ3="SELL",MI4="BUY",ML3>MK4),1,0))#=IF(AND(BE2="BUY",BE3="BUY",BE4="BUY",BG2<BG1,BG3<BG2,BG4<BG3),1,IF(AND(BQ3="SELL",BP4="BUY",BH3>BG4),1,0))
        MS.append(1 if MJ[i-2] == "SELL" and MJ[i-1] == "SELL" and MJ[i] == "SELL" and ML[i-2] > ML[i-3] and ML[i-1] > ML[i-2] and ML[i] > ML[i-1] else (1 if MI[i-1] == "BUY" and MJ[i] == "SELL" and MK[i-1] < ML[i] else 0))
        #=IF(AND(MJ2="SELL",MJ3="SELL",MJ4="SELL",ML2>ML1,ML3>ML2,ML4>ML3),1,IF(AND(MI3="BUY",MJ4="SELL",MK3<ML4),1,0))=IF(AND(BQ2="SELL",BQ3="SELL",BQ4="SELL",BH2>BH1,BH3>BH2,BH4>BH3),1,IF(AND(BP3="BUY",BQ4="SELL",BG3<BH4),1,0))
        MT.append("BUY" if MP[i] - MR[i] == 1 else "-")#==IF(MP3-MR3=1,"BUY","-")=IF(BL3-BN3=1,"BUY","-")
        MU.append("SELL" if MQ[i] - MS[i] == 1 else "-")#=IF(MQ3-MS3=1,"SELL","-")=IF(BM3-BO3=1,"SELL","-")
    MV = [0]
    MW = [0]
    MX = [0]
    MY = [0]
    MZ = [0]
    for i in range(1,len(E)):
        MV.append(C[i] if MT[i] == "BUY" else MV[i-1])#=IF(MT3="BUY",C3,MV2)
        MW.append(MV[i] if MV[i-1] == 0 and MV[i] > 0 else MW[i-1])#=IF(AND(MV2=0,MV3>0),MV3,MW2)
        MX.append(0 if MW[i] == 0 else MW[i] - C[i])#=IF(MW3=0,0,MW3-C3)
        MY.append(sum(MX[:i+1:]))#=SUM($MX$3:MX3)
        MZ.append(0 if MY[i-1] == 0 else (MY[i] - MY[i-1])/MY[i-1])#=IF(MY2=0,0,(MY3-MY2)/MY2)
    NA = [0] + [MZ[i] - MZ[i-1] for i in range(1,len(E))]#=MZ3-MZ2
    NB = [0]
    NC = [0]
    for i in range(1,len(E)):
        NB.append(C[i] if MU[i] == "SELL" else NB[i-1])#=IF(MU3="SELL",C3,NB2)
        NC.append(NB[i] if NB[i-1] == 0 and NB[i] > 0 else NC[i-1])#=IF(AND(NB2=0,NB3>0),NB3,NC2)
    ND = [0] + [0 if NB[i] == 0 else C[i] - NC[i] for i in range(1,len(E))]#=IF(NB3=0,0,(C3-NC3))
    NE = [0] + [sum(ND[:i+1:]) for i in range(1,len(E))]#=SUM($ND$3:ND3)
    NF = [0] + [NE[i]/B[i] for i in range(1,len(E))]#=SUM($ND$3:ND3)/B3
    NG = [0] + [MV[i]/2 + NB[i]/2 for i in range(1,len(E))]#=(MV3+NB3)/2
    NH = [0] + [NF[i] - NF[i-1] for i in range(1,len(E))]#=NF3-NF2
    NI = [0] + [1 if NH[i-1] > 0 and NH[i] < 0 and NF[i] > 0 else 0 for i in range(1,len(E))]#=IF(AND(NH2>0,NH3<0,NF3>0),1,0)
    NJ = [0] + [1 if NH[i-1] < 0 and NH[i] > 0 and NF[i] < 0 else 0 for i in range(1,len(E))]#=IF(AND(NH2<0,NH3>0,NF3<0),1,0)
    NK = [0] + [1 if NE[i-2] <= 0 and NE[i-1] > 0 and NE[i] > 0 else 0 for i in range(1,len(E))]#=IF(AND(NE1<=0,NE2>0,NE3>0),1,0)
    NL = [0] + [1 if NE[i-2] >= 0 and NE[i-1] < 0 and NE[i] < 0 else 0 for i in range(1,len(E))]#=IF(AND(NE1>=0,NE2<0,NE3<0),1,0)
    NM = [0] + [C[i] if NI[i] == 1 else 0 for i in range(1,len(E))]#=IF(NI3=1,VALUE(C3),0)
    NN = [0] + [1 if NM[i] > 0 else 0 for i in range(1,len(E))]#=IF(NM3>0,1,0)
    NO = [0] + [NN[:i+1:].count(1) for i in range(1,len(E))]#=COUNTIF($NN3:NN$3,1)
    NP = [0] + [C[i] if NJ[i] == 1 else 0 for i in range(1,len(E))]#=IF(NJ3=1,VALUE(C3),0)
    NQ = [0] + [1 if NP[i] > 0 else 0 for i in range(1,len(E))]#=IF(NP3>0,1,0)
    NR = [0] + [NQ[:i+1:].count(1) for i in range(1,len(E))]#=COUNTIF($NQ3:NQ$3,1)
    NS = [0] + [C[i] if NK[i] == 1 else 0 for i in range(1,len(E))]#=IF(NK3=1,VALUE(C3),0)
    NT = [0] + [1 if NS[i] > 0 else 0 for i in range(1,len(E))]#=IF(NS3>0,1,0)
    NU = [0] + [NT[:i+1:].count(1) for i in range(1,len(E))]#=COUNTIF($NT$4:NT4,1)
    NV = [0] + [C[i] if NL[i] == 1 else 0 for i in range(1,len(E))]#=IF(NL3=1,VALUE(C3),0)
    NW = [0] + [1 if NV[i] > 0 else 0 for i in range(1,len(E))]#=IF(NV3>0,1,0)
    NX = [0] + [NW[:i+1:].count(1) for i in range(1,len(E))]#=COUNTIF($NW3:NW$4,1)
    NY = [0] + [0 if NO[i] == 0 else sum(NM[:i+1:])/NO[i] for i in range(1,len(E))]#=IF(NO3=0,0,SUM($NM$3:NM3)/NO3)
    NZ = [0]
    for i in range(1,len(E)):
        NZ.append(NY[i] if NY[i-1] == 0 and NY[i] > 0 else NZ[i-1])#=IF(AND(NY2=0,NY3>0),NY3,NZ2)
    OA = [0] + [NY[i] - NZ[i] for i in range(1,len(E))]#=NY3-NZ3
    OB = [0] + [OA[i] - OA[i-1] for i in range(1,len(E))]#=OA3-OA2
    OC = [0] + [0 if NR[i] == 0 else sum(NP[:i:])/NR[i] for i in range(1,len(E))]#=IF(NR3=0,0,SUM($NP3:NP$3)/NR3)
    OD = [0]
    for i in range(1,len(E)):
        OD.append(OC[i] if OC[i-1] == 0 and OC[i] > 0 else OD[i-1])#=IF(AND(OC2=0,OC3>0),OC3,OD2)
    OE = [0] + [OC[i] - OD[i] for i in range(1,len(E))]#=OC3-OD3
    OF = [0] + [OE[i] - OE[i-1] for i in range(1,len(E))]#=OE3-OE2
    OG = [0] + [0 if NU[i] == 0 else sum(NS[:i+1:])/NU[i] for i in range(1,len(E))]#=IF(NU3=0,0,SUM($NS$3:NS3)/NU3)
    OH = [0]
    for i in range(1,len(E)):
        OH.append(OG[i] if OG[i-1] == 0 and OG[i] > 0 else OH[i-1])#=IF(AND(OG2=0,OG3>0),OG3,OH2)
    OI = [0] + [OG[i] - OH[i] for i in range(1,len(E))]#=OG3-OH3
    OJ = [0] + [OI[i] - OI[i-1] for i in range(1,len(E))]#=OI3-OI2
    OK = [0] + [0 if NX[i] == 0 else sum(NV[:i+1:])/NX[i] for i in range(1,len(E))] #=IF(NX3=0,0,SUM($NV$3:NV3)/NX3)
    OL = [0]
    for i in range(1,len(E)):
        OL.append(OK[i] if OK[i-1] == 0 and OK[i] > 0 else OL[i-1])#=IF(AND(OK2=0,OK3>0),OK3,OL2)
    OM = [0] + [OK[i] - OL[i] for i in range(len(E))]#=OK3-OL3
    ON = [0] + [OM[i] - OM[i-1] for i in range(len(E))]#=OM3-OM2
    OO = [0]
    OP = [0]
    OQ = [0]
    OR = [0]
    for i in range(1,len(E)):
        OO.append(MV[i] if MV[i-1] == 0 and MV[i] > 0 else OO[i-1])#=IF(AND(MV2=0,MV3>0),MV3,OO2)
        OP.append(NB[i] if NB[i-1] == 0 and NB[i] > 0 else OP[i-1])#=IF(AND(NB2=0,NB3>0),NB3,OP2)
        OQ.append(OO[i] if OO[i-1] == 0 and OO[i] > 0 else (OP[i] if OP[i-1] == 0 and OP[i] > 0 else OQ[i-1]))#=IF(AND(OO2=0,OO3>0),OO3,IF(AND(OP2=0,OP3>0),OP3,OQ2))
        OR.append(OQ[i] if OQ[i-1] == 0 and OQ[i] > 0 else OR[i-1])#=IF(AND(OQ2=0,OQ3>0),OQ3,OR2)
    OS = [0] + [C[i] - OR[i] if OR[i] > 0 else 0 for i in range(1,len(E))]#=IF(OR3>0,C3-OR3,0)
    OT = [0] + [OR[i] - C[i] if OR[i] > 0 else 0 for i in range(1,len(E))]#=IF(OR3>0,OR3-C3,0)
    OU = [0] + [sum(OS[:i+1:]) for i in range(1,len(E))]#=SUM($OS$3:OS3)
    OV = [0] + [sum(OT[:i+1:]) for i in range(1,len(E))]#=SUM($OT$3:OT3)
    OW = [0] + [OU[i]/B[i] for i in range(1,len(E))]#=OU3/B3
    OX = [0] + [OW[i] - OW[i-1] for i in range(1,len(E))]#=OW3-OW2
    OY = [0] + [OV[i]/B[i] for i in range(1,len(E))]#=OV3/B3
    OZ = [0] + [OY[i] - OY[i-1] for i in range(1,len(E))]#=OY3-OY2
    PA = [0] + [1 if OX[i-1] > 0 and OX[i] < 0 and OU[i] > 0 else 0 for i in range(1,len(E))]#=IF(AND(OX2>0,OX3<0,OU3>0),1,0)
    PB = [0] + [1 if OY[i-1] < 0 and OY[i] > 0 and OV[i] > 0 else 0 for i in range(1,len(E))]#=IF(AND(OY2<0,OY3>0,OV3>0),1,0)
    PC = [0] + [1 if OU[i-2] <= 0 and OU[i-1] > 0 and OU[i] > 0 else 0 for i in range(1,len(E))]#=IF(AND(OU1<=0,OU2>0,OU3>0),1,0)
    PD = [0] + [1 if OV[i-2] <= 0 and OV[i-1] > 0 and OV[i] > 0 else 0 for i in range(1,len(E))]#=IF(AND(OV1<=0,OV2>0,OV3>0),1,0)
    PE = [0] + [C[i] if PA[i] == 1 else 0 for i in range(1,len(E))]#=IF(PA3=1,VALUE(C3),0)
    PF = [0] + [1 if PE[i] > 0 else 0 for i in range(1,len(E))]#=IF(PE3>0,1,0)
    PG = [0] + [PF[:i+1:].count(1) for i in range(1,len(E))]#=COUNTIF($PF$4:PF4,1)
    PH = [0] + [C[i] if PB[i] == 1 else 0 for i in range(1,len(E))]#=IF(PB3=1,VALUE(C3),0)
    PI = [0] + [1 if PH[i] > 0 else 0 for i in range(1,len(E))]#=IF(PH3>0,1,0)
    PJ = [0] + [PI[:i+1:].count(1) for i in range(1,len(E))]#=COUNTIF($PI$4:PI4,1)
    PK = [0] + [C[i] if PC[i] == 1 else 0 for i in range(1,len(E))]#=IF(PC3=1,VALUE(C3),0)
    PL = [0] + [1 if PK[i] > 0 else 0 for i in range(1,len(E))]#=IF(PK3>0,1,0)
    PM = [0] + [PL[:i+1:].count(1) for i in range(1,len(E))]#=COUNTIF($PL$4:PL4,1)
    PN = [0] + [C[i] if PD[i] == 1 else 0 for i in range(1,len(E))]#=IF(PD3=1,VALUE(C3),0)
    PO = [0] + [1 if PN[i] > 0 else 0 for i in range(1,len(E))]#=IF(PN3>0,1,0)
    PP = [0] + [PO[:i+1:].count(1) for i in range(1,len(E))]#=COUNTIF($PO$4:PO4,1)
    PQ = [0] + [0 if PG[i] == 0 else sum(PE[:i+1:])/PG[i] for i in range(1,len(E))]#=IF(PG4=0,0,SUM($PE$4:PE4)/PG4)
    PR = [0]
    for i in range(1,len(E)):
        PR.append(PQ[i] if PQ[i-1] == 0 and PQ[i] > 0 else PR[i-1])#=IF(AND(PQ2=0,PQ3>0),PQ3,PR2)
    PS = [0] + [PQ[i] - PR[i] for i in range(1,len(E))]#=PQ3-PR3
    PT = [0] + [PS[i] - PS[i-1] for i in range(1,len(E))]#=PS3-PS2
    PU = [0] + [0 if PJ[i] == 0 else sum(PH[:i+1:])/PJ[i] for i in range(1,len(E))]#=IF(PJ4=0,0,SUM($PH$4:PH4)/PJ4)
    PV = [0]
    for i in range(1,len(E)):
        PV.append(PU[i] if PU[i-1] == 0 and PU[i] > 0 else PV[i-1])#=IF(AND(PU2=0,PU3>0),PU3,PV2)
    PW = [0] + [PU[i] - PV[i] for i in range(1,len(E))]#=PU3-PV3
    PX = [0] + [PW[i] - PW[i-1] for i in range(1,len(E))]#=PW3-PW2
    PY = [0] + [0 if PM[i] == 0 else sum(PK[:i+1:])/PM[i] for i in range(1,len(E))]#=IF(PM4=0,0,SUM($PK$4:PK4)/PM4)
    PZ = [0]
    for i in range(1,len(E)):
        PZ.append(PY[i] if PY[i-1] == 0 and PY[i] > 0 else PZ[i-1])#=IF(AND(PY2=0,PY3>0),PY3,PZ2)
    QA = [0] + [PY[i] - PZ[i] for i in range(1,len(E))]#=PY3-PZ3
    QB = [0] + [QA[i] - QA[i-1] for i in range(1,len(E))]#=QA3-QA2
    QC = [0] + [0 if PP[i] == 0 else sum(PN[:i+1:])/PP[i] for i in range(1,len(E))]#=IF(PP4=0,0,SUM($PN$4:PN4)/PP4)
    QD = [0]
    for i in range(1,len(E)):
        QD.append(QC[i] if QC[i-1] == 0 and QC[i] > 0 else QD[i-1])#=IF(AND(QC2=0,QC3>0),QC3,QD2)
    QE = [0] + [QC[i] - QD[i] for i in range(1,len(E))]#=QC3-QD3
    QF = [0] + [OE[i] - OE[i-1] for i in range(1,len(E))]#=QE3-QE2
    QG = [0] + [PQ[i]/2 +NY[i]/2 if PQ[i] > 0 and NY[i] > 0 else PQ[i] + NY[i] for i in range(1,len(E))]#=IF(AND(PQ3>0,NY3>0),(PQ3+NY3)/2,(PQ3+NY3))
    QH = [0]
    for i in range(1,len(E)):
        QH.append(QG[i] if QG[i-1] == 0 and QG[i] > 0 else QH[i-1])#=IF(AND(QG2=0,QG3>0),QG3,QH2)
    QI = [0] + [QG[i] -QH[i] for i in range(1,len(E))]#=QG3-QH3
    QJ = [0] + [QI[i] - QI[i-1] for i in range(1,len(E))]#=QI3-QI2
    QK = [0] + [PU[i]/2 + OC[i]/2 if PU[i] > 0 and OC[i] > 0 else PU[i] + OC[i] for i in range(1,len(E))] #=IF(AND(PU3>0,OC3>0),(PU3+OC3)/2,(PU3+OC3))
    QL = [0]
    for i in range(1,len(E)):
        QL.append(QK[i] if QK[i-1] == 0 and QK[i] > 0 else QL[i-1])#=IF(AND(QK2=0,QK3>0),QK3,QL2)
    QM = [0] + [QK[i] -QL[i] for i in range(1,len(E))]#=QK3-QL3
    QN = [0] + [QM[i] - QM[i-1] for i in range(1,len(E))]#=QM3-QM2
    QO = [QG[i]/2 + PY[i]/2for i in range(len(E))]#=(OG3+PY3)/2
    QP = [0]
    for i in range(1,len(E)):
        QP.append(QO[i] if QO[i-1] == 0 and QO[i] > 0 else QP[i-1])#=IF(AND(QO2=0,QO3>0),QO3,QP2)
    QQ = [0] + [QO[i] - QP[i] for i in range(1,len(E))]#=QO3-QP3
    QR = [0] + [QQ[i] - QQ[i-1] for i in range(1,len(E))]#=QQ3-QQ2
    QS = [QC[i]/2 + OK[i]/2 for i in range(len(E))]#=(QC3+OK3)/2
    QT = [0]
    for i in range(1,len(E)):
        QT.append(QS[i] if QS[i-1] == 0 and QS[i] > 0 else QT[i-1])#=IF(AND(QS2=0,QS3>0),QS3,QT2)
    QU = [0] + [QS[i] - QT[i] for i in range(1,len(E))]#=QS3-QT3
    QV = [0] + [QU[i] - QU[i-1] for i in range(1,len(E))]#=QU3-QU2

    SW = [0]
    SX = [0]
    SXA = [0]
    SXB = [0]
    SXC = [0]
    SY = [0]
    SZ = [0]
    for i in range(1,len(E)):
        SW.append(1 if MT[i] == "BUY" else 0)  # =IF(MT3="BUY",1,0)
        SX.append(2 if MU[i] == "SELL" else 0)  # =IF(MU3="SELL",2,0)
        SXA.append(SW[:i+1:].count(1))  # =COUNTIF(SW$2:$SW3,1)
        SXB.append(SX[:i+1:].count(2))  # =COUNTIF(SX$2:$SX3,2)
        SXC.append(1 if SXB[i] > SXA[i] and SXA[i] > 0 else (2 if SXA[i] > SXB[i] and SXB[i] > 0 else (1 if SXB[i] >= 2 and SXB[i] > SXA[i] else (2 if SXA[i] >= 2 and SXA[i] > SXB[i] else SXC[
            i - 1]))))  # =IF(AND(SXB3>SXA3,SXA3>0),1,IF(AND(SXA3>SXB3,SXB3>0),2,SXC2))=IF(AND(SXB3>SXA3,SXA3>0),1,IF(AND(SXA3>SXB3,SXB3>0),2,IF(AND(SXB3>=2,SXB3>SXA3),1,IF(AND(SXA>=2,SXA3>SXB3),2,TJ2))))
        SY.append(1 if PM[i] > 0 and PM[i] > PP[i] else (1 if PM[i - 1] == 0 and PM[i] > 0 and PM[i] == PP[
            i - 1] else 0))  # =IF(AND(PM3>0,PM3>PP3),1,IF(AND(PM2=0,PM3>0,PM3=PP2),1,0))
        SZ.append(2 if PP[i] > 0 and PP[i] > PM[i] else (2 if PP[i - 1] == 0 and PP[i] > 0 and PP[i] == PM[
            i - 1] else 0))  # =IF(AND(PP3>0,PP3>PM3),2,IF(AND(PP2=0,PP3>0,PP3=PM2),2,0))
    TA = [0]
    TB = [0]
    TC = [0]
    TD = [0]
    TDA = [0]
    TDB = [0]
    TE = [0]
    TF = [0]
    TG = [0]
    TH = [0]
    TI = [0]
    TJ = [0]
    TK = [0]
    TL = [0]
    TM = [0]
    TN = [0]
    TO = [0]
    TP = [0]
    TQ = [0]
    TR = [0]
    TS = [0]
    TT = [0]
    TU = [0]
    TVA = [0]
    TVB = [0]
    for i in range(1, len(E)):
        TA.append(1 if SY[i] == 1 else (2 if SZ[i] == 2 else TA[i - 1]))  # =IF(SY3=1,1,IF(SZ3=2,2,TA2))
        TB.append(2 if TA[i] == 1 and SW[i] == 1 else (2 if TA[i] == 2 and SX[i] == 2 else (
            1 if TA[i] == 1 and SX[i] == 1 else (1 if TA[i] == 2 and SW[i] == 1 else TB[i - 1]))))
        # =IF(AND(TA3=1,SW3=1),2,IF(AND(TA3=2,SX3=2),2,IF(AND(TA3=1,SX3=2),1,IF(AND(TA3=2,SW3=1),1,TB2))))*
        TC.append(1 if TE[i - 1] == 1 and TA[i] == 1 and SX[i] == 2 and TB[i] == 1 else (
            1 if TA[i] == 2 and SX[i] == 2 else 0))  # =IF(AND(TE2=1,TA3=1,SX3=2,TB3=1),1,IF(AND(TA3=2,SX3=2),1,0))
        TD.append(1 if TE[i - 1] == 2 and TA[i] == 2 and SW[i] == 1 and TB[i] == 1 else (
            1 if TA[i] == 1 and SW[i] == 1 else 0))  # =IF(AND(TE2=2,TA3=2,SW3=1,TB3=1),1,IF(AND(TA3=1,SW3=1),1,0))
        TDA.append(0 if TC[i] == 1 and SXC[i] == 1 and TA[i] == 1 else (
            1 if TC[i] == 0 and SXC[i] == 2 and TA[i] == 2 else TC[
                i]))  # =IF(AND(TC3=1,SXC3=1,TA3=1),0,IF(AND(TC3=0,SXC3=2,TA3=2),1,TC3))
        TDB.append(0 if TD[i] == 1 and SXC[i] == 2 and TA[i] == 2 else (
            1 if TD[i] == 0 and SXC[i] == 1 and TA[i] == 1 else TD[
                i]))  # =IF(AND(TD3=1,SXC3=2,TA3=2),0,IF(AND(TD3=0,SXC3=1,TA3=1),1,TD3))
        TE.append(1 if SXC[i - 1] == 0 and SXC[i] == 1 else (
            2 if SXC[i - 1] == 0 and SXC[i] == 2 else TE[i - 1]))  # =IF(AND(SXC2=0,SXC3=1),1,IF(AND(SXC2=0,SXC3=2),2,TQ2))
        TF.append(C[i] if TE[i-1] == 0 and TE[i] == 1 else (C[i] if TE[i-1] == 0 and TE[i] == 2 else TF[i - 1]))  # =IF(QW3=1,OR3,IF(QW3=2,OR3,TF2))
        TG.append(C[i] - TF[i] if TE[i] == 1 else 0)  # =IF(TE3=1,C3-TF3,0)
        TH.append(sum(TG[:i+1:]))  # =SUM($TG$3:TG3)
        TI.append(TF[i] - C[i] if TE[i] == 2 else 0)  # =IF(TE3=2,TF3-C3,0)
        TJ.append(sum(TI[:i+1:]))  # =SUM($TI$3:TI3)
        TK.append(TG[i] if TE[i] == 1 else (TI[i] if TE[i] == 2 else 0))  # =IF(TE3=1,TG3,IF(TE3=2,TI3,0))
        TL.append(1 if TE[i - 1] == 1 and TDA[i] == 1 else (2 if TE[i - 1] == 2 and TDB[i] == 1 else (
            1 if TE[i - 1] == 1 and B[i] > 60 and TP[i - 1] <= 0 else (
                2 if TE[i - 1] == 2 and B[i] > 60 and TP[i - 1] <= 0 else TL[i - 1]))))
        # =IF(AND(TE2=1,TDA3=1),1,IF(AND(TE2=2,TDB3=1),2,IF(AND(TE2=1,B3>60,TP2<0),1,IF(AND(TE2=2,B3>60,TP2<0),2,TL2))))*
        TM.append(TE[i] - TL[i])  # =TE3-TL3
        TN.append(TH[i] if TM[i] == 1 else (TJ[i] if TM[i] == 2 else TN[i - 1]))  # =IF(TM3=1,TH3,IF(TM3=2,TJ3,TN2))
        TO.append(TG[i] * (stock_v - B[i]) if TM[i - 1] == 1 and TL[i] == 1 else (
            TI[i] * (stock_v - B[i]) if TM[i - 1] == 2 and TL[i] == 2 else TO[
                i - 1]))  # =IF(AND(TM2=1,TL3=1),TG3*(390-B3),IF(AND(TM2=2,TL3=2),TI3*(390-B3),TO2))
        TP.append(TN[i] + TO[i])  # =TN3+TO3
        TQ.append(1 if TE[i - 1] == 1 and TDA[i] == 1 else (2 if TE[i - 1] == 2 and TDB[i] == 1 else TQ[
            i - 1]))  # =IF(AND(TE2=1,TDA3=1),1,IF(AND(TE2=2,TDB3=1),2,TQ2))*
        TR.append(TE[i] - TQ[i])  # =TE3-TQ3
        TS.append(TH[i] if TR[i] == 1 else (TJ[i] if TR[i] == 2 else TS[i - 1]))  # =IF(TR3=1,TH3,IF(TR3=2,TJ3,TS2))
        TT.append(TG[i] * (stock_v - B[i]) if TR[i - 1] == 1 and TQ[i] == 1 else (
            TI[i] * (stock_v - B[i]) if TR[i - 1] == 2 and TQ[i] == 2 else TT[
                i - 1]))  # =IF(AND(TR2=1,TQ3=1),TG3*(390-B3),IF(AND(TR2=2,TQ3=2),TI3*(390-B3),TT2))
        TU.append(TS[i] + TT[i])  # =(TS3+TT3)
        TVA.append(1 if TM[i] == 0 and SXC[i] == 1 and TA[i] == 1 else 0)  # =IF(AND(TM3=0,SXC3=1,TA3=1),1,0)
        TVB.append(1 if TM[i] == 0 and SXC[i] == 2 and TA[i] == 2 else 0)  # =IF(AND(TM3=0,SXC3=2,TA3=2),1,0)
    TX = [0]
    TV = [0]
    TW = [0]
    TY = [0]
    TZ = [0]
    UA = [0]
    UB = [0]
    UC = [0]
    UD = [0]
    UE = [0]
    UF = [0]
    UG = [0]
    UH = [0]
    UI = [0]
    UJ = [0]
    UK = [0]
    UL = [0]
    UM = [0]
    UN = [0]
    for i in range(1, len(E)):
        TX.append(1 if TM[i] == 0 and TVA[i - 1] == 0 and TVA[i] == 1 else (
            2 if TM[i] == 0 and TVB[i - 1] == 0 and TVB[i] == 1 else TX[i - 1]))
        # =IF(AND(TM3=0,TVA2=0,TVA3=1),1,IF(AND(TM3=0,TVB2=0,TVB3=1),2,TX2))
        TV.append(1 if TX[i - 1] == 1 and TA[i] == 1 and SX[i] == 2 else 0)  # =IF(AND(TX2=1,TA3=1,SX3=2),1,0)
        TW.append(1 if TX[i - 1] == 2 and TA[i] == 2 and SW[i] == 1 else 0)  # =IF(AND(TX2=2,TA3=2,SW3=1),1,0)
        TY.append(C[i] if TX[i - 1] == 0 and TX[i] == 1 else (C[i] if TX[i - 1] == 0 and TX[i] == 2 else TY[
            i - 1]))  # =IF(AND(TX2=0,TX3=1),C3,IF(AND(TX2=0,TX3=2),C3,TY2))
        TZ.append(C[i] - TY[i] if TX[i] == 1 else 0)  # =IF(TX3=1,C3-TY3,0)
        UA.append(sum(TZ[:i+1:]))  # =SUM($TZ$3:TZ3)
        UB.append(TY[i] - C[i] if TX[i] == 2 else 0)  # =IF(TX3=2,TY3-C3,0)
        UC.append(sum(UB[:i+1:]))  # =SUM($UB$3:UB3)
        UD.append(UA[i] if TX[i] == 1 else (UC[i] if TX[i] == 2 else 0))  # =IF(TX3=1,UA3,IF(TX3=2,UC3,0))
        UE.append(1 if TX[i - 1] == 1 and TV[i] == 1 else (2 if TX[i - 1] == 2 and TW[i] == 1 else (
            1 if TX[i - 1] == 1 and B[i] > 60 and UI[i - 1] <= 0 else (
                2 if TX[i - 1] == 2 and B[i] > 60 and UI[i - 1] <= 0 else UE[i - 1]))))
        # =IF(AND(TX2=1,TV3=1),1,IF(AND(TX2=2,TW3=1),2,IF(AND(TX2=1,B3>60,UI2<0),1,IF(AND(TX2=2,B3>60,UI2<0),2,UE2))))
        UF.append(TX[i] - UE[i])  # =TX3-UE3
        UG.append(UD[i] if UF[i] == 1 else UD[i] if UF[i] == 2 else UG[i - 1])  # =IF(UF3=1,UD3,IF(UF3=2,UD3,UG2))
        UH.append(TZ[i] * (stock_v - B[i]) if UF[i - 1] == 1 and UE[i] == 1 else (
            UB[i] * (stock_v - B[i]) if UF[i - 1] == 2 and UE[i] == 2 else UH[
                i - 1]))  # =IF(AND(UF2=1,UE3=1),TZ3*(390-B3),IF(AND(UF2=2,UE3=2),UB3*(390-B3),UH2))
        UI.append(UG[i] + UH[i])  # =UG3+UH3
        UJ.append(1 if TX[i] == 1 and TV[i] == 1 else (
            2 if TX[i] == 2 and TW[i] == 1 else UJ[i - 1]))  # =IF(AND(TX3=1,TV3=1),1,IF(AND(TX3=2,TW3=1),2,UJ2))
        UK.append(TX[i] - UJ[i])  # =TX3-UJ3
        UL.append(UD[i] if UK[i] == 1 else (UD[i] if UK[i] == 2 else UL[i - 1]))  # =IF(UK3=1,UD3,IF(UK3=2,UD3,UL2))
        UM.append(TZ[i] * (stock_v - B[i]) if UK[i - 1] == 1 and UJ[i] == 1 else (
            UB[i] * (stock_v - B[i]) if UK[i - 1] == 2 and UJ[i] == 2 else UM[
                i - 1]))  # IF(AND(UK2=1,UJ3=1),TZ3*(390-B3),IF(AND(UK2=2,UJ3=2),UB3*(390-B3),UM2))
        UN.append(UL[i] + UM[i])  # =UL3+UM3

    #仿生半球入场
    QW = [0]
    QX = [0]
    QY = [0]
    QZ = [0]
    RA = [0]
    RB = [0]
    RC = [0]
    RD = [0]
    RE = [0]
    RF = [0]
    RG = [0]
    RH = [0]
    RI = [0]
    RJ = [0]
    RK = [0]
    RL = [0]
    RM = [0]
    for i in range(1,len(E)):
        QW.append(1 if OU[i - 1] == 0 and OU[i] > 0 else (
            2 if OV[i - 1] == 0 and OV[i] > 0 else QW[i - 1]))  # =IF(AND(OU2=0,OU3>0),1,IF(AND(OV2=0,OV3>0),2,QW2))
        QX.append(OR[i] if QW[i] == 1 else (OR[i] if QW[i] == 2 else QX[i-1]))#=IF(QW3=1,OR3,IF(QW3=2,OR3,QX2))
        QY.append(C[i] - QX[i] if QW[i] == 1 else 0)#=IF(QW3=1,C3-QX3,0)
        QZ.append(sum(QY[:i+1:]))#=SUM($QY$3:QY3)
        RA.append(QX[i] - C[i] if QW[i] == 2 else 0)#=IF(QW3=2,QX3-C3,0)
        RB.append(sum(RA[:i+1:]))#=SUM($RA$3:RA3)
        RC.append(QY[i] if QW[i] == 1 else (RA[i] if QW[i] == 2 else 0))#=IF(QW3=1,QY3,IF(QW3=2,RA3,0))
        RD.append(1 if QW[i - 1] == 1 and QI[i] < 0 and QJ[i] < 0 else (
            2 if QW[i - 1] == 2 and QM[i] > 0 and QN[i] > 0 else (2 if QW[i - 1] == 2 and QJ[i] > 0 else (
                1 if QW[i - 1] == 1 and QN[i] < 0 else (1 if QW[i] == 1 and B[i] > 60 and RH[i - 1] < 0 else (
                    2 if QW[i - 1] == 2 and B[i] > 60 and RH[i - 1] < 0 else RD[i - 1]))))))
        # =IF(AND(QW2=1,QI3<0,QJ3<0),1,IF(AND(QW2=2,QM3>0,QN3>0),2,IF(AND(QW2=2,QJ3>0),2,IF(AND(QW2=1,QN3<0),1,IF(AND(QW2=1,B3>60,RH2<0),1,IF(AND(QW2=2,B3>60,RH2<0),2,RD2))))))
        RE.append(QW[i] - RD[i])#=QW3-RD3
        RF.append(QZ[i] if RE[i] == 1 else (RB[i] if RE[i] == 2 else RF[i-1]))#=IF(RE3=1,QZ3,IF(RE3=2,RB3,RF2))
        RG.append(QY[i]*(stock_v-B[i]) if RE[i-1] == 1 and RD[i] == 1 else (RA[i]*(stock_v-B[i]) if RE[i-1] == 2 and RD[i] == 2 else RG[i-1]))#=IF(AND(RE2=1,RD3=1),QY3*(390-B3),IF(AND(RE2=2,RD3=2),RA3*(390-B3),RG2))
        RH.append(RF[i] + RG[i])#=RF3+RG3
        RI.append(1 if QW[i] == 1 and QI[i] < 0 and QJ[i] < 0 else (2 if QW[i] == 2 and QM[i] > 0 and QN[i] > 0 else (
            2 if QW[i] == 2 and QJ[i] > 0 else (1 if QW[i] == 1 and QN[i] < 0 else RI[i - 1]))))
        # =IF(AND(QW3=1,QI3<0,QJ3<0),1,IF(AND(QW3=2,QM3>0,QN3>0),2,IF(AND(QW3=2,QJ3>0),2,IF(AND(QW3=1,QN3<0),1,RI2))))
        RJ.append(QW[i] - RI[i])#=QW3-RI3
        RK.append(QZ[i] if RJ[i] == 1 else (RB[i] if RJ[i] == 2 else RK[i-1]))#=IF(RJ3=1,QZ3,IF(RJ3=2,RB3,RK2))
        RL.append(QY[i]*(stock_v-B[i]) if RJ[i-1] == 1 and RI[i] == 1 else (RA[i]*(stock_v-B[i]) if RJ[i-1] == 2 and RI[i] == 2 else RL[i-1]))#=IF(AND(RJ2=1,RI3=1),QY3*(390-B3),IF(AND(RJ2=2,RI3=2),RA3*(390-B3),RL2))
        RM.append(RK[i] + RL[i])#=(RK3+RL3)
    RN = [0]
    RNA = [0]
    RO = [0]
    RP = [0]
    RQ = [0]
    RR = [0]
    RS = [0]
    RT = [0]
    RU = [0]
    RV = [0]
    RW = [0]
    RX = [0]
    RY = [0]
    RZ = [0]
    SA = [0]
    SB = [0]
    SC = [0]
    SD = [0]
    for i in range(1,len(E)):
        RN.append(1 if RE[i] == 0 and TA[i] == 1 else (2 if RE[i] == 0 and TA[i] == 2 else RN[i-1]))
        #=IF(AND(RE3=0,TA3=1),1,IF(AND(RE3=0,TA3=2),2,RN2))
        RNA.append(1 if RN[i-1] == 0 and RN[i] == 1 else (2 if RN[i-1] == 0 and RN[i] == 2 else RNA[i-1]))#=IF(AND(RN2=0,RN3=1),1,IF(AND(RN2=0,RN3=2),2,RNA2))
        RO.append(C[i] if RNA[i-1] == 0 and RNA[i] == 1 else (C[i] if RNA[i-1] == 0 and RNA[i] == 2 else RO[i-1]))#=IF(AND(RN2=0,RN3=1),C3,IF(AND(RN2=0,RN3=2),C3,RO2))
        RP.append(C[i] - RO[i] if RNA[i] == 1 else 0)#=IF(RN3=1,C3-RO3,0)
        RQ.append(sum(RP[:i+1:]))#=SUM($RP$3:RP3)
        RR.append(RO[i] - C[i] if RNA[i] == 2 else 0)#=IF(RN3=2,RO3-C3,0)
        RS.append(sum(RR[:i+1:]))#=SUM($RR$3:RR3)
        RT.append(RQ[i] if RNA[i] == 1 else (RS[i] if RNA[i] == 2 else 0))#=IF(RN3=1,RQ3,IF(RN3=2,RS3,0))
        RU.append(1 if RNA[i - 1] == 1 and QI[i] < 0 and QJ[i] < 0 else (
            2 if RNA[i - 1] == 2 and QM[i] > 0 and QN[i] > 0 else (
                1 if RNA[i - 1] == 1 and B[i] > 60 and RY[i - 1] <= 0 else (
                    2 if RNA[i - 1] == 2 and B[i] > 60 and RY[i - 1] <= 0 else RU[i - 1]))))
        # =IF(AND(RN2=1,QI3<0,QJ3<0),1,IF(AND(RN2=2,QM3>0,QN3>0),2,IF(AND(RN2=1,B3>60,RY2<=0),1,IF(AND(RN2=2,B3>60,RY2<=0),2,RU2))))
        RV.append(RNA[i] - RU[i])#=RN3-RU3
        RW.append(RT[i] if RV[i] == 1 else (RT[i] if RV[i] == 2 else RW[i-1]))#=IF(RV3=1,RT3,IF(RV3=2,RT3,RW2))
        RX.append(RP[i]*(stock_v-B[i]) if RV[i-1] == 1 and RU[i] == 1 else (RR[i] *(stock_v-B[i]) if RV[i-1] == 2 and RU[i] == 2 else RX[i-1]))#=IF(AND(RV2=1,RU3=1),RP3*(390-B3),IF(AND(RV2=2,RU3=2),RR3*(390-B3),RX2))
        RY.append(RW[i] + RX[i])#=RW3+RX3
        RZ.append(1 if RNA[i] == 1 and QI[i] < 0 and QJ[i] < 0 else (2 if RNA[i] == 2 and QM[i] > 0 and QN[i] > 0 else RZ[
            i - 1]))  # =IF(AND(RN3=1,QI3<0,QJ3<0),1,IF(AND(RN3=2,QM3>0,QN3>0),2,RZ2))
        SA.append(RNA[i] - RZ[i])#=RN3-RZ3
        SB.append(RT[i] if SA[i] == 1 else (RT[i] if SA[i] == 2 else SB[i-1]))#=IF(SA3=1,RT3,IF(SA3=2,RT3,SB2))
        SC.append(RP[i]*(stock_v-B[i]) if SA[i-1] == 1 and RZ[i] == 1 else (RR[i]*(stock_v-B[i]) if SA[i-1] == 2 and RZ[i] == 2 else SC[i-1]))#=IF(AND(SA2=1,RZ3=1),RP3*(390-B3),IF(AND(SA2=2,RZ3=2),RR3*(390-B3),SC2))
        SD.append(SB[i] + SC[i])#=SB3+SC3
    SE = [0]
    for i in range(1,len(E)):
        SE.append(1 if RE[i-1] == 1 and RD[i] == 1 and RH[i-1] <= 0 and B[i] > 60 else (1 if RE[i-1] == 2 and RD[i] == 2 and RH[i-1] <= 0 and B[i] > 60 else SE[i-1]))
        #=IF(AND(RE2=1,RD3=1,RH2<=0,B3>60),1,IF(AND(RE2=2,RD3=2,RH2<=0,B3>60),1,SE2))
    SF = ["BUY" if QW[i-1] == 0 and QW[i] == 1 else ("SELL" if QW[i-1] == 0 and QW[i] == 2 else 0) for i in range(len(E))]#=IF(AND(QW2=0,QW3=1),"BUY",IF(AND(QW2=0,QW3=2),"SELL",0))
    SG = ["BUY" if RN[i-1] == 0 and RN[i] == 1 else ("SELL" if RN[i-1] == 0 and RN[i] == 2 else (0 if SE[i] == 1 else 0)) for i in range(len(E))]#=IF(AND(RN2=0,RN3=1),"BUY",IF(AND(RN2=0,RN3=2),"SELL",IF(SE3=1,0,0)))

    SH = [0] + [RH[i] if SE[i] == 1 else RH[i] + RY[i] for i in range(1,len(E))]#=IF(SE3=1,RH3,RH3+RY3)
    SI = [0] + [RM[i] + SD[i] for i in range(1,len(E))]#=RM3+SD3
    SJ = QX#=VALUE(QX3)
    SK = [0] + [SH[i] - SH[i-1] for i in range(1,len(E))]#=SH3-SH2
    SL = [0] + [SI[i] - SI[i-1] for i in range(1,len(E))]#=SI3-SI2
    SM = [0] + [0 if SJ[i] == 0 else SK[i]/SJ[i] for i in range(1,len(E))]#=IF(SJ3=0,0,SK3/SJ3)
    SN = [0] + [0 if SJ[i] == 0 else SL[i]/SJ[i] for i in range(1,len(E))]#=IF(SJ3=0,0,SL3/SJ3)
    SO = [0] + [1 if SM[i] > 0.01 else 0 for i in range(1,len(E))]#=IF(SM3>1%,1,0)
    SP = [0] + [1 if SN[i] > 0.01 else 0 for i in range(1,len(E))]#=IF(SN3>1%,1,0)
    SQ = [0] + [SO[:i+1:].count(1) for i in range(1,len(E))]#=COUNTIF($SO$3:SO3,1)
    SR = [0] + [SP[:i+1:].count(1) for i in range(1,len(E))]#=COUNTIF($SP$3:SP3,1)
    SS = [0] + [SQ[i]/B[i] for i in range(1,len(E))]#=SQ4/B4
    ST = [0] + [SR[i]/B[i] for i in range(1,len(E))]#=SR4/B4
    SU = [0]
    SV = [0]
    for i in range(1,len(E)):
        SU.append(1 if SJ[i-2] == 0 and SJ[i-1] > 0 and SS[i-1] > 0 and SS[i] > SS[i-1] else SU[i-1])#=IF(AND(SJ2=0,SJ3>0,SS3>0,SS4>SS3),1,SU3)
        SV.append(1 if SJ[i-2] == 0 and SJ[i-1] > 0 and ST[i-1] > 0 and ST[i] > ST[i-1] else SV[i-1])#=IF(AND(SJ2=0,SJ3>0,ST3>0,ST4>ST3),1,SV3)

    UO = [0]
    for i in range(1,len(E)):
        UO.append(1 if TM[i-1] == 1 and TL[i] == 1 and B[i] > 60 and TP[i-1] <= 0 else (1 if TM[i-1] == 2 and TL[i] == 2 and B[i] > 60 and TP[i-1] <= 0 else UO[i-1]))
        #=IF(AND(TM2=1,TL3=1,TP2<=0,B3>60),1,IF(AND(TM2=2,TL3=2,TP2<=0,B3>60),1,UO2))
    UP = ["BUY" if TE[i-1] == 0 and TE[i] > 0 else ("SELL" if TE[i-1] == 0 and TE[i] == 2 else 0) for i in range(len(E))]#=IF(AND(TE2=0,TE3=1),"BUY",IF(AND(TE2=0,TE3=2),"SELL",0))
    UQ = ["BUY" if TX[i-1] == 0 and TX[i] == 1 else ("SELL" if TX[i-1] == 0 and TX[i] == 2 else (0 if UO[i] == 0 else 0)) for i in range(len(E))]#=IF(AND(TX2=0,TX3=1),"BUY",IF(AND(TX2=0,TX3=2),"SELL",IF(UO3=1,0,0)))

    UR = [0] + [TP[i] if UO[i] == 1 else UI[i] + TP[i] for i in range(1,len(E))]#=IF(UO3=1,TP3,UI3+TP3)
    US = [0] + [TU[i] + UN[i] for i in range(1,len(E))]#TU3+UN3
    UT = [0] + [1 if TR[i] == 1 else (2 if TR[i] == 2 else (1 if UK[i] == 1 else (2 if UK[i] == 2 else 0))) for i in range(1,len(E))]#=IF(TR3=1,1,IF(TR3=2,2,IF(UK3=1,1,IF(UK3=2,2,0))))
    UU = [0] + [1 if RJ[i] == 1 else (2 if RJ[i] == 2 else (1 if SA[i] == 1 else (2 if SA[i] == 2 else 0))) for i in range(1,len(E))]#=IF(RJ3=1,1,IF(RJ3=2,2,IF(SA3=1,1,IF(SA3=2,2,0))))
    UV = TF#VALUE(TF3)
    UW = [0] + [UR[i] - UR[i-1] for i in range(1,len(E))]#=UR3-UR2
    UX = [0] + [US[i] - US[i-1] for i in range(1,len(E))]#=US3-US2
    UY = [0] + [0 if UV[i] == 0 else UW[i]/UV[i] for i in range(1,len(E))]#=IF(UV3=0,0,UW3/UV3)
    UZ = [0] + [0 if UV[i] == 0 else UX[i]/UV[i] for i in range(1,len(E))]#=IF(UV3=0,0,UX3/UV3)
    VA = [0] + [1 if UY[i] > 0.01 else 0 for i in range(1,len(E))]#=IF(UY3>1%,1,0)
    VB = [0] + [1 if UZ[i] > 0.01 else 0 for i in range(1,len(E))]#=IF(UZ3>1%,1,0)
    VC = [0] + [VA[:i+1:].count(1) for i in range(1,len(E))]#=COUNTIF($VA$3:VA3,1)
    VD = [0] + [VB[:i+1:].count(1) for i in range(1,len(E))]#=COUNTIF($VB$3:VB3,1)
    VE = [0] + [VC[i]/B[i] for i in range(1,len(E))]#=VC3/B3
    VF = [0] + [VD[i]/B[i] for i in range(1,len(E))]#=VD3/B3
    VG = [0]
    VH = [0]
    for i in range(1,len(E)):
        VG.append(1 if UV[i-2] == 0 and UV[i-1] > 0 and VE[i-1] > 0 and VE[i] > VE[i-1] else VG[i-1])#=IF(AND(UV2=0,UV3>0,VE3>0,VE4>VE3),1,VG3)
        VH.append(1 if UV[i-2] == 0 and UV[i-1] > 0 and VF[i-1] > 0 and VF[i] > VF[i-1] else VH[i-1])#=IF(AND(UV2=0,UV3>0,VF3>0,VF4>VF3),1,VH3)
    VI = [0]
    VJ = [0]
    for i in range(1,len(E)):
        VI.append(1 if HX[i] >= SI[i] else (2 if SI[i] >= HX[i] else VI[i-1]))#=IF(HX3>=SI3,1,IF(SI3>=HX3,2,VI2))
        VJ.append(VI[i] if VI[i-1] == 0 and VI[i] > 0 else VJ[i-1])#=IF(AND(VI2=0,VI3>0),VI3,VJ2)
    VK = KH
    VL = US
    VM = [0] + [HC[i] if VJ[i] == 1 else (SI[i] if VJ[i] == 2 else 0) for i in range(1,len(E))]#=IF(VJ3=1,HX3,IF(VJ3=2,SI3,0))
    VN = [0] + [VK[i] + VL[i] +VM[i] for i in range(1,len(E))]#VK3+VL3+VM3
    VO = KI
    VP = UT
    VQ = [0] + [KJ[i] if VJ[i] == 1 else (UU[i] if VJ[i] == 2 else 0) for i in range(1,len(E))]#=IF(VJ3=1,KJ3,IF(VJ3=2,UU3,0))
    VR = [0] + [0 if VO[i] == 1 and VP[i] == 2 else (0 if VO[i] == 2 and VP[i] == 1 else (1 if VO[i] == 1 and VP[i] == 0 else (2 if VO[i] == 2 and VP[i] == 0 else (1 if VO[i] == 0 and VP[i] == 1 else (2 if VO[i] == 0 and VP[i] == 2 else (1 if VO[i] == 1 and VP[i] == 1 else (2 if VO[i] == 2 and VP[i] == 2 else 0))))))) for i in range(1,len(E))]
    #=IF(AND(VO3=1,VP3=2),0,IF(AND(VO3=2,VP3=1),0,IF(AND(VO3=1,VP3=0),1,IF(AND(VO3=2,VP3=0),2,IF(AND(VO3=0,VP3=1),1,IF(AND(VO3=0,VP3=2),2,IF(AND(VO3=1,VP3=1),1,IF(AND(VO3=2,VP3=2),2,0))))))))
    VS = [0] + [0 if VO[i] == 1 and VQ[i] == 2 else (0 if VO[i] == 2 and VQ[i] == 1 else (1 if VO[i] == 1 and VQ[i] == 0 else (2 if VO[i] == 2 and VQ[i] == 0 else (1 if VO[i] == 0 and VQ[i] == 1 else (2 if VO[i] == 0 and VQ[i] == 2 else (1 if VO[i] == 1 and VQ[i] == 1 else (2 if VO[i] == 2 and VQ[i] == 2 else 0))))))) for i in range(1,len(E))]
    #=IF(AND(VO3=1,VQ3=2),0,IF(AND(VO3=2,VQ3=1),0,IF(AND(VO3=1,VQ3=0),1,IF(AND(VO3=2,VQ3=0),2,IF(AND(VO3=0,VQ3=1),1,IF(AND(VO3=0,VQ3=2),2,IF(AND(VO3=1,VQ3=1),1,IF(AND(VO3=2,VQ3=2),2,0))))))))
    VT = [0] + [1 if VQ[i] == 0 and VR[i] == 1 else (1 if VQ[i] == 1 and VR[i] == 0 else (1 if VQ[i] == 1 and VR[i] == 1 else (2 if VQ[i] == 0 and VR[i] == 2 else (2 if VQ[i] == 2 and VR[i] == 0 else (2 if VQ[i] == 2 and VR[i] == 2 else 0))))) for i in range(1,len(E))]
    #=IF(AND(VQ3=0,VR3=1),1,IF(AND(VQ3=1,VR3=0),1,IF(AND(VQ3=1,VR3=1),1,IF(AND(VQ3=0,VR3=2),2,IF(AND(VQ3=2,VR3=0),2,IF(AND(VQ3=2,VR3=2),2,0))))))
    VUA = [0] + [VR[:i+1:].count(1) + VS[:i+1:].count(1) + VT[:i+1:].count(1) for i in range(1,len(E))]#=COUNTIF(VR3:VT3,1)
    VVA = [0] + [VR[:i+1:].count(2) + VS[:i+1:].count(2) + VT[:i+1:].count(2) for i in range(1,len(E))]#=COUNTIF(VR3:VT3,2)
    VU = [0]
    VV = [0]
    for i in range(1,len(E)):
        VU.append(VUA[i] - VUA[i-1])
        VV.append(VVA[i] - VVA[i-1])
    VWA = [0] + [1 if VU[i] - VV[i] > 0 else (2 if VV[i] - VU[i] > 0 else 0) for i in range(1,len(E))]#=IF(VU3-VV3>0,1,IF(VV3-VU3>0,2,0))
    VW = [0] + [0 if VWA[i] == 1 and SXC[i] == 1 and TA[i] == 1 else (0 if VWA[i] == 1 and IMC[i] == 1 and IP[i] == 1 else (0 if VWA[i] == 2 and SXC[i] == 2 and TA[i] == 2 else (0 if VWA[i] == 2 and IMC[i] == 2 and IP[i] == 2 else VWA[i]))) for i in range(1,len(E))]
    #=IF(AND(VWA3=1,SXC3=1,TA3=1),0,IF(AND(VWA3=1,IMC3=1,IP3=1),0,IF(AND(VWA3=2,SXC3=2,TA3=2),0,IF(AND(VWA3=2,IMC3=2,IP3=2),0,VWA3))))
    VX = [0] + [VO[:i+1:].count(1) + VP[:i+1:].count(1) + VQ[:i+1:].count(1) for i in range(1,len(E))]#=COUNTIF(VO3:VQ3,1)
    VY = [0] + [VO[:i+1:].count(2) + VP[:i+1:].count(2) + VQ[:i+1:].count(2) for i in range(1,len(E))]#=COUNTIF(VO3:VQ3,2)
    VZ = [0] + [VX[i] if VW[i] == 1 else (VY[i] if VW[i] == 2 else 0) for i in range(1,len(E))]#=IF(VW3=1,VX3,IF(VW3=2,VY3,0))
    WA = [0] + [stock_v - B[i] for i in range(1,len(E))]#=390-B3
    WB = [0] + [WA[i] if VZ[i] == 0 else VZ[i]*WA[i] for i in range(1,len(E))]#=IF(VZ3=0,WA3,VZ3*WA3)
    WC = C
    WD = [0]
    WE = [0]
    WF = [0]
    WG = [0]
    WH = [0]
    WI = [0]
    WJ = [0]
    WK = [0]
    WL = [0]
    WM = [0]
    WN = [0]
    WO = [0]
    WP = [0]
    WQ = [0]
    WR = [0]
    WS = [0]
    WT = [0]
    WU = [0]
    WV = [0]
    WW = [0]
    WX = [0]
    WY = [0]
    for i in range(1,len(E)):
       WD.append(2 if B[i] > 5 and VN[i] < 0 and VW[i-1] == 0 and VW[i] == 1 else (2 if B[i] > 5 and VN[i] < 0 and VW[i-1] == 2 and VW[i] == 1 else (2 if B[i] > 5 and VN[i] < 0 and VW[i] == 1 else WD[i-1])))
       #=IF(AND(B3>5,VN3<0,VW2=0,VW3=1),2,IF(AND(B3>5,VN3<0,VW2=2,VW3=1),2,IF(AND(B3>5,VN3<0,VW3=1),2,WD2)))
       WE.append(WB[i] if WD[i-1] == 0 and WD[i] == 2 else WE[i-1])#=IF(AND(WD2=0,WD3=2),WB3,WE2)
       WF.append(C[i] if WD[i-1] == 0 and WD[i] == 2 else WF[i-1])#=IF(AND(WD2=0,WD3=2),C3,WF2)
       WG.append(1 if VZ[i] == 0 else (VZ[i] if VZ[i] > 0 else WG[i-1]))#=IF(VZ3=0,1,IF(VZ3>0,VZ3,WG2))
       WH.append((WF[i] - C[i])*WG[i] if WD[i] == 2 else 0)#=IF(WD3=2,(WF3-C3)*WG3,0)
       WI.append(2 if WD[i-1] == 2 and VW[i-1] == 1 and VW[i] == 0 else (2 if WD[i-1] == 2 and VW[i-1] == 1 and VW[i] == 2 else (2 if WD[i-1] == 2 and WH[i] > 0 else WI[i-1])))
       #=IF(AND(WD2=2,VW2=1,VW3=0),2,IF(AND(WD2=2,VW2=1,VW3=2),2,IF(AND(WD2=2,WH3>0),2,WI2)))
       WJ.append(WD[i] - WI[i])#=WD3-WI3
       WK.append((WF[i] - C[i])*WE[i] if WJ[i-1] == 2 and WI[i] == 2 else WK[i-1])#=IF(AND(WJ2=2,WI3=2),(WF3-C3)*WE3,WK2)
       WL.append(WH[i] if WJ[i] == 2 else (WH[i] if WJ[i-1] == 2 and WI[i] == 2 else WL[i-1]))#=IF(WJ3=2,WH3,IF(AND(WJ2=2,WI3=2),WH3,WL2))
       WM.append(sum(WL[:i+1:]) if WJ[i] == 2 else WM[i-1])#=IF(WJ3=2,SUM($WL$3:WL3),WM2)
       WN.append(WK[i] + WM[i])#=WK3+WM3
       WO.append(2 if B[i] > 5 and VN[i] < 0 and WJ[i] == 0 and VW[i-1] == 0 and VW[i] == 1 else (2 if B[i] > 5 and VN[i] < 0 and WJ[i] == 0 and VW[i-1] == 2 and VW[i] == 1 else WO[i-1]))
       #=IF(AND(B3>5,VN3<0,WJ3=0,VW2=0,VW3=1),2,IF(AND(B3>5,VN3<0,WJ3=0,VW2=2,VW3=1),2,WO2))
       WP.append(WB[i] if WO[i-1] == 0 and WO[i] == 2 else WP[i-1])#=IF(AND(WO2=0,WO3=2),WB3,WP2)
       WQ.append(C[i] if WO[i-1] == 0 and WO[i] == 2 else WQ[i-1])#=IF(AND(WO2=0,WO3=2),C3,WQ2)
       WR.append(1 if VZ[i] == 0 else (VZ[i] if VZ[i] > 0 else WR[i-1]))#=IF(VZ3=0,1,IF(VZ3>0,VZ3,WR2))
       WS.append((WQ[i] - C[i])*WR[i] if WO[i] == 2 else 0)#=IF(WO3=2,(WQ3-C3)*WR3,0)
       WT.append(2 if WO[i-1] == 2 and VW[i-1] == 1 and VW[i] == 0 else (2 if WO[i-1] == 2 and VW[i-1] == 1 and VW[i] == 2 else (2 if WO[i-1] == 2 and WS[i] > 0 else WT[i-1])))
       #=IF(AND(WO2=2,VW2=1,VW3=0),2,IF(AND(WO2=2,VW2=1,VW3=2),2,IF(AND(WO2=2,WS3>0),2,WT2)))
       WU.append(WO[i] - WT[i])#=WO3-WT3
       WV.append((WQ[i] - C[i])*WP[i] if WU[i-1] == 2 and WT[i] == 2 else MV[i-1])#=IF(AND(WU2=2,WT3=2),(WQ3-C3)*WP3,WV2)
       WW.append(WS[i] if WU[i] == 2 else (WS[i] if WU[i-1] == 2 and WT[i] == 2 else WW[i-1]))#=IF(WU3=2,WS3,IF(AND(WU2=2,WT3=2),WS3,WW2))
       WX.append(sum(WW[:i+1:]) if WU[i] == 2 else WX[i-1])#=IF(WU3=2,SUM($WW$3:WW3),WX2)
       WY.append(WV[i] + WX[i])#=WV3+WX3
    WZ = [0]
    XA = [0]
    XB = [0]
    XC = [0]
    XD = [0]
    XE = [0]
    XF = [0]
    XG = [0]
    XH = [0]
    XI = [0]
    XJ = [0]
    XK = [0]
    XL = [0]
    XM = [0]
    XN = [0]
    XO = [0]
    XP = [0]
    XQ = [0]
    XR = [0]
    XS = [0]
    XT = [0]
    XU = [0]
    for i in range(1,len(E)):
        WZ.append(1 if B[i] > 5 and VN[i] < 0 and VW[i-1] == 0 and VW[i] == 2 else (1 if B[i] > 5 and VN[i] < 0 and VW[i-1] == 1 and VW[i] == 2 else (1 if B[i] > 5 and VN[i] < 0 and VW[i] == 2 else WZ[i-1])))
        #=IF(AND(B3>5,VN3<0,VW2=0,VW3=2),1,IF(AND(B3>5,VN3<0,VW2=1,VW3=2),1,IF(AND(B3>5,VN3<0,VW3=2),1,WZ2)))
        XA.append(WB[i] if WZ[i-1] == 0 and WZ[i] == 1 else XA[i-1])#=IF(AND(WZ2=0,WZ3=1),WB3,XA2)
        XB.append(C[i] if WZ[i-1] == 0 and WZ[i] == 1 else XB[i-1])#=IF(AND(WZ2=0,WZ3=1),C3,XB2)
        XC.append(1 if VZ[i] == 0 else (VZ[i] if VZ[i] > 0 else XC[i-1]))#=IF(VZ3=0,1,IF(VZ3>0,VZ3,XC2))
        XD.append((C[i] - XB[i])*XC[i] if WZ[i] == 1 else 0)#=IF(WZ3=1,(C3-XB3)*XC3,0)
        XE.append(1 if WZ[i-1] == 1 and VW[i-1] == 2 and VW[i] == 0 else (1 if WZ[i-1] == 1 and VW[i-1] == 2 and VW[i] == 1 else (1 if WZ[i-1] == 1 and XD[i] > 0 else XE[i-1])))
        #=IF(AND(WZ2=1,VW2=2,VW3=0),1,IF(AND(WZ2=1,VW2=2,VW3=1),1,IF(AND(WZ2=1,XD3>0),1,XE2)))
        XF.append(WZ[i] - XE[i])#=WZ3-XE3
        XG.append((C[i] - XB[i])*XA[i] if XF[i-1] == 1 and XE[i] == 1 else XG[i-1])#=IF(AND(XF2=1,XE3=1),(C3-XB3)*XA3,XG2)
        XH.append(XD[i] if XF[i] == 1 else (XD[i] if XF[i-1] == 1 and XE[i] == 1 else XH[i-1]))#=IF(XF3=1,XD3,IF(AND(XF2=1,XE3=1),XD3,XH2))
        XI.append(sum(XH[:i+1:]) if XF[i] == 1 else XI[i-1])#=IF(XF3=1,SUM($XH$2:XH3),XI2)
        XJ.append(XG[i] + XI[i])#=XG3+XI3
        XK.append(1 if B[i] > 5 and VN[i] < 0 and XF[i] == 0 and VW[i-1] == 0 and VW[i] == 2 else (1 if B[i] > 5 and VN[i] < 0 and XF[i] == 0 and VW[i-1] == 1 and VW[i] == 2 else (1 if B[i] > 5 and VN[i] < 0 and XF[i] == 0 and VW[i] == 2 else XK[i-1])))
        #=IF(AND(B3>5,VN3<0,XF3=0,VW2=0,VW3=2),1,IF(AND(B3>5,VN3<0,XF3=0,VW2=1,VW3=2),1,IF(AND(B3>5,VN3<0,XF3=0,VW3=2),1,XK2)))
        XL.append(WB[i] if XK[i-1] == 0 and XK[i] == 1 else XL[i-1])#=IF(AND(XK2=0,XK3=1),WB3,XL2)
        XM.append(C[i] if XK[i-1] == 0 and XK[i] == 1 else XM[i-1])#=IF(AND(XK2=0,XK3=1),C3,XM2)
        XN.append(1 if VZ[i] == 0 else (VZ[i] if VZ[i] > 0 else XN[i-1]))#=IF(VZ3=0,1,IF(VZ3>0,VZ3,XN2))
        XO.append((C[i] - XM[i])*XN[i] if XK[i] == 1 else 0)#=IF(XK3=1,(C3-XM3)*XN3,0)
        XP.append(1 if XK[i-1] == 1 and VW[i-1] == 2 and VW[i] == 0 else (1 if XK[i-1] == 1 and VW[i-1] == 2 and VW[i] == 1 else (1 if XK[i-1] == 1 and XO[i] > 0 else XP[i-1])))
        #=IF(AND(XK2=1,VW2=2,VW3=0),1,IF(AND(XK2=1,VW2=2,VW3=1),1,IF(AND(XK2=1,XO3>0),1,XP2)))
        XQ.append(XK[i] - XP[i])#=XK3-XP3
        XR.append((C[i] - XM[i])*XL[i] if XQ[i-1] == 1 and XP[i] == 1 else XR[i-1])#=IF(AND(XQ2=1,XP3=1),(C3-XM3)*XL3,XR2)
        XS.append(XO[i] if XQ[i] == 1 else (XO[i] if XQ[i-1] == 1 and XP[i] == 1 else XS[i-1]))#=IF(XQ3=1,XO3,IF(AND(XQ2=1,XP3=1),XO3,XS2))
        XT.append(sum(XS[:i+1:]) if XQ[i] == 1 else XT[i-1])#=IF(XQ3=1,SUM($XS$3:XS3),XT2)
        XU.append(XR[i] + XT[i])#=XR3+XT3
    XV = [0] + [WN[i] + WY[i] + XJ[i] + XU[i] for i in range(1,len(E))]#=WN3+WY3+XJ3+XU3
    XW = [0] + [XV[i] + UR[i] + SH[i] + KG[i] + HW[i] for i in range(1,len(E))]#=XV3+UR3+SH3+KG3+HW3
    XX = [0]
    XY = [0]
    for i in range(1,len(E)):
        XX.append("H-BUY" if WZ[i-1] == 0 and WZ[i] > 0 else ("H-BUY" if XK[i-1] == 0 and XK[i] > 0 else 0))#=IF(AND(WZ2=0,WZ3>0),"H-BUY",IF(AND(XK2=0,XK3>0),"H-BUY",XX2))
        XY.append("H-SELL" if WD[i-1] == 0 and WD[i] > 0 else ("H-SELL" if WO[i-1] == 0 and WO[i] > 0 else 0))#=IF(AND(WD2=0,WD3>0),"H-SELL",IF(AND(WO2=0,WO3>0),"H-SELL",XY2))

    # print(HU)
    # print(HV)
    # print(IJ)
    # print(KE)
    # print(KF)
    # print(KV)
    # print(SF)
    # print(SG)
    # print(SU)
    # print(UP)
    # print(UQ)
    # print(VG)
    # print(XX)
    # print(XY)

    return  HU,HV,IJ,KE,KF,KV,SF,SG,SU,UP,UQ,VG,XX,XY



