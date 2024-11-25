import random  # 引入随机模块，用于随机选择或生成随机数。
import base  # 引入游戏基础模块，包含基础类和功能。

class SimpleAI(base.Enemy):  # 定义 SimpleAI 类，继承自 base 模块中的 Enemy 类。
    def perform_turn(self, game_manager):  # 定义 perform_turn 方法，控制 AI 每轮的行为逻辑。
        """
        简单模式下的AI决策逻辑：
        - 优先从玩家手中抽取“废牌”。
        - 如果没有废牌，则从牌堆抽取0~3张牌。
        - 判断是否需要出牌，如果手牌构成两个有效组，优先出掉颜色不同但数字相同的组。
        - 返回操作决策：["steal", target_name] / ["draw", count] / ["discard", group] / ["finish"]
        """
        # 1. 优先从玩家手中抽取“废牌”
        for opponent in game_manager.player_list:  # 遍历所有玩家。
            if opponent != self:  # 确保目标玩家不是自己。
                critical_card = self.find_useless_card(opponent)  # 检查对手是否有“废牌”。
                if critical_card and game_manager.steal:  # 如果找到废牌并且允许偷牌。
                    stolen_card = game_manager.steal_cards(opponent)  # 从对方手中偷牌。
                    self.add(stolen_card)  # 将偷来的牌加入自己的手牌。
                    return ["steal", opponent.name]  # 返回偷牌操作的决策结果。

        # 2. 从牌堆抽取0~3张牌
        available_cards = game_manager.cards.copy()  # 创建牌堆的副本，避免直接修改原牌堆。
        for player in game_manager.player_list:  # 遍历所有玩家。
            for card in player.hands:  # 遍历每位玩家的手牌。
                if card in available_cards:  # 如果该牌在牌堆中。
                    available_cards.remove(card)  # 从牌堆中移除这张牌。

        draw_count = random.randint(0, 3)  # 随机生成要抽取的牌数（0~3）。
        if draw_count > 0 and game_manager.draw:  # 如果需要抽牌并且允许抽牌。
            drawn_cards = random.sample(available_cards, draw_count)  # 从牌堆中随机抽取指定数量的牌。
            self.add(drawn_cards)  # 将抽到的牌加入自己的手牌。
            return ["draw", draw_count]  # 返回抽牌操作的决策结果。

        # 3. 判断是否需要弃牌
        valid_groups = self.generate_valid_groups()  # 生成当前手牌中的所有有效牌组。
        if valid_groups:  # 如果存在有效牌组。
            # 优先选择颜色不同但数字相同的组
            color_diff_groups = [
                group for group in valid_groups if len(set(card.colour for card in group)) == len(group)
            ]  # 筛选颜色不同但数字相同的牌组。
            if color_diff_groups:  # 如果找到符合条件的组。
                group = color_diff_groups[0]  # 选择第一组。
            else:  # 如果没有符合条件的组。
                group = valid_groups[0]  # 选择第一个有效组。

            return ["discard", group]  # 返回弃牌操作的决策结果。

        # 4. 如果完成所有操作，结束回合
        return ["finish", 0]  # 返回结束回合的决策结果。

    def find_useless_card(self, opponent):  # 定义 find_useless_card 方法，用于查找对手的“废牌”。
        """
        检查对手手中是否有“废牌”（即关键牌）。
        废牌定义：对手只有一张牌时，该牌被认为是废牌。
        """
        if len(opponent.hands) == 1:  # 如果对手手中只剩下一张牌。
            return opponent.hands[0]  # 返回这张牌。
        return None  # 否则返回 None。

    def generate_valid_groups(self):  # 定义 generate_valid_groups 方法，用于生成有效牌组。
        """
        根据当前手牌生成所有可能的有效牌组。
        有效牌组包括：
        1. 连续三个数字的牌，颜色相同。
        2. 相同数字的三张牌，颜色可以不同。
        """
        groups = []  # 初始化一个空列表，用于存储有效牌组。

        # 按颜色连续数字
        colours = set(card.colour for card in self.hands)  # 获取手牌中所有的颜色集合。
        for colour in colours:  # 遍历每种颜色。
            cards = [card for card in self.hands if card.colour == colour]  # 筛选出颜色相同的牌。
            cards.sort(key=lambda c: c.number)  # 按照牌的数字进行排序。
            for i in range(len(cards) - 2):  # 遍历每组三张连续的牌。
                if (cards[i + 1].number == cards[i].number + 1 and
                        cards[i + 2].number == cards[i].number + 2):  # 如果三张牌的数字连续。
                    groups.append([cards[i], cards[i + 1], cards[i + 2]])  # 将这三张牌作为一组加入有效组列表。

        # 按数字相同不同颜色
        numbers = set(card.number for card in self.hands)  # 获取手牌中所有的数字集合。
        for number in numbers:  # 遍历每个数字。
            cards = [card for card in self.hands if card.number == number]  # 筛选出数字相同的牌。
            if len(cards) >= 3:  # 如果至少有三张数字相同的牌。
                groups.append(cards[:3])  # 将前三张牌作为一组加入有效组列表。

        return groups  # 返回所有有效牌组。


