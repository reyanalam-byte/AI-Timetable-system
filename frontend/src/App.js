import React, { useState } from "react";
import API from "./api";

function App() {

  const [teacher, setTeacher] = useState("");
  const [replacements, setReplacements] = useState([]);

  const markAbsent = async () => {

    const response = await API.post(
      `/teacher/absent/${teacher}`
    );

    setReplacements(response.data.replacements);
  };

  return (
    <div style={{ padding: "30px" }}>

      <h1>AI Timetable System</h1>

      <input
        type="text"
        placeholder="Enter Teacher Name"
        onChange={(e) => setTeacher(e.target.value)}
      />

      <button onClick={markAbsent}>
        Mark Absent
      </button>

      <hr />

      {
        replacements.map((item, index) => (

          <div key={index}>

            <h3>
              Section {item.section}
            </h3>

            <p>
              Replacement:
              {item.replacementTeacher}
            </p>

          </div>
        ))
      }

    </div>
  );
}

export default App;