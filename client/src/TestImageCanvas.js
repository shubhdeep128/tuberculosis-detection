import "./App.css";
import { useState, useEffect } from "react";
import base64 from "base-64";
import CanvasDraw from "react-canvas-draw";
import Button from "react-bootstrap/Button";
import Container from "react-bootstrap/Container";
import Row from "react-bootstrap/Row";
import Col from "react-bootstrap/Col";
import Jumbotron from "react-bootstrap/Jumbotron";
import ImageUploader from "react-images-upload";

var fileDownload = require("js-file-download");

function App(props) {
  let saveableCanvas;
  let [url, setUrl] = useState(null);
  const [pictures, setPictures] = useState([]);
  const [fileName, setFileName] = useState(null);

  // let [load, setLoad] = useState(false);
  // useEffect(() => {
  //   setUrl(
  //     "https://assets.fireside.fm/file/fireside-images/podcasts/images/b/bc7f1faf-8aad-4135-bb12-83a8af679756/cover.jpg?v=3"
  //   );
  //   console.log(url);
  // }, []);
  const handleSubmit = () => {
    const data = saveableCanvas.getSaveData();
    console.log(data);
    fileDownload(data, fileName);
  };
  const onDrop = (picture) => {
    setPictures([...pictures, picture]);
  };
  const handleBack = () => {
    setPictures([]);
  };
  const handleChange = (event) => {
    setPictures(event.target.files);
  };
  useEffect(() => {
    if (pictures.length !== 0) {
      setFileName(pictures[0].name.split(".")[0] + ".json");
      var reader = new FileReader();
      var imgUrl = reader.readAsDataURL(pictures[0]);
      reader.onloadend = (e) => {
        setUrl([reader.result]);
      };
    } else {
      setFileName(null);
      setUrl(null);
    }
  }, [pictures]);

  if (pictures.length === 0) {
    return (
      <Container style={{ marginTop: "2%" }}>
        <Jumbotron>
          <h1>Welcome</h1>
          <p>Upload an image to draw on</p>

          <input type="file" onChange={handleChange} />
        </Jumbotron>
      </Container>
    );
  } else {
    console.log(pictures[0]);
    console.log(url);
    return (
      url && (
        <Container fluid>
          <Row>
            <Col className="justify-content-md-center">
              <h1 style={{ fontSize: "26px", marginTop: "20px" }}>
                Draw around the boils/scars and click on submit
              </h1>
            </Col>
          </Row>
          <Row>
            <Col className="justify-content-md-center">
              <CanvasDraw
                ref={(canvasDraw) => (saveableCanvas = canvasDraw)}
                imgSrc={url}
                brushRadius={2}
                hideGrid={true}
                brushColor="#fff"
                style={{ margin: "20px" }}
                lazyRadius={0}
              ></CanvasDraw>
            </Col>
          </Row>
          <Row className="justify-content-md-center">
            <Col>
              <Button
                style={{ margin: "5px" }}
                variant="warning"
                onClick={() => {
                  saveableCanvas.undo();
                }}
              >
                Undo
              </Button>
              <Button
                style={{ margin: "5px" }}
                variant="danger"
                onClick={() => {
                  saveableCanvas.clear();
                }}
              >
                Clear
              </Button>
            </Col>
          </Row>
          <Row>
            <Col className="justify-content-md-center">
              <Button
                style={{ width: "250px", margin: "25px" }}
                onClick={handleSubmit}
              >
                Submit
              </Button>
            </Col>
          </Row>
          <Row>
            <Col className="justify-content-md-center">
              <Button
                style={{ width: "250px", margin: "25px" }}
                onClick={handleBack}
                variant="dark"
              >
                Go Back
              </Button>
            </Col>
          </Row>
        </Container>
      )
    );
  }
}

export default App;
