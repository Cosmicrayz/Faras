# Faras

## Background on the game

Faras is a close cousin of poker played in Nepal where players are dealt 3 cards (it is also known under the name Brag). 
Players go around in a circle betting or folding based on their hands. The file `hand.py` seeks to compute a 
Monte Carlo simulation what the likelihood of each hand is and how likely a hand is to win.

## How likely are the hands.

### The hands in Faras have the following ordering:

<p align="center">
  <img src="https://user-images.githubusercontent.com/58432106/202872756-06df6953-61b1-46c7-9741-f34f678ab315.png"/>
</p>

There are a few interesting things to note. First of all we see that the **Double Run** is the least likely hand but is actually not the highest ranked.
Also compared to traditional poker we have the **Run** outranking **Colour** traditional 5 card poker has the **Flush** outrank the **Straight**. This is actually due to the chances of getting the same suit being smaller than getting the 3 sequential cards.

## Calculation of probabilities

Let us attempt to calculate the probabilites of each hand. There are <img src="https://latex.codecogs.com/svg.image?\binom{52}{3}&space;"> possible hands

### Trial
We have 13 choices for the card value and we choose 3 out of 4 suits. So we get:
<p align="center"> <img src="https://latex.codecogs.com/svg.image?\frac{\binom{13}{1}&space;\cdot&space;\binom{4}{3}}{\binom{52}{3}}&space;\approx&space;0.24&space;\%&space;"> </p>

### Double Run
The valid sequences run are A23, 234, 345, ..., QKA. so the first card is in the range A-Q (the sequence starting with KA2 is not valid) hence there are 12 sequences and they all must be the same suit. So we get:
<p align="center"> <img src="https://latex.codecogs.com/svg.image?\frac{\binom{12}{1}\cdot&space;4^3&space;-&space;\binom{12}{1}\cdot&space;\binom{4}{1}&space;}{\binom{52}{3}}&space;\approx&space;&space;0.22\%"> </p>


### Run
As before there are 12 valid sequences. Here for each of the 3 cards we choose their suit independently meaning 4 choices for each but we must subtract the occurences of a Double Run. So we get:
<p align="center"> <img src="https://latex.codecogs.com/svg.image?\frac{\binom{12}{1}\cdot&space;4^3&space;-&space;\binom{12}{1}\cdot&space;\binom{4}{1}&space;}{\binom{52}{3}}&space;\approx&space;&space;3.26\%"> </p>

### Colour
We can pick any 3 of the 13 possible values and any of the 4 suits. But we need to subtract the possibility of a double run. So we get
<p align="center"> <img src="https://latex.codecogs.com/svg.image?\frac{\binom{13}{3}\cdot&space;\binom{4}{1}&space;-&space;\binom{12}{1}\cdot&space;\binom{4}{1}&space;}{\binom{52}{3}}&space;\approx&space;&space;4.96\%"> </p>

### Pair
We have 2 distinct of the 2 values we elect one of them to be the pair while the other value is singular. For suits we need to choose 2 suits of the possible 4 for the pair and the single card can be any of the 4 suits. 
<p align="center"> <img src="https://latex.codecogs.com/svg.image?\frac{\binom{13}{2}\cdot&space;\binom{2}{1}&space;\cdot&space;\binom{4}{2}\cdot&space;\binom{4}{1}&space;}{\binom{52}{3}}&space;\approx&space;&space;16.94\%"> </p>

### High Card
This is just the remaining hands that have not been counted above. So we get:
<p align="center"> <img src="https://latex.codecogs.com/svg.image?\frac{\binom{52}{3}&space;-&space;\text{Above}}{\binom{52}{3}}&space;\approx&space;&space;74.39\%"> </p>


