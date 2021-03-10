import "./App.css";
import { useState, useEffect } from "react";
import base64 from "base-64";
import CanvasDraw from "react-canvas-draw";

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
      <div className="App">
        <CanvasDraw
          ref={(canvasDraw) => (saveableCanvas = canvasDraw)}
          imgSrc={url}
        ></CanvasDraw>
        <button
          onClick={() => {
            console.log(saveableCanvas.getSaveData());
          }}
        ></button>
      </div>
    )
  );
}

export default App;
