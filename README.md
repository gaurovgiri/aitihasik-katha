# Aitihasik Katha (Historical Stories)

An AI-powered historical storytelling platform that automatically generates engaging video content from historical documents. The system uses RAG (Retrieval-Augmented Generation) to create compelling narratives, generates images, synthesizes audio, and produces complete video documentaries.

## 🖵 Demo

<video src="examples/example1.mp4" controls width="300"></video>

## 🎯 Features

- **📚 Document Ingestion**: Process PDF documents (English and Nepali) with OCR support
- **🤖 AI Story Generation**: Generate compelling historical narratives using RAG and LLM
- **🖼️ Image Generation**: Create relevant historical images for story segments
- **🎙️ Audio Synthesis**: Convert text to speech with natural voice-over
- **🎬 Video Production**: Automatically generate complete documentary-style videos
- **🌐 Translation**: Support for multilingual content (English/Nepali)
- **💾 Vector Database**: Chromadb-based embedding storage for efficient retrieval

## 🏗️ Architecture

The pipeline consists of the following components:

1. **PDF Ingestion** → Extract and process historical content from PDFs
2. **Vector Store** → Store document embeddings for semantic search
3. **Story Generation** → Use RAG to generate engaging narratives
4. **Image Generation** → Create visuals for story segments
5. **Audio Generation** → Synthesize voice-over audio
6. **Video Production** → Merge images and audio into final video

## 📁 Project Structure

```
aitihasik-katha/
├── pyproject.toml
├── requirements.txt
├── README.md
├── data/
│   ├── audios/
│   ├── images/
│   ├── videos/
│   ├── output/
│   ├── embeddings/
│   └── pdfs/
│       ├── en/
│       └── ne/
├── src/
│   ├── aitihasik_katha/
│   │   ├── __main__.py
│   │   ├── pipeline.py
│   │   ├── cli.py
│   │   ├── core/
│   │   │   └── settings.py
│   │   ├── services/
│   │   │   ├── story_service.py
│   │   │   ├── image_service.py
│   │   │   ├── audio_service.py
│   │   │   ├── subtitle_service.py
│   │   │   └── video_service.py
│   │   ├── ingest/
│   │   │   └── pdf_ingestor.py
│   │   ├── storage/
│   │   │   └── vector_store.py
│   │   └── utils/
│   │       ├── gcs.py
│   │       ├── ocr.py
│   │       └── translation.py
```

## 🚀 Getting Started

### Prerequisites

- Python 3.10+
- Tesseract OCR (for PDF text extraction)
- FFmpeg (for video processing)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/aitihasik-katha.git
   cd aitihasik-katha
   ```

2. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
    pip install -e .
   ```

3. **Install system dependencies**
   ```bash
   # Ubuntu/Debian
   sudo apt-get update
   sudo apt-get install tesseract-ocr tesseract-ocr-nep ffmpeg

   # macOS
   brew install tesseract tesseract-lang ffmpeg
   ```

4. **Set up environment variables**
   
   Create a `.env` file in the project root:
   ```env
    CHAT_MODEL=gemini-2.0-flash
   EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
    GEMINI_API_KEY=your_gemini_api_key_here
    IMAGE_CHAT_MODEL=gemini-2.0-flash
    IMAGE_MODEL=imagegeneration@006
    AUDIO_MODEL=chirp3-hd
   ```

5. **Set up Google Cloud credentials**
   
   Place your `google.json` credentials file in the project root.

## 📖 Usage

### 1. Ingest PDF Documents

First, add your historical PDF documents to the appropriate directory:
- English PDFs → `data/pdfs/en/`
- Nepali PDFs → `data/pdfs/ne/`

Then run ingestion:
```bash
python -m aitihasik_katha ingest --base-dir data/pdfs
```

### 2. Run the Complete Pipeline

Execute the full pipeline to generate a video:
```bash
python -m aitihasik_katha run
```

This will:
1. Generate a story from your historical documents
2. Create images for each story segment
3. Generate audio voice-overs
4. Produce individual video clips
5. Merge everything into a final video: `data/videos/final_output.mp4`

### 3. Individual Components

You can also run components separately:

**Generate a story only:**
```python
from aitihasik_katha.services.story_service import generate_story

story = generate_story()
print(story)
```

**Generate audio:**
```python
from aitihasik_katha.services.audio_service import generate_audio

generate_audio("Your text here", "output.mp3")
```

**Generate images:**
```python
from aitihasik_katha.services.image_service import generate_image

generate_image("Description of the image", "output.png")
```

## 🔧 Configuration

Edit `src/aitihasik_katha/core/settings.py` to customize:

- **Models**: Change LLM and embedding models
- **Directories**: Modify data storage locations
- **OCR Settings**: Adjust Tesseract configurations
- **API Keys**: Update service credentials

## 🛠️ Technologies Used

- **LangChain**: Prompt orchestration
- **Google Gemini / Vertex AI**: Text, image, and video generation
- **Google Cloud Speech + TTS**: Audio transcription and synthesis
- **Tesseract**: OCR for image-based PDFs
- **Sentence Transformers**: Text embeddings
- **FFmpeg**: Video and audio processing

## 📊 Workflow

```
PDF Documents
    ↓
[Text Extraction + OCR]
    ↓
[Chunking & Embedding]
    ↓
[Vector Store (ChromaDB)]
    ↓
[RAG: Retrieve + Generate Story]
    ↓
[Generate Images] → [Generate Audio]
    ↓              ↓
    [Create Video Clips]
            ↓
    [Merge Final Video]
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Historical document sources
- Open-source LLM and AI communities
- Contributors and maintainers

## 📧 Contact

For questions or feedback, please open an issue on GitHub.

---

**Note**: This project is designed for educational and research purposes related to historical storytelling and AI-powered content generation.
