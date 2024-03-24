

def isSubsetWithArithmetic(word_indices, target):
    dp = {0: ""}
    for word, index in word_indices:
        num = len(word)
        new_dp = {}
        for val, equation in dp.items():
            # Addition
            new_val = val + num
            new_dp[new_val] = f"{equation} + {word}" if equation else word
            # Subtraction
            new_val = val - num
            new_dp[new_val] = f"{equation} - {word}" if equation else f"-{word}"
            # Multiplication
            new_val = val * num
            new_dp[new_val] = f"({equation}) * {word}" if equation else word
            if num != 0 and val % num == 0:  # Avoid division by zero
                # Division
                new_val = val // num
                new_dp[new_val] = f"({equation}) / {word}" if equation else word
        dp = new_dp
    
    if target in dp:
        print("Equation:", dp[target], "=", target)
        
        return True
    else:
        return False

# Example usage:
sentences = [
    "This is a sample sentence for demonstration purposes.",
    "Another example sentence with more words to demonstrate.",
    "A short sentence."
]

for sentence in sentences:
    print("\nAnalyzing sentence:", sentence)
    word_indices = [(word, index) for index, word in enumerate(sentence.lower().split())]
    for i in range(10):
        target = i+1
        if isSubsetWithArithmetic(word_indices, target):
            print("Subset with the given target value exists")
        else:
            print("No subset with the given target value exists")
