import random
suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Two':2, 'Three':3, 'Four':4, 'Five':5, 'Six':6, 'Seven':7, 'Eight':8, 
            'Nine':9, 'Ten':10, 'Jack':10, 'Queen':10, 'King':10, 'Ace':11}

"""What I did:
I created just the Player and Dealer class, Dealer would deal the cards for himself and the player, receive the bet, add cards
view points, etc

Player get to add cards, stand, bet, view points, and gains"""

import pdb

class Card():
    
    def __init__(self,suit,rank):
        self.suit=suit
        self.rank=rank
        self.value=values[rank]
    
    def __str__(self):
        return f'{self.rank} of {self.suit}'


class Dealer():
     
    def __init__(self, name, pot=0):
        self.deck = []
        self.all_cards = []
        self.pot = pot
        self.name = name
        
        for suit in suits:
            for rank in ranks:
                self.deck.append(Card(suit,rank))
    
    def shuffle(self):
        return random.shuffle(self.deck)
    
    def deal_one(self):
        return self.deck.pop(0)
    
    def receive_bet(self,betting_amount):
        self.pot+=betting_amount
    
    def hit_one(self,card):
        print(f"Dealer hit a {card.rank}")
        if card.value== 11:
            if self.view_points()+11>21 and self.view_points()+1<=21:
                card.value=1
            elif self.view_points()+11<=21 and self.view_points()+1<=21:
                card.value=11
            else:
                card.value=1
        self.all_cards.append(card)
 
    
    def stand(self):
        print("You chose to stand")
        pass
    
    def view_points(self):
        total = 0
        for card in self.all_cards:
            total+=card.value
            if card.rank== "Ace":
                if total+11>21 and total+1<=21:
                    card.value==1
                if total+11<=21 and total+1<=21:
                    card.value==11
                    
        if total==21 and len(self.all_cards)==2:
            print("Blackjack!")
        return total

class Player():
    
    
    def __init__(self,name,total_money):
        self.all_cards = []
        self.name=name
        self.total_money=total_money
    
    def view_points(self):
        total = 0
        for card in self.all_cards:
            if card.rank== "Ace":
                if total+11>21 and total+1<=21:
                    card.value==1
                elif total+11<=21 and total+1<=21:
                    card.value==11
 
            total+=card.value
                    
        return total
        
    def bet(self,bet):
        self.total_money-=bet

    def gain(self,gain):
        self.total_money+=gain
    
    def hit_one(self,new_card):
        print(f"You hit a {new_card.rank}")
        if new_card.value== 11:
            if self.view_points()+11>21 and self.view_points()+1<=21:
                new_card.value=1
            elif self.view_points()+11<=21 and self.view_points()+1<=21:
                new_card.value=1
            else:
                new_card.value=1
        self.all_cards.append(new_card)

    
    def stand(self):
        print("You chose to stand")
        pass

#Player setup
player_one=Player("Player One",5000)

#Dealer setup
main_dealer=Dealer("Dealer")
main_dealer.shuffle()

#Game logic
i=0
#player and dealer turn
turn = player_one
player_turn = True
black_jack_player = False
black_jack_dealer = False
busted = False

def reset():
    global i, turn, player_turn, black_jack_player, black_jack_dealer, busted
    i=0
    turn = player_one
    player_turn = True
    black_jack_player = False
    black_jack_dealer = False
    busted = False
    player_one.all_cards=[]
    main_dealer.all_cards=[]


while True:


    while True:
        if i ==0:
            if player_turn:
                while True:
                    print(f"You have ${player_one.total_money}")
                    bet_amount = int(input("Please enter betting amount: "))
                    if bet_amount<= turn.total_money:
                        turn.bet(bet_amount)
                        main_dealer.receive_bet(bet_amount)
                        break
                    else:
                        print("Try again! Not enough money!")

        if i<=1:
            turn.hit_one(main_dealer.deal_one())
            if turn.view_points()==21 and len(turn.all_cards)==2:
                if not player_turn:
                    black_jack_dealer = True
                    break
                else:
                    print(f"Blackjack!")
                    black_jack_player = True
                    player_turn = False
                    turn = main_dealer
                    print("Dealer's turn")
                    i=0
                    continue
               
            i+=1
        if i>=2:
            if player_turn:
                while True:
                    print("""Please select your action:
    1. Hit
    2. Stand
    3. Split
    4. View cards""")     
                    action = int(input(""))
                    if action in [1,2,4]:
                        break
                    else:
                        print("Incorrect Prompt!")
            else:
                if turn.view_points() < player_one.view_points():
                    action = 1
                else:
                    action = 2
            if action == 1:
                turn.hit_one(main_dealer.deal_one())
                i+=1
                if turn.view_points()>21:
                    print(f"{turn.name}'s busted!")
                    break
            elif action == 2:
                if not player_turn:
                    break
                turn.stand()
                total_points=turn.view_points()
                print(f"{turn.name}'s' total point is {total_points}")
                print("Dealer's turn")
                turn = main_dealer
                player_turn = False
                i=0
                continue
            elif action == 3:
                pass

            elif action == 4:
                current_point = player_one.view_points()
                print(current_point)


    if player_one.view_points() > main_dealer.view_points() and player_one.view_points() <=21 :
        print(f"You win {bet_amount}!")
        player_one.gain(bet_amount*2)
        reset()
        continue
    elif player_one.view_points()>21:
        #check if there is an Ace
        for each_card in player_one.all_cards:
            if each_card.rank == "Ace":
                each_card.value = 1
            if player_one.view_points() <= 21:
                break
            else:
                busted = True
                break
        if busted:
            print("You busted!")
            print(f"You lost {bet_amount}")
            reset()
            continue
        elif player_one.view_points() > main_dealer.view_points():
            print(f"You win {bet_amount}!")
            player_one.gain(bet_amount*2)
            reset()
            continue

        else:
        
            print(f"You lost {bet_amount}")
            reset()
            continue
    elif main_dealer.view_points()>21:
        if player_one.view_points() <=21:
            print(f"You win {bet_amount}!")
            player_one.gain(bet_amount*2)
            reset()
            continue
        else:
            i=0
            continue
    elif black_jack_player:
        if not black_jack_dealer:
            print(f"You win {bet_amount*2}!")
            player_one.gain(bet_amount*2)

        else:
            print("It's a draw! Both got Blackjack")
            player_one.gain(bet_amount)
        reset()
        continue

    elif black_jack_dealer:
        print(f"You lost {bet_amount}! Dealer got Blackjack")
        player_one.bet(bet_amount)
        reset()
        continue

    elif player_one.view_points()==main_dealer.view_points():
        print("It's a draw")
        reset()
        continue

    else:
        print(f"You lost {bet_amount}! Dealer has better hand")
        if player_one.total_money==0:
            print("Game Over! You lost all your money!")
            break
        else:
            reset()
            continue