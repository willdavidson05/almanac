import math 
# (-sum(p_i)log_2(p))
# entropy = -sum(p * math.log2(p) for p in probabilities if p > 0)
# p(x_i) = 1/loc
# entropy = sum * probability *math.log2(probability), what do i do for sum????
def calculate_shannon_entropy(loc_changes : int) -> int:
    probability = 1 / loc_changes
    entropy = -loc_changes * probability * math.log2(probability)
    print(entropy)
    return entropy
