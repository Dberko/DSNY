# Draw a decision tree:
#      1           2         3
#   2  3  4      3 4 5     4 5 6
# 3 4 5
# Say n == 3. The number of paths to 3 represents the number of distinct ways that the bunny can hop to reach 3 steps. res = 4.
# Notice the overlapping sub-problems. Why compute the sub tree for 2 twice? Use DP.
# dp[i], distinct number of ways to reach the ith step
# Base Case: n == 0: 0, n == 1: 1, n == 2: 2, n == 3: 4
# Recursive Case: dp[i] = dp[i - 1] + dp[i - 2] + dp[i - 3]
# Time: O(n), Space: O(n)

def bunnyHops(n):
    if n < 0:
        return -1
    if n == 0:
        return 0
    if n == 1:
        return 1
    if n == 2:
        return 2
    if n == 3:
        return 4

    def topDown():
        dp = {}
        dp[0] = 0
        dp[1] = 1
        dp[2] = 2
        dp[3] = 4

        def dfs(n):
            if n in dp:
                return dp[n]
            dp[n] = dfs(n-1) + dfs(n-2) + dfs(n-3)
            return dp[n]
        return dfs(n)

    def bottomUp():
        dp = [0] * (n + 1)
        dp[0] = 0
        dp[1] = 1
        dp[2] = 2
        dp[3] = 4
        for i in range(4, n + 1):
            dp[i] = dp[i - 1] + dp[i - 2] + dp[i - 3]
        return dp[-1]
    return bottomUp()


def main():
    assert(bunnyHops(-1) == -1)
    assert(bunnyHops(0) == 0)
    assert(bunnyHops(1) == 1)
    assert(bunnyHops(2) == 2)
    assert(bunnyHops(3) == 4)
    assert(bunnyHops(4) == 7)
    assert(bunnyHops(5) == 13)
    assert(bunnyHops(6) == 24)
    assert(bunnyHops(10) == 274)
    return


if __name__ == "__main__":
    main()
