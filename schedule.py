import random;
import time;
start_time = time.time()

NoofCourses = int(input("Please enter the number of courses:")) # Total no of courses to make schedule for 
CoursesList=[]
for i in range(NoofCourses): #getting iput from user for the name of each cource 
    CoursesList.append(input(f"Please enter the name of course {i+1}:"))

NoofHalls = int(input("Please enter the number of available exam halls: ")) # Total no of halls to make schedule for 
NoofTimeSlots = int(input("Please enter the number of available time slots: ")) # Total no of available time slots
CourseConflict = []
SlotTime=int(input("Please enter the time duration of a slot: "))
ExamTime=int(input("please enter the time duration of a exam: "))
MaxHallTime=NoofTimeSlots*SlotTime
#Taking some constants from the given examples
Popsize = 100  # number of individuals in the population
numofgen = 100  # number of generations to run the genetic algorithm
Mutprob = 0.1  # probability of mutation for an offspring
Crossprob = 0.8  # probability of crossover for two parents
Parentsize = 5  # size of tournament for parent selection

# Taking a list of courses that has conflicts
for i in range(int(input("Please enter the number of conflicting pairs: "))):
    C1, C2, NoofStud = input("Please enter the code of courses with a conflict (separated by a space) and then the no. of students having the conflict: ").split()
    CourseConflict.append((C1, C2,NoofStud))


# Defining the possible solution representation i.e. a list of tuples (course, time_slot, hall)
def PossibleSolution():
    return [(C, random.randint(1, NoofTimeSlots), random.randint(1, NoofHalls)) for C in CoursesList]

def getStudents(c1,c2):
    for i in CourseConflict:
        if i[0]== c1 and i[1]==c2:
            return i[2]
        elif i[1]==c1 and i[0]==c2:
            return i[2]
    return 0
#Making a fitness function
def FitnessFunction(solution):
    conflicts = 0
    HallHours = [0] * NoofHalls
    print("Solution="+str(solution))
    for i in range(NoofCourses):
        for j in range(i+1, NoofCourses):
            if (i+1, j+1) not in CourseConflict and (j+1, i+1) not in CourseConflict:
                if solution[i][1] == solution[j][1] and solution[i][2] == solution[j][2]:
                    conflicts += 1
        HallHours[solution[i][2]-1] += 1
    penalty = sum(max(0, hours -NoofTimeSlots) for hours in HallHours)

    #checking for common students 
    for i in solution:
        for j in solution:
            if i[0]!=j[0] and i[1]==j[1]:
                penalty+=(10*(int(getStudents(i[0],j[0]))))/2 
    
    #checking for exceeding time
    if ExamTime>SlotTime:
       penalty+= NoofCourses*100
    
    
    print(penalty)
    return conflicts + penalty

# Defining the genetic algorithm functions by first initializing the initial population
def InitialPopulation(Popsize):
    return [PossibleSolution() for i in range(Popsize)]

#Making a Parent selection
def ParentSelection(Pop, Parentsize):
    SelectedParent = []
    for i in range(len(Pop)):
        Parent = random.sample(Pop, Parentsize)
        Winner = min(Parent, key=lambda x: FitnessFunction(x))
        SelectedParent.append(Winner)
    return SelectedParent

#Crossover Point code and making chromosomes out of it
def Crossover(parent1, parent2, Crossprob):
    if random.random() < Crossprob:
        Crosspoint = random.randint(1, len(parent1)-1)
        chromosome1 = parent1[:Crosspoint] + parent2[Crosspoint:]
        chromosome2 = parent2[:Crosspoint] + parent1[Crosspoint:]
        return chromosome1, chromosome2
    else:
        return parent1, parent2
    
#Mutating the solutions 
def Mutation(solution, Mutprob):
    Mutated = list(solution)
    for i in range(len(Mutated)):
        if random.random() < Mutprob:
            Mutated[i] = (Mutated[i][0], random.randint(1, NoofTimeSlots), random.randint(1, NoofHalls))
    return Mutated

def GeneticAlgo(Popsize, Parentsize, Crossprob, Mutprob, numofgen):
    population = InitialPopulation(Popsize)
    for i in range(numofgen):
        SelectedParent = ParentSelection(population, Parentsize)
        offspring = []
        for j in range(0, len(SelectedParent), 2):
            if j+1 < len(SelectedParent):
                chromosome1, chromosome2 = Crossover(SelectedParent[j], SelectedParent[j+1], Crossprob)
                offspring.append(Mutation(chromosome1, Mutprob))
                offspring.append(Mutation(chromosome2, Mutprob))
        population = SelectedParent + offspring
    bestsolution = min(population, key=lambda x: FitnessFunction(x))
    return bestsolution, FitnessFunction(bestsolution)

[Bestsolution,FitnessValue]=GeneticAlgo(100,5,0.5,0.2,2)
print("Best Solution:")
print(Bestsolution)
print("Fitness Value")
print(FitnessValue)
end_time = time.time()

execution_time = end_time - start_time
print(f"Execution time: {execution_time} seconds")