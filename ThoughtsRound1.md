# Sampling Methods
| - | Successful Parses | Functional | Sensible | Denominator |
| --- | --- | --- | --- | --- |
| **Greedy**             | 16 | 15 | 11 | 17 |
| **Beam_5**             | 65 | 65 | 50 | 85 |
| **sample_k=0_p=0_t=1** | 16 | 6 | 2 | 0 |


### Greedy
* Overall pretty reasonable
* Seems to be a bit of modal collapse:
  * Elf Goblin & Teferi have the same abilities of {T}: Add C; {1}{W}: Add {C}
    * Second half doesn't make sense, so I'm kinda surprised. woulda expected like ETB draw a card to get memorized instead. Neat.
  * Velicraptor go Vroom and Sliver Dodecahedron are functionally the same card
### Beam_5
* Obviously beam_1==beam_2==...beam_5
  * Maybe means I should use a bigger model
* For the most part it's a slight variation in the text compared to greedy
  * In Gramagul, the greedy type is "Human Archer", which is reasonable. But for beam_5 it's "Ramagul"
    *  So it doesn't really capture the funky name well
* Really likes repeating planeswalker abilities 
  * Both Gideons, Teferi

# Particular Cards