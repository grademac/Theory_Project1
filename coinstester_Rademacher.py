import time

TIME_LIMIT_SECONDS = 5 * 60

def check_coins(coins, target, assignment):
    """
    Check if a combination of coins matches the target.
    :param coins: List of available coin denominations.
    :param target: The target amount of money.
    :param assignment: Current coin counts for each denomination.
    :return: True if the current assignment matches the target amount, False otherwise.
    """
    total = 0
    for i in range(len(coins)):
        total += coins[i] * assignment[i]
    return total == target

def brute_force_coin_solver(coins, target):
    """
    Solves the coin combination problem by brute force.
    :param coins: List of available coin denominations.
    :param target: The target amount of money to achieve.
    :return: A tuple (Satisfiable, assignment, exec_time) where Satisfiable is a bool indicating if a solution was found,
             assignment is a list showing how many of each coin to use, and exec_time is the time taken in microseconds.
    """
    start = time.time()  # Start timer
    n = len(coins)
    assignment = [0] * n  # Start with zero of each coin
    max_uses = target // min(coins) + 1  
    
    # iterate through all possible assignments of coins, up to a reasonable maximum number of coins
    while assignment[n-1] <= max_uses:  # Stop when the highest denomination exceeds its maximum use limit
        if check_coins(coins, target, assignment):
            end = time.time()  # End timer
            exec_time = int((end - start) * 1e6)  # Convert to microseconds
            return True, assignment, exec_time
        
        if time.time() - start > TIME_LIMIT_SECONDS: #skip case if taking longer than set time limit
            print("Skipping this assignment due to time limit...")
            break
        # Generate next assignment
        for i in range(n):
            if assignment[i] < max_uses:
                assignment[i] += 1
                break
            else:
                assignment[i] = 0
        else:
            break

    end = time.time()  # End timer
    exec_time = int((end - start) * 1e6)  # Convert to microseconds
    return False, assignment, exec_time

def read_coin_problem(file_path):
    """
    Reads the coin problem from a file. Each line contains the size, target value, and coin values.
    :param file_path: Path to the file containing the coin problem data.
    :return: A list of tuples where each tuple is (size, target, coins).
    """
    problems = []
    with open(file_path, 'r') as file:
        for line in file:
            tokens = line.split()
            size = tokens[0]  # 'small', 'medium', or 'large'
            target = int(tokens[1])  # The target value
            coins = list(map(int, tokens[2:]))  # Coin denominations
            problems.append((size, target, coins))
    return problems

def solve_coin_problems_from_file(file_path, output_file, output2_file, output3_file):
    """
    Solves all coin problems from the input file.
    :param file_path: Path to the input file.
    """
    with open(output_file, 'w') as output, open(output2_file, 'w') as output2, open(output3_file, 'w') as output3:
        problems = read_coin_problem(file_path)
        for problem in problems:
            size, target, coins = problem
            print(f"Solving {size} problem: Target: {target}, Coins: {coins}")
            output3.write(f"Solving {size} problem: Target: {target}, Coins: {coins}\n")
            result = brute_force_coin_solver(coins, target)
            if result[0]:
                print(f"Satisfiable: {result[1]} solves the target of {target}")
                output.write(f"Satisfiable\n")
                output2.write(f"{result[2]}\n")
                output3.write(f"Satisfiable: {result[1]} solves the target of {target}\n")
            else:
                print(f"Unsatisfiable: No combination of coins can solve the target of {target}")
                output.write(f"Unsatisfiable\n")
                output2.write(f"{result[2]}\n")
                output3.write(f"Unsatisfiable: No combination of coins can solve the target of {target}\n")
            print(f"Execution time: {result[2]} microseconds\n")

file_path = '4test.txt'
output1 = '4SATresults.txt'
output2 = '4Timeresults.txt'
output3 = '4results.txt'
solve_coin_problems_from_file(file_path, output1, output2, output3)
