## Generating Magic the Gathering cards using GPT2.


## File Structure:
CardNamesRoundN: All cards generated for Nth version of the model. Each directory contains a all cards generated with that name across all different generation methods  
GenerationTypesRoundN: All cards generated for the Nth version of the model. Each directory contaisn all cards generated with that hyperparmater set across different cards.  

### Different model versions:
(corresponds to CardNamesRoundN/GenerationTypesRoundN)
1. using "gpt2" (as named by huggingface pretrained models). Nothing fancy here, just that.
2. Increase model capacity to use gpt-2 medium (twice as big)

### Future steps
* Use sep tokens for end of cards...
* Add mtg custom stuff to vocabulary