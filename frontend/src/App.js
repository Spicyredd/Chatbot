import React, { useState, useEffect, useRef } from "react";
import axios from "axios";
import "./App.css";

function App() {
  const [text, setText] = useState("");
  const [file, setFile] = useState(null);
  const [messages, setMessages] = useState([]);
  const messagesEndRef = useRef(null);
  const [toggle, setToggle] = useState(false);
  const [loading, setLoading] = useState(false); // State to trigger loading animation



  const handleTextChange = (e) => setText(e.target.value);

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];
    if (selectedFile && selectedFile.type === "application/pdf") {
      setFile(selectedFile);
    } else {
      alert("Please upload a valid PDF file.");
      e.target.value = "";
    }
  };

  // Handle clearing the attached file
  const handleClearFile = () => {
    setFile(null);
  };

  const fetchMessages = async () => {
    try {
      const response = await axios.get("http://127.0.0.1:8000/api/messages/");
      if (response.status === 200) setMessages(response.data);
    } catch (error) {
      console.error("Error fetching messages:", error);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (file) {
      const newFileMessage = {
        sender: "You",
        message: `${file.name}`,
      };
      setMessages((prev) => [...prev, newFileMessage]);

      const fileData = new FormData();
      fileData.append("pdf", file);
      try {
        setLoading(true);
        await axios.post("http://127.0.0.1:8000/api/filepost/", fileData, {
          headers: { "Content-Type": "multipart/form-data" },
        });
        // setMessages((prev) => [...prev, newFileMessage]);
        setFile(null);
        setLoading(false);
        setMessages((prev) => [...prev, {'sender': 'gemini', 'message': 'File Received'}]);
      } catch (error) {
        console.error(
          "Error sending file:",
          error.response?.data || error.message
        );
      }
      
    }

    if (text) {
      const newMessage = { sender: "You", message: text };
      setMessages((prev) => [...prev, newMessage]);

      const temp_text = text;
      setText("");
      const textData = new FormData();
      textData.append("message", temp_text);
      textData.append("toggle", toggle)
      try {
        setLoading(true);
        const response = await axios.post(
          "http://127.0.0.1:8000/api/post/",
          textData,
          {
            headers: { "Content-Type": "multipart/form-data" },
          }
        );
        setLoading(false);
        setMessages(response.data);
      } catch (error) {
        console.error(
          "Error sending text message:",
          error.response?.data || error.message
        );
      }
    }
  };

  useEffect(() => {
    fetchMessages();
  }, []);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  return (
    <div className="flex items-center justify-center bg-gray-100 h-screen w-[100svw]">
      <div className="size-[90%] p-8 bg-white shadow-lg rounded-xl min-w-[400px]">
        <div className="mb-6 size-[90%] min-w-[100%] overflow-y-auto border border-gray-300 rounded-lg p-4 bg-gray-50">
          {messages.length === 0 ? (
            <p className="text-gray-400 text-center">No messages yet.</p>
          ) : (
            messages.map((msg, index) => (
              <p
                key={index}
                className={`mb-4 p-3 rounded-lg max-w-xs ${
                  msg.sender === "You"
                    ? "ml-auto bg-blue-500 text-white "
                    : "bg-gray-200 min-w-[40%]"
                }`}
              >
                {msg.message}
              </p>
            ))
          )}
          <div ref={messagesEndRef} />
            {/* Display the loading animation */}
        {loading && (
          <div className="ai-loading">
            <div className="loading-spinner"></div> {/* Example spinner */}
            <span>Thinking ...</span>
          </div>
        )}
        </div>
        <form
          onSubmit={handleSubmit}
          className="flex flex-col space-y-4 bg-gray-100 p-4 rounded-lg shadow-md"
        >
          {/* Message Input with Embedded File Attachment */}
          <div className="relative flex items-center w-full">
            <input
              type="text"
              value={text}
              onChange={handleTextChange}
              placeholder="Type your message..."
              className="w-full p-3 pl-12 pr-4 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
            />
          <div className="flex items-center space-x-3 min-w-[100px] max-w-[100px] toggle">
              
              <span className="text-gray-700">
                {toggle ?"Nepali" : "English"}
              </span>
              <label className="relative inline-flex items-center cursor-pointer">
                <input
                  type="checkbox"
                  checked={toggle}
                  onChange={() => setToggle((prev) => !prev)}
                  className="sr-only peer"
                />
                <div className="w-11 h-6 bg-gray-300 rounded-full peer-checked:bg-blue-600 transition duration-300 relative">
                  <div
                    className={`absolute left-1 top-1 w-4 h-4 bg-white rounded-full transition-transform ${
                      toggle ? "translate-x-5" : ""
                    }`}
                  />
                </div>
              </label>
            </div>

            {/* File Attachment (Embedded inside text input) */}
            <label
              htmlFor="file-input"
              className="absolute left-3 top-1/2 transform -translate-y-1/2 cursor-pointer text-xl text-gray-500"
            >
              +
            </label>
            <input
              id="file-input"
              type="file"
              onChange={handleFileChange}
              accept="application/pdf"
              className="hidden" // Hide the default file input
            />

            {/* Send Button on the Side */}
            <button
              type="submit"
              className="ml-3 bg-blue-600 text-white p-3 rounded-lg hover:bg-blue-700 transition duration-300"
            >
              Send
            </button>
          </div>

          {/* Display the selected file */}
          {file && (
            <div className="flex justify-between items-center bg-gray-200 p-2 rounded-lg">
              <span className="text-sm text-gray-700 truncate">
                {file.name}
              </span>
              <button
                type="button"
                onClick={handleClearFile}
                className="text-sm text-blue-600 hover:text-blue-800"
              >
                Remove
              </button>
            </div>
          )}
        </form>
      </div>
    </div>
  );
}

export default App;
