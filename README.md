# HomeworkBot
****
## What is HomeworkBot?
**HomeworkBot** is a Discord Bot built for **School Discord Servers**. Its purpose is to be a **better to-do list** for **students**.
## Current Functions
Currently, HomeworkBot is a Minimum Viable product (MVP). For Admins, there are currently 6 admin commands, allowing you to add and remove: valid periods, valid classes, and valid teacher names.  
There are also currently 7 rudimentary homework commands (can be used by anyone). 3 of which allow you to view the valid periods, classes, and teachers.  
The other 4 pertain to entering in homework into your to-do list and modifying things about your homeworks.
### Admin Commands
- #### /insert_class_periods
- #### /insert_class_names
- #### /insert_teacher_names
- #### /remove_periods
- #### /remove_class_names
- #### /remove_teacher_names
### Homework Commands
- #### /show_class_periods
- #### /show_class_names
- #### /show_teacher_names
- #### /show_homework (CURRENTLY ONLY SUPPORTS 3 HOMEWORK DUE TO MAXIMUM EMBED FIELD LIMITS BY DISCORD)
- #### /add_homework
- #### /remove_homework
- #### /change_homework_status
## Future Functions
HomeworkBot is, as mentioned previously, a MVP. It currently only has the core functions as a to-do list.  
As development continues, new commands and more features will be added. 
### Planned Features  
* Syncing whenever a Homework is added.
* Syncing as an optional setting for users.
* Automatically deleting Homework that is past-due.
* Sending multiple embeds to circumvent maximum embed field limits. 
### Other Potential Additions
* Reliability Scores for syncers. (Basically, people are graded on how good their syncs are)
* Using a Reliability Score as a filter. (Allowing users to limit who they get their syncs from)


## How to Setup?
1. ### Install Dependencies
   **In your terminal, do:**
    >    pip install -r requirements.txt   

    This downloads the dependencies.
2. ### Create a .env file
    Simply create a file named .env and enter in your details.  
    > DISCORD_TOKEN="INSERT YOUR TOKEN HERE"  
   > DATABASE="INSERT YOUR DATABASE HERE"  
   > USERNAME="INSERT YOUR USERNAME HERE"  
   > HOST="INSERT YOUR HOSTNAME HERE"  
   > PASSWORD="INSERT YOUR PASSWORD HERE"  
   > AUTHORIZED_USER="INSERT YOUR USER ID HERE"  
    
    Fill out all of these fields with your specific information.  
    Token is your bot token and Authorized User is your Discord User ID.  
    Everything else is database details to connect to your database. 
3. ### Enter whatever you want into periods, classes, and teacher names.
    That is all the bot setup done! Now you can run the program, go on Discord and start entering stuff in.