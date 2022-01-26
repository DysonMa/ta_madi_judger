import "./File.css";
import React, { useEffect, useState, useContext, useRef } from "react";
import { FileContext } from "./App";
import parse from "html-react-parser";
import { Tabs, Tab, Button } from "react-bootstrap";

export const Title = () => {
  const { title } = useContext(FileContext);
  return (
    <div style={{ margin: 12 }}>
      <h2>
        <div>
          <span style={{ color: "#2e9191", fontSize: "0.8em" }}>{title}</span>
        </div>
      </h2>
    </div>
  );
};

export const UploadButton = () => {
  const { title, withUploadBtn, setContents, setSelectedFiles } =
    useContext(FileContext);

  const handleDisplayFileDetails = async (e) => {
    // `e.target.files` is an object
    const files = Array.from(e.target?.files).map((file) => {
      const reader = new FileReader();
      return new Promise((resolve) => {
        // Resolve the promise after reading file
        reader.onload = () => resolve(reader.result);
        reader.readAsText(file);
      });
    });
    const contents = await Promise.all(files);
    setContents(contents);
    setSelectedFiles(e.target?.files);
  };

  return withUploadBtn ? (
    <div style={{ marginBottom: 22 }}>
      <input
        multiple={title === "CODE" ? false : true}
        type="file"
        id="input"
        name="input"
        // className="d-none"
        onChange={handleDisplayFileDetails}
      />
    </div>
  ) : (
    <div style={{ marginBottom: 22 }}>Below are the {title} files contents</div>
  );
};

const Data = () => {
  const { contents, selectedFiles } = useContext(FileContext);

  if (!selectedFiles || !contents) return null;

  const get_lines_with_number = (content) => {
    const lines = content.split("\n");
    return lines
      .map((line, id) => {
        const isIndent = /^\s+/.exec(line)?.[0].length >= 4 ?? false;
        if (isIndent) {
          const indent = /^\s+/.exec(line)[0];
          const indentCnt = indent.length;
          line = line.replace(indent, "&nbsp".repeat(indentCnt));
        }

        // #c3ccdf
        //   #9db3e3
        const LINE_NUM_PADDING = 3;
        const onlyAnswerColor = "#FFCBBD";
        const onlyOutputColor = "#C8F0DA";
        const neitherColor = "#c3ccdf";
        let color = "#9db3e3";
        if (line.startsWith("- ")) color = onlyAnswerColor;
        if (line.startsWith("+ ")) color = onlyOutputColor;
        if (line.startsWith("? ")) color = neitherColor;

        return `<div style="background-color:${color};height:fit-content;padding-left:15px"><b style="color:aliceblue">${
          "&nbsp".repeat(LINE_NUM_PADDING - String(id + 1).length) + (id + 1)
        }</b>${"&nbsp".repeat(3)}<span>${line}</span></div>`;
      })
      .join("\r\n");
  };

  // each tab content
  const TabContent = (content) => (
    <div
      style={{
        border: "groove",
        margin: "30px 0",
        // padding: "15px 0",
        maxHeight: "50vh",
        overflowY: "scroll",
      }}
    >
      <div
        style={{
          textAlign: "left",
          //   whiteSpace: "pre-line",
        }}
      >
        <code
          style={{
            color: "black",
            fontSize: "1.1em",
            lineHeight: "1.8em",
          }}
        >
          {parse(content)}
        </code>
      </div>
    </div>
  );

  // all tabs content
  const TabContents = () =>
    contents.map((content, id) => (
      <Tab
        key={id}
        eventKey={selectedFiles[id].name}
        title={selectedFiles[id].name}
      >
        {TabContent(get_lines_with_number(content))}
      </Tab>
    ));

  return (
    <Tabs
      defaultActiveKey={selectedFiles[0].name}
      id="uncontrolled-tab-example"
      className="mb-3"
    >
      {TabContents()}
    </Tabs>
  );
};

const HintMessage = () => {
  const fileContext = useContext(FileContext);
  return fileContext.withUploadBtn ? (
    <div style={{ margin: 20 }}>
      <h4>Choose before Pressing the {fileContext.title} button</h4>
    </div>
  ) : (
    <div style={{ margin: 20 }}>
      <h4>Press the submit button to show the output</h4>
    </div>
  );
};

export const FileInfo = () => {
  const { contents } = useContext(FileContext);
  return contents ? <Data /> : <HintMessage />;
};
