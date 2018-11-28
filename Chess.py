import random
import time


rad_0 = ["a", "b", "c", "d", "e", "f", "g", "h"]
rad_1 = ["8", "♖", "♘", "♗", "♕", "♔", "♗", "♘", "♖", "8"]
rad_2 = ["7", "♙", "♙", "♙", "♙", "♙", "♙", "♙", "♙", "7"]
rad_3 = ["6", " ", " ", " ", " ", " ", " ", " ", " ", "6"]
rad_4 = ["5", " ", " ", " ", " ", " ", " ", " ", " ", "5"]
rad_5 = ["4", " ", " ", " ", " ", " ", " ", " ", " ", "4"]
rad_6 = ["3", " ", " ", " ", " ", " ", " ", " ", " ", "3"]
rad_7 = ["2", "♟", "♟", "♟", "♟", "♟", "♟", "♟", "♟", "2"]
rad_8 = ["1", "♜", "♞", "♝", "♛", "♚", "♝", "♞", "♜", "1"]
rad_9 = ["a", "b", "c", "d", "e", "f", "g", "h"]

brett = (rad_0, rad_1, rad_2, rad_3, rad_4, rad_5, rad_6, rad_7, rad_8, rad_9)
brikker = {"svart": ["♙", "♖", "♘", "♗", "♕", "♔"], "hvit": ["♟", "♜", "♞", "♝", "♛", "♚"]}
hvite_offiserer = {"T": "♜", "S": "♞", "L": "♝", "D": "♛"}
svarte_offiserer = {"T": "♖", "S": "♘", "L": "♗", "D": "♕"}
konger = ["♚", "♔"]
dronninger = ["♛", "♕"]
taarn = ["♜", "♖"]
loepere_springere = ["♝", "♞", "♗", "♘"]
boender = ["♟", "♙"]
verdi = {"♟": 1, "♜": 5, "♞": 3, "♝": 3, "♛": 12, "♚": 5, "♙": 1, "♖": 5, "♘": 3, "♗": 3, "♕": 12, "♔": 5, " ": 0}
bokstaver = ("a", "b", "c", "d", "e", "f", "g", "h")
tall = ("1", "2", "3", "4", "5", "6", "7", "8")


def print_rute(linje, rad):
    if (linje + rad) % 2 == 0:
        if " " in brett[rad][linje]:
            print("███│", end="")
        else:
            print("▌" + str(brett[rad][linje]) + "▐│", end="")
    else:
        if " " in brett[rad][linje]:
            print("   │", end="")
        else:
            print(" " + str(brett[rad][linje]) + " │", end="")


def print_brett():
    print("    ", end="")
    for bokstav in rad_0:
        print(bokstav + "   ", end="")
    print("")
    for rad in range(1, 9):
        print(" ─┼───┼───┼───┼───┼───┼───┼───┼───┼─")
        print(brett[rad][0] + " │", end="")
        for linje in range(1, 9):
            print_rute(linje, rad)
        print(" " + brett[rad][9])
    print(" ─┼───┼───┼───┼───┼───┼───┼───┼───┼─")
    print("    ", end="")
    for bokstav in rad_9:
        print(bokstav + "   ", end="")
    print("")


# t = tilstand
t = {"hvitt_trekk": True, "simulasjon": False, "sjakk": False, "matt": False, "patt": False}


def hent(rl):
    return brett[rl[0]][rl[1]]


def sjekk_gyldig_rute(rute):
    rute_linje = 0
    rute_rad = 0
    if rute[0].isalpha():
        rute[0] = rute[0].lower()
        while rute_linje == 0:
            for i in range(len(bokstaver)):
                if rute[0] in bokstaver[i]:
                    rute_linje = i + 1
                    break
            if rute_linje == 0:
                print("Ugyldig input: Første tegn må være en bokstav mellom a og h).")
            break
    else:
        print("Ugyldig input: Første tegn må være en bokstav mellom a og h.")
    if rute[1].isdigit():
        while rute_rad == 0:
            for i in range(len(tall)):
                if rute[1] in tall[i]:
                    rute_rad = 9 - (i + 1)
                    break
            if rute_rad == 0:
                print("Ugyldig input: Andre tegn må være et tall mellom 1 og 8.")
            break
    else:
        print("Ugyldig input: Andre tegn må være et tall mellom 1 og 8.")
    return rute_linje, rute_rad


def fri_vertikal(fra_rl, til_rl):
    fri_bane = True
    if fra_rl[0] < til_rl[0]:
        retning = 1
    else:
        retning = - 1
    for i in range(abs(fra_rl[0] - til_rl[0]) - 1):
        if hent([fra_rl[0] + retning * (i + 1), fra_rl[1]]) != " ":
            fri_bane = False
    return fri_bane


def fri_horisontal(fra_rl, til_rl):
    fri_bane = True
    if fra_rl[1] < til_rl[1]:
        retning = 1
    else:
        retning = - 1
    for i in range(abs(fra_rl[1] - til_rl[1]) - 1):
        if hent([fra_rl[0], fra_rl[1] + retning * (i + 1)]) != " ":
            fri_bane = False
    return fri_bane


def fri_diagonal(fra_rl, til_rl):
    fri_bane = True
    retning = [0, 0]
    if fra_rl[0] < til_rl[0]:
        retning[0] = 1
    else:
        retning[0] = -1
    if fra_rl[1] < til_rl[1]:
        retning[1] = 1
    else:
        retning[1] = -1
    for i in range(abs(fra_rl[1] - til_rl[1]) - 1):
        if hent([fra_rl[0] + retning[0] * (i + 1), fra_rl[1] + retning[1] * (i + 1)]) != " ":
            fri_bane = False
    return fri_bane


def gyldig_bonde(fra_rl, til_rl):
    if t["hvitt_trekk"]:
        retning = -1
    else:
        retning = 1
    gyldig = False
    if fra_rl[1] == til_rl[1]:
        if fra_rl[0] + retning == til_rl[0]:
            if hent(til_rl) == " ":
                gyldig = True
        elif (fra_rl[0] + (2 * retning) == til_rl[0] and t["hvitt_trekk"] and fra_rl[0] == 7) or (fra_rl[0] + (2 * retning) == til_rl[0] and not t["hvitt_trekk"] and fra_rl[0] == 2):
            neste_steg = [fra_rl[0] + retning, fra_rl[1]]
            if hent(neste_steg) == " " and hent(til_rl) == " ":
                gyldig = True
    elif fra_rl[1] + 1 == til_rl[1] or fra_rl[1] - 1 == til_rl[1]:
        if fra_rl[0] + retning == til_rl[0] and hent(til_rl) != " ":
            gyldig = True
    return gyldig


def gyldig_taarn(fra_rl, til_rl):
    gyldig = False
    if fra_rl[0] == til_rl[0]:
        gyldig = fri_horisontal(fra_rl, til_rl)
    elif fra_rl[1] == til_rl[1]:
        gyldig = fri_vertikal(fra_rl, til_rl)
    return gyldig


def gyldig_springer(fra_rl, til_rl):
    gyldig = False
    if abs(fra_rl[0] - til_rl[0]) == 1 and abs(fra_rl[1] - til_rl[1]) == 2:
        gyldig = True
    elif abs(fra_rl[0] - til_rl[0]) == 2 and abs(fra_rl[1] - til_rl[1]) == 1:
        gyldig = True
    return gyldig


def gyldig_loeper(fra_rl, til_rl):
    gyldig = False
    if abs(fra_rl[0] - til_rl[0]) == abs(fra_rl[1] - til_rl[1]):
        gyldig = fri_diagonal(fra_rl, til_rl)
    return gyldig


def gyldig_dronning(fra_rl, til_rl):
    gyldig = False
    if fra_rl[0] == til_rl[0]:
        gyldig = fri_horisontal(fra_rl, til_rl)
    elif fra_rl[1] == til_rl[1]:
        gyldig = fri_vertikal(fra_rl, til_rl)
    elif abs(fra_rl[0] - til_rl[0]) == abs(fra_rl[1] - til_rl[1]):
        gyldig = fri_diagonal(fra_rl, til_rl)
    return gyldig


def gyldig_konge(fra_rl, til_rl):
    gyldig = False
    if abs(fra_rl[0] - til_rl[0]) <= 1 and abs(fra_rl[1] - til_rl[1]) <= 1:
        gyldig = True
    return gyldig


def sjekk_gyldig_trekk(fra_rl, til_rl):
    gyldig = False
    if hent(fra_rl) == "♙" or hent(fra_rl) == "♟":
        gyldig = gyldig_bonde(fra_rl, til_rl)
    elif hent(fra_rl) == "♖" or hent(fra_rl) == "♜":
        gyldig = gyldig_taarn(fra_rl, til_rl)
    elif hent(fra_rl) == "♘" or hent(fra_rl) == "♞":
        gyldig = gyldig_springer(fra_rl, til_rl)
    elif hent(fra_rl) == "♗" or hent(fra_rl) == "♝":
        gyldig = gyldig_loeper(fra_rl, til_rl)
    elif hent(fra_rl) == "♕" or hent(fra_rl) == "♛":
        gyldig = gyldig_dronning(fra_rl, til_rl)
    elif hent(fra_rl) == "♔" or hent(fra_rl) == "♚":
        gyldig = gyldig_konge(fra_rl, til_rl)
    return gyldig


def sjekk_konge_i_sjakk():
    konge_i_sjakk = False
    konge_rl = [0, 0]
    if t["hvitt_trekk"]:
        spiller = "hvit"
    else:
        spiller = "svart"
    for rad in range(1, 9):
        for linje in range(1, 9):
            if (t["hvitt_trekk"] and brett[rad][linje] == "♔") or (not t["hvitt_trekk"] and brett[rad][linje] == "♚"):
                konge_rl = [rad, linje]
    for rad in range(1, 9):
        for linje in range(1, 9):
            if brett[rad][linje] in brikker[spiller]:
                if sjekk_gyldig_trekk([rad, linje], konge_rl):
                    konge_i_sjakk = True
    return konge_i_sjakk


def sjekk_egen_konge_i_sjakk(fra_rl, til_rl):
    t["simulasjon"] = True
    brett_kopi = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    for i in brett_kopi:
        brett_kopi[i] = brett[i].copy()
    if t["hvitt_trekk"]:
        t["hvitt_trekk"] = False
        spiller = "svart"
    else:
        t["hvitt_trekk"] = True
        spiller = "hvit"
    brett[til_rl[0]][til_rl[1]] = hent(fra_rl)
    brett[fra_rl[0]][fra_rl[1]] = " "
    egen_konge_i_sjakk = sjekk_konge_i_sjakk()
    if t["hvitt_trekk"]:
        t["hvitt_trekk"] = False
    else:
        t["hvitt_trekk"] = True
    t["simulasjon"] = False
    for rad in range(1, 9):
        for linje in range(1, 9):
            brett[rad][linje] = brett_kopi[rad][linje]
    return egen_konge_i_sjakk


def sjekk_sjakk_matt():
    sjakk_matt = True
    if t["hvitt_trekk"]:
        t["hvitt_trekk"] = False
        spiller = "svart"
    else:
        t["hvitt_trekk"] = True
        spiller = "hvit"
    for rad_f in range(1, 9):
        for linje_f in range(1, 9):
            if brett[rad_f][linje_f] in brikker[spiller]:
                for rad_t in range(1, 9):
                    for linje_t in range(1, 9):
                        t["simulasjon"] = True
                        brett_kopi = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
                        for i in brett_kopi:
                            brett_kopi[i] = brett[i].copy()
                        gyldig_trekk = sjekk_gyldig_trekk([rad_f, linje_f], [rad_t, linje_t])
                        if brett[rad_t][linje_t] in brikker[spiller] and gyldig_trekk:
                            gyldig_trekk = False
                        if gyldig_trekk:
                            brett[rad_t][linje_t] = hent([rad_f, linje_f])
                            brett[rad_f][linje_f] = " "
                            if t["hvitt_trekk"]:
                                t["hvitt_trekk"] = False
                            else:
                                t["hvitt_trekk"] = True
                            if not sjekk_konge_i_sjakk():
                                sjakk_matt = False
                                # print("Mulige trekk:", [rad_f, linje_f], [rad_t, linje_t])
                            if t["hvitt_trekk"]:
                                t["hvitt_trekk"] = False
                            else:
                                t["hvitt_trekk"] = True
                        t["simulasjon"] = False
                        for rad in range(1, 9):
                            for linje in range(1, 9):
                                brett[rad][linje] = brett_kopi[rad][linje]
    if t["hvitt_trekk"]:
        t["hvitt_trekk"] = False
    else:
        t["hvitt_trekk"] = True
    return sjakk_matt


def forvandling_m():
    for linje in range(1, 9):
        if hent([1, linje]) == "♟":
            print_brett()
            gyldig = False
            offiserer = ["D", "T", "L", "S"]
            print("En hvit bonde har nådd enden av brettet og må forvandles til en offiser. Velg en av følgende:")
            while not gyldig:
                offiser = input("D = dronning, T = tårn, L = løper, S = springer: ")
                if offiser.upper() in offiserer:
                    brett[1][linje] = hvite_offiserer[offiser.upper()]
                    gyldig = True
                else:
                    print("Ugyldig input. Velg en av fløgende:")
        elif hent([8, linje]) == "♙":
            print_brett()
            gyldig = False
            offiserer = ["D", "T", "L", "S"]
            print("En svart bonde har nådd enden av brettet og må forvandles til en offiser. Velg en av følgende:")
            while not gyldig:
                offiser = input("D = dronning, T = tårn, L = løper, S = springer: ")
                if offiser.upper() in offiserer:
                    brett[8][linje] = svarte_offiserer[offiser.upper()]
                    gyldig = True
                else:
                    print("Ugyldig input. Velg en av fløgende:")


def forvandling_b():
    for linje in range(1, 9):
        if hent([1, linje]) == "♟":
            print_brett()
            brett[1][linje] = "♛"
        elif hent([8, linje]) == "♙":
            print_brett()
            brett[8][linje] = "♕"


def risiko(fra_rl, til_rl):
    risk = 0
    if t["hvitt_trekk"]:
        spiller = "hvit"
    else:
        spiller = "svart"
    for rad_t in range(1, 9):
        for linje_t in range(1, 9):
            if brett[rad_t][linje_t] in brikker[spiller] and brett[rad_t][linje_t] not in konger:
                brikke = brett[rad_t][linje_t]
                counter = 0
                if t["hvitt_trekk"]:
                    t["hvitt_trekk"] = False
                else:
                    t["hvitt_trekk"] = True
                for rad_f in range(1, 9):
                    for linje_f in range(1, 9):
                        if brett[rad_f][linje_f] not in brikker[spiller] and brett[rad_f][linje_f] != " ":
                            gyldig_trekk = sjekk_gyldig_trekk([rad_f, linje_f], [rad_t, linje_t])
                            if gyldig_trekk:
                                if brett[rad_t][linje_t] not in brikker[spiller] and brett[rad_t][linje_t] != " ":
                                    gyldig_trekk = False
                            if gyldig_trekk:
                                counter += 1/(1 + counter)
                if t["hvitt_trekk"]:
                    t["hvitt_trekk"] = False
                else:
                    t["hvitt_trekk"] = True
                risk += (verdi[brikke] * counter)
    return risk


def analyser(fra_rl, til_rl):
    score = verdi[hent(til_rl)]
    foerste_risiko = risiko(fra_rl, til_rl)
    score -= foerste_risiko
    if t["hvitt_trekk"]:
        t["hvitt_trekk"] = False
    else:
        t["hvitt_trekk"] = True
    score += risiko(fra_rl, til_rl)
    if t["hvitt_trekk"]:
        t["hvitt_trekk"] = False
    else:
        t["hvitt_trekk"] = True
    t["simulasjon"] = True
    brett_kopi = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    for i in brett_kopi:
        brett_kopi[i] = brett[i].copy()
    brett[til_rl[0]][til_rl[1]] = hent([fra_rl[0], fra_rl[1]])
    brett[fra_rl[0]][fra_rl[1]] = " "
    andre_risiko = risiko(fra_rl, til_rl)
    score -= andre_risiko
    if andre_risiko < foerste_risiko:
        if t["hvitt_trekk"]:
            t["hvitt_trekk"] = False
        else:
            t["hvitt_trekk"] = True
        score += risiko(fra_rl, til_rl)
        if t["hvitt_trekk"]:
            t["hvitt_trekk"] = False
        else:
            t["hvitt_trekk"] = True
    t["simulasjon"] = False
    for rad in range(1, 9):
        for linje in range(1, 9):
            brett[rad][linje] = brett_kopi[rad][linje]
    return score


def menneske():
    if t["hvitt_trekk"]:
        spiller = "hvit"
    else:
        spiller = "svart"
    gyldig_trekk = False
    while not gyldig_trekk:
        gyldig_brikke = False
        while not gyldig_brikke:
            fra = list(input("Det er " + spiller + " spiller sitt trekk. Hvilken brikke vil du flytte? "))
            fra_linje = 0
            fra_rad = 0
            if len(fra) == 2:
                fra_linje, fra_rad = sjekk_gyldig_rute(fra)
            else:
                print("Ugyldig input: Skriv inn nøyaktig 2 tegn(bokstav og tall).\n")
            if fra_linje and fra_rad:
                if brett[fra_rad][fra_linje] in brikker[spiller]:
                    gyldig_brikke = True
                    fra_rl = [fra_rad, fra_linje]
                else:
                    print("Ugyldig. Det er ingen " + spiller + " brikke der.\n")
        avbryt_trekk = False
        while not gyldig_trekk and not avbryt_trekk:
            til = list(input("Hvor vil du flytte " + fra[0] + fra[1] + " til? [Q for annen brikke] "))
            if til == ["q"] or til == ["Q"]:
                avbryt_trekk = True
            else:
                gyldig_destinasjon = False
                gyldig_flytt = False
                egen_konge_i_sjakk = False
                til_linje = 0
                til_rad = 0
                if len(til) == 2:
                    til_linje, til_rad = sjekk_gyldig_rute(til)
                else:
                    print("Ugyldig input: Skriv inn nøyaktig 2 tegn(bokstav og tall).\n")
                if til_linje and til_rad:
                    if brett[til_rad][til_linje] not in brikker[spiller]:
                        gyldig_destinasjon = True
                        til_rl = [til_rad, til_linje]
                        if sjekk_gyldig_trekk(fra_rl, til_rl):
                            gyldig_flytt = True
                            if sjekk_egen_konge_i_sjakk(fra_rl, til_rl):
                                egen_konge_i_sjakk = True
                                print("Ugyldig. Kan ikke sette egen konge i sjakk.\n")
                            if gyldig_destinasjon and gyldig_flytt and not egen_konge_i_sjakk:
                                gyldig_trekk = True
                        else:
                            print("Ugyldig. Kan ikke flytte dit.\n")
                    else:
                        print("Ugyldig. Der står det allerede en " + spiller + " brikke.\n")
    brett[til_rl[0]][til_rl[1]] = hent(fra_rl)
    brett[fra_rl[0]][fra_rl[1]] = " "
    forvandling_m()


def bot():
    if t["hvitt_trekk"]:
        spiller = "hvit"
    else:
        spiller = "svart"
    beste_score = -100
    beste_liste = []
    gyldig_trekk = False
    for rad_f in range(1, 9):
        for linje_f in range(1, 9):
            if brett[rad_f][linje_f] in brikker[spiller]:
                for rad_t in range(1, 9):
                    for linje_t in range(1, 9):
                        t["simulasjon"] = True
                        brett_kopi = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
                        for i in brett_kopi:
                            brett_kopi[i] = brett[i].copy()
                        gyldig_trekk = sjekk_gyldig_trekk([rad_f, linje_f], [rad_t, linje_t])
                        if ((brett[rad_t][linje_t] in brikker[spiller]) or sjekk_egen_konge_i_sjakk([rad_f, linje_f], [rad_t, linje_t])) and gyldig_trekk:
                            gyldig_trekk = False
                        if gyldig_trekk:
                            score = analyser([rad_f, linje_f], [rad_t, linje_t])
                            if score > beste_score:
                                beste_score = score
                                beste_liste = [[[rad_f, linje_f], [rad_t, linje_t]]]
                            elif score == beste_score:
                                beste_liste.append([[rad_f, linje_f], [rad_t, linje_t]])
    if len(beste_liste) > 0:
        beste_trekk = random.choice(beste_liste)
        brett[beste_trekk[1][0]][beste_trekk[1][1]] = hent(beste_trekk[0])
        brett[beste_trekk[0][0]][beste_trekk[0][1]] = " "
    else:
        t["patt"] = True
    forvandling_b()


def trekk():
    print_brett()
    if t["sjakk"]:
        print("              - Sjakk -")
    if t["hvitt_trekk"]:
        menneske()
    else:
        bot()
    forvandling_m()
    if sjekk_konge_i_sjakk():
        t["sjakk"] = True
    else:
        t["sjakk"] = False
    if t["sjakk"]:
        t["matt"] = sjekk_sjakk_matt()
    if t["hvitt_trekk"]:
        t["hvitt_trekk"] = False
    else:
        t["hvitt_trekk"] = True


c = 0

while not t["matt"] and not t["patt"]:
    trekk()
    c += 1
    # print("Antall trekk:", c)
print_brett()
if t["matt"]:
    print("Gratulerer! Sjakk matt!")
elif t["patt"]:
    print("Patt. Spillet endte i remis.")
print("Antall trekk:", c)
