from pyrogram import Client
TOKEN = '6122853784:AAFicZRlkquME4SOM4N34Sxg2PwXorR8zK8'
ADMIN_ID = 6001909175
api_id = 26017773
api_hash = 'eb6b6fa7473e6d04f7f3bb48d87e7dc1'
client = Client(name='anon', bot_token=TOKEN, api_id=api_id, api_hash=api_hash)
client.start()
f = open('cap.jpg', 'rb')
client.send_photo(ADMIN_ID, caption='Пройдите капчу', photo=f)
client.terminate()
client.disconnect()
f.close()


@client.on_message()
def set_cap(client, message):
    file = open('cap.txt', 'w')
    file.write(message.text)
    file.close()
    exit()


client.run()
