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
├── src/
│   ├── pipeline.py         # Main execution pipeline
│   ├── story_gen.py        # Story generation with RAG
│   ├── audio_gen.py        # Audio synthesis
│   ├── image_gen.py        # Image generation
│   ├── video_gen.py        # Video production
│   ├── ingest_pdfs.py      # PDF processing and ingestion
│   ├── vector_store.py     # Vector database operations
│   ├── translate.py        # Translation utilities
│   ├── image2text.py       # OCR and image-to-text
│   ├── config.py           # Configuration management
│   └── helper.py           # Helper utilities
├── data/
│   ├── audio/             # Generated audio files
│   ├── images/            # Generated images
│   ├── videos/            # Final video outputs
│   ├── pdfs/              # Source PDF documents
│   │   ├── en/           # English PDFs
│   │   └── ne/           # Nepali PDFs
│   ├── embeddings/        # Vector database storage
│   └── output/            # Processing outputs
├── requirements.txt       # Python dependencies
├── test.py               # Test scripts
└── google.json           # API credentials
```

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- [Ollama](https://ollama.ai/) (for local LLM)
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
   ```

3. **Install system dependencies**
   ```bash
   # Ubuntu/Debian
   sudo apt-get update
   sudo apt-get install tesseract-ocr tesseract-ocr-nep ffmpeg

   # macOS
   brew install tesseract tesseract-lang ffmpeg
   ```

4. **Install Ollama and pull the required model**
   ```bash
   # Install Ollama from https://ollama.ai/
   ollama pull llama2  # or your preferred model
   ```

5. **Set up environment variables**
   
   Create a `.env` file in the project root:
   ```env
   CHAT_MODEL=llama2
   EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
   COLLECTION_NAME=historical_documents
   GCP_API_KEY=your_google_cloud_api_key_here
   ```

6. **Set up Google Cloud credentials**
   
   Place your `google.json` credentials file in the project root.

## 📖 Usage

### 1. Ingest PDF Documents

First, add your historical PDF documents to the appropriate directory:
- English PDFs → `data/pdfs/en/`
- Nepali PDFs → `data/pdfs/ne/`

Then run the ingestion script:
```python
from src.ingest_pdfs import load_pdf
from src.vector_store import vector_store

# Process and store documents
docs = load_pdf("data/pdfs/en/your_document.pdf", language="en")
vector_store.add_documents(docs)
```

### 2. Run the Complete Pipeline

Execute the full pipeline to generate a video:
```bash
python src/pipeline.py
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
from src.story_gen import generate_story

story = generate_story()
print(story)
```

**Generate audio:**
```python
from src.audio_gen import generate_audio

generate_audio("Your text here", "output.mp3")
```

**Generate images:**
```python
from src.image_gen import generate_image

generate_image("Description of the image", "output.png")
```

## 🔧 Configuration

Edit `src/config.py` to customize:

- **Models**: Change LLM and embedding models
- **Directories**: Modify data storage locations
- **OCR Settings**: Adjust Tesseract configurations
- **API Keys**: Update service credentials

## 🛠️ Technologies Used

- **LangChain**: LLM orchestration and RAG pipeline
- **Ollama**: Local LLM inference
- **ChromaDB**: Vector database for embeddings
- **ElevenLabs**: Text-to-speech audio generation
- **PDFPlumber**: PDF text extraction
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
