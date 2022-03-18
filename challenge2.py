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
    assert(bunnyHops(4) == 7)
    assert(bunnyHops(5) == 13)
    return


if __name__ == "__main__":
    main()
