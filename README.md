# MusicBattleships
Battleship: the musical

Project Distription:
  The idea behind "Battleship: The Musical" is to simulate how submariners have to memorized different engine sounds to 
determine the model and country of origin of ship nearby. But memorizing a dozen different minute differences in engine sounds,
our team decided to make it fun and intuitive. We used the different timbre of instruments as a tool to help any person decern 
the difference of the ships on the board of a normal game of battleship. In our battleship game, the player utilizes a submarine
that is on the enemy board. They can move around in the submarine and aim their sonar in varying directions to pinpoint locations 
of enemy ships. Each ship has its own instrument that plays whenever hit by a sonar bean shot by the submarine. Though, At the
same time, each player must be cognizant of how much battery they still have in their submarine, or else they risk one of their
ships going into distress!!



How the Game Main Gameplay Loop Plays {{ Documentation }}:

Our battles are waged in phases!

First Phase (Sonar Phase):

    Position:
      Type in the coordinates into your keyboard
      (your coordinates will be shown in the terminal)
    
    Aiming:
      Press '[' or ']' to rotate the sonar cone left and right respectively
      Press '-' or '+' to increase or decrease the sonar power respectively
    
    Pulsing Submarine Sonar:
      When you're happy with the position and aim of your submarine, press 'SPACE' to pulse your sonar
    
    Listen:
      This is the most important part. You must listen carefully for the musical melody made by the ships, if any
      The quieter the instrument in the melody, the further away the ship is
      (Remember that every ship is themed with a different instrument)

Second Phase (Missile Phase):

    Position:
      Same as the 'sonar phase' positioning
      Type in the coordinates into your keyboard
      (your coordinates will be shown in the terminal)
    
    Launching the Missile:
      Same as the 'sonar phase' positioning
      When you're happy with the position and aim of your radicle, press 'SPACE' to fire your missile
      The space aimed at will highlight green on an miss and red on a hit

Third Phase (Regroup):
  
    The phase is all about regrouping your arsenals and preparing for an enemy attach
    (Basically waiting on your opponents turn)


Things to Rememeber and to Look Out For:
  
    Sonar Resource Management:
    
      Sonar Charge and Power:
        Your subarine have a finite amount of battery charge that we call 'charge'
        Everytime you pulse your sonar, you use an amount of your sonar charge proportional your sonar pulse power level, 'power'
        The sonar power is roughly proportional to the width and radius of your sonar cone
        This all basically means that if your use too much sonar power on too many rounds, you may run out of charge
      
      Running Out of Sonar Charge and Distress Calls:
        If the unfortunate situation that you find yourself with no more sonar charge occures, don't worry too much
        Your sonar charge will recharge to 50% at the beginning of your next turn
        But! There's a catch! One of your own ships will go into a distress call mode to let your subarine know the position to recharge
        The problem is that that lets your enemy know a rough location of that ship
        This location will by highlighted green tiles on the enemy sonar map (but this is not an exact location)
        The distress call only last until the end of your enemies turn
        Long story short, don't let your submarine sonar charge run out!
      
      How to Recharge Your Sonar:
        As stated above, when your sonar runs out, one of your ships go into a distress call
        But after that your submarine is recharged to 50%
        This is not optimal though, because you're putting your ship at risk
        The only other way to recharge your ship is to hit an enemy ship
        When you hit an enemy ship, your submarine gains 25% of its max charge
        So stay hitting ships
        (there were plans for a way to forfeit a sonar pulse to charge 50%, but this was not added)
      
      
    Special Abilities:
      
      Pinpoint Accuracy:
        When increasing your submarine sonar to max power, if you have the charge
        You focus your sonar into one consentrated beam that, if you hit, allows you to know the precise coordinate that a ship resides
        This is not the location of the entire ship though
        It is only a coordinate that a part of the ship resides in
        This ability uses about 90% of your sonar charge, so it can be risky
        
      Destroy Enemy Submarine:
        This is the 'shoot the moon' stratagy 
        This ability allows you to destrow the enemy submarine for 2 rounds
        While a player has no submarine, they can not use sonar to find enemy ships and have to shoot blind
        This powerful move comes with a few downsides
          First:  the ability requires that your sonar charge is completely full to use
          Second: your sonar charge is completely depleted down to 0%
          Third: every single one of your ships go into a destress call to triangulate the location of the enemy submarine
        The third downside is the most harsh
        This means that the enemy will get a glimps of the rough location of all your ships
        Take that as you will
      
      
    Miscellaneous:
      There are some situations where your submarine is directly under an enemy ship
      In these cases, the game will tell you that you are directly under and ship
      There you have an option to either shoot one of the four tiles around your submarine or shoot your oen submarine
      Yes you can shoot your own submarine
      If you decide to for whatevery reason you have
      You loose your submarine for two rounds
      
      
How the Game is Setup:
    This game was deside to be played on a duel monitor setup where the two monitors are facing apart. When launching the game,
  place the window with half the window on one monitor and the other half on the other monitor. This game is also played on 
  one keyboard.
  

This was all that the game has to offer in its current form
I hope this helps you understand how to play
