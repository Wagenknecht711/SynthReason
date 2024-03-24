def isSubsetWithArithmetic(nums, target):
    dp = {0: ""}
    for num in nums:
        new_dp = {}
        for val, equation in dp.items():
            # Addition
            new_val = val + num
            new_dp[new_val] = f"{equation} + {num}" if equation else str(num)
            # Subtraction
            new_val = val - num
            new_dp[new_val] = f"{equation} - {num}" if equation else f"-{num}"
            # Multiplication
            new_val = val * num
            new_dp[new_val] = f"({equation}) * {num}" if equation else str(num)
            if num != 0 and val % num == 0:  # Avoid division by zero
                # Division
                new_val = val // num
                new_dp[new_val] = f"({equation}) / {num}" if equation else str(num)
        dp = new_dp
    
    if target in dp:
        print("Equation:", dp[target], "=", target)
        return True
    else:
        return False

# Example usage:
nums = [3, 34, 4, 12, 5, 2]
target = 9
if isSubsetWithArithmetic(nums, target):
    print("Subset with the given target value exists")
else:
    print("No subset with the given target value exists")
