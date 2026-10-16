 EXTENSION 5: RUNNING ORDER

I added the Running Order class to help the MC organise and manage performances during the Campus Talent Show.
This class keeps a list of all the performances that have been successfully booked for the show.
It has three main methods:
 1. add() - Adds a new performance to the running order.
 2. remove() - Removes a performance from the list.
 3. display() - Shows all booked performances in the order, they were added, together with their duration in minutes.
    
If no performances have been added, the display() method
 shows a message saying "No acts booked."
 
 I also connected the RunningOrder class to the TalentShow , so that every talent show has its own running order.
 When the MC books a performance, the program first checks, whether there is enough time left using the ShowClock class.
 
If there is enough time, the performance is added to the running order. If there is not enough time, it is not added.

 This extension demonstrates Object-Oriented Programming
concepts such as classes, objects, methods, and composition.
 The main purpose of this extension is to help the MC.
 
Keep track of booked performances, know which act comes
 first or next, and manage the talent show in an organised way.
