from Pyro4 import expose
from heapq import merge

class Solver:

    def __init__(self, workers=None, input_file_name=None, output_file_name=None):
        self.input_file = input_file_name
        self.output_file = output_file_name
        self.workers = workers

    def solve(self):
        total_numbers = self.read_input()
        chunk_size = total_numbers / len(self.workers)
        encoded_parts = []
        last_worker_index = len(self.workers) - 1

        for i in range(0, last_worker_index):
            start_index = i * chunk_size
            end_index = start_index + chunk_size
            encoded_parts.append(self.workers[i].mymap(start_index, end_index))

        encoded_parts.append(self.workers[last_worker_index].mymap(last_worker_index * chunk_size, total_numbers))
        all_encoded = self.myreduce(encoded_parts)
        self.write_output(all_encoded)

    def read_input(self):
        with open(self.input_file, 'r') as f:
            line = f.readline()
            return int(line.strip())
 
    @staticmethod
    def generate_fibonacci(max_value):
        fib_sequence = [1, 2]
        while True:
            next_fib = fib_sequence[-1] + fib_sequence[-2]
            if next_fib > max_value or next_fib < 0:
                break
            fib_sequence.append(next_fib)
        return fib_sequence

    @staticmethod
    def fibonacci_code(number):
        if number <= 0:
            raise ValueError("Number must be positive for Fibonacci coding")
    
        fib_sequence = Solver.generate_fibonacci(number)
        index = len(fib_sequence) - 1

        while index >= 0 and fib_sequence[index] > number:
            index -= 1

        code_bits = [0] * (index + 1)
        remaining = number

        for i in range(index, -1, -1):
            if fib_sequence[i] <= remaining:
                code_bits[i] = 1
                remaining -= fib_sequence[i]

        code_bits.append(1)
        return ''.join(map(str, code_bits))
    

    @staticmethod
    @expose
    def mymap(a, b):
        res_arr = []
        for n in range(a+1,b+1):
            res_arr.append(Solver.fibonacci_code(n))
        return res_arr
    
    def myreduce(self, mapped):
        result = []
        for sublist in mapped:
            if hasattr(sublist, 'value'):
                result.extend(sublist.value)
            else:
                result.extend(sublist)
        return result

    def write_output(self, output_list):
        with open(self.output_file, 'w') as f:
            for code in output_list:
                f.write(code + '\n')