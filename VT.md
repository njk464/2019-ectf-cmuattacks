
# Potential attacks
- No integrity check on game body
- Extra large games
  - Appending bytes (i.e. 512M of 'A') to a predefined game leads to r2/r0 control when we play the game

# Attacks that don't work
- Ethernet based attacks
- Bruteforcing 
