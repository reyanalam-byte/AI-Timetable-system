import React, { useState } from "react";
import API from "./api";

function App() {

  const [teacher, setTeacher] = useState("");
  const [replacements, setReplacements] = useState([]);

  const markAbsent = async () => {

    try {

      const response = await API.post(
        `/teacher/absent/${teacher}`
      );

      setReplacements(response.data.replacements);

    } catch (error) {

      alert("Error connecting to backend");

      console.log(error);
    }
  };

  return (

    <div style={{ padding: "30px" }}>

      <h1>AI Timetable System</h1>

      <input
        type="text"
        placeholder="Enter Teacher Name"
        value={teacher}
        onChange={(e) => setTeacher(e.target.value)}
        style={{
          padding: "10px",
          width: "250px",
          marginRight: "10px"
        }}
      />

      <button
        onClick={markAbsent}
        style={{
          padding: "10px 20px",
          cursor: "pointer"
        }}
      >
        Mark Absent
      </button>

      <hr />

      <h2>AI Replacement Result</h2>

      <p>
        <b>Absent Teacher:</b> {teacher}
      </p>

      <p>
        <b>Total Replacements:</b> {replacements.length}
      </p>

      {

        replacements.map((item, index) => (

          <div
            key={index}
            style={{
              border: "1px solid gray",
              padding: "15px",
              marginTop: "10px",
              borderRadius: "10px"
            }}
          >

            <h3>
              Section {item.section}
            </h3>

            <p>
              <b>Class:</b> {item.class}
            </p>

            <p>
              <b>Subject:</b> {item.subject}
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

        ))

      }

    </div>
  );
}

export default App;