import React, { useState } from "react";
import API from "./api";

function App() {

  // =====================================
  // Replacement System
  // =====================================

  const [teacher, setTeacher] = useState("");
  const [replacementData, setReplacementData] = useState(null);

  // =====================================
  // AI Chatbot
  // =====================================

  const [query, setQuery] = useState("");
  const [chatResponse, setChatResponse] = useState("");

  // =====================================
  // AI Timetable Generator
  // =====================================

  const [generatedTimetable, setGeneratedTimetable] = useState([]);
  const [aiInsights, setAiInsights] = useState("");

  // =====================================
  // MARK ABSENT
  // =====================================

  const markAbsent = async () => {

    const response = await API.post(
      `/teacher/absent/${teacher}`
    );

    setReplacementData(response.data);
  };

  // =====================================
  // AI CHATBOT
  // =====================================

  const askAI = async () => {

    const response = await API.post(
      "/chatbot",
      {
        query: query
      }
    );

    setChatResponse(response.data.response);
  };

  // =====================================
  // GENERATE TIMETABLE
  // =====================================

  const generateTimetable = async () => {

    const response = await API.post(
      "/generate-timetable"
    );

    setGeneratedTimetable(
      response.data.generatedTimetable
    );

    setAiInsights(
      response.data.aiInsights
    );
  };

  return (

    <div style={{ padding: "30px", fontFamily: "Arial" }}>

      <h1>AI Timetable System</h1>

      <hr />

      {/* ===================================== */}
      {/* ABSENT TEACHER SYSTEM */}
      {/* ===================================== */}

      <h2>AI Replacement System</h2>

      <input
        type="text"
        placeholder="Enter Teacher Name"
        value={teacher}
        onChange={(e) => setTeacher(e.target.value)}
        style={{
          padding: "10px",
          width: "300px"
        }}
      />

      <button
        onClick={markAbsent}
        style={{
          padding: "10px",
          marginLeft: "10px"
        }}
      >
        Mark Absent
      </button>

      <br />
      <br />

      {
        replacementData && (

          <div>

            <h3>
              Absent Teacher:
              {" "}
              {replacementData.absentTeacher}
            </h3>

            <h3>
              Total Replacements:
              {" "}
              {replacementData.totalReplacements}
            </h3>

            {
              replacementData.replacements.map(
                (item, index) => (

                  <div
                    key={index}
                    style={{
                      border: "1px solid gray",
                      padding: "15px",
                      marginBottom: "15px",
                      borderRadius: "10px"
                    }}
                  >

                    <h2>
                      Section {item.section}
                    </h2>

                    <p>
                      <b>Class:</b>
                      {" "}
                      {item.class}
                    </p>

                    <p>
                      <b>Subject:</b>
                      {" "}
                      {item.subject}
                    </p>

                    <p>
  <b>Replacement Teacher:</b>
  {" "}
  {item.replacementTeacher}
</p>

<p>
  <b>AI Score:</b>
  {" "}
  {item.aiScore}
</p>

<p>
  <b>Mode:</b>
  {" "}
  {item.mode}
</p>

                  </div>

                )
              )
            }

          </div>

        )
      }

      <hr />

      {/* ===================================== */}
      {/* AI CHATBOT */}
      {/* ===================================== */}

      <h2>AI Chatbot</h2>

      <input
        type="text"
        placeholder="Ask AI anything..."
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        style={{
          padding: "10px",
          width: "400px"
        }}
      />

      <button
        onClick={askAI}
        style={{
          padding: "10px",
          marginLeft: "10px"
        }}
      >
        Ask AI
      </button>

      <br />
      <br />

      <div
        style={{
          border: "1px solid gray",
          padding: "15px",
          borderRadius: "10px"
        }}
      >
        {chatResponse}
      </div>

      <hr />

      {/* ===================================== */}
      {/* AI TIMETABLE GENERATOR */}
      {/* ===================================== */}

      <h2>AI Timetable Generator</h2>

      <button
        onClick={generateTimetable}
        style={{
          padding: "10px"
        }}
      >
        Generate AI Timetable
      </button>

      <br />
      <br />

      {
        generatedTimetable.length > 0 && (

          <div>

            <h3>Generated Timetable</h3>

            {
              generatedTimetable.map((item, index) => (

                <div
                  key={index}
                  style={{
                    border: "1px solid gray",
                    padding: "15px",
                    marginBottom: "15px",
                    borderRadius: "10px"
                  }}
                >

                  <p>
                    <b>Section:</b>
                    {" "}
                    {item.section}
                  </p>

                  <p>
                    <b>Class:</b>
                    {" "}
                    {item.class}
                  </p>

                  <p>
                    <b>Subject:</b>
                    {" "}
                    {item.subject}
                  </p>

                  <p>
                    <b>Teacher:</b>
                    {" "}
                    {item.teacher}
                  </p>

                  <p>
                    <b>Period:</b>
                    {" "}
                    {item.period}
                  </p>

                </div>

              ))
            }

            <div
              style={{
                border: "1px solid black",
                padding: "15px",
                borderRadius: "10px",
                backgroundColor: "#f5f5f5"
              }}
            >

              <h3>AI Insights</h3>

              <p>
                {aiInsights}
              </p>

            </div>

          </div>

        )
      }

    </div>

  );
}

export default App;