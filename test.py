class Solution:
    def twoSum(self, nums, target):
        res = []
        for i in range(len(nums)):
            if res and target - nums[res[0]] == nums[i]:
                res.append(i)
                return res
            if target - nums[i] in nums:
                res.append(i)


s = Solution()
print(s.twoSum([3, 2, 4], 6))
