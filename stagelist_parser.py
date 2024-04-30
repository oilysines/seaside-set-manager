import os
import re

path = os.getcwd()

#extracting stagelist data
stagelist = open(r'%s/Stagelist.txt' % path)

starters = []

stagefix = ','.join(stagelist)

starter1 = re.findall(r'(?<=Starters:\W)[a-zA-Z\W]+(?=\W\WCounterpicks:)',stagefix)[0]

starter1 = starter1.replace(r',','')

starters = starter1.split('\n')
starters = list(filter(None, starters))

startercount = len(starters)

# ban patterns
_1pattern = [0]
_2pattern = [1]
_3pattern = [1,1]
_4pattern = [1,2]
_5pattern = [1,2,1]
_6pattern = [1,2,1,1]
_7pattern = [1,2,2,1]

def patt(x):
    return globals()[f'_{x}pattern']

