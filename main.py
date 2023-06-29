import kivy
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.clock import Clock
import random, math, threading
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

    def solve_sudoku(self, i, j, callback=None):
        if i == self.N - 1 and j == self.N:
            return True

        if j == self.N:
            i += 1
            j = 0

        if self.mat[i][j] != 0:
            return self.solve_sudoku(i, j + 1, callback)

        for num in range(1, self.N + 1):
            if self.checkIfSafe(i, j, num):
                self.mat[i][j] = num
                if callback:
                    callback(self.mat, i, j, True)
                if self.solve_sudoku(i, j + 1, callback):
                    return True

                # if no number can be placed, undo and try again
                self.mat[i][j] = 0
                if callback:
                    callback(self.mat, i, j, False)
                # Schedule the next invocation instead of sleeping
                Clock.schedule_once(lambda dt: self.solve_sudoku(i, j, callback), 0.1)

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
        print('Load Puzzle button pressed')

    def help_pressed(self, instance):
        print('Help button pressed')

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
        Clock.schedule_once(lambda dt: self.reset_color(i, j), 0.5)

    def reset_color(self, i, j):
        self.sudoku_board[i][j].background_color = (1, 1, 1, 1)

    def solve_puzzle_pressed(self, instance):
        self.visualize_solve()

    def save_puzzle_pressed(self, instance):
        print('Save Puzzle button pressed')

    def back_pressed(self, instance):
        self.manager.transition.direction = 'right'
        self.manager.current = 'main_menu'
    
    def check_solution_pressed(self, instance):
        board = [[int(cell.text) if cell.text.isdigit() else 0 for cell in row] for row in self.sudoku_board]
        if self.sudoku.is_correct_solution(board):
            print('Congratulations! Your solution is correct.')
        else:
            print('Oops! Your solution is not correct. Keep trying.')


class PyDoKuApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(MainMenu(name='main_menu'))
        sm.add_widget(SudokuPuzzle(name='sudoku_puzzle'))

        return sm

if __name__ == "__main__":
    PyDoKuApp().run()