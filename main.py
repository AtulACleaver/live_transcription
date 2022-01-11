from deepgram import Deepgram
import asyncio, json

# The API key you created in step 1
DEEPGRAM_API_KEY = 'ADD YOUR API KEY'

# Name and extension of the file you downloaded (e.g. sample.wav)
PATH_TO_FILE = 'Bueller-Life-moves-pretty-fast.wav'

async def main():
    # Initializes the Deepgram SDK
    dg_client = Deepgram(DEEPGRAM_API_KEY)

    # Creates a websocket connection to Deepgram
    socket = await dg_client.transcription.live({'punctuate': True})

    print('Connection Opened!')

    # Handle sending audio to the socket
    async def process_audio(connection):
        # Grab your audio file
        with open(PATH_TO_FILE, 'rb') as audio:
            # Chunk up the audio to send
            CHUNK_SIZE_BYTES = 8192
            CHUNK_RATE_SEC = 0.001
            chunk = audio.read(CHUNK_SIZE_BYTES)
            while chunk:
                connection.send(chunk)
                await asyncio.sleep(CHUNK_RATE_SEC)
                chunk = audio.read(CHUNK_SIZE_BYTES)

            # Indicate that we've finished sending data
            await connection.finish()

    # Receive transcriptions based on sent streams and write them to the console
    socket.register_handler(socket.event.CLOSE, lambda _: print('Connection closed.'))

    # Print incoming transcription objects
    socket.register_handler(socket.event.TRANSCRIPT_RECEIVED, print)

    # Send the audio to the socket
    await process_audio(socket)

asyncio.run(main())