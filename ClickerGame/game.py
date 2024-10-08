import tkinter as tk
from tkinter import ttk
# Upgrades data: cost, cps, name, image, Is modifier?
rabbit = (20, 1, 'Rabbit','rabbit.png', False)
squirrel = (80, 2, 'Squirrel', 'squirrel.png', False)
farmer = (150, 5, 'Farmer', 'farmer.png', False)
harvester = (400, 12, 'Harvester', 'harvester.png', False)
greenhouse = (800, 25, 'Greenhouse','greenhouse.png', False)
murray = (1, -1, 'Murray', 'murray.png', False)
# Click modifier data: Cost, modify amount, name image
iron_hoe = (100, 1, 'Iron hoe', 'Iron_Hoe.png', True)
golden_hoe = (500, 2, 'Golden hoe', 'Golden_Hoe.png', True)
diamond_hoe = (1000, 4, 'Diamond hoe', 'Diamond_Hoe.png', True)
# Achievements data: Name, Description, Image
achivements_data = [('Rabbit Roundup','Buy five Rabbits', 'rabbit.png'),
                    ('Squirrel Squadron','Buy five Squirrels', 'squirrel.png'),
                    ('Cultivation Commander','Employ three farmers', 'farmer.png'),
                    ('Harvesting Haven','Buy three harvesters', 'harvester.png'),
                    ('Greenhouse Gardener','Buy two greenhouses', 'greenhouse.png'),
                    ('CARROT DOMINATION','Own ten greenhouses', 'greenhouse.png'),
                    ('???', 'Own 50 Murrays', 'universe.png'),
                    ('Clicking Champion', 'Reach 15 carrots per click', 'cursor.png'),
                    ('Clicking Grandmaster', 'Reach 40 carrots per click', 'cursor2.png'),
                    ('Thousand-Carrot Harvest', 'Reach 1000 carrots', 'carrot.png'),
                    ('Ten-thousand Carrot Harvest', 'Reach 10000 Carrots', 'carrots2.png'),
                    ('Crown of Carrots', 'Reach 100000 carrots', 'carrots3.png')]
Active_Window = '' 
achivement_objects=[] # List to hold all the achivement objects
completed_achivements = [] # List to hold all the completed achivements
def check_achivement(): # This function runs itself every second to check all the acheivements
    # The way it checks the achivements is really confusing and and weird
    global shop, g, completed_achivements
    # The achivements list is created again every single time
    # If the achivements list is stored globally, it will never update because it is static
    # The values are stored as decimals (real value/target value)
    achievements = [shop.rabbit.count/5, shop.squirrel.count/5, shop.farmer.count/3, shop.harvester.count/3, shop.greenhouse.count/2, shop.greenhouse.count/10, shop.murray.count/50, g.click_modifier/10, g.click_modifier/20, g.score/1000, g.score/10000, g.score/100000]
    # There is a second global list of the indexes of all the completed achievements
    for i in completed_achivements: # Loop through the list of completed achievements
        achievements[i] = 2 # Sets the achivement to 2 because its already been met (it has to be an int)
    for each_achievement in achievements: # Loops through through the other achivements
        # This is possible as the achivement requirements and the achivement objects lists share the same indexes
        # Meaning they share the same position in two different lists
        achivement_objects[achievements.index(each_achievement)].status = each_achievement # Set the status of the achivement
        if each_achievement < 2 and each_achievement >= 1: # It will be true if the requirement has been met
            completed_achivements.append(achievements.index(each_achievement)) # Add the achivement to the completed list
            window = tk.Toplevel() # Create an window
            window.title='Achievement' 
            window.geometry('320x200')
            title = ttk.Label(window, text='ACHIVEMENT GET!', font=('Comic Sans MS',20)) # Add text
            title.pack()
            achivement_name = ttk.Label(window, text=achivement_objects[achievements.index(each_achievement)].name, font=('Comic Sans MS',20)) # Add text
            achivement_name.pack()
            achivement_img = tk.PhotoImage(file=achivement_objects[achievements.index(each_achievement)].img)
            achivement_img_label = ttk.Label(window, image=achivement_img, font=('Comic Sans MS',20)) # Add text
            achivement_img_label.pack()
            achivement_img_label.image=achivement_img # Corbin showed me that this line prevents the image from being garbage collected
            achivement_objects[achievements.index(each_achievement)].status = 'Completed' # Set the status of the achivement object to completed
            root.after(2000, lambda:window.destroy()) # Destroy the window after 2000ms
    root.after(1000, lambda: check_achivement()) # The function calls itself after 1000ms

class Game: # I made the game a class so that it is easier to access the tkinter widgets and data of the game at any point in the code
    # Create the properties of the game
    # Innit called when the class is initiated to create all the tkinter widgets
    def __init__(self, parent):
        # Assign properties that are relevant to the game
        self.score = 0
        self.autoclick = 0
        self.click_modifier = 1
        # Create the widgets of the Game 
        global root # root is the actual root window
        self.title = ttk.Label(parent, text='Carrot Clicker', font=('Comic Sans MS', 50))
        self.title.pack()

        root.after(1000, self.autoGame_increment) # Increment the carrots by the cps every second
        
        self.img = tk.PhotoImage(file='main_carrot.png') # Load the image of a carrot
        self.carrot_button = ttk.Button(parent, image=self.img, command=self.click) # Image button
        self.carrot_button.pack(fill='x') # Stretch the button to fill the frame in the x direction
        self.label = ttk.Label(parent, text=f'Score: {self.score}', font=('Comic Sans MS',50))
        self.label.pack() # Text showing the score
        self.cps_info = ttk.Label(parent, text=f'Farming {self.autoclick} carrots per second', font=('Comic Sans MS',20))
        self.cps_info.pack()
        self.modifier_info = ttk.Label(parent, text=f'Currently gaining: {self.click_modifier} carrots per click', font=('Comic Sans MS',20))
        self.modifier_info.pack()
    def click(self): # Function run when the button is clicked
        self.score += g.click_modifier # Increase the score by the click modifier
        self.label.config(text=f'Score: {self.score}')
    def autoGame_increment(self): # Increase the score every second by autoclick
        self.modifier_info.configure(text=f'Currently gaining {self.click_modifier} carrots per click')
        self.cps_info.configure(text=f'Farming {self.autoclick} carrots per second') # Update the text to show the autoclicks per second
        self.score += self.autoclick # Add the amount of autoclicks to the score
        self.label.config(text=f'Score: {self.score}') # Update the score text
        root.after(1000, self.autoGame_increment) # Method calls itself to loop
class Shop: # Like the game object, the shop class is made so it is easier to access the tkinter widgets at any point in the code
    def __init__(self, parent):
        self.title = ttk.Label(parent, text="Upgrades", font=('Comic Sans MS',50))
        self.title.pack() # Load the title of the shop
        #https://blog.teclado.com/tkinter-scrollable-frames/
        canvas = tk.Canvas(parent, width=500)
        scrollbar = ttk.Scrollbar(parent, orient="vertical", command=canvas.yview)
        self.shop_frame = ttk.Frame(canvas)
        self.shop_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=self.shop_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        global rabbit, squirrel, farmer, harvester, greenhouse
        # Make all the upgrades inherited by the shop class
        # There are astrisks because i need to load the data from the list into arguments
        self.rabbit = Upgrades(*rabbit, self.shop_frame)
        self.squirrel = Upgrades(*squirrel,self.shop_frame)
        self.farmer = Upgrades(*farmer,self.shop_frame)
        self.harvester = Upgrades(*harvester,self.shop_frame)
        self.greenhouse = Upgrades(*greenhouse,self.shop_frame)
        self.murray = Upgrades(*murray,self.shop_frame)
        self.iron_hoe = Upgrades(*iron_hoe, self.shop_frame)
        self.golden_hoe = Upgrades(*golden_hoe, self.shop_frame)
        self.diamond_hoe = Upgrades(*diamond_hoe, self.shop_frame)
class Upgrades: # The upgrade class is a "template" for each upgrade. This is efficient as the game can make as many upgrade objects as possible
    # Innit is called when an upgrade is made
    def __init__(self, cost, cps, name, img, is_modifier, parent):
        global shop
        # Initiate the properties of the Upgrade to the arguments given when the object was created
        self.count, self.cost, self.cps, self.name, self.modifier = 0, cost, cps, name, is_modifier
        self.img = tk.PhotoImage(file=img) # Load the image using tkinter
        self.Create_upgrade(parent) # Load all the UI
    def Create_upgrade(self, parent): # Create the tkinter widgets inside of the parent
        self.frame = ttk.LabelFrame(parent)
        self.frame.pack(fill='x') # fill='x'
        self.frame.columnconfigure(1, minsize=280) # Make the minimum size of the 2nd column 280pixels
        self.frame.columnconfigure(2, minsize=150) # Make the minimum size of the 3rd column 150pixels
        self.image = ttk.Label(self.frame, image=self.img)
        self.image.grid(column=0, row=0) # Put the image at 0,0 in the grid
        if self.modifier:
            self.text = ttk.Label(self.frame, text=f'{self.name} \n+{self.cps} click modifier (Owned {self.count})', font=('Comic Sans MS',15)) 
        else: 
            self.text = ttk.Label(self.frame, text=f'{self.name} \n+{self.cps} cps (Owned {self.count})', font=('Comic Sans MS',15)) 
        self.text.grid(column=1, row=0, sticky=tk.W) # Add the text that aligns towards the left
        self.buy_item = ttk.Button(self.frame, text=f"Buy (${self.cost})", style='Accent.TButton', command=lambda: self.Buy_upgrade())
        self.buy_item.grid(column=2, row=0, sticky=tk.W) # Add the button on the 3rd column

    def Buy_upgrade(self): # Buy Upgrade method
        global g
        if self.cost <= g.score: # Check if there is enough money
            g.score -= self.cost # Remove the money
            self.cost = round(self.cost*1.5) # Increase the cost of the upgrade by 1.5x
            # Update the widgets with new info
            self.buy_item.config(text=f"Buy (${self.cost})") 
            self.count += 1 # Increase the amount of itself
            if self.modifier:
                g.click_modifier += self.cps # Add cps
                self.text.configure(text=f'{self.name} \n+{self.cps} click modifier (Owned {self.count})')
            else:
                g.autoclick += self.cps # Add cps
                self.text.configure(text=f'{self.name} \n+{self.cps} cps (Owned {self.count})')
            g.label.config(text=f'Score: {g.score}') 
class Achievements: # The achievement class is a template for all the achivements. It makes creating achivements easy and efficient.
    # Innit is called when an achivement object is made
    def __init__(self, name, desc,img):
        # Create the properties of the upgrade to the arguments given when the object was created
        self.name, self.desc, self.img = name, desc, img
        self.status = 0
    def Create_Achivement(self, parent, index): # Load the tkinter widgets into the 'parent'
        self.photo=tk.PhotoImage(file=self.img) # Load the image using tkinter
        self.button = tk.Button(parent, image=self.photo, command=(self.Create_Window)) # Create the button used to open the window
        self.button.grid(column=index%2, row=index//2, padx=(10,0), pady=(5,5))
    def Create_Window(self): # Make a window showing achivement data
        global Active_Window
        try: Active_Window.destroy() # Destroy any other achievement windows if there are any
        except: pass
        self.root = tk.Toplevel() # Create a window
        self.root.title='Achievement'
        Active_Window=self.root # Set the active window to the one just created
        self.image = ttk.Label(self.root, image=self.photo)
        self.image.pack(side=tk.LEFT) # Add an image on the left
        self.name_label = ttk.Label(self.root, text=self.name, font=('Comic Sans MS',30))
        self.name_label.pack() # Add the name into the window
        self.label = ttk.Label(self.root, text=self.desc, font=('Comic Sans MS',20))
        self.label.pack() # Add the achivement's description into the label
        if self.status==2: # Check if the achivement has been met. If the value is 2, it has already been met
            self.label = ttk.Label(self.root, text=f'Completed', font=('Comic Sans MS',20)) # Set the status text to Completed
        else: # If the achivement hasn't been met, show a percentage of completion
            self.label = ttk.Label(self.root, text=f'Status: {round(self.status*100)}% completed', font=('Comic Sans MS',20))
        self.label.pack()
class Showcase: # The achivement showcase. Its just a class so that it is easier to reference later
    def __init__(self, parent):
        global g, achivement_objects 
        self.title = ttk.Label(parent,text="Achievements", font=('Comic Sans MS',50)) 
        self.title.pack() # Load the title of the achivements showcase
        self.frame = ttk.Frame(parent) # Create a frame for all the achievements
        self.frame.pack(anchor='center')
        for i in range(len(achivements_data)): # Iterate through all the achivement data
            achivement_objects.append(Achievements(*achivements_data[i])) # Create an achivement object and add it to the list
            achivement_objects[i].Create_Achivement(self.frame,i) # Load the UI of the achivement using the arguements for parent and index
        check_achivement() # Continously checks if an achivement has been met
root = tk.Tk()
root.title("Game")
root.state("zoomed")
# Make the main frames of the game
Game_frame = ttk.Frame(root, width=600) 
Game_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
Game_frame.propagate(0)
Upgrades_frame = ttk.Frame(root)
Upgrades_frame.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)
showcase_frame = ttk.Frame(root)
showcase_frame.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)
# Create the Main Objects
g = Game(Game_frame) # The main game object is called g to avoid confusion with the class
shop = Shop(Upgrades_frame) # The shop is called shop
showcase = Showcase(showcase_frame)
root.mainloop() # Run tkinter loop
