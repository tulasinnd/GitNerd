
// import { useEffect, useState } from "react";
// import { useParams } from "react-router-dom";

// function Interview() {
//   const { sessionId } = useParams();

//   const [question, setQuestion] = useState("");

//   useEffect(() => {
//     startInterview();
//   }, []);

//   async function startInterview() {
//     const response = await fetch("http://127.0.0.1:8000/interview/chat", {
//       method: "POST",
//       headers: {
//         "Content-Type": "application/json",
//       },
//       body: JSON.stringify({
//         session_id: sessionId,
//         answer: "",
//       }),
//     });

//     const data = await response.json();

//     setQuestion(data.question);
//   }

//   return (
//     <div style={{ color: "white", padding: "30px" }}>
//       <h1>Interview</h1>

//       <p>{question}</p>
//     </div>
//   );
// }

// export default Interview;



import "../App.css";
import { useState, useRef, useEffect } from "react";
import { useParams } from "react-router-dom";
import ReactMarkdown from "react-markdown";

function Interview() {
  const { sessionId } = useParams();

  const chatEndRef = useRef();
  const started = useRef(false);

  const [interviewAnswer, setInterviewAnswer] = useState("");
  const [generatingQuestion, setGeneratingQuestion] = useState(false);
  const [thinking, setThinking] = useState(false);
  const [interviewMessages, setInterviewMessages] = useState([]);

  // Start interview only once
  useEffect(() => {
    if (started.current) return;

    started.current = true;
    startInterview();
  }, []);

  // Auto-scroll to latest message
  useEffect(() => {
    chatEndRef.current?.scrollIntoView({
      behavior: "smooth",
    });
  }, [interviewMessages, thinking]);

  async function startInterview() {
    try {
      const response = await fetch(
        "http://127.0.0.1:8000/interview/chat",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            session_id: sessionId,
            answer: "",
          }),
        }
      );

      const data = await response.json();

      if (data.success) {
        setInterviewMessages([
          {
            role: "assistant",
            content: data.question,
          },
        ]);
      }
    } catch (error) {
      console.error(error);
    }
  }

  async function sendInterviewAnswer() {
    if (interviewAnswer.trim() === "") return;

    const answer = interviewAnswer;

    setGeneratingQuestion(true);

    // Show user's answer immediately
    setInterviewMessages((previousMessages) => [
      ...previousMessages,
      {
        role: "user",
        content: answer,
      },
    ]);

    setInterviewAnswer("");

    setThinking(true);

    try {
      const response = await fetch(
        "http://127.0.0.1:8000/interview/chat",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            session_id: sessionId,
            answer: answer,
          }),
        }
      );

      const data = await response.json();

      setThinking(false);

      if (data.success && !data.interview_completed) {
        setInterviewMessages((previousMessages) => [
          ...previousMessages,
          {
            role: "assistant",
            content: data.question,
          },
        ]);
      }

    //   if (data.interview_completed) {
    //     setInterviewMessages((previousMessages) => [
    //       ...previousMessages,
    //       {
    //         role: "assistant",
    //         content: "🎉 Interview completed!",
    //       },
    //     ]);
    //   }
    if (data.interview_completed) {
        setInterviewMessages((previousMessages) => [
            ...previousMessages,
            {
            role: "assistant",
            content: data.feedback,
            },
        ]);
        }
    } catch (error) {
      setThinking(false);
      console.error(error);
    } finally {
      setGeneratingQuestion(false);
    }
  }

  return (
    <div className="learning-page">
      <div className="learning-header">
        <h2>🎤 Repository Interview</h2>
      </div>

      <div className="chat-window">
        {interviewMessages.map((message, index) => (
          <div
            key={index}
            className={
              message.role === "assistant"
                ? "assistant-message"
                : "user-message"
            }
          >
            {/* <div className="message-body">
              {message.content}
            </div> */}
            <div className="message-body">
            <ReactMarkdown>
                {message.content}
            </ReactMarkdown>
            </div>
          </div>
        ))}

        {thinking && (
          <div className="assistant-message thinking-message">
            <div className="message-body">
              Preparing next interview question...
            </div>
          </div>
        )}

        <div ref={chatEndRef}></div>
      </div>

      <div className="chat-input">
        <div className="chat-input-container">
          <input
            type="text"
            placeholder="Type your answer..."
            value={interviewAnswer}
            onChange={(e) => setInterviewAnswer(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === "Enter") {
                sendInterviewAnswer();
              }
            }}
          />

          <button
            onClick={sendInterviewAnswer}
            disabled={generatingQuestion}
          >
            {generatingQuestion ? "Wait..." : "Submit"}
          </button>
        </div>
      </div>
    </div>
  );
}

export default Interview;