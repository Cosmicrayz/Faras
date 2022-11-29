from enum import IntEnum
from valid_sequences import VALID_SEQUENCES
import random
from collections import Counter
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

HAND_ORDER = ["High Card", "Pair", "Colour", "Run", "Double Run", "Trial"]


class HandRanks(IntEnum):
    HIGH_CARD = 1
    PAIR = 2
    COLOUR = 3
    RUN = 4
    DOUBLE_RUN = 5
    TRIAL = 6


class Card:
    FACE_CARDS = {"J": 11, "Q": 12, "K": 13, "A": 1}

    def __init__(self, symbol, suit):
        # Allow something like "AH" to be passed in
        if suit is None:
            if symbol[0].isdigit():
                self.symbol = int(symbol[0])
            else:
                self.symbol = symbol[0]
            self.suit = symbol[1]
        else:
            self.suit = suit
            self.symbol = symbol
        self.value = self.get_value()

    def get_value(self):
        if isinstance(self.symbol, int) and self.symbol in range(2, 11):
            return self.symbol
        elif self.symbol in Card.FACE_CARDS:
            return Card.FACE_CARDS[self.symbol]
        raise ValueError("Invalid Symbol: %s" % self.symbol)

    def __repr__(self):
        return str(self.symbol) + self.suit

    def __str__(self):
        return self.__repr__()


class Deck:
    def __init__(self):
        self.cards = []
        self.build_deck()

    def build_deck(self):
        for symbol in list(range(2, 11)) + ["J", "Q", "K", "A"]:
            for suit in ["C", "H", "S", "D"]:
                self.cards.append(Card(symbol, suit))
        self.cards.sort(key=lambda x: (x.suit, x.value))

    def shuffle_deck(self):
        random.shuffle(self.cards)

    def deal(self):
        if len(self.cards):
            return self.cards.pop(0)
        raise ValueError("No cards in the deck")

    def deal_shuffled(self):
        self.shuffle_deck()
        return self.deal()

    def deal_multiple(self, n=1):
        cards = []
        for i in range(n):
            cards.append(self.deal())
        return cards


class Hand:
    def __init__(self, cards):
        if all([isinstance(i, Card) for i in cards]):
            self.cards = sorted(cards, key=lambda x: (x.suit, x.value))
        else:
            self.cards = sorted(
                [Card(i, None) for i in cards], key=lambda x: (x.suit, x.value)
            )

    def __str__(self):
        return " ".join([i.__str__() for i in self.cards])

    def get_hand_rank(self):
        values = sorted([i.value for i in self.cards])
        suits = sorted([i.suit for i in self.cards])
        if len(set(values)) == 1:
            return HandRanks.TRIAL
        # If the suit is the same and they are next to each other sequentially
        if len(set(suits)) == 1 and values in VALID_SEQUENCES:
            return HandRanks.DOUBLE_RUN
        # If they are sequentially next to each other
        if values in VALID_SEQUENCES:
            return HandRanks.RUN
        # If the suit is the same
        if len(set(suits)) == 1:
            return HandRanks.COLOUR
        if len(set(values)) == 2:
            return HandRanks.PAIR
        return HandRanks.HIGH_CARD

    def __ge__(self, other):
        return self.get_hand_rank() >= other.get_hand_rank()

    def __gt__(self, other):
        return self.get_hand_rank() > other.get_hand_rank()


def sim_hand_probability(max_sims):
    hands = []
    for i in range(max_sims):
        D = Deck()
        D.shuffle_deck()
        H = Hand(D.deal_multiple(3))
        hands.append(H.get_hand_rank())
    return Counter([i.name.replace("_", " ").title() for i in sorted(hands)])


def sim_winning_hand(n_players=2, max_sims=10**6):
    winning_hands = []
    for i in range(max_sims):
        D = Deck()
        D.shuffle_deck()
        hands = [Hand(D.deal_multiple(3)) for j in range(n_players)]
        winning_hands.append(max(hands).get_hand_rank())
    return Counter([i.name.replace("_", " ").title() for i in sorted(winning_hands)])


def plot_winning_hands(max_sims=10**6):
    fig, ax = plt.subplots(3, 3, figsize=(20, 20))
    for idx, n_players in enumerate(range(2, 11)):
        y_pos, x_pos = divmod(idx, 3)
        df = pd.DataFrame.from_dict(
            sim_winning_hand(n_players, max_sims), orient="index"
        ).reset_index()
        df = df.rename(columns={"index": "Hand Name", 0: "Frequency"})
        df["Win Probability"] = df["Frequency"].apply(
            lambda x: x / df["Frequency"].sum()
        )
        ax[y_pos, x_pos].set_title(f"{n_players} Players")
        ax[y_pos, x_pos].set_facecolor("#000928")
        ax[y_pos, x_pos].bar(df["Hand Name"], df["Win Probability"], color="#318181")
        ax[y_pos, x_pos].bar_label(
            ax[y_pos, x_pos].containers[0],
            label_type="edge",
            color="white",
        )
        ax[y_pos, x_pos].set_xlabel("")
        ax[y_pos, x_pos].set_ylim(0, 1)
        ax[y_pos, x_pos].set_yticklabels(
            ["{:.2f}".format(x) for x in ax[y_pos, x_pos].get_yticks()]
        )
    plt.savefig(r"C:\Users\Cosmic\Pictures\Winning Hand Probability.png")


def plot_hand_probability(max_sims):
    df = pd.DataFrame.from_dict(
        sim_hand_probability(max_sims), orient="index"
    ).reset_index()
    df = df.rename(columns={"index": "Hand Name", 0: "Frequency"})
    df["Probability"] = df["Frequency"].apply(lambda x: x / df["Frequency"].sum())
    fig, ax = plt.subplots()
    ax.set_facecolor("#000928")
    ax.bar(df["Hand Name"], df["Probability"], color="#318181")
    ax.set_ylabel("Probability")
    ax.bar_label(ax.containers[0], label_type="edge", color="white")
    ax.set_ylim(0, 1)
    ax.set_yticklabels(["{:.2f}".format(x) for x in ax.get_yticks()])
    plt.savefig(r"C:\Users\Cosmic\Pictures\Hand Probability.png")


if __name__ == "__main__":
    plot_hand_probability(10**7)
    print("Done Simulating Hand Probabilities")
    plot_winning_hands(10**7)
    print("Done Simulating Winning Hands")
