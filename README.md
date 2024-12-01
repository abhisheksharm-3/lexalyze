# ✨ Lexalyze ✨

<p align="center">
  <img src="https://socialify.git.ci/abhisheksharm-3/lexalyze/image?font=Source%20Code%20Pro&language=1&name=1&owner=1&pattern=Charlie%20Brown&stargazers=1&theme=Dark" alt="Lexalyze Project">
</p>

🚧 **Current Status**: Proof of Concept in Active Development 
*We're in the early stages of bringing Lexalyze to life. The current version is a foundational prototype that demonstrates our vision. While functional, expect some rough edges as we refine the technology. Our commitment is to rapidly improve the platform's accuracy, usability, and capabilities through iterative development and cutting-edge generative AI techniques.*

---

<p align="center">
  Lexalyze is an AI-powered legal document analysis platform that lets you upload, analyze, and extract insights from legal documents. Leveraging advanced NLP models, it provides comprehensive document reports and intelligent Q&A capabilities.
</p>

---

## 🚀 **Live Demo**
Check out Lexalyze in action: [**Lexalyze**](https://lexalyze.vercel.app/)

---

## 🧐 **Features**
Lexalyze offers powerful legal document intelligence with these standout features:

### 📄 **Document Analysis**  
- Upload legal documents for comprehensive analysis
- Generate detailed reports in multiple formats
- Extract key insights and summaries
- Ask specific questions about document content

### 🤖 **Advanced AI Models**  
- Question Answering powered by RoBERTa Base SQuAD2
- Document Summarization using BART Large CNN

### 💻 **Interactive User Interface**  
- Built with **SvelteKit** for a responsive and intuitive experience
- Seamless document upload and analysis workflow

---

## 🏗️ **Project Structure**

### Frontend (`client` Directory)
```plaintext
client/
├── src/                 # SvelteKit source code
│   ├── routes/          # Application routes
│   ├── lib/             # Shared components and utilities
├── static/              # Static assets
├── svelte.config.js     # SvelteKit configuration
├── package.json         # Frontend package dependencies
├── vercel.json          # Vercel configuration
```

### Backend (`server` Directory)
```plaintext
server/
├── app/
│   ├── api/             # FastAPI endpoints
│   ├── models/          # AI model loading and inference
│   ├── services/        # Core business logic
│   ├── utils/           # Utility functions
├── requirements.txt     # Python dependencies
├── main.py              # FastAPI application entry point
```

---

## 🛠️ **Installation Steps**

### **Prerequisites**
- **Node.js** (v20+ recommended)  
- **Python** (v3.10+)  
- **pip** for Python dependency management  

### **Installation**

1. **Clone the Repository**  
   ```bash
   git clone https://github.com/abhisheksharm-3/lexalyze.git
   cd lexalyze
   ```

2. **Install Frontend Dependencies**  
   ```bash
   cd client
   npm install
   ```

3. **Set Up Backend**  
   ```bash
   cd ../server
   pip install -r requirements.txt
   ```

4. **Run the Application**  
   - Start the backend (FastAPI):  
     ```bash
     uvicorn main:app --reload
     ```
   - Start the frontend (SvelteKit):  
     ```bash
     cd ../client
     npm run dev
     ```

5. **Access the app**  
   Open your browser and navigate to [http://localhost:5173](http://localhost:5173)

---

## 🚢 **Deployment**

### Frontend
- **Platform**: [Vercel](https://vercel.com)  
- Deployed at [lexalyze.vercel.app](https://lexalyze.vercel.app)

### Backend
- **Platform**: [Koyeb](https://www.koyeb.com)  
- Deployed as a containerized FastAPI application

---

## 🧠 **AI Models**

### Question Answering
- **Model**: RoBERTa Base SQuAD2
- Provides precise answers to specific questions about legal documents

### Summarization
- **Model**: BART Large CNN
- Generates concise and coherent document summaries

---

## 💡 **Usage**
1. Open the application at [lexalyze.vercel.app](https://lexalyze.vercel.app)  
2. Upload your legal document  
3. Generate a detailed report or ask specific questions  
4. Download reports in your preferred format 🎉  

---

## 🧰 **Technologies Used**

- **Frontend**: [SvelteKit](https://kit.svelte.dev)  
- **Backend**: [FastAPI](https://fastapi.tiangolo.com)  
- **AI Models**:
  - Question Answering: [RoBERTa Base SQuAD2](https://huggingface.co/deepset/roberta-base-squad2)
  - Summarization: [BART Large CNN](https://huggingface.co/facebook/bart-large-cnn)
- **Deployment**:  
  - Frontend: [Vercel](https://vercel.com)  
  - Backend: [Koyeb](https://www.koyeb.com)

---

## ❤️ **Like My Work?**
Explore more of my projects at [**abhisheksharma.tech/projects**](https://abhisheksharma.tech/projects)