import lab1.blumshub as blumshub
import sys
from collections import Counter

def poker_test(bits: list) -> bool:

    segments = []
    for i in range(0, 20000, 4):
        chunk = bits[i:i+4]

        val = int("".join(map(str, chunk)), 2)
        segments.append(val)

    counts = Counter(segments)
    f_sum_sq = sum(count**2 for count in counts.values())

    
    x = (16 / 5000) * f_sum_sq - 5000
    
    print(f"Wynik testu pokerowego (X): {x:.2f}")
    
    
    return 2.16 < x < 46.17


def single_bit_test(bits: list) -> bool:
   
    count_1 = bits.count(1)

    return (count_1 > 9725 and count_1 < 10275)

def series_test(bits: list):
 
    intervals = {
        1: (2315, 2685),
        2: (1114, 1386),
        3: (527, 723),
        4: (240, 384),
        5: (103, 209),
        6: (103, 209) 
    }

    runs_0 = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0}
    runs_1 = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0}

    if len(bits) == 0:
        return False, "Brak danych"

    current_val = bits[0]
    current_run = 0

    for bit in bits + [None]:  
        if bit == current_val:
            current_run += 1
        else:

            target_dict = runs_1 if current_val == 1 else runs_0
            length = current_run if current_run < 6 else 6
            target_dict[length] += 1
           
            current_val = bit
            current_run = 1

    all_passed = True
    report = []

    for length, (low, high) in intervals.items():
        for val, counts in [("Zera", runs_0), ("Jedynki", runs_1)]:
            count = counts[length]
            status = "OK" if low <= count <= high else "FAIL"
            if status == "FAIL":
                all_passed = False
            
            desc = f"{val} dlugosci {length if length < 6 else '6+'}: {count} (zakres {low}-{high}) -> {status}"
            report.append(desc)

    return all_passed, report

def long_series(bits: list) -> bool:
    count = 1
    for i in range(1, len(bits)):
        if bits[i] == bits[i-1]:
            count += 1
            if count > 25:
                return False
        else:
            count = 1
    return True

def main(p, q, seed=None):

    bbs = blumshub.BlumBlumShub(p, q)
    bits = bbs.generate_bits(20000)

    if single_bit_test(bits):
        print("Test pojedynczego bitu: ZALICZONY")
    else:
        print("Test pojedynczego bitu: NIEZALICZONY")

    if poker_test(bits):
        print("Test pokerowy: ZALICZONY")
    else:    
        print("Test pokerowy: NIEZALICZONY")
    
    series_result, series_report = series_test(bits)
    if series_result:
        print("Test serii: ZALICZONY")
    else:
        print("Test serii: NIEZALICZONY")
    for line in series_report:
        print(line)

    if long_series(bits):
        print("Test dlugich serii: ZALICZONY")
    else:
        print("Test dlugich serii: NIEZALICZONY")
    

if __name__ == "__main__":
    args = sys.argv[1:]
    if len(args) == 2:
        p, q = map(int, args)
        main(p, q)
    else:
        p, q = 61157, 69857    

    main(p, q)

    


    