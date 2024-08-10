from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QPushButton, QLineEdit, QTextEdit
import random

def get_deck():
    suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
    ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace']
    deck = [rank + ' of ' + suit for suit in suits for rank in ranks]
    random.shuffle(deck)
    return deck

class CardGame(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(250, 250, 800, 800)
        self.setWindowTitle("Card Game")
        
        self.setStyleSheet("background-color:#eed9c4")

        self.deck = get_deck()
        self.re_value = self.get_re_value()
        self.user_hand = []
        self.computer_hand = []

        self.init_ui()

    def get_re_value(self):
        ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace']
        values = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 1]
        return dict(zip(ranks, values))

    def init_ui(self):
        
        self.label = QLabel("Welcome to 'The Bigger the Better' Card Game!", self)
        self.label.setGeometry(150, 20, 700, 40)
        self.label.setStyleSheet("color:#6d3228")
        self.label.setFont(QtGui.QFont("Rubik", 16, QtGui.QFont.Bold))



        self.instructions = QLabel(
            """In this game both user and computer will be provided limited cards, and based upon the values of 
            the cards they have, their score will be determined and hence the victory.""", self)
        self.instructions.setGeometry(50, 70, 700, 80)
        self.instructions.setStyleSheet("color:#6d3228")
        self.instructions.setFont(QtGui.QFont("Rubik",10,QtGui.QFont.Bold))

        self.type=QLabel("""There are two type of games available:
                         1. Total values
                         2. All cards matter""",self)
        self.type.setGeometry(400, 140,300,100)
        self.type.setStyleSheet("color:#ff785b")
        self.type.setFont(QtGui.QFont("Rubik",10,QtGui.QFont.Bold))



        self.type_input = QLineEdit(self)
        self.type_input.setPlaceholderText("Enter game type (1 or 2)")
        self.type_input.setGeometry(50, 160, 200, 30)
        self.type_input.setStyleSheet("background-color:#6d3228;color:#eed9c4;border-radius:10px")

        self.submit_button = QPushButton("Submit", self)
        self.submit_button.setGeometry(270, 160, 100, 30)
        self.submit_button.clicked.connect(self.submit_choice)
        self.submit_button.setStyleSheet("background-color:#6d3228;border-radius:15px;color:#eed9c4")

        self.show_deck_button = QPushButton("Show Deck", self)
        self.show_deck_button.setGeometry(50, 200, 100, 30)
        self.show_deck_button.clicked.connect(self.show_deck)
        self.show_deck_button.setStyleSheet("background-color:#6d3228;border-radius:15px;color:#eed9c4")


        self.result_text = QTextEdit(self)
        self.result_text.setStyleSheet("background-color:#ffefe6;color:#6d3228; border-radius:10px; padding:10px;")
        self.result_text.setGeometry(50, 240, 700, 300)
        self.result_text.setReadOnly(True)

    def submit_choice(self):
        try:
            game_type = int(self.type_input.text())
            if game_type not in [1, 2]:
                self.result_text.setText("Error: Please enter 1 or 2.")
                return

            self.play_game(game_type)
        except ValueError:
            self.result_text.setText("Error: Please enter a valid number.")


    def show_deck(self):
        deck_display = "\n".join(self.deck)
        self.result_text.setText(deck_display)
        self.result_text.setStyleSheet("color:#6d3228;background-color:#ffefe6")
        self.result_text.setFont(QtGui.QFont("Rubik",10,QtGui.QFont.Bold))


    def play_game(self, game_type):
        self.user_hand = []
        self.computer_hand = []
        random.shuffle(self.deck)

        no_to_pop, ok = QtWidgets.QInputDialog.getInt(self, 'Number of Cards', 'How many cards do you want to draw?', 1, 1, 10)
        if not ok:
            return

        for _ in range(no_to_pop):
            self.user_hand.append(self.deck.pop())
            self.computer_hand.append(self.deck.pop())

        user_total, comp_total = self.calculate_totals()

        result = self.format_results(game_type, user_total, comp_total)
        self.result_text.setText(result)

    def calculate_totals(self):
        user_total = sum(self.re_value[card.split(' of ')[0]] for card in self.user_hand)
        comp_total = sum(self.re_value[card.split(' of ')[0]] for card in self.computer_hand)
        return user_total, comp_total
    



    def format_results(self, game_type, user_total, comp_total):
        result = ""

        if game_type == 1:
            result += "<b>Sum of All Cards</b><br><br>"
            result += f"User Cards: {', '.join(self.user_hand)}<br>"
            result += f"Computer Cards: {', '.join(self.computer_hand)}<br><br>"
            result += f"<b>Score:</b><br> User: {user_total}<br> Computer: {comp_total}<br>"
        elif game_type == 2:
            result += "<b>Each Card Matters</b><br><br>"
            for user_card, comp_card in zip(self.user_hand, self.computer_hand):
                user_card_value = self.re_value[user_card.split(' of ')[0]]
                comp_card_value = self.re_value[comp_card.split(' of ')[0]]
                result += f"<b>Round:</b> {self.user_hand.index(user_card) + 1}<br>"
                result += f"User Card: {user_card} (Value: {user_card_value})<br>"
                result += f"Computer Card: {comp_card} (Value: {comp_card_value})<br>"
                if user_card_value > comp_card_value:
                    result += "<b>USER WINS</b><br>"
                elif user_card_value == comp_card_value:
                    result += "<b>IT'S A DRAW</b><br>"
                else:
                    result += "<b>COMPUTER WINS</b><br>"

        return f"<span style='color:#6d3228; font-family: Rubik; font-size: 10pt;'>{result}</span>"

        

if __name__ == '__main__':
    app = QApplication([])
    game_window = CardGame()
    game_window.show()
    app.exec_()
