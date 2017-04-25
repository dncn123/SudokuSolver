import numpy as np
import zipfile
import os
         
fantasy_zip = zipfile.ZipFile('sudoku.zip')
fantasy_zip.extractall()
fantasy_zip.close()

## Loading code from kaggle where sudoku data came from
quizzes = np.zeros((1000000, 81), np.int32)
solutions = np.zeros((1000000, 81), np.int32)
for i, line in enumerate(open('sudoku.csv', 'r').read().splitlines()[1:]):
    quiz, solution = line.split(",")
    for j, q_s in enumerate(zip(quiz, solution)):
        q, s = q_s
        quizzes[i, j] = q
        solutions[i, j] = s
quizzes = quizzes.reshape((-1, 9, 9))
solutions = solutions.reshape((-1, 9, 9))
np.save("quizzes", quizzes)
np.save("solutions", solutions)
os.remove("sudoku.csv")
