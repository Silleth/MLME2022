# MLME2022 README

## Setup

### Items
You will all the code in the **NLP Processing** Folder. There you will be met with another folder called **Output**. You will find an **Unreal** and **Python** version of the most recent dataset, once you execute the code inside of the **DialogueTool.py**. If you choose to move the **DialogueTool.py**, you will generate a new **Output** folder, as it spawns from its registered directory.

From the directory of this repository you will also find a folder called **"C++ Exhibit"**. This folder contains the most important part of the Unreal Project code, and is also the code that is displayed in the included report.

#### I DO NOT RECOMMEND INSTALLING THE UNREAL PROJECT

I am just as excited for this project as you are, but I will try and see if I can't give a display at the exam instead. I am unsure how many Unreal Engine projects you have tried to install unshipped, but I can tell that the ReadMe may be convoluted due to the potential error it could create.

## ReadMe

### DialogueTool.py

You are required to have **Python 3.10** installed to not avoid any incompatibility issues with Tensorflow 2. Any other modules you would have to install in a virtual environment is set up to automatically install once you run the DialogueTool. If you do not like this, you should feel free to comment them out and install them on your own terms. 

These are the modules to download, in case you were curious:
<ul>
  <li>tensorflow</li>
  <li>tensorflow_hub</li>
  <li>numpy</li>
  <li>Fourth item</li>
  <li>matplotlib</li>
  <li>seaborn</li>
  <li>pandas</li>
</ul>

Press the play button and figures should pop up sequentually as you click them away. First time launching can take some time. Oh, and that's it! You've gotten plots, data and perhaps a far too overdone documentation inside of the file. I do apologize for that.

### Downloading, installing and launching the Unreal Engine 5 Project

#### Requirements:
<ul>
  <li>Unreal Engine 5.1.0</li>
  <li>Visual Studio 2019 (comes with installation)</li>
  <li>Keyboard to Press "F" near NPCs</li>
</ul>

I respect your time, so I will try and make it brief. You will need an **Epic Account**, to install **the latest Unreal Engine (5.1.0)**. Choosing C++ with Unreal Engine automacally increases the project size by a few GB due to the uncompiled nature of Unreal. That way, I was unable to upload the project on Github. Worry not, because I was able to zip the file to my trusty **Google Drive**

Link to my Google Drive: <https://drive.google.com/file/d/17VEwL5Cewca0vYi36joKCV-4BV0K1gZE/view?usp=sharing>

This may take a while to install. Once installed, put it somewhere safe with the allocated space.

You start up the **ML_Project.sln** if you want to browse through the C++ side of things. I believe if you just use **ML_Project.uproject**, they may leave you alone. **This way you can not do any fixes on the fly in c++** as the live coding won't work. 

To make the live coding work, you have to rebuild the entire project inside of Visual Studio. If it does it conventiently fast, it will most likely say that it cannot find the module ML_Project. Then you rebuild yet again and it will fix itself.

Once in and you can see the platforming level and an NPC, **you may want to delete the NPC** and dive into the **Conent/ThirdPerson/Blueprints/BP_NPC** to deploy a new character. This is because this has been my testing bed for quite some time, and a lot of crashes happens. The scene component that is called SC_DialogueM does not work as intended, the way it has been released. 

If everything looks fine, you can try and play the scene. A couple of things can go wrong here. The most prevalent is that the **BP_NPC** managed to remove the DataTable **PlayerDialogue**. You fix this by going into the Blueprint view and select the component from the component view and press on the square called **Player Dialogue**. This is also here where you can alternate between **Player Dialogue Num**. Due to the scacity of the dialogue, only a few lines got the most answers for you. I would recommend keeping it at 8.

In case you would have a look at it, you find the file in **Content/Files/PlayerDialogue**. The file itself has to be replaced in **File Explorer** if you want to try new data or expand on the already existing dialogue lines. The world is your oyster.

You talk to the NPC, by entering their collider **(The Trigger box)**. Once you collide, the c++ side will check it you are near and **if you then press "F**, you should see a UI displaying the answer. Currently all you can do is to chat it up until it begrundingly tells you it is done talking to you. 

### You Should be good to go! 

