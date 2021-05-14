# MusicBattleships
Battleship: the musical

Project Distription:
  The idea behind "Battleship: The Musical" is to simulate how submariners have to memorize different engine sounds to 
determine the model and country of origin of ships nearby. Memorizing a dozen minute differences in engine sounds is boring, so
our team decided to make it fun and intuitive. We used the different timbre of instruments as a tool to help any person decern 
each ship in the game battleship. In our battleship, the player utilizes a submarine
that is on the enemy board. They can move around in the submarine and aim their sonar in varying directions to pinpoint locations 
of enemy ships. Each ship has its own instrument that plays whenever hit by a sonar bean shot by the submarine. At the
same time, each player must be cognizant of how much battery they still have in their submarine, or else they risk one of their
ships going into distress!!



How the Game Main Gameplay Loop Plays {{ Documentation }}:

Our battles are waged in phases!

First Phase (Sonar Phase):

    Position:
      Type the coordinates into your keyboard
      (your coordinates will be shown in the terminal)
    
    Aiming:
      Press '[' or ']' to rotate the sonar cone left or right respectively
      Press '-' or '+' to increase or decrease the sonar power respectively
    
    Pulsing Submarine Sonar:
      When you're happy with the position and aim of your submarine, press 'SPACE' to pulse your sonar
    
    Listen:
      This is the most important step. You must listen carefully for the musical melody made by the ships, if any
      The quieter the instrument in the melody, the further away the ship is
      (Remember that every ship is themed with a different instrument)

Second Phase (Missile Phase):

    Position:
      Same as the 'sonar phase' positioning
      Type the coordinates into your keyboard
      (your coordinates will be shown in the terminal)
    
    Launching the Missile:
      Same as the 'sonar phase' positioning
      When you're happy with the position and aim of your reticle, press 'SPACE' to fire your missile
      The space aimed at will highlight green on a miss and red on a hit

Third Phase (Regroup):
  
    This phase is all about regrouping your arsenals and preparing for an enemy attack
    (Basically waiting on your opponent's turn)


Things to Rememeber and to Look Out For:
  
    Sonar Resource Management:
    
      Sonar Charge and Power:
        Your subarine have a finite amount of battery charge that we call 'charge'
        Everytime you pulse your sonar, you use an amount of your sonar charge proportional your sonar pulse power level, 'power'
        The sonar power is roughly proportional to the width and radius of your sonar cone
        This all basically means that if your use too much sonar power on too many rounds, you may run out of charge
      
      Running Out of Sonar Charge and Distress Calls:
        If the unfortunate situation that you find yourself with no more sonar charge occurs, don't worry too much
        Your sonar charge will recharge to 50% at the beginning of your next turn
        But! There's a catch! One of your own ships will go into a distress call mode that allows your subarine to recharge
        The problem is that your enemy will now know the rough location of that ship
        This location will by highlighted green tiles on the enemy sonar map (but this is not an exact location)
        The distress call only last until the end of your enemies turn
        Long story short, don't let your submarine run out of charge!
      
      How to Recharge Your Sonar:
        As stated above, when your sonar runs out, one of your ships will go into a distress call
        But after that your submarine will recharge to 50%
        This is not optimal though, because you're putting one of your ships at risk
        The only other way to recharge your submarine is to hit an enemy ship
        When you hit an enemy ship, your submarine gains 25% of its maximum charge
        So stay hitting ships
        (there were plans for a way to forfeit a sonar pulse to charge 25%, but this was not added)
      
      
    Special Abilities:
      
      Pinpoint Accuracy:
        When increasing your submarine sonar to maximum power, if you have the charge
        You focus your sonar into one consentrated beam that, if you hit, allows you to know the precise coordinate that a ship resides
        However, this is not the location of the entire ship
        It is only a coordinate that a part of the ship resides in
        This ability uses about 90% of your sonar charge, so it can be risky
        
      Destroy Enemy Submarine:
        This is the 'shoot the moon' strategy 
        This ability allows you to destroy the enemy submarine for 2 rounds
        While a player has no submarine, they can not use their sonar to find the enemy ships and are forced shoot blindly
        This powerful move comes with a few downsides
          First:  the ability requires that your sonar charge is completely full to use
          Second: your sonar charge is completely depleted down to 0%
          Third: every single one of your ships go into a destress call to triangulate the location of the enemy submarine
        The third downside is the most harsh
        This means that the enemy will get a glimpes of the rough location of all your ships
        Take that as you will
      
      
    Miscellaneous:
      There are some situations where your submarine is directly under an enemy ship
      In these cases, the game will tell you that you are directly under a ship
      You then have an option to either shoot one of the four tiles around your submarine or shoot your own submarine
      Yes you can shoot your own submarine
      If you are so inclined, you loose your submarine for two rounds
      
      
How the Game is Setup:
    This game was designed to be played on a dual monitor setup where the two monitors are facing apart. When launching the game,
  place the window with half on one monitor and the other half on the other monitor. This game is also played on 
  one keyboard.
  

This was all that the game has to offer in its current form
I hope this helps you understand how to play
