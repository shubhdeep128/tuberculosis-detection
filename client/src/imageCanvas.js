import "./App.css";
import { useState, useEffect } from "react";
import base64 from "base-64";
import CanvasDraw from "react-canvas-draw";
import Button from "react-bootstrap/Button";
import Container from "react-bootstrap/Container";
import Row from "react-bootstrap/Row";

function App(props) {
  let saveableCanvas;
  let [url, setUrl] = useState(null);
  // let [load, setLoad] = useState(false);
  useEffect(() => {
    setUrl(base64.decode(props.match.params.url));
    console.log(base64.decode(props.match.params.url));
  }, []);
  return (
    url && (
      <Container>
        <Row></Row>
        <h1 style={{ fontSize: "26px", marginTop: "20px" }}>
          Draw around the boils/scars and click on submit
        </h1>
        <CanvasDraw
          ref={(canvasDraw) => (saveableCanvas = canvasDraw)}
          imgSrc={url}
          brushRadius={2}
          hideGrid={true}
          brushColor="#fff"
          style={{ margin: "20px" }}
          canvasHeight={400}
          canvasWidth={300}
        ></CanvasDraw>
        <Button
          style={{ margin: "5px" }}
          variant="warning"
          onClick={() => {
            console.log(saveableCanvas.undo());
          }}
        >
          Undo
        </Button>
        <Button
          style={{ margin: "5px" }}
          variant="danger"
          onClick={() => {
            console.log(saveableCanvas.clear());
          }}
        >
          Clear
        </Button>
        <Button
          style={{ display: "block" }}
          onClick={() => {
            console.log(saveableCanvas.getSaveData());
            window.ReactNativeWebView.postMessage("Hello!");
          }}
        >
          Submit
        </Button>
      </Container>
    )
  );
}

export default App;
