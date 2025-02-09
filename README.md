# 🎬 AI-Generated YouTube Shorts 🚀

Automatically generate **AI-powered YouTube Shorts** with **AI voiceovers** and **Minimax AI video generation**. This script creates high-quality videos **without requiring manual work**, making content creation effortless!

## ✨ **Features**
✔ **AI-generated scripts** using OpenAI (GPT-3.5)  
✔ **Realistic AI voiceovers** using ElevenLabs  
✔ **AI-powered video generation** via Minimax AI  
✔ **Automatic merging of video & voiceover**  
✔ **Hands-free YouTube Shorts creation**  
✔ **Deletes temporary files to save storage**  

---

## 🛠️ **Installation**
### 1️⃣ **Clone the Repository**
```bash
git clone https://github.com/yourusername/AI-YouTube-Shorts.git
cd AI-YouTube-Shorts
```

### 2️⃣ **Set Up a Virtual Environment (Recommended)**
```bash
python -m venv venv
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate  # Windows
```

### 3️⃣ **Install Dependencies**
```bash
pip install -r requirements.txt
```

---

## 🔑 **API Keys Setup**
This project requires API keys for **OpenAI, ElevenLabs, and Minimax AI**.  

1. **Create a `.env` file** in the root directory:
```ini
OPENAI_API_KEY=your_openai_api_key
ELEVENLABS_API_KEY=your_elevenlabs_api_key
MINIMAX_API_KEY=your_minimax_api_key
```
2. **Get API Keys:**
   - **[OpenAI API Key](https://platform.openai.com/signup)**
   - **[ElevenLabs API Key](https://beta.elevenlabs.io/)**
   - **[Minimax AI API Key](https://minimax.ai/)**

---

## 🚀 **Usage**
### **Run the Script**
```bash
python Generate_VideoForYT.py
```
### **How It Works:**
1️⃣ Enter a topic for your YouTube Shorts (⭐Remember there is a default propmt for generating 'riddles' in the main function which you can change as per your wish)
-
2️⃣ AI generates a script based on the topic
-
3️⃣ ElevenLabs creates a realistic AI voiceover
-
4️⃣ Minimax AI generates an AI-powered video
-
5️⃣ The script merges video & audio automatically
-
6️⃣ Final video is saved as final_video.mp4
-
7️⃣ Important Note 1: The final video that will be generate will be around 6-8 seconds**
-
8️⃣ Important Note 2: Also for Eleven Labs API you can get 10000 credits for free, Minimax ai API you can get upto 3 videos for free.
---

## 🔥 **Future Improvements**
✅ **Support for multiple video styles**  
✅ **Custom background music integration**  
✅ **Automated video uploading to YouTube using Selenium**   
---

## 📝 **License**
This project is **open-source** under the **MIT License**.

---

## ⭐ **Like this project? Give it a Star on GitHub!**
If you find this project useful, don't forget to **⭐ star** it on GitHub! 😊
```
