import torch
import os
import requests
import json
import openai
import random
import imageio
from moviepy.editor import VideoFileClip, AudioFileClip
import datetime
from dotenv import load_dotenv
from gtts import gTTS
from elevenlabs import stream
from elevenlabs.client import ElevenLabs 
import time


# Load environment variables from .env file
load_dotenv()

# Get API keys from .env file
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
MINIMAX_API_KEY = os.getenv("MINIMAX_API_KEY")

# Initialize ElevenLabs client
client = ElevenLabs(api_key=ELEVENLABS_API_KEY)

model = "video-01"
output_file_name = "generated_video.mp4"

# Function to generate script
def generate_youtube_script(topic, prompt):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=175  # Approx. 1.5-minute script
    )
    script_text = response["choices"][0]["message"]["content"]
    return script_text

# Define topic
def generate_and_save_script(topic, prompt):
    script = generate_youtube_script(topic, prompt)

    if not script.strip():
        raise ValueError("❌ Error: The script text is empty! Cannot generate voiceover.")

    filename = "youtube_script.txt"
    with open(filename, "w", encoding="utf-8") as file:
        file.write(script)
    
    print(f"✅ New script generated and saved as {filename}\n")
    return script  # FIX: Return script so it can be used in generate_voiceover()

# Generate voiceover using ElevenLabs
def generate_voiceover(script, voice_type="JBFqnCBsd6RMkjVDRZzb"):
    if not script.strip():
        raise ValueError("❌ Error: The script text is empty! Cannot generate voiceover.")

    print(f"🎙️ Generating voiceover with text:\n{script}\n")

    audio_stream = client.text_to_speech.convert_as_stream(
        text=script,
        voice_id=voice_type,
        model_id="eleven_multilingual_v2"
    )
    with open("voiceover.mp3", "wb") as f:
        for chunk in audio_stream:
            f.write(chunk)
    
    print("✅ Voiceover generated successfully: voiceover.mp3")
    return "voiceover.mp3"

# Submit video generation task
def invoke_video_generation(prompt):
    print("🚀 Submitting video generation task...")
    url = "https://api.minimaxi.chat/v1/video_generation"
    
    payload = json.dumps({
        "prompt": prompt,
        "model": model
    })
    
    headers = {
        'authorization': 'Bearer ' + MINIMAX_API_KEY,
        'content-type': 'application/json',
    }

    response = requests.post(url, headers=headers, data=payload)

    if response.status_code != 200:
        print(f"❌ Video generation failed: {response.text}")
        return None

    task_id = response.json().get('task_id', '')
    print(f"✅ Video generation task submitted successfully! Task ID: {task_id}")
    return task_id

# Check video generation status
def query_video_generation(task_id):
    url = f"https://api.minimaxi.chat/v1/query/video_generation?task_id={task_id}"
    headers = {'authorization': 'Bearer ' + MINIMAX_API_KEY}

    response = requests.get(url, headers=headers)
    status = response.json().get('status', 'Unknown')

    print(f"⏳ Video status: {status}")

    if status == 'Success':
        return response.json().get('file_id', ''), "Finished"
    elif status in ["Preparing", "Queueing", "Processing"]:
        return "", status
    elif status in ["Fail", "Unknown"]:
        return "", "Fail"
    
    return "", "Unknown"

# Fetch the generated video
def fetch_video_result(file_id):
    print("📥 Downloading generated video...")
    url = f"https://api.minimaxi.chat/v1/files/retrieve?file_id={file_id}"
    headers = {'authorization': 'Bearer ' + MINIMAX_API_KEY}

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"❌ Failed to download video: {response.text}")
        return None

    download_url = response.json()['file']['download_url']
    print(f"📩 Video download link: {download_url}")

    with open(output_file_name, 'wb') as f:
        f.write(requests.get(download_url).content)
    
    print(f"✅ Video downloaded successfully: {output_file_name}")
    return output_file_name

# Merge video and voiceover
def merge_video_audio(video_file, audio_file, output_file="final_video.mp4"):
    print("🎬 Merging video and audio...")
    
    video = VideoFileClip(video_file)
    audio = AudioFileClip(audio_file)

    final_video = video.set_audio(audio)
    final_video.write_videofile(output_file, codec="libx264", fps=24)

    print(f"✅ Final video saved as {output_file}")

    # Cleanup temporary files
    os.remove(video_file)
    os.remove("youtube_script.txt")
    os.remove("voiceover.mp3")
    print("🗑️ Temporary files deleted successfully!")

    return output_file

# Main function
def main():
    topic = input("Enter today's topic of interest: ")
    prompt = f"Generate a 10 to 12-second engaging YouTube Shorts riddle script based on the topic '{topic}', keep the tone as per the topic provided. Keep it short and attractive. Note: the riddle must contain a tricy brain teaser question also."

    # Step 1: Generate script
    script_text = generate_and_save_script(topic, prompt=prompt)

    # Step 2: Generate voiceover
    audio_file = generate_voiceover(script_text, voice_type="JBFqnCBsd6RMkjVDRZzb")

    # Step 3: Generate AI Video
    task_id = invoke_video_generation(prompt=prompt)
    if not task_id:
        print("❌ Video generation failed. Exiting...")
        return

    # Step 4: Wait for video generation to complete
    while True:
        time.sleep(10)
        file_id, status = query_video_generation(task_id)

        if file_id:
            video_file = fetch_video_result(file_id)
            if video_file:
                break
        elif status == "Fail":
            print("❌ Video generation failed. Exiting...")
            return

    # Step 5: Merge video and audio
    merge_video_audio(video_file, audio_file)

    print("🚀 AI Video Generation Complete! Your final video is ready!")

# Run the script
if __name__ == "__main__":
    main()
