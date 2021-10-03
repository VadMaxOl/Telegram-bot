# Telegram-bot
Telegram-bot for hotel search

Project: telegram bot for site analysis Hotels.com and search for suitable hotels for the user
Author: Baibekov Vadim Albertovich
The name of the bot in telegram: VENOM_newbot
The project structure includes the following files:

main - is responsible for the dialog with the user and receives commands from him
hotels - accepts parameters, searches for hotels and returns a list with hotels back to main for output to the user
foto - a separate file for searching for photos of hotels
config - to contain a token
history - this log file will appear in the process. Teams and found hotels are saved in it.

To run the program, you must:

1. Copy the repository to your computer
2. To install the necessary libraries, write in the terminal: pip install -r requirements.txt
3. To launch the bot: write "python" in the PyCharm terminal main.py " (or in any other IDE)
4. To stop the bot: press Ctrl+C and wait

After launching the program, the user can write any message.
If the entered message is not "Hello" or "hello", the bot will ask the user to enter the command /help or /helloworld.
List of commands available to the user:

/help - when clicked, the message "Write Hello" will appear
/helloworld - when clicked, "This is a Telegram bot for finding hotels. Author Baibekov Vadim Albertovich"
/ lowprice - search for the cheapest hotels in the city.
a) After clicking, the user will be prompted to enter the search city.
The city must be entered in English letters (for example, boston). The city, preferably, should be large.
It doesn't matter for the program - the name of the city will be entered with a capital letter or with a small one.
b) Next, the program will ask: "Enter the number of hotels (no more than 8)"
The number of 8 hotels is a limitation on the TOR to reduce the query execution time (10-15 seconds)
The program will find the cheapest hotels according to a pre-established sorting method (from cheap to expensive).
c) After displaying the list of hotels, the bot will ask: "Do you want to see photos of selected hotels?"
Answer options: "Yes", "yes". With any other response, the program terminates and starts again.
d) If the answer to the previous question was yes, the bot will ask you to enter the number of photos to view for each hotel.
There is a limit on TK - a maximum of 3 photos. After the photo is output, the program terminates and waits for the next command.
/highprice - search for the most expensive hotels in the city.
The description of this command does not differ from the /lowprice command. The only difference is that reverse sorting is used here.
From expensive hotels to cheap ones.
/bestdeal - hotels that are optimal in price and location.
After entering the command, it is requested:
a) the search city.
b) number of hotels.
c) the price range of the cost of hotels per day. You need to enter the range with a hyphen and without spaces (example: 10-50)
d) the range of the distance of hotels from the city center. You need to enter the range with a hyphen and without spaces (example: 5-30)
e) does the user want to see photos of hotels
f) number of hotel photos
/history is a command that allows you to get the search history of hotels as a separate file.
The file will contain the history of commands entered by the user with the date and time.
And also, found hotels.

The program provides protection against incorrectly entered commands.

If a non-existing city is entered or the program does not find anything in the specified city, a message will appear:
'A non-existing city has been entered or there are no hotels matching the search conditions'
If the user tries to enter the number of hotels more than 8, as well as the number of photos more than 3, a message will appear:
You have entered more than 8 hotels. Do you want to break the program?! :) or you have entered more than 3 photos. Do you want to break the program?! :)
And the program will start again.
If the user in the /bestdeal command tries to enter a range of prices or distances where the first number is greater than the second, it will be output:
"Actually, the first number should be less than the second. Do you want to break the program?! :)"
The program will start again.

Good luck!
