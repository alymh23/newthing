class Card:
    def __init__(self, colour, number):
        assert isinstance(number, int)#是用于检查变量类型的断言语句。它的作用是确保 number 变量是整数类型 (int)。
        self.colour = colour
        self.number = number

    def __str__(self):
        return f'{self.colour} {self.number}'

class CollectionOfCards:
    def __init__(self, card_list):
        self.collection = []
        for card in card_list:
            if isinstance(card, Card):
                self.collection.append(card)
            else:
                colour, number = card.split()
                self.collection.append(Card(colour, int(number)))

    def is_valid_group(self):#同色连续数字或同数异色
        # 检查同色连续数字的序列
        same_colour = {}  # {same_colour:[different_number]}以颜色为键分组相同颜色的卡片数字
        for card in self.collection:
            if card.colour not in same_colour:
                same_colour[card.colour] = []
            same_colour[card.colour].append(card.number)
        # 遍历颜色分组，检查是否存在同色连续数字的有效组
        for numbers in same_colour.values():
            numbers.sort()
            consecutive_count=1#从第二个数开始比较，它和前面的数字比较，假设它是连续的
            for i in range(1,len(numbers)):
                if numbers[i] == numbers[i-1]+1:#后面的数字和前面的数+1？
                    consecutive_count+=1
                    if consecutive_count>=3:
                        return True
                else:
                    consecutive_count=1

        # 检查同数不同色的组合
        same_number = {}  # {same_numbers:set(different_colour)}
        for card in self.collection:
            if card.number not in same_number:
                same_number[card.number] = set()
            same_number[card.number].add(card.colour)

        # 遍历数字分组，检查是否存在同数不同色的有效组
        if len(same_number) == 1:
            #same_number.values() 返回字典中的所有值（即每个数字对应的颜色集合）。0] 取出列表中的第一个（也是唯一的）颜色集合，赋值给 colours。
            colours = list(same_number.values())[0]#需要先将 dict_values 转换为列表后才能使用索引访问。
            if len(colours) == len(self.collection) and len(colours) >= 3:
                return True
        return False

        # 若不符合任何有效组条件，返回 False

    def find_valid_group(self):
        # 查找是否存在一个有效的组合
        n = len(self.collection)
        for i in range(1, n+1):#i代表子集长度
            for j in range(n+1-i):
                subset = self.collection[j:j + i]#取长度为 i 的子集。
                if CollectionOfCards([str(card) for card in subset]).is_valid_group():
                    #将 subset 转换为字符串列表，生成一个新的 CollectionOfCards 对象。
                  #调用 is_valid_group() 方法检查该子集是否符合有效组的条件。如果该子集是有效组，则返回 subset。
                    return subset
        return None

    def find_largest_valid_group(self):
        """
        在集合中寻找最大的有效组。
        若找到多个相同大小的有效组，可返回任意一个；若无有效组，返回 None。
        """
        if not self.collection:
            return None
        # 记录最长序列
        longest_seq = []
        # 使用字典存储按颜色分组的卡片
        colour_groups = {}
        # 使用集合存储数字
        seen_numbers = set()
        #检查同色连续数字的序列：
        for card in self.collection:
            if card.colour not in colour_groups:
                colour_groups[card.colour] = []
            colour_groups[card.colour].append(card)#为了后续输出完整卡牌

            # 如果数字已经见过，直接加入
            if card.number in seen_numbers:
                continue
            seen_numbers.add(card.number)

            # 检查相同花色的连续序列colour_groups = {colour：[cards]}
            for colour, cards in colour_groups.items():
                cards.sort(key=lambda x: x.number)
                current_seq = []
                for i in range(len(cards)):
                    if i == 0 or cards[i].number == cards[i - 1].number + 1:
                        current_seq.append(cards[i])
                    else:
                        if len(current_seq) > len(longest_seq):
                            longest_seq = current_seq
                        current_seq = [cards[i]]#更新最长序列
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
        #浅拷贝 (copy()) 已经满足需求，因为只需要一个新的列表对象来存储 Card 引用。如果对 Card 对象本身没有修改需求，那么浅拷贝在效率和功能上都是最佳选择。
        new_hand = CollectionOfCards(self.collection.copy())
        new_hand.collection.append(new_card)

        # 检查新的手牌是否形成有效组
        if new_hand.is_valid_group():
            return new_hand
        return None

    def find_valid_new_group(self):
        """查找可以形成有效组的所有可能新牌"""
        """
can_form_valid_group_with_card(self, new_card) 需要一个 new_card 参数，因为它要检查特定的一张新卡片能否与当前集合形成有效组。
find_valid_new_group(self) 不需要 new_card 参数，因为它是在尝试所有可能的卡片组合，并调用 can_form_valid_group_with_card 方法逐一验证是否能形成有效组。
        """
        valid_groups = []
        for colour in ['red', 'blue', 'green', 'yellow']:
            for number in range(1, 11):
                card = Card(colour, number)
                if self.can_form_valid_group_with_card(card):
                    valid_groups.append(card)

        return CollectionOfCards([f"{c.colour} {c.number}" for c in valid_groups]).collection


def probability_of_valid_group(hands: list[CollectionOfCards]):
    first_player_hand = hands[0]

    if first_player_hand is None or first_player_hand.is_valid_group():
        return 1.0

    need_cards = first_player_hand.find_valid_new_group()
    need_cards_n = len(need_cards)
    if need_cards_n <= 0:
        return 0.0
    # 每张牌有两张，牌堆剩余数为need_cards_n * 2
    left_cards_n = need_cards_n * 2

    # 统计所有玩家的手牌
    # have_n_dict 是一个字典，用于记录每张牌的数量。
    # have_n 用来统计所有玩家手牌的总张数。
    have_n_dict = {}
    have_n = 0
    for player_hand in hands:
        for card in player_hand.collection:
            card_key = f"{card.colour} {card.number}"
            have_n_dict[card_key] = have_n_dict.get(card_key, 0) + 1
            have_n += 1

    # 检查需要的牌是否在已有牌中
    for card in need_cards:
        card_key = f"{card.colour} {card.number}"
        if have_n_dict.get(card_key, 0) >= 2:
            return 0.0
        else:
            left_cards_n -= have_n_dict.get(card_key, 0)  # 减去已有的牌数量
    """
    80.0 - have_n 表示牌堆中未被玩家持有的剩余牌数量。
left_cards_n / (80.0 - have_n) 是所需牌的数量与剩余牌的比值，表示从牌堆中抽到所需牌以形成有效组的概率。
    """
    probability = left_cards_n / (80.0 - have_n)
    return probability
