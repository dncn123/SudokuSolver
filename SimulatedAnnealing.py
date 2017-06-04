from collections import Counter
import numpy as np

class SimAnn(object):
    def __init__(self, quiz, method = 'switch2', c=0.9):
        self.sqsubset = self.get_sqsubset()
        self.c = c ## factor to reduce temp by
        self.quizoriginal = quiz
        self.method = method ## method to select next quiz
        self.fitness_tracked = []
        self.new_quiz = np.zeros((9,9))
        self.current_quiz = self.starting_quiz()
        self.current_error = self.get_error(self.current_quiz)
        self.starting_temp = 150.0

    ## This is used to subset the array into the 9 smaller squares it is made up of
    def get_sqsubset(self):
        sqsubset = np.zeros((9,9,9))
        sqsubset[0,:3,:3] = 1
        sqsubset[1,:3,3:6] = 1
        sqsubset[2,:3,6:9] = 1
        sqsubset[3,3:6,:3] = 1
        sqsubset[4,3:6,3:6] = 1
        sqsubset[5,3:6,6:9] = 1
        sqsubset[6,6:9,:3] = 1
        sqsubset[7,6:9,3:6] = 1
        sqsubset[8,6:9,6:9] = 1
        return sqsubset==1
    
    ## Set initial quiz
    def starting_quiz(self):
        init_quiz = self.quizoriginal.copy()
        for sub in self.sqsubset:
            s = set(init_quiz[sub].flatten())
            inputs = []
            for j in range(1,10):
                if j not in s:
                    inputs.append(j)
            inputs = np.array(inputs)
            np.random.shuffle(inputs)
            sset = sub&(self.quizoriginal==0)
            init_quiz[sset] = inputs
        return init_quiz
    
    ## Count the number of repeats in rows and columns of quiz to get idea of quiz fitness
    def get_error(self, quiz):
        error = 0
        #rows 
        for row in quiz:
            c = Counter(row)
            c = np.array(list(c.values()))
            error += sum(c[c>1])
        #columns
        for col in quiz.T:
            c = Counter(col)
            c = np.array(list(c.values()))
            error += sum(c[c>1])
        return error
    
    ## The two methods for picking next solution 
    ## Note that shuffle cell reduces the error quickly but doesn't 
    ## manage to get over the line
    def propose_quiz(self):
        self.new_quiz = self.current_quiz.copy()
        if self.method == 'shufflecell':
            sset = self.sqsubset[np.random.randint(0,9),:,:]\
                            &(self.quizoriginal==0)
            shuf = self.current_quiz[sset]
            np.random.shuffle(shuf)
            self.new_quiz[sset] = shuf
        elif self.method == 'switch2':
            sset = self.sqsubset[np.random.randint(0,9),:,:]\
                            &(self.quizoriginal==0)
            switchtemp = self.new_quiz[sset].copy()
            swaps = np.random.randint(0,sset.sum(),2)
            switchtemp[swaps[0]], switchtemp[swaps[1]] \
                    = switchtemp[swaps[1]], switchtemp[swaps[0]]
            self.new_quiz[sset] = switchtemp
        self.new_quiz = self.new_quiz.astype(int)
 
    def run(self, times = 100):
        self.fitness_tracked.append(self.current_error)
        T = self.starting_temp
        for i in range(times):
            self.propose_quiz()
            error = self.get_error(self.new_quiz)
            if error == 0:
                print("We have our solution!")
                print()
                print(self.new_quiz)
                break
            elif (error < self.current_error):
                self.current_quiz = self.new_quiz.copy()
                self.current_error = error
            elif np.exp((self.current_error - error)/T) > \
                        np.random.rand():
                self.current_quiz = self.new_quiz.copy()
                self.current_error = error
            self.fitness_tracked.append(self.current_error)
            T = self.c*T




























