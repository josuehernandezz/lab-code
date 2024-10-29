my basic idea is this:

i am a grad student and i need to plot a lot of different kinds of data. such as UV-Vis, FTIR, PLQY, XRD, etc.

i want to group each of these areas of analysis in their own directories all grouped under a parent folder called 'code'

my idea is i want my helper.py file which is used to actually convert the raw text files with test/data points to a cleaned data only file. i don't want to have to copy my helper.py file into each sub directory (FTIR, XRD, etc.) into every file since i will use this helper file frequently.

and to futher confirm i run every python file by navigating to its respective directory 

code/PLQY/(my python files)

and i do:

python my_file.py

so i am running the python file in it's specific directory. but the issue i have is that python doesn't seem to know that my helper.py file is in a parent directory and it seems also just as repetitive and unnneccesary to import the sys.path file into every single file. can you help me with this? what is the best solution so i follow the DRY principle.