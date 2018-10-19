import os, sys
from time import sleep
import pandas as pd
import pickle

Day = 0 # assume Day 0 initially
RewardList = [] # assume RewardList is empty

' Check to see if pickled files for Day and Reward List exist'

if os.path.isfile('DayCount.pkl') and os.path.isfile('RewardFile.pkl'):
    DayIn = open('DayCount.pkl', 'rb')
    Day = pickle.Unpickler(DayIn).load()
    DayIn.close()

    RewardIn = open('RewardFile.pkl', 'rb')
    RewardList = pickle.Unpickler(RewardIn).load()

    HabitIn = open('Habittochange.pkl', 'rb')
    CurrentReward = pickle.Unpickler(HabitIn).load()
    HabitIn.close()

    if Day <= len(RewardList):
        ResponseIn = open('UserResponse.pkl','rb')
        df = pickle.load(ResponseIn)
        ResponseIn.close()

        print ('WELCOME BACK')
        print(f'Experimend Day:{Day}\n')
        Location = input('Enter the location where you felt the craving \n')
        Time = input('Enter the time for the craving \n')
        EmotionalState = input('What is your emotional state like right now? \n ')
        OtherPeople = input('Who is currently around you?\n')
        PreAction = input('What action preceded the urge?\n')
        data = [Location,Time,EmotionalState,OtherPeople,PreAction,0,0,0,0]
        df.loc[Day] = data
        

        ExpReward = RewardList[Day-1]

        print (f'Today instead if {CurrentReward} you will try {ExpReward}')
        sleep(3)     # sleep for 5 minutes
        ThreeWords = []    
        ExpWords = input(' What comes to your mind after you experimented with this new reward, Write 3 words seperated by commas: ')
        ThreeWords = ExpWords.split(',')
        print (ThreeWords)
        df.loc[Day]['Word 1'] = ThreeWords[0]
        df.loc[Day]['Word 2'] = ThreeWords[1]
        df.loc[Day]['Word 3'] = ThreeWords[2]

        print ('I will check back in 15 min to see if you still have the urge')

        sleep(3)  # sleep for 15 minutes

        print (f'How do you feel now ? Do you still have the urge to try {CurrentReward} \n')

        FeelUrge = input('Do you? (Y/N) : \n')

        df.loc[Day]['Still Feel The Urge'] = FeelUrge
        Day = Day+1
        
        ResponseOut = open('UserResponse.pkl','wb')
        pickle.dump(df, ResponseOut)
        ResponseOut.close()

        RewardIn.close()

        DayOut = open ('DayCount.pkl', 'wb')
        pickle.dump(Day, DayOut)
        DayOut.close()

    elif Day > len(RewardList):

        end_of_exp = input('Would you like to print the data for your experiments? (Y/N): ')
        if end_of_exp =='Y' or end_of_exp=='y':
            ResponseIn = open('UserResponse.pkl','rb')
            df = pickle.load(ResponseIn)

            print (df)
        else:
            print ("Alright see you later")
            sys.exit()

    
else:
    HabitRoutine = input('Habit/Behavior you would want to change?\n')

    print('Cravings drive habits and Rewards satisfy cravings, next we figure out what cravings drive your behavior\n')
    
    RoutineCraving = input('what is the craving that drives/satisfies your habit/routine?\n')
    CurrentReward = input ('What is the reward of the routine? \n')
    'Part 2: Figure out cravings'
    print ('Cravings drive habits, habits are satisfied buy rewards')
    print ('For instance a craving to have more energy drives your habit of going for another cup of coffee\n')
    print ('In the above example Craving : burst of energy\n')
    print ('The reward: Cup of Coffee\n')
    print ('Next figure out alternate rewards that can satisfy the same cravings, for the above example the alternate rewards could be a. walk outside b. stretching etc\n')

    RewardList = []
    NextReward = "Y"
    while NextReward =="Y" or NextReward =="y":
      Reward = input ('Enter alternative rewards for your craving\n')
      RewardList.append(Reward)
      NextReward = input('Can you think of another alternative Reward? (Y/N)\n')

    RewardOut = open('RewardFile.pkl' , 'wb')

    pickle.dump(RewardList, RewardOut)

    RewardOut.close()

    Day = 1 # Start with Day one
    df = pd.DataFrame(columns=['Location','Time','Emotional State','OtherPeople','PreAction','Word 1','Word 2','Word 3','Still Feel The Urge'])
    print(f'Experimend Day:{Day}\n')
    Location = input('Enter the location where you felt the craving \n')
    Time = input('Enter the time for the craving \n')
    EmotionalState = input('What is your emotional state like right now? \n ')
    OtherPeople = input('Who is currently around you?\n')
    PreAction = input('What action preceded the urge?\n')
    data = [Location,Time,EmotionalState,OtherPeople,PreAction,0,0,0,0]
    df.loc[Day]=data
    df.index.name = 'Day'
    ExpReward = RewardList[Day-1]

    print (f'Today instead if {CurrentReward} you will try {ExpReward}')
    sleep(3)     # sleep for 5 minutes
    ThreeWords = []    
    ExpWords = input(' What comes to your mind after you experimented with this new reward, Write 3 words seperated by commas: ')
    ThreeWords = ExpWords.split(',')
    print (ThreeWords)
    df.loc[Day]['Word 1'] = ThreeWords[0]
    df.loc[Day]['Word 2'] = ThreeWords[1]
    df.loc[Day]['Word 3'] = ThreeWords[2]

    print ('I will check back in 15 min to see if you still have the urge')

    sleep(3)  # sleep for 15 minutes

    print (f'How do you feel now ? Do you still have the urge to try {CurrentReward} \n')

    FeelUrge = input('Do you? (Y/N) : \n')

    df.loc[Day]['Still Feel The Urge'] = FeelUrge

    print ('see you tomorrow')

    ResponseOut = open('UserResponse.pkl' , 'wb')
    pickle.dump(df, ResponseOut)
    ResponseOut.close()

    Day = Day+1
    DayOut = open('DayCount.pkl', 'wb')
    pickle.dump(Day, DayOut)
    DayOut.close()

    HabitOut = open('Habittochange.pkl', 'wb')
    pickle.dump(CurrentReward, HabitOut)
    HabitOut.close()

    


    
