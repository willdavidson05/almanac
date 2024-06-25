from scipy.stats import entropy
import math 
import pathlib 
from git_parser import calculate
def calculate_shannon_entropy(repo_path : pathlib.Path) -> int:


    # cal lthe calculate fucntion 
    pass
entropy = -sum(p * math.log2(p) for p in _ if p > 0)
# return entropy
