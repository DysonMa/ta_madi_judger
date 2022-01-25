import "./App.css";
import React, { useEffect, useState, createContext, useReducer } from "react";
import axios from "axios";
import { Title, UploadButton, FileInfo } from "./File";
import { Button } from "react-bootstrap";

export const FileContext = createContext();

function App() {
  // code
  const [codeContents, setCodeContents] = useState("");
  const [selectedCodeFiles, setSelectedCodeFiles] = useState(null);
  // input
  const [inputContents, setInputContents] = useState("");
  const [selectedInputFiles, setSelectedInputFiles] = useState(null);
  // answer
  const [answerContents, setAnswerContents] = useState("");
  const [selectedAnswerFiles, setSelectedAnswerFiles] = useState(null);
  // output
  const [outputContents, setOutputContents] = useState("");
  const [selectedOutputFiles, setSelectedOutputFiles] = useState(null);
  // diff
  const [diffContent, setDiffContent] = useState("");
  const [selectedDiffFile, setSelectedDiffFile] = useState(null);

  // run code to get generated output files from servers
  const onFileUpload = async () => {
    if (selectedCodeFiles === null || selectedInputFiles === null) {
      alert("Please select CODE and INPUT files first");
      return;
    }

    const codeFile = selectedCodeFiles[0];

    if (codeFile.type !== "text/x-python") {
      alert("Not a python type!");
      return;
    }

    const formData = new FormData();
    formData.append("CODE", codeFile, codeFile.name);

    Array.from(selectedInputFiles).forEach((file, id) => {
      formData.append(`INPUT_${id + 1}`, file, file.name);
    });
    Array.from(selectedAnswerFiles).forEach((file, id) => {
      formData.append(`ANSWER_${id + 1}`, file, file.name);
    });

    const res = await axios.post("http://localhost:5000/run", formData);

    console.log(res.data);

    setOutputContents(res.data.content);
    setSelectedOutputFiles(res.data.filename);
  };

  // get diff files from servers
  const onFileDiff = async () => {
    if (selectedAnswerFiles === null || selectedOutputFiles === null) {
      alert("Please select ANSWER and generate OUTPUT files first");
      return;
    }

    const res = await axios.get("http://localhost:5000/diff");
    console.log(res.data);

    setDiffContent(res.data.content);
    setSelectedDiffFile(res.data.filename);
  };

  // choose state for specified title
  const useFileState = (title) => {
    let contents = null;
    let setContents = null;
    let selectedFiles = null;
    let setSelectedFiles = null;
    switch (title) {
      case "CODE":
        contents = codeContents;
        setContents = setCodeContents;
        selectedFiles = selectedCodeFiles;
        setSelectedFiles = setSelectedCodeFiles;
        break;
      case "INPUT":
        contents = inputContents;
        setContents = setInputContents;
        selectedFiles = selectedInputFiles;
        setSelectedFiles = setSelectedInputFiles;
        break;
      case "ANSWER":
        contents = answerContents;
        setContents = setAnswerContents;
        selectedFiles = selectedAnswerFiles;
        setSelectedFiles = setSelectedAnswerFiles;
        break;
      case "OUTPUT":
        contents = outputContents;
        setContents = setOutputContents;
        selectedFiles = selectedOutputFiles;
        setSelectedFiles = setSelectedOutputFiles;
        break;
      case "DIFF":
        contents = diffContent;
        setContents = setDiffContent;
        selectedFiles = selectedDiffFile;
        setSelectedFiles = setSelectedDiffFile;
        break;
    }
    return {
      contents: [contents, setContents],
      selectedFiles: [selectedFiles, setSelectedFiles],
    };
  };

  // each file section
  const File = ({ title, withUploadBtn = true }) => {
    const {
      contents: [contents, setContents],
      selectedFiles: [selectedFiles, setSelectedFiles],
    } = useFileState(title);

    const fileContext = {
      title,
      withUploadBtn,
      contents,
      setContents,
      selectedFiles,
      setSelectedFiles,
    };

    return (
      <FileContext.Provider value={fileContext}>
        <div
          style={{
            display: "flex",
            flexDirection: "column",
            width: "50%",
            margin: "0 3vw",
          }}
        >
          <Title />
          <UploadButton />
          <FileInfo />
        </div>
      </FileContext.Provider>
    );
  };

  return (
    <div className="App">
      <header className="App-header">
        <p>TA Madi's Code Judger</p>
      </header>
      <div className="App-body">
        <div
          style={{
            display: "flex",
            flexDirection: "row",
          }}
        >
          <File title="CODE" />
          <File title="INPUT" />
        </div>
        <Button variant="primary" onClick={onFileUpload}>
          Run code
        </Button>
        <div
          style={{
            display: "flex",
            flexDirection: "row",
          }}
        >
          <File title="ANSWER" />
          <File title="OUTPUT" withUploadBtn={false} />
        </div>
        <div>
          <Button variant="primary" onClick={onFileDiff}>
            Compare
          </Button>
        </div>
        <div
          style={{
            display: "flex",
            flexDirection: "column",
            alignItems: "center",
          }}
        >
          <File title="DIFF" withUploadBtn={false} />
        </div>
      </div>
    </div>
  );
}

export default App;
