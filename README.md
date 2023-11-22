To install dependencies:
pip3 install -r requirements.txt

To run the bot as a process
nohup python -m forwarder &

Incase new members join the internal group, (or someone in the group is promoted, the chat id may change) incase this happens:
1. On the internal group type "/id"
2. You should get a negtative number as a reply.
3. Now, take this number and edit the "chat_list.json" file and put that number as the value of the source.
4. Restart the bot.

