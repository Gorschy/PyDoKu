I want you to create a Sudoku back tracking algorithm visalizer in Python using kivy. It should have the following features
- A mainmenu containing a title PyDoKu, a button 'New Puzzle', another button 'Load Puzzle', another button 'Help' and a final button 'Exit'
- The New Puzzle button should generate a complete Sudoku Puzzle, remove values from the puzzle to create an incomplete sudoku puzzle and then display that to the user.
- The puzzle screen should have a solve button, a save button and a back button.
- The solve button will solve the puzzle using a backtracking algorithm and visualize the process to the user.
- The save button should save the puzzle to be loaded at another point in time.
- The back button should take the user back to the main menu.
- The load button should display a list of saved puzzles that the user can load.
- The help button should contain basic information on how to play sudoku, and also have a difficulty selector that adjusts how many values are removed from the puzzle when it is generated.
- The exit button should close down the application.

ToDo
- Help 
    - Information on the project & how to play sudoku (done)
- Save/Load puzzle 
    - Save a puzzle into a datatype maybe json (done)
    - Need to separate user inputs from the puzzles starting values (done)
- Check solution 
    - Should highlight errors (done)
- New puzzle
    - Difficulty setting
    - Display starting values some other way