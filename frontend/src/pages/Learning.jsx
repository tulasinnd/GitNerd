import "../App.css";
import ReactMarkdown from "react-markdown";
import { useState, useRef, useEffect } from "react";
import { useParams } from "react-router-dom";

function Learning() {
  const { sessionId } = useParams();
  
  const chatEndRef = useRef();

  const [learningQuestion, setLearningQuestion] = useState("");

  const [generatingAnswer, setGeneratingAnswer] = useState(false);

  const [thinking, setThinking] = useState(false);

  const [learningMessages, setLearningMessages] = useState([
    {
      role: "assistant",
      content:
        "Hello! 👋 I've finished studying your repository. Ask me anything about the repository architecture, source code, execution flow, technologies, or implementation details. What would you like to explore first?",
    },
  ]);

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({
        behavior: "smooth",
    });
}, [learningMessages, thinking]);
  

async function sendLearningQuestion() {
  if (learningQuestion.trim() === "") return;

  const question = learningQuestion;

  setGeneratingAnswer(true);

  // Show the user's question immediately
  setLearningMessages((previousMessages) => [
    ...previousMessages,
    {
      role: "user",
      content: question,
    },
  ]);

  // Clear the input immediately
  setLearningQuestion("");
  setThinking(true);

  try {
    const response = await fetch(
      "http://127.0.0.1:8000/learning/chat",
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          session_id: sessionId,
          question: question,
        }),
      }
    );

    const data = await response.json();

    if (data.success) {
      setThinking(false);

      // Add only the assistant message
      setLearningMessages((previousMessages) => [
        ...previousMessages,
        {
          role: "assistant",
          content: data.answer,
        },
      ]);
      setGeneratingAnswer(false);
    }
  } catch (error) {
    setThinking(false);
    setGeneratingAnswer(false);
    console.error(error);
  }
}

  return (
    <div  className="learning-page">

      <div className="learning-header">
        <h2>📘 Repository Learning</h2>
      </div>

      <div className="chat-window">

        {learningMessages.map((message, index) => (
          

          <div
            key={index}
            className={
              message.role === "assistant"
                ? "assistant-message"
                : "user-message"
            }
          >

            <div className="message-body">
              <ReactMarkdown>
                {message.content}
              </ReactMarkdown>
            </div>

          </div>

        ))}

         {/* Thinking Bubble */}
        {thinking && (
          <div className="assistant-message thinking-message">
            <div className="message-body">
              Analyzing repository...
            </div>
          </div>
        )}

        <div ref={chatEndRef}></div>

      </div>

     <div className="chat-input">

    <div className="chat-input-container">

        <input
            type="text"
            placeholder="Ask anything about this repository..."
            value={learningQuestion}
            onChange={(e) => setLearningQuestion(e.target.value)}
            onKeyDown={(e) => {
                if (e.key === "Enter") {
                    sendLearningQuestion();
                }
            }}
        />

        <button
            onClick={sendLearningQuestion}
            disabled={generatingAnswer}
        >
            {generatingAnswer ? "Wait..." : "Send"}
        </button>

    </div>

</div>

    </div>
  );
}

export default Learning;