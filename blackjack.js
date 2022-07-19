var prompt = require("prompt-sync")();

class Card {
    constructor(suit,value){
        this.suit = suit;
        this.value = value;
    }
}

class Deck {
    constructor(){
        this.cards = [];
        let suits = ["♠", "♣", "♥", "♦"];
        let values = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"];
        for (let i = 0;i<suits.length;i++){
            for (let x = 0;x < values.length;x++){
                this.cards.push(new Card(suits[i],values[x]));
            }
        }
    }

    shuffle() {
        let currentIndex = this.cards.length,  randomIndex;

        // While there remain elements to shuffle.
        while (currentIndex != 0) {

            // Pick a remaining element.
            randomIndex = Math.floor(Math.random() * currentIndex);
            currentIndex--;

            // And swap it with the current element.
            [this.cards[currentIndex], this.cards[randomIndex]] = [
                this.cards[randomIndex], this.cards[currentIndex]];
        }
    }

    draw() {
        return this.cards.shift()
    }
}

class Hand {
    constructor(hide){
        this.cards = [];
        this.hide = hide;
        this.value = 0;
    }

    pull_card(card){
        this.cards.push(card);
    }

    get_value(){
        this.value = 0;
        let ace = 0;
        for (let i = 0; i < this.cards.length; i++){
            if (!isNaN(this.cards[i].value)){
                this.value += parseInt(this.cards[i].value);
            } else {
                if (["J", "Q", "K"].includes(this.cards[i].value)) {
                    this.value += 10;
                } else {
                    ace += 1;
                }
            }
        }
        for (let i = 0; i < ace; i++){
            if (this.value > 11) {
                this.value += 1;
            } else {
                this.value += 11;
            }
        }
        return this.value;
    }

    get_hand(show = false){
        let build = "";
        if (!this.hide || show){
            for (let i = 0; i < this.cards.length; i++){
                build += this.cards[i].suit + this.cards[i].value + " ";
            }
            build += "\nCard Value: " + this.get_value();
            return build;
        } else {
            build += this.cards[0].suit + this.cards[0].value + "  ?\nCard Value: ?";
            return build;
        }
    }
}

var active = true

while (active){
    game_deck = new Deck();
    game_deck.shuffle();
    var player = new Hand(false);
    var dealer = new Hand(true);

    for (let i = 0;i < 2;i++){
        player.pull_card(game_deck.draw())
        dealer.pull_card(game_deck.draw())
    }

    while(dealer.get_value() == 21){
        dealer.cards.shift()
        dealer.pull_card(game_deck.draw())
    }

    while(player.get_value() == 21){
        player.cards.shift()
        player.pull_card(game_deck.draw())
    }

    console.log("-----------------------------------------")
    console.log("You have: \n" + player.get_hand())
    console.log("Dealer has: \n" + dealer.get_hand())
    console.log("-----------------------------------------")

    var not_blackjack = true

    while (not_blackjack) {
        const choice = prompt("What do you want to do? (hit,stand): ");
    
        if (choice.toLowerCase() == "hit") {
            player.pull_card(game_deck.draw())
            if (check_bust() || check_5cards() || check_21()){
                not_blackjack = false
            }
        } else if (choice.toLowerCase() == "stand") {
            while (dealer.get_value() <= 17) {
                dealer.pull_card(game_deck.draw())
                if (check_bust() || check_5cards() || check_21()){
                    not_blackjack = false
                }
            }
            if (not_blackjack) {
                check_stand()
                not_blackjack = false
            }
        } else {
            console.log("\nThat does not look like a valid option, please try again.")
        }

        if (not_blackjack) {
            console.log("-----------------------------------------")
            console.log("You have: \n" + player.get_hand())
            console.log("Dealer has: \n" + dealer.get_hand())
            console.log("-----------------------------------------")
        } else {
            console.log("You had: \n" + player.get_hand())
            console.log("Dealer had: \n" + dealer.get_hand(true))
            console.log("-----------------------------------------")
            while (true) {
                const again = prompt("Do you want to play again? (yes,no): ")
                if (again.toLowerCase() == "yes") {
                    break
                } else {
                    active = false
                    break
                }
            }
        }
    }
}

function check_21() {
    if (player.get_value() == 21 && dealer.get_value != 21) {
        console.log("-----------------------------------------")
        console.log("You have 21! You win!")
        return true
    } else if (dealer.get_value() == 21) {
        console.log("-----------------------------------------")
        console.log("The dealer has 21! You lose!")
        return true
    } else if (dealer.get_value() == 21 && player.get_value() == 21) {
        console.log("-----------------------------------------")
        console.log("Both you and the dealer have 21! You tie.")
        return true
    }
}

function check_bust() {
    if (player.get_value() >= 21){
        console.log("-----------------------------------------")
        console.log("You went over 21, busted!")
        return true
    } else if (dealer.get_value() >= 21){
        console.log("-----------------------------------------")
        console.log("The dealer went over 21, you win!")
        return true
    } else {
        return false
    }
}

function check_stand(){
    if (player.get_value() == dealer.get_value) {
        console.log("-----------------------------------------")
        console.log("You both have the same value! You tie.")
    } else if (player.get_value() >= dealer.get_value()){
        console.log("-----------------------------------------")
        console.log("You have a higher value than the dealer. You win!")
    } else {
        console.log("-----------------------------------------")
        console.log("The dealer has a higher value than you. You lose! ")
    }
}

function check_5cards(){
    if (player.cards.length == 5) {
        console.log("-----------------------------------------")
        console.log("You took 5 cards without going over 21. You win!")
        return true
    } else if (dealer.cards.length == 5){
        console.log("-----------------------------------------")
        console.log("The dealer took 5 cards without going over 21. You lose!")
        return true
    } else {
        return false
    }
}