# import random
import os
import time

class ArrayInterpreter:
    def __init__(self):
        self.arrays = {chr(i): [] for i in range(ord('A'), ord('Z') + 1)}

    def execute_command(self, command):
        parts = command.strip().split(',')
        if not parts:
            return
        try:
            cmd = parts[0].strip().split()[0].lower()

            if cmd == 'load':
                array_name = parts[0].strip().split()[1].upper()
                filename = parts[1].strip()
                self.load(array_name, filename)
            elif cmd == 'save':
                array_name = parts[0].strip().split()[1].upper()
                filename = parts[1].strip()
                self.save(array_name, filename)
            elif cmd == 'rand':
                array_name = parts[0].strip().split()[1].upper()
                count = int(parts[1].strip())
                lb = int(parts[2].strip())
                rb = int(parts[3].strip())
                self.rand(array_name, count, lb, rb)
            elif cmd == 'concat':
                array_name_a = parts[0].strip().split()[1].upper()
                array_name_b = parts[1].strip().upper()
                self.concat(array_name_a, array_name_b)
            elif cmd == 'free':
                array_name = parts[0].strip().split()[1].upper()
                self.free(array_name)
            elif cmd == 'remove':
                array_name = parts[0].strip().split()[1].upper()
                start_index = int(parts[1].strip())
                count = int(parts[2].strip())
                self.remove(array_name, start_index, count)
            elif cmd == 'copy':
                array_name_a = parts[0].strip().split()[1].upper()
                start_index = int(parts[1].strip())
                end_index = int(parts[2].strip())
                array_name_b = parts[3].strip().upper()
                self.copy(array_name_a, start_index, end_index, array_name_b)
            elif cmd == 'sort':
                array_name = parts[0].strip().split()[1][0].upper()
                order = parts[0].strip().split()[1][1]
                self.sort(array_name, order)
            elif cmd == 'shuffle':
                array_name = parts[0].strip().split()[1].upper()
                self.shuffle_array(array_name)
            elif cmd == 'stats':
                array_name = parts[0].strip().split()[1].upper()
                self.stats(array_name)
            elif cmd == 'print':
                array_name = parts[0].strip().split()[1].upper()
                if parts[1].strip().lower() == 'all':
                    self.print_all(array_name)
                elif len(parts) == 2:
                    index = int(parts[1].strip())
                    self.print_element(array_name, index)
                elif len(parts) == 3:
                    start_index = int(parts[1].strip())
                    end_index = int(parts[2].strip())
                    self.print_range(array_name, start_index, end_index)
            else:
                print(f"Неизвестная команда: {command}")
        except Exception as e:
            print(f"Ошибка при выполнении команды '{command}': {e}")

    def load(self, array_name, filename):
        if not os.path.exists(filename):
            raise FileNotFoundError(f"Файл {filename} не найден.")
        with open(filename, 'r') as file:
            content = file.read()
            try:
                self.arrays[array_name] = list(map(int, content.split()))
            except ValueError:
                self.arrays[array_name] = [int(x) for x in content.split() if x.isdigit()]
        print(f"Массив {array_name} загружен из {filename}")

    def save(self, array_name, filename):
        with open(filename, 'w') as file:
            file.write(' '.join(map(str, self.arrays[array_name])))
        print(f"Массив {array_name} сохранен в {filename}")

    # def rand(self, array_name, count, lb, rb):
    #     self.arrays[array_name] = [random.randint(lb, rb) for _ in range(count)]
    #     print(f"Массив {array_name} заполнен {count} случайными элементами в диапазоне [{lb}, {rb}]")
    def rand(self, array_name, count, lb, rb):
        seed = int(time.time())
        randint = self.custom_random(seed)
        self.arrays[array_name] = [randint(lb, rb) for _ in range(count)]
        print(f"Массив {array_name} заполнен {count} случайными элементами в диапазоне [{lb}, {rb}]")

    def concat(self, array_name_a, array_name_b):
        self.arrays[array_name_a] += self.arrays[array_name_b]
        print(f"Массив {array_name_a} конкатенирован с {array_name_b}")

    def free(self, array_name):
        self.arrays[array_name] = []
        print(f"Массив {array_name} очищен")

    def remove(self, array_name, start_index, count):
        del self.arrays[array_name][start_index:start_index + count]
        print(f"Удалено {count} элементов из массива {array_name}, начиная с индекса {start_index}")

    def copy(self, array_name_a, start_index, end_index, array_name_b):
        self.arrays[array_name_b] = self.arrays[array_name_a][start_index:end_index + 1]
        print(f"Элементы с {start_index} по {end_index} из массива {array_name_a} скопированы в массив {array_name_b}")

    def quicksort(self, array, low, high):
        if low < high:
            pi = self.partition(array, low, high)
            self.quicksort(array, low, pi - 1)
            self.quicksort(array, pi + 1, high)

    def partition(self, array, low, high):
        pivot = array[high]
        i = low - 1
        for j in range(low, high):
            if array[j] <= pivot:
                i = i + 1
                array[i], array[j] = array[j], array[i]
        array[i + 1], array[high] = array[high], array[i + 1]
        return i + 1

    def sort(self, array_name, order):
        if order not in ['+', '-']:
            raise ValueError("Порядок должен быть '+' или '-'")
        if order == '+':
            self.quicksort(self.arrays[array_name], 0, len(self.arrays[array_name]) - 1)
        elif order == '-':
            self.quicksort(self.arrays[array_name], 0, len(self.arrays[array_name]) - 1)
            self.arrays[array_name].reverse()
        print(f"Массив {array_name} отсортирован в {'возрастающем' if order == '+' else 'убывающем'} порядке")

    # def shuffle(self, array_name):
    #     random.shuffle(self.arrays[array_name])
    #     print(f"Массив {array_name} перемешан")

    def custom_random(self, seed):
        def randint(low, high):
            nonlocal seed
            a = 1664525
            c = 1013904223
            m = 2 ** 32
            seed = (a * seed + c) % m
            return low + seed % (high - low + 1)

        return randint

    def shuffle_array(self, array_name, seed=None):
        if seed is None:
            seed = int(time.time())
        randint = self.custom_random(seed)
        array = self.arrays[array_name]
        n = len(array)
        for i in range(n - 1, 0, -1):
            j = randint(0, i)
            array[i], array[j] = array[j], array[i]
        print(f"Массив {array_name} перемешан")


    def stats(self, array_name):
        array = self.arrays[array_name]
        if not array:
            print(f"Массив {array_name} пуст")
            return
        size = len(array)
        max_val = max(array)
        min_val = min(array)
        max_indices = [i for i, x in enumerate(array) if x == max_val]
        min_indices = [i for i, x in enumerate(array) if x == min_val]
        freq = {x: array.count(x) for x in array}
        most_frequent = max(freq, key=lambda k: (freq[k], k))
        mean_val = sum(array) / size
        max_deviation = max(abs(x - mean_val) for x in array)
        print(f"Статистика массива {array_name}:\n"
              f"Размер: {size}\n"
              f"Максимум: {max_val} на индексах {max_indices}\n"
              f"Минимум: {min_val} на индексах {min_indices}\n"
              f"Наиболее частый элемент: {most_frequent}\n"
              f"Среднее значение: {mean_val}\n"
              f"Максимальное отклонение от среднего: {max_deviation}")

    def print_element(self, array_name, index):
        if index < 0 or index >= len(self.arrays[array_name]):
            print(f"Индекс {index} вне границ массива {array_name}")
        else:
            print(f"{array_name}[{index}] = {self.arrays[array_name][index]}")

    def print_range(self, array_name, start_index, end_index):
        if start_index < 0 or end_index >= len(self.arrays[array_name]) or start_index > end_index:
            print(f"Неверный диапазон [{start_index}:{end_index}] для массива {array_name}")
        else:
            print(f"{array_name}[{start_index}:{end_index}] = {self.arrays[array_name][start_index:end_index + 1]}")

    def print_all(self, array_name):
        print(f"{array_name} = {self.arrays[array_name]}")

def main():
    interpreter = ArrayInterpreter()
    while True:
        try:
            command = input("Введите команду: ")
            if command.lower() in {'выход', 'quit', 'exit'}:
                break
            interpreter.execute_command(command)
        except EOFError:
            break

if __name__ == '__main__':
    main()
