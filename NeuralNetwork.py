import time, math, random, pygame, os, sys
from pygame.locals import *
pygame.init()

CREATURE_COUNT = 20
NEURON_COUNT = 4
STEPS_PER_SIMULATION = 1
CHANCE_OF_MUTATION = .5
AMMOUNT_OF_MUTATION = 2
SECONDS_TO_RUN = 2
INITIAL_ERROR = 10**4
inputDataSet = [1, 2, 3]
outputDataSet = [10, 20, 30]

class creature:
     def __init__(self, noOfNeurons):
          self.error = INITIAL_ERROR
          self.neuronList = list()
          self.synapseList = list()
          for n in range(noOfNeurons):
               X = int(320+200*math.cos(n*2*math.pi/(noOfNeurons)))
               Y = int(240+200*math.sin(n*2*math.pi/(noOfNeurons)))
               if (n == 0):
                    color = (50,255,0)
               elif (n == 1):
                    color = (255,50,0)
               else:
                    color = (random.randint(0,200),random.randint(0,200),random.randint(0,255))
               radius = 15
               self.neuronList.append(neuron(X,Y, color, radius))
          for n in self.neuronList:
               for l in self.neuronList:
                    self.synapseList.append(synapse(n,l))

class neuron:
     def __init__(self, X, Y, color, radius):
          self.X = X
          self.Y = Y
          self.boxThreshold = random.random()
          self.inbox = random.random()
          self.box = random.random()
          self.color = color
          self.radius = radius
          self.time = 0
          self.timeThreashold = random.randint(0,4)
          self.fireStrength = random.random()
          self.boxDrain = random.random()

class synapse:
     def __init__(self, N1, N2):
          self.neuron1 = N1
          self.neuron2 = N2
          self.color = (0,0,0)
          self.weight = random.random()

def drawCreature(creature):
     screen = pygame.display.set_mode((640,480))
     screen.fill((255,255,255))
     
     for n in creature.neuronList:
          n.X = int(320+200*math.cos(creature.neuronList.index(n)*2*math.pi/(len(creature.neuronList))))
          n.Y = int(240+200*math.sin(creature.neuronList.index(n)*2*math.pi/(len(creature.neuronList))))

     synapseMinWeight = creature.synapseList[0].weight
     synapseMaxWeight = creature.synapseList[0].weight
     for s in creature.synapseList:
        synapseMinWeight = min(synapseMinWeight,s.weight)
        synapseMaxWeight = max(synapseMaxWeight,s.weight)

     neuronMinStrength = creature.neuronList[0].fireStrength
     neuronMaxStrength = creature.neuronList[0].fireStrength
     for n in creature.neuronList:
        neuronMinStrength = min(neuronMinStrength,n.fireStrength)
        neuronMaxStrength = max(neuronMaxStrength,n.fireStrength)
     print "NMinS=", neuronMinStrength
     print "NMaxS=", neuronMaxStrength
     print "difference=", neuronMaxStrength-neuronMinStrength

     for s in creature.synapseList:
          normalizedMultiplier = (s.weight - synapseMinWeight)/(synapseMaxWeight - synapseMinWeight)
          brightness = int(255 * normalizedMultiplier)
          pygame.draw.line(screen, (brightness,brightness,0), (s.neuron1.X, s.neuron1.Y), (s.neuron2.X, s.neuron2.Y), 1+int(6*normalizedMultiplier))

     for n in creature.neuronList:
          normalizedMultiplier == (n.fireStrength-neuronMinStrength)/(neuronMaxStrength-neuronMinStrength)
          print "nM = ", normalizedMultiplier
          n.radius = 5+int(20*normalizedMultiplier)
          brightness = int(255 * normalizedMultiplier)
          n.color = (0,brightness,brightness)

     for n in creature.neuronList:
          pygame.draw.circle(screen, n.color, (n.X,n.Y), n.radius)

          font = pygame.font.Font(None, 18)
          text1 = font.render(str(round(n.box,2)), 1, (10, 10, 10))
          text2 = font.render(str(round(n.fireStrength,2)), 1, (10, 10, 10))
          text3 = font.render("Top number is neuron value", 1, (10, 10, 10))
          text4 = font.render("Bottom number is neuron fire strength", 1, (10, 10, 10))
          textpos1 = text1.get_rect()
          textpos2 = text2.get_rect()
          textpos1.centerx = n.X
          textpos1.centery = n.Y
          textpos2.centerx = n.X
          textpos2.centery = n.Y+12
          screen.blit(text1, textpos1)
          screen.blit(text2, textpos2)
          screen.blit(text3, (0,0))
          screen.blit(text4, (0,12))
     pygame.display.update()

def stepCreature(creature):
     for n in creature.neuronList:
         # if (n.time > n.timeThreashold):
         #      if (n.box > n.boxThreshold):
          #=================
                    sList = findSynapses(creature,n)
                    for s in sList:
                         s.neuron2.inbox += n.fireStrength * s.weight * n.box
                    n.time = 0
                    n.box = 0
          #=================
     for n in creature.neuronList:
          n.time += 1
          n.box += n.inbox
          n.box = n.box * n.boxDrain
          n.inbox = 0
     return creature

def findSynapses (creature, neuron):
     sList = list()
     for s in creature.synapseList:
          if (s.neuron1 == neuron) :
               sList.append(s)
     return sList

def simulateCreature (creature, noOfSteps, inputNeuron, inputValue, outputNeuron, outputValue):
     for step in range(noOfSteps):
          creature.neuronList[inputNeuron].box = inputValue
          creature.neuronList[inputNeuron].inbox = 0
          creature = stepCreature(creature)
          creature.neuronList[inputNeuron].box = inputValue
          creature.neuronList[inputNeuron].inbox = 0
     creature.error += abs(outputValue - creature.neuronList[outputNeuron].box)
     creature.neuronList[inputNeuron].inbox = 0
     creature.neuronList[inputNeuron].box = inputValue
     #print creature.error
     return creature

def trainPopulation(population, inputDataSet, outputDataSet): #data sets are array of the same length
     for c in population:
          #if c.error == INITIAL_ERROR:
               c.error = 0
               for i in range(len(inputDataSet)):
                    inD = inputDataSet[i]
                    outD = outputDataSet[i]
                    c = simulateCreature(c, STEPS_PER_SIMULATION, 0, inD, 1, outD)
     return population

def mate (mother, father):
     child = creature(len(mother.neuronList))
     n = child.neuronList
     m = mother.neuronList
     f = father.neuronList
     for i in range(len(child.neuronList)):
          n[i].boxThreshold   = random.choice( [m[i].boxThreshold,   f[i].boxThreshold]   )
          n[i].fireStrength   = random.choice( [m[i].fireStrength,   f[i].fireStrength]   )
          n[i].boxDrain       = random.choice( [m[i].boxDrain,       f[i].boxDrain]       )
          n[i].timeThreashold = random.choice( [m[i].timeThreashold, f[i].timeThreashold] )

     s = child.synapseList
     m = mother.synapseList
     f = father.synapseList
     for i in range(len(child.synapseList)):
          s[i].weight = random.choice( [m[i].weight, f[i].weight] )

     return child

def mutatePopulation (population, chanceOfMutation, ammountOfMutation):
     for c in population:
          for n in c.neuronList:
               if (random.random() <= chanceOfMutation):
                    n.boxThreshold *= ammountOfMutation * random.random()
               if (random.random() <= chanceOfMutation):
                    n.fireStrength *= ammountOfMutation * random.random()
               if (random.random() <= chanceOfMutation):
                    n.boxDrain *= ammountOfMutation * random.random()
               if (random.random() <= chanceOfMutation):
                    n.timeThreashold += random.randint(-1,1)
          for s in c.synapseList:
               if (random.random() <= chanceOfMutation):
                    s.weight *= ammountOfMutation * random.random()
     return population


def generateStartingPopulation():
     population = list()
     for c in range( CREATURE_COUNT ):
          population.append( creature( NEURON_COUNT ) )
     return population

def getAvgErrorOfPopulation(population):
     summation = 0
     populationCount = len(population)
     for c in population:
          summation += c.error
     avgError = summation / populationCount
     return avgError

def pruneUnfitCreatures(population, avgError):
     for c in population:
          if (c.error > avgError):
            population.remove(c)
     return population

def repopulate(population):
     p = list(population)
     while (len(population) < CREATURE_COUNT):
          mother = random.choice( p )
          father = random.choice( p )
          if not (mother == father):
            population.append( mate( mother , father ) )
     return population

#create a list of creatures
population = generateStartingPopulation()
startTime = time.time()
stopTime = startTime+SECONDS_TO_RUN
runTime = stopTime - startTime
halfTime = startTime + runTime/2
now = time.time()

generations = 1
print "CHANCE OF MUTATION:", CHANCE_OF_MUTATION
print "AMMOUNT OF MUTATION:", AMMOUNT_OF_MUTATION
while now < stopTime:
     now = time.time()
     if now > halfTime:
          CHANCE_OF_MUTATION = CHANCE_OF_MUTATION /2
          #AMMOUNT_OF_MUTATION = AMMOUNT_OF_MUTATION /2
          halfTime = (halfTime + stopTime) / 2
          print "Generation: ", generations
          print "   chance of mutation:  ", CHANCE_OF_MUTATION
          print "   ammount of mutation: ", AMMOUNT_OF_MUTATION
          
     #print "generation:", generations
     generations+=1
     #mutate all properties of all creatures in population with CHANCE_OF_MUTATION
     popultion = mutatePopulation( population, CHANCE_OF_MUTATION, AMMOUNT_OF_MUTATION )
     #train all creatures on a data set
     population = trainPopulation(population, inputDataSet, outputDataSet)
     #find average error in population
     averageError = getAvgErrorOfPopulation(population)
     #remove creatures from population with below average error
     population = pruneUnfitCreatures(population, averageError)
     #crossbreed randomly chosen parents from the remaining population and append them to population until at CREATURE_COUNT
     population = repopulate(population)
print "Total Generations:", generations
bestCreature = population[0]
for c in population:
     if (c.error < bestCreature.error):
          bestCreature = c
bestCreature.neuronList[0].box = inputDataSet[0]
bestCreature.neuronList[0].inbox = 0
bestCreature = stepCreature(bestCreature)
bestCreature.neuronList[0].box = inputDataSet[0]
bestCreature.neuronList[0].inbox = 0
drawCreature(bestCreature)

# Event loop.

Index = 0
running = True
while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
            running = False
        elif event.type is pygame.KEYDOWN:
            keyname = pygame.key.name(event.key)
            if keyname == "space":
                  if Index < len(inputDataSet):
                    print "Input Data Index:", Index+1
                    simulateCreature (bestCreature, STEPS_PER_SIMULATION, 0, inputDataSet[Index], 1, outputDataSet[Index])
                    Index += 1
                  else:
                    Index = 0
                  drawCreature(bestCreature)

