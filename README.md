# Discord-Media-Extractor
This script will use your downloaded data from discord and go through all messages and download all images and videos you have ever sent through DMs

### Use
This script simply uses the data that discord sends you when you request it will look through all direct messages and look for a a image/video, these are found by the discord url given by discord 'https://cdn.discordapp.com/attachments/'. It will then download all of these into a `downloads` file then into either `images` or `videos` inside the `messages` folder.

### How to use
- Download account data from discord (Settings > Privacy & Safety > Request Data)
- Download data once sent to email (This could take up to a month depending on your account age.)
- Download the `main.py` file
- Place `main.py` in 'package/messages'
- Install the requirements.
- Run `main.py`

It will then run and look through all folders inside the messages folder, though all the .csv of message data, and pull all discord links for all images and videos sent and will download them to `package/messages/downloads/images-videos`. 

This can take a long time to excecute up to hours to fully complete, it depends on internet speed mostly and also how much data and files you have to download, the code itself is optimised for max speed.

Any issues or questions feel free to message me on discord @LukeeSucks
