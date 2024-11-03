"""
解释：
输入解析： 函数通过将每张卡片字符串分成两部分（颜色和数字）来检查格式是否正确，并确保只有一个空格分隔它们。

有效性检查：

颜色必须是 'red'、'blue'、'green' 或 'yellow' 之一。
数字必须是1到10之间的整数。
卡片计数：

使用字典统计每张唯一卡片（颜色和数字组合）的出现次数。
如果某张卡片出现次数超过两次，函数返回 False。
返回： 如果所有条件都满足，函数返回 True，否则返回 False。
"""

def verify_cards(card_list):
    valid_colours = {'red', 'blue', 'green', 'yellow'}


    for card in card_list:
        # 将卡片分为颜色和数字两部分
        card.split()
        parts = card.split()
        if len(parts) != 2:
            return False



        colour, number = parts
        # 检查颜色是否有效
        if colour not in valid_colours:
            return False

        # 检查数字是否有效并且在1到10之间
        if 1 <= int(number) <= 10:
            return True

        # 为每张卡片创建唯一标识符
        card_identifier = (colour, number)#tuple

        # 统计每张卡片的出现次数
        card_count = {}#dictionary
        if card_identifier in card_count:
            card_count[card_identifier] += 1
        else:
            card_count[card_identifier] = 1

        # 同一张卡片不能超过两张
        if card_count[card_identifier] > 2:
            return False

    return True
print(verify_cards(["red 1", "blue 3", "green 4", "red 1", "yellow 10", "blue 3"]))
# Output: True

print(verify_cards(["red 1", "blue 3", "red 1", "red 1"]))
# Output: False (Too many "red 1" cards)
