"""
Автоматический поиск оффсета viewangles в hw.dll.
Запускай из папки проекта: python scan.py
"""
import struct, time, sys
import pymem, pymem.process

PROCESS = "cs.exe"
HW_DLL  = "hw.dll"

def scan():
    print("Подключаюсь к cs.exe...")
    try:
        pm  = pymem.Pymem(PROCESS)
        mod = pymem.process.module_from_name(pm.process_handle, HW_DLL)
        base = mod.lpBaseOfDll
        size = mod.SizeOfImage
        print(f"hw.dll база: 0x{base:08X}  размер: 0x{size:08X}")
    except Exception as e:
        print(f"Ошибка: {e}")
        input("Enter для выхода")
        return

    print("\nШАГ 1: Встань в игре и НЕ ДВИГАЙ мышь 3 секунды...")
    time.sleep(3)

    # Читаем весь hw.dll
    print("Сканирую память hw.dll...")
    try:
        data = pm.read_bytes(base, size)
    except:
        # Читаем по кускам
        data = b''
        chunk = 0x1000
        for off in range(0, size, chunk):
            try: data += pm.read_bytes(base + off, min(chunk, size-off))
            except: data += b'\x00' * min(chunk, size-off)

    # Ищем все float которые похожи на pitch (от -90 до 90)
    candidates = []
    for i in range(0, len(data)-8, 4):
        try:
            pitch, yaw = struct.unpack_from('ff', data, i)
            if -89 < pitch < 89 and -180 < yaw < 180:
                candidates.append((i, pitch, yaw))
        except:
            pass

    print(f"Найдено кандидатов: {len(candidates)}")

    print("\nШАГ 2: Повернись В ИГРЕ влево на 90° и не двигайся 2 сек...")
    time.sleep(3)

    # Читаем снова и ищем кандидаты у которых yaw изменился
    try:
        data2 = pm.read_bytes(base, size)
    except:
        data2 = b''
        for off in range(0, size, 0x1000):
            try: data2 += pm.read_bytes(base + off, min(0x1000, size-off))
            except: data2 += b'\x00' * min(0x1000, size-off)

    matches = []
    for (off, p1, y1) in candidates:
        try:
            p2, y2 = struct.unpack_from('ff', data2, off)
            if -89 < p2 < 89 and -180 < y2 < 180:
                if abs(y2 - y1) > 20:   # yaw изменился — это оно
                    matches.append((off, p2, y2))
        except:
            pass

    if not matches:
        print("\nНичего не нашли. Попробуй повернуться сильнее.")
        input("Enter для выхода")
        return

    print(f"\nНайдено совпадений: {len(matches)}")
    print("\nТоп результатов:")
    for off, p, y in matches[:10]:
        print(f"  offset=0x{off:08X}  →  VIEWANGLES = 0x{off:08X}   pitch={p:.1f}  yaw={y:.1f}")

    best_off = matches[0][0]
    print(f"\n=== ЗАМЕНИ В core/offsets.py ===")
    print(f"VIEWANGLES = 0x{best_off:08X}")
    print(f"================================")

    input("\nEnter для выхода")

scan()
