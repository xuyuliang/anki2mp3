# Import boto3 library
import boto3

# Create a session object with a socket 5 proxy at 127.0.0.1:1080
# session = requests.Session()
# session.proxies = {
#   'http': 'socks5://127.0.0.1:1080',
#   'https': 'socks5://127.0.0.1:1080'
# }
# Create a client object for Amazon Polly service
client = boto3.client('polly',region_name='us-east-1')

# Define the text to synthesize
text = "Hello, this is a test of Amazon Text to Speech Polly."

# Define the voice ID and output format parameters
voice_id = "Joanna"
# voice_id = "Brian"

output_format = "mp3"

# Call the synthesize_speech method with the text and other parameters
response = client.synthesize_speech(Text=text, VoiceId=voice_id, OutputFormat=output_format)

# Check if the request was successful
if response["ResponseMetadata"]["HTTPStatusCode"] == 200:
  # Get the audio stream from the response as bytes
  audio_stream = response["AudioStream"].read()

  # Write the bytes to a file
  with open("output.mp3", "wb") as f:
    f.write(audio_stream)

  # Print a success message
  print("Audio file saved as output.mp3")
else:
  # Print an error message
  print("Request failed: ", response["ResponseMetadata"]["HTTPErrorMessage"])