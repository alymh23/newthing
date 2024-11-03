class Card:
    def __init__(self, colour, number):
        assert isinstance(number, int)#是用于检查变量类型的断言语句。它的作用是确保 number 变量是整数类型 (int)。
        self.colour = colour
        self.number = number

    def __str__(self):
        return f'{self.colour} {self.number}'
class CollectionOfCards:
    def __init__(self,card_list):
        self.collection=[]#self.collection = [Card(colour, int(number)) for colour, number in (card.split() for card in card_strings)]
        for card in card_list:
            card_strings=card.split()
            colour, number = card_strings[0], int(card_strings[1])  # 获取颜色和数字，并将数字转换为整数
        # 创建 Card 对象并添加到集合中
            self.collection.append(Card(colour, number))
    def is_valid_group(self):
        # 检查同色连续数字的序列
        same_colour = {}#{same_colour:different_number}
        for card in self.collection:
            if card.colour not in same_colour:
                same_colour[card.colour] = []
            same_colour[card.colour].append(card.number)
        # 遍历颜色分组，检查是否存在同色连续数字的有效组
        # for numbers in same_colour.values():
        #     numbers.sort()
        #     for i in range(len(numbers) - 2):  # 用 len(numbers) - 2 可以保证循环在遍历时，剩余的元素足够我们取到三个连续的数字进行比较，这样可以避免索引超出范围导致的错误。
        #         if numbers[i] + 1 == numbers[i + 1] and numbers[i + 1] + 1 == numbers[i + 2]:
        #             return True
        for numbers in same_colour.values():
            numbers.sort()
            consecutive_count=1
            for i in range(1,len(numbers)):
                if numbers[i] == numbers[i-1]+1:
                    consecutive_count+=1
                    if consecutive_count>=3:
                        return True
                else:
                    consecutive_count=1

        # 检查同数不同色的组合
        same_number = {}#{same_numbers:different_colour}
        for card in self.collection:
            if card.number not in same_number:
                same_number[card.number] = set()
            same_number[card.number].add(card.colour)

        # 遍历数字分组，检查是否存在同数不同色的有效组
        if len(same_number) == 1:
            colours = list(same_number.values())[0]
            if len(colours) == len(self.collection) and len(colours) >= 3:
                return True
        # 若不符合任何有效组条件，返回 False
        return False

    def find_valid_group(self):
        # 查找是否存在一个有效的组合
        n = len(self.collection)
        for i in range(1, n + 1):
            for j in range(n - i + 1):
                subset=self.collection[j:j+i]
                if CollectionOfCards([str(card) for card in subset]).is_valid_group():
                    return subset
        return None

    def find_largest_valid_group(self):
        if not self.collection:
            return None

            # 记录最长序列
        longest_seq = []
        # 使用字典存储按颜色分组的卡片
        colour_groups = {}
        # 使用集合存储数字
        seen_numbers = set()

        for card in self.collection:
            if card.colour not in colour_groups:
                colour_groups[card.colour] = []
            colour_groups[card.colour].append(card)

            # 如果数字已经见过，直接加入
            if card.number in seen_numbers:
                continue
            seen_numbers.add(card.number)

            # 检查相同花色的连续序列
            current_seq = []
            for colour, cards in colour_groups.items():
                cards.sort(key=lambda x: x.number)
                current_seq = []
                for i in range(len(cards)):
                    # 如果当前卡牌不连续，则进入 else 语句，表示连续序列被打断。
                    # 首先检查current_seq的长度是否比longest_seq长。如果是，则将current_seq更新为longest_seq，表示找到了一个更长的连续序列。
                    # 然后，将current_seq重置为包含当前卡牌cards[i]的新序列，从该卡牌开始重新计数新的连续序列。
                    if i == 0 or cards[i].number == cards[i - 1].number + 1:
                        current_seq.append(cards[i])
                        # 在 else 中，首先检查current_seq的长度是否比longest_seq长。如果是，则将
                        # current_seq更新为longest_seq，表示找到了一个更长的连续序列。然后，将
                        # current_seq重置为包含当前卡牌cards[i]的新序列，从该卡牌开始重新计数新的连续序列。
                        # 检查剩余的连续序列：在每次遍历颜色的卡牌列表结束后，检查
                        # current_seq是否比longest_seq长，以确保最后一段连续序列（如果是最长的）也能被记录。
                    else:
                        if len(current_seq) > len(longest_seq):
                            longest_seq = current_seq
                        current_seq = [cards[i]]
                if len(current_seq) > len(longest_seq):
                    longest_seq = current_seq

        # 检查不同花色但数字相同的序列
        for number in seen_numbers:
            current_seq = [card for card in self.collection if card.number == number]
            if len(current_seq) > len(longest_seq):
                longest_seq = current_seq

        # 返回找到的最长序列
        if longest_seq:
            return CollectionOfCards([str(card) for card in longest_seq]).collection

        return None
    def can_form_valid_group_with_card(self, new_card):
        """判断加一张新牌后是否能形成有效组"""
        # 创建一个新的手牌集合，包含已有的牌和新加的牌
        new_hand = CollectionOfCards(self.collection.copy())
        new_hand.collection.append(new_card)

        # 检查新的手牌是否形成有效组
        if new_hand.is_valid_group():
            return new_hand
        return None

    def find_valid_new_group(self):
        """查找可以形成有效组的所有可能新牌"""
        valid_groups = []
        for colour in ['red', 'blue', 'green', 'yellow']:
            for number in range(1, 11):
                card = Card(colour, number)
                if self.can_form_valid_group_with_card(card):
                    valid_groups.append(card)

        return CollectionOfCards([f"{c.colour} {c.number}" for c in valid_groups]).collection

# print(CollectionOfCards(['red 6', 'blue 8']).is_valid_group())
# False
# False
# print(CollectionOfCards(['red 6', 'blue 6', 'yellow 6']).is_valid_group())
# True
# True
# print(CollectionOfCards(['red 6', 'blue 6', 'yellow 6', 'blue 7']).is_valid_group())
# False
# False
# print(card_groups_equal(CollectionOfCards(['red 6', 'blue 6', 'yellow 6', 'blue 7']).find_valid_group(), [Card('red', 6), Card('blue', 6), Card('yellow', 6)]))
# True
# True
# print(CollectionOfCards(['red 6', 'blue 6', 'blue 6', 'blue 7']).find_valid_group() is None)
# True
# True
# print(card_groups_equal(CollectionOfCards(['red 6', 'blue 6', 'yellow 6', 'green 7', 'green 6', 'green 5']).find_largest_valid_group(), [Card('red', 6), Card('blue', 6), Card('yellow', 6), Card('green', 6)]))
# True
# True
# turn largest_group if largest_group else None