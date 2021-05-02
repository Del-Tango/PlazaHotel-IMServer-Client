# PlazaHotel-IMServer-Client

The PlazaHotel project is an instant messaging application which allows clients to book a room that is not currently in use and set a guest list of aliases they are expecting to the conversation. 

Available rooms are grouped together on hotel floors, and each floor (with the exception of level 0) is protected by a level access pass. If the client that booked the room decided to set a guest list, only the specified guests can join the conversation, otherwise, anyone with a level access pass can join the conversation, if the number of members does not exceed the rooms capacity. 

Clients connect via SSH to a dedicated user that the PlazaHotel sets up. The client will startup at login, and all interrupt signals like Ctrl - C, Ctrl - D, Ctrl - Z will logout the user. 

The main application logic is built using Python3, and the CLI interface is written using BASH with some help from the MachineDialogue framework (v2.1 LookingGlass).

For a quick-start guide, go to the following blog post: https://alvearesolutions.wordpress.com/2021/04/25/plaza-hotel-v1-0-whispers-im-server-client/
