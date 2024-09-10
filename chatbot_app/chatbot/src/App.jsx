import "./App.css";
import { useState } from "react";
import axios from "axios";

function App() {
  const [question, setQuestion] = useState("");
  const [pdfFile, setPdfFile] = useState(null);
  const [response, setResponse] = useState("");
  const [loading, setLoading] = useState(false);

  const handleFileChange = (e) => {
    console.log(e.target.files[0]);
    setPdfFile(e.target.files[0]);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);

    const formData = new FormData();
    formData.append("question", question);
    formData.append("pdf_file", pdfFile);

    try {
      const res = await axios.post(
        "http://localhost:8000/rag-chat/",
        formData,
        {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        }
      );

      setResponse(res.data.response);
      console.log(response);
    } catch (error) {
      console.error("There was an error!", error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <h1 className="header">RAG Chatbot</h1>
      <form onSubmit={handleSubmit}>
        <div className="form">
          <label className="input-label">PDF File:</label>
          <input
            type="file"
            accept="application/pdf"
            onChange={handleFileChange}
            required
          />
        </div>
        <div className="chat-ui">
          {question && (
            <div>
              <p className="user-question">{question}</p>
            </div>
          )}
          {response && (
            <div>
              <p className="response">{response}</p>
            </div>
          )}
        </div>

        <div className="question-input">
          <input
            type="text"
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            required
            className="input"
            placeholder="Start Asking!"
          />
          <button type="submit">
            <svg
              xmlns="http://www.w3.org/2000/svg"
              width="16"
              height="16"
              fill="currentColor"
              viewBox="0 0 16 16"
            >
              <path d="M15.854.146a.5.5 0 0 1 .11.54l-5.819 14.547a.75.75 0 0 1-1.329.124l-3.178-4.995L.643 7.184a.75.75 0 0 1 .124-1.33L15.314.037a.5.5 0 0 1 .54.11ZM6.636 10.07l2.761 4.338L14.13 2.576zm6.787-8.201L1.591 6.602l4.339 2.76z" />
            </svg>
          </button>
          {loading && <div className="spinner"></div>}
        </div>
      </form>
    </div>
  );
}

export default App;
