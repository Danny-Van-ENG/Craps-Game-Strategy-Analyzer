import time
import random
import math

# Game Rules
# Pass roll (button off):
# 2, 3, 12 craps
# 7, 11 win
# 1, 4, 5, 6, 8, 10 point

class colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    END = '\033[0m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'

dice_rolls = {
    2: 0,
    3: 0,
    4: 0,
    5: 0,
    6: 0,
    7: 0,
    8: 0,
    9: 0,
    10: 0,
    11: 0,
    12: 0
}

def roll_dice():
    dice_1 = random.randint(1, 6)
    dice_2 = random.randint(1, 6)
    sum_of_dice = dice_1 + dice_2

    print("- Rolling dice...")
    print(f"- Dice 1: {dice_1}")
    print(f"- Dice 2: {dice_2}")
    print(f"- Dice sum: {sum_of_dice}")

    dice_rolls[sum_of_dice] += 1
    return sum_of_dice

class Board:
    def __init__(self):
        self.round_count = 0
        self.roll_streak = 0
        self.highest_roll_streak = 0
        self.balances = {}

        self.current_point_round = False
        self.point = 0
        self.balance = 50
        self.bets = {
            'pass_line': 0,
            2: 0,
            3: 0,
            4: 0,
            5: 0,
            6: 0,
            7: 0,
            8: 0,
            9: 0,
            10: 0,
            11: 0,
            12: 0
        }

    def print_balance(self):
        print(f'--- Balance ${self.balance}')

    def print_board(self):
        print('--- Board')
        print(f'--- [6]: ${self.bets[6]}')
        print(f'--- [8]: ${self.bets[8]}')
        print(f'--- [Pass Line]: ${self.bets["pass_line"]}')

    def clear_board(self):
        # Subtract total amount on board from balance
        total_amount_on_board = self.bets['pass_line'] + self.bets[6] + self.bets[8]
        self.balance -= total_amount_on_board

        # Clear all bets
        self.bets['pass_line'] = 0
        self.bets[6] = 0
        self.bets[8] = 0

        # Turn button off
        self.point = 0

    def place_bet(self, number, bet):
        if number == 'pass':
            self.bets['pass_line'] += bet
        elif number == 6:
            self.bets[6] += bet
        elif number == 8:
            self.bets[8] += bet

    def pass_line_round(self):
        self.round_count += 1
        print(f'----- Pass Line Round ----- {self.round_count}')
        self.print_balance()
        self.print_board()

        sum_of_dice = roll_dice()
        pass_states = {7, 11}
        no_pass_states = {2, 3, 12}

        if sum_of_dice in pass_states:
            self.balance += self.bets['pass_line']  # Pay the win
            print(colors.GREEN + f'Craps Master: {sum_of_dice} Pass')
            print(f'Paid ${self.bets["pass_line"]} \n' + colors.END)
            self.balances[self.round_count] = self.balance
            self.pass_line_round()  # Play the pass line again
            self.roll_streak += 1
            self.highest_roll_streak = max(self.highest_roll_streak, self.roll_streak)
        elif sum_of_dice in no_pass_states:
            print(colors.RED + f'Craps Master: {sum_of_dice} No Pass \n' + colors.END)
            self.clear_board()
            self.balances[self.round_count] = self.balance
            self.roll_streak = 0
        else:
            self.point = sum_of_dice
            print(colors.BLUE + f'Point is now on {self.point}\n' + colors.END)
            if self.point != 6 and game.bets[6] == 0:
                game.place_bet(6, 6)
            if self.point != 8 and game.bets[8] == 0:
                game.place_bet(8, 6)
            self.roll_streak += 1
            self.highest_roll_streak = max(self.highest_roll_streak, self.roll_streak)
            self.point_round()

    def point_round(self):
        self.round_count += 1
        self.current_point_round = True
        print(f'----- Point Round ----- {self.round_count}')
        self.print_balance()
        self.print_board()

        sum_of_dice = roll_dice()
        craps_state = 7
        winnable_states = {4, 5, 6, 8, 9, 10}

        if sum_of_dice == craps_state:  # Craps
            print(colors.RED + f'Craps Master: {sum_of_dice} Craps \n' + colors.END)
            self.clear_board()
            self.balances[self.round_count] = self.balance
            self.current_point_round = False
            self.roll_streak = 0
        elif sum_of_dice == self.point:  # Hit point
            print(colors.GREEN + f'Craps Master: {sum_of_dice} Point Hit')
            print(f'Paid ${self.bets["pass_line"]} \n' + colors.END)
            self.balance += self.bets['pass_line']
            self.balances[self.round_count] = self.balance
            self.roll_streak += 1
            self.highest_roll_streak = max(self.highest_roll_streak, self.roll_streak)
            self.point_round()
        elif sum_of_dice in winnable_states:
            if self.bets[sum_of_dice] > 0:
                payout_rate = 0
                if self.bets[sum_of_dice] == 6 or self.bets[sum_of_dice] == 8:
                    payout_rate = 7/6
                self.balance += math.floor(payout_rate * self.bets[sum_of_dice])
                print(colors.GREEN + f'Craps Master: {sum_of_dice} Bet Hit')
                print(f'Paid: ${math.floor(payout_rate * self.bets[sum_of_dice])} \n' + colors.END)
            else:
                print(colors.YELLOW + f'Craps Master: {sum_of_dice} No bet, moving on \n' + colors.END)

            self.roll_streak += 1
            self.highest_roll_streak = max(self.highest_roll_streak, self.roll_streak)
            self.balances[self.round_count] = self.balance
            self.point_round()
        else:
            print(colors.YELLOW + f'Craps Master: {sum_of_dice} Moving on \n' + colors.END)
            self.roll_streak += 1
            self.highest_roll_streak = max(self.highest_roll_streak, self.roll_streak)
            self.point_round()
game = Board()
while True:
    if game.balance < 5:
        break
    time.sleep(0)
    if game.bets['pass_line'] == 0:
        game.place_bet('pass', 5)

    game.pass_line_round()

print(f'END DATA: ')
print(f'Roll Variance:')
for key, value in dice_rolls.items():
    pass
    #print(f"Dice {key}: {value}")

print(f'Round Balances:')
peak_balance = 50
peak_balance_round = 0

for key, value in game.balances.items():
    #print(f"Round {key}: Balance ${value}")
    if value > peak_balance:
        peak_balance = value
        peak_balance_round = key

green = '\033[92m'
print(colors.GREEN + f'\nBeginning balance: $50')
print(f'Ending Balance: ${game.balance}')
print(f'Dice Rolls to ${game.balance}: {game.round_count}')
print(f'Peak Balance: ${peak_balance} on Roll {peak_balance_round}')
print(f'Longest Roll Streak Without Craps: {game.highest_roll_streak} rolls' + colors.END)
