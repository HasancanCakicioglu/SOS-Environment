def count_sos(matrix):
    sos_count = 0
    n = len(matrix)
    for y in range(n):
        for x in range(n):
            if matrix[y][x] == 'S':
                # Sağa doğru SOS kontrolü
                if x + 2 < n and matrix[y][x+1] == 'O' and matrix[y][x+2] == 'S':
                    sos_count += 1
                # Aşağı doğru SOS kontrolü
                if y + 2 < n and matrix[y+1][x] == 'O' and matrix[y+2][x] == 'S':
                    sos_count += 1
                # Sağ çapraz doğru SOS kontrolü
                if x + 2 < n and y + 2 < n and matrix[y+1][x+1] == 'O' and matrix[y+2][x+2] == 'S':
                    sos_count += 1
                # Sol çapraz doğru SOS kontrolü
                if x - 2 >= 0 and y + 2 < n and matrix[y+1][x-1] == 'O' and matrix[y+2][x-2] == 'S':
                    sos_count += 1
    return sos_count

def place_symbol_and_count_sos(matrix, row, col, symbol):
    n = len(matrix)
    if matrix[row][col] == "O":  # Eğer belirtilen konum boşsa devam edilir
        matrix[row][col] = symbol  # Belirtilen sembolü belirtilen konuma yerleştirilir
        sos_count = 0  # SOS sayacı başlatılır
        # Sağa doğru SOS kontrolü
        if col + 2 < n and matrix[row][col+1] == 'O' and matrix[row][col+2] == 'S':
            sos_count += 1
        # Aşağı doğru SOS kontrolü
        if row + 2 < n and matrix[row+1][col] == 'O' and matrix[row+2][col] == 'S':
            sos_count += 1
        # Sağ çapraz doğru SOS kontrolü
        if col + 2 < n and row + 2 < n and matrix[row+1][col+1] == 'O' and matrix[row+2][col+2] == 'S':
            sos_count += 1
        # Sol çapraz doğru SOS kontrolü
        if col - 2 >= 0 and row + 2 < n and matrix[row+1][col-1] == 'O' and matrix[row+2][col-2] == 'S':
            sos_count += 1
        return sos_count
    else:
        print("Belirtilen konum dolu!")
        return -1


# Örnek matris
matrix = [
    ['S', 'O', 1, 'S', 'O'],
    ['S', 'O', 'S', 'O', 'S'],
    ['O', 'S', 'O', 'S', 'O'],
    ['S', 'O', 'O', 'S', 'S']
]


sos_count = count_sos(matrix)
print("Toplam SOS Sayısı:", sos_count)

