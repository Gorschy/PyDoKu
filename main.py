import kivy
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.clock import Clock
import random, math, threading, time, json

kivy.require('1.11.1')





class Sudoku:
    def __init__(self, N, K):
        self.N = N
        self.K = K
        self.SRN = int(math.sqrt(N))
        self.mat = [[0 for _ in range(N)] for _ in range(N)]
        self.fillValues()
    #... (Sudoku class methods would go here, not displayed due to space limitation)
    def fillValues(self):
        # Fill the diagonal of SRN x SRN matrices
        self.fillDiagonal()
 
        # Fill remaining blocks
        self.fillRemaining(0, self.SRN)
 
        # Remove Randomly K digits to make game
        self.removeKDigits()
     
    def fillDiagonal(self):
        for i in range(0, self.N, self.SRN):
            self.fillBox(i, i)
     
    def unUsedInBox(self, rowStart, colStart, num):
        for i in range(self.SRN):
            for j in range(self.SRN):
                if self.mat[rowStart + i][colStart + j] == num:
                    return False
        return True
     
    def fillBox(self, row, col):
        num = 0
        for i in range(self.SRN):
            for j in range(self.SRN):
                while True:
                    num = self.randomGenerator(self.N)
                    if self.unUsedInBox(row, col, num):
                        break
                self.mat[row + i][col + j] = num
     
    def randomGenerator(self, num):
        return math.floor(random.random() * num + 1)
     
    def checkIfSafe(self, i, j, num):
        return (self.unUsedInRow(i, num) and self.unUsedInCol(j, num) and self.unUsedInBox(i - i % self.SRN, j - j % self.SRN, num))
     
    def unUsedInRow(self, i, num):
        for j in range(self.N):
            if self.mat[i][j] == num:
                return False
        return True
     
    def unUsedInCol(self, j, num):
        for i in range(self.N):
            if self.mat[i][j] == num:
                return False
        return True
     
        
    def fillRemaining(self, i, j, callback=None):
            # Check if we have reached the end of the matrix
            if i == self.N - 1 and j == self.N:
                return True
        
            # Move to the next row if we have reached the end of the current row
            if j == self.N:
                i += 1
                j = 0
        
            # Skip cells that are already filled
            if self.mat[i][j] != 0:
                return self.fillRemaining(i, j + 1, callback)
        
            # Try filling the current cell with a valid value
            for num in range(1, self.N + 1):
                if self.checkIfSafe(i, j, num):
                    self.mat[i][j] = num
                    if callback:  # Call the callback function if it's provided
                        callback(self.mat, i, j, True)  # True indicates this is a correct move
                    if self.fillRemaining(i, j + 1, callback):
                        return True
                    self.mat[i][j] = 0
                    if callback:  # Call the callback function if it's provided
                        callback(self.mat, i, j, False)  # False indicates this is a backtrack move

            return False
    
    def removeKDigits(self):
        count = self.K
 
        while (count != 0):
            i = self.randomGenerator(self.N) - 1
            j = self.randomGenerator(self.N) - 1
            if (self.mat[i][j] != 0):
                count -= 1
                self.mat[i][j] = 0
     
        return
 
    def printSudoku(self):
        for i in range(self.N):
            for j in range(self.N):
                print(self.mat[i][j], end=" ")
            print()
    
    def is_correct_solution(self, board):
        # check each row
        for i in range(self.N):
            if sorted(board[i]) != list(range(1, self.N + 1)):
                return False
        # check each column
        for j in range(self.N):
            if sorted([board[i][j] for i in range(self.N)]) != list(range(1, self.N + 1)):
                return False
        # check each box
        for i in range(0, self.N, self.SRN):
            for j in range(0, self.N, self.SRN):
                box = []
                for x in range(i, i + self.SRN):
                    for y in range(j, j + self.SRN):
                        box.append(board[x][y])
                if sorted(box) != list(range(1, self.N + 1)):
                    return False
        return True
    
    def solve(self, callback=None):
        self.solve_sudoku(0, 0, callback)

    def solve_sudoku(self, i=0, j=0, callback=None):
        if i == 9:
            i = 0
            j += 1
            if j == 9:
                return True

        if self.mat[i][j] > 0:
            return self.solve_sudoku(i + 1, j, callback)

        for num in range(1, 10):
            if self.checkIfSafe(i, j, num):
                self.mat[i][j] = num
                if callback:
                    callback(self.mat, i, j, True)
                time.sleep(0.25)  # This is where the delay occurs

                if self.solve_sudoku(i + 1, j, callback):
                    return True

                # if no number can be placed, undo and try again
                if callback:
                    callback(self.mat, i, j, False)  # False indicates this is a backtrack move
                self.mat[i][j] = 0
                time.sleep(0.25)  # This is where the delay occurs

        return False

class SudokuCell(TextInput):
    def __init__(self, number=0, **kwargs):
        super(SudokuCell, self).__init__(**kwargs)
        self.multiline = False
        if number != 0:
            self.text = str(number)
            self.readonly = True  # numbers provided by the puzzle are read-only
        else:
            self.text = ''

    def insert_text(self, substring, from_undo=False):
        if len(substring) > 1 or not substring.isdigit() or not 1 <= int(substring) <= 9:
            return
        return super(SudokuCell, self).insert_text(substring, from_undo=from_undo)

class MainMenu(Screen):
    def __init__(self, **kwargs):
        super(MainMenu, self).__init__(**kwargs)
        self.layout = GridLayout(cols=1)

        # Add PyDoKu Label
        self.layout.add_widget(Label(text='PyDoKu'))

        # New Puzzle button
        self.new_puzzle = Button(text='New Puzzle')
        self.new_puzzle.bind(on_release=self.new_puzzle_pressed)
        self.layout.add_widget(self.new_puzzle)

        # Load Puzzle button
        self.load_puzzle = Button(text='Load Puzzle')
        self.load_puzzle.bind(on_release=self.load_puzzle_pressed)
        self.layout.add_widget(self.load_puzzle)

        # Help button
        self.help = Button(text='Help')
        self.help.bind(on_release=self.help_pressed)
        self.layout.add_widget(self.help)

        # Exit button
        self.exit = Button(text='Exit')
        self.exit.bind(on_release=self.exit_pressed)
        self.layout.add_widget(self.exit)

        self.add_widget(self.layout)

    def new_puzzle_pressed(self, instance):
        self.manager.transition.direction = 'left'
        self.manager.current = 'sudoku_puzzle'

    def load_puzzle_pressed(self, instance):
        self.manager.get_screen('sudoku_puzzle').load_puzzle_pressed()
        self.manager.transition.direction = 'left'
        self.manager.current = 'sudoku_puzzle'

    def help_pressed(self, instance):
        self.manager.transition.direction = 'left'
        self.manager.current = 'help_screen'

    def exit_pressed(self, instance):
        print('Exit button pressed')
        App.get_running_app().stop()


class SudokuPuzzle(Screen):
    def __init__(self, **kwargs):
        super(SudokuPuzzle, self).__init__(**kwargs)
        self.layout = GridLayout(cols=9)

        # Generate a new Sudoku puzzle
        self.sudoku = Sudoku(9, 40)

        # Create a 9x9 Sudoku board of text input boxes
        self.sudoku_board = [[SudokuCell(self.sudoku.mat[i][j]) for j in range(9)] for i in range(9)]
        for row in self.sudoku_board:
            for cell in row:
                self.layout.add_widget(cell)

        #... (SudokuPuzzle class methods would go here, not displayed due to space limitation)
        # Check Solution button
        self.check_solution = Button(text='Check Solution')
        self.check_solution.bind(on_release=self.check_solution_pressed)
        self.layout.add_widget(self.check_solution)

        # Solve Puzzle button
        self.solve_puzzle = Button(text='Solve Puzzle')
        self.solve_puzzle.bind(on_release=self.solve_puzzle_pressed)
        self.layout.add_widget(self.solve_puzzle)

        # Save Puzzle button
        self.save_puzzle = Button(text='Save Puzzle')
        self.save_puzzle.bind(on_release=self.save_puzzle_pressed)
        self.layout.add_widget(self.save_puzzle)

        # Back button
        self.back = Button(text='Back')
        self.back.bind(on_release=self.back_pressed)
        self.layout.add_widget(self.back)

        self.add_widget(self.layout)

    def visualize_solve(self):
        # Define a function that will be run on a different thread
        def run_solve_method():
            # Solve the Sudoku puzzle with visualization
            self.sudoku.solve(self.update_cell)

        # Start a new thread that runs the above function
        threading.Thread(target=run_solve_method).start()

    def update_cell(self, mat, i, j, is_correct):
        # Schedule the update_ui method to be run on the main thread
        Clock.schedule_once(lambda dt: self.update_ui(mat, i, j, is_correct))

    def update_ui(self, mat, i, j, is_correct):
        # Update the text and color of the cell
        self.sudoku_board[i][j].text = str(mat[i][j])
        self.sudoku_board[i][j].background_color = (0, 1, 0, 1) if is_correct else (1, 0, 0, 1)

        # Reset the color of the cell after a delay
        Clock.schedule_once(lambda dt: self.reset_color(i, j), 0.25)

    def reset_color(self, i, j):
        self.sudoku_board[i][j].background_color = (1, 1, 1, 1)

    def solve_puzzle_pressed(self, instance):
        self.visualize_solve()

    def back_pressed(self, instance):
        self.manager.transition.direction = 'right'
        self.manager.current = 'main_menu'
    
    def check_solution_pressed(self, instance):
        board = [[int(cell.text) if cell.text.isdigit() else 0 for cell in row] for row in self.sudoku_board]
        if self.sudoku.is_correct_solution(board):
            print('Congratulations! Your solution is correct.')
        else:
            print('Oops! Your solution is not correct. Keep trying.')

    def save_puzzle_pressed(self, instance):
        board = [[{'number': int(cell.text) if cell.text.isdigit() else 0, 'readonly': cell.readonly} for cell in row] for row in self.sudoku_board]
        with open('sudoku_save.json', 'w') as f:
            json.dump(board, f)
        print('Game Saved!')

    def load_puzzle_pressed(self):
        with open('sudoku_save.json', 'r') as f:
            loaded_board = json.load(f)
        for i, row in enumerate(loaded_board):
            for j, cell_data in enumerate(row):
                self.sudoku_board[i][j].text = str(cell_data['number']) if cell_data['number'] != 0 else ''
                self.sudoku_board[i][j].readonly = cell_data['readonly']
        print('Game Loaded!')

    def highlight_cells(self, cells, color):
        for cell in cells:
            cell.background_color = color

    def find_conflicts(self, board):
        conflicts = []
        for i in range(9):
            for j in range(9):
                value = board[i][j]
                if value == 0:  # cell is empty
                    conflicts.append(self.sudoku_board[i][j])
                else:
                    # check the row
                    for x in range(9):
                        if board[i][x] == value and x != j:
                            conflicts.append(self.sudoku_board[i][x])
                            conflicts.append(self.sudoku_board[i][j])
                    
                    # check the column
                    for y in range(9):
                        if board[y][j] == value and y != i:
                            conflicts.append(self.sudoku_board[y][j])
                            conflicts.append(self.sudoku_board[i][j])

                    # check the box
                    box_start_row, box_start_col = i - i % 3, j - j % 3
                    for x in range(3):
                        for y in range(3):
                            cur_x, cur_y = box_start_row + x, box_start_col + y
                            if board[cur_x][cur_y] == value and (cur_x != i or cur_y != j):
                                conflicts.append(self.sudoku_board[cur_x][cur_y])
                                conflicts.append(self.sudoku_board[i][j])
        return list(set(conflicts))  # remove duplicates

    def reset_colors(self):
        for row in self.sudoku_board:
            for cell in row:
                cell.background_color = (1, 1, 1, 1)

    def check_solution_pressed(self, instance):
        board = [[int(cell.text) if cell.text.isdigit() else 0 for cell in row] for row in self.sudoku_board]
        if self.sudoku.is_correct_solution(board):
            self.highlight_cells([cell for row in self.sudoku_board for cell in row], (0, 1, 0, 1))
        else:
            conflicts = self.find_conflicts(board)
            self.highlight_cells(conflicts, (1, 0, 0, 1))
        Clock.schedule_once(lambda dt: self.reset_colors(), 2)  # Reset colors after 2 seconds
        

class HelpScreen(Screen):
    def __init__(self, **kwargs):
        super(HelpScreen, self).__init__(**kwargs)
        self.layout = GridLayout(cols=1)

        # Add Help information
        help_text = ("Welcome to PyDoKu!\n\n"
                     "This is a simple Sudoku game where you can test your Sudoku skills.\n\n"
                     "Here's how you play:\n\n"
                     "- The objective is to fill a 9x9 grid so that each column, each row,\n"
                     "  and each of the nine 3x3 boxes contains the digits from 1 to 9.\n"
                     "- You can't repeat any digit within the same row, column, or 3x3 box.\n\n"
                     "Good luck!")
        self.layout.add_widget(Label(text=help_text))

        # Back button
        self.back = Button(text='Back')
        self.back.bind(on_release=self.back_pressed)
        self.layout.add_widget(self.back)

        self.add_widget(self.layout)

    def back_pressed(self, instance):
        self.manager.transition.direction = 'right'
        self.manager.current = 'main_menu'


class PyDoKuApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(MainMenu(name='main_menu'))
        sm.add_widget(SudokuPuzzle(name='sudoku_puzzle'))
        sm.add_widget(HelpScreen(name='help_screen'))  # add this line

        return sm


if __name__ == "__main__":
    PyDoKuApp().run()