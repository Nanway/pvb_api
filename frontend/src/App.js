import React, { Component } from 'react';
import '../node_modules/bootstrap/dist/css/bootstrap.css';
import './App.css';
import spinner from './spinner.png';
import axios from 'axios'

function PredictionButton(props) {
  return <button className="btn Predict-button" onClick={props.onClick}
  >Predict
        </button>
}

function UploadButton(props) {
  return <button className="btn App-button">{props.displayText}</button>
}

class UploadInput extends Component {
  constructor(props) {
    super(props);
  }

  shouldComponentUpdate(nextprops) {
    return nextprops.shouldUpdate;
  }

  render() {
    return <input type="file" className="App-input"
      onChange={(event) => { this.props.onClick(event) }} />
  }
}

class App extends Component {
  constructor(props) {
    super(props);
    this.state = {
      fileSelected: false,
      file: undefined,
      predicting: false,
      prediction: "None",
      failed: undefined,
      probability: undefined,
      serverOnline: false

    }
    this.handleInputClick = this.handleInputClick.bind(this);
    this.handlePredictClick = this.handlePredictClick.bind(this);
  }

  changeServerStatus(status) {
    this.setState({ serverOnline: status })
  }

  pingServer() {
    axios.get('https://pvb-api.herokuapp.com/', { timeout: 1000 * 150 }).then((response) => {
      console.log(response)
      if (response.status === 404) {
        this.changeServerStatus(false)
      } else {
        console.log("Changing server to online")
        this.changeServerStatus(true)
      }
    }, (error) => {
      console.log("Changing server to offline")
      this.changeServerStatus(false)
    })
  }

  handleInputClick(event) {
    try {
      this.setState({
        fileSelected: true,
        file: event.target.files[0],
        fileURL: URL.createObjectURL(event.target.files[0]),
        predicting: false,
        prediction: "None",
        failed: undefined,
        probability: undefined,
        serverOnline: false
      });
      this.pingServer()

    } catch (error) {
    }
  }

  handlePredictClick() {
    this.setState({ predicting: true });
    const fd = new FormData();
    fd.append('image', this.state.file, this.state.file.name);
    console.log("yeet11");
    axios.post('https://pvb-api.herokuapp.com/api/make_prediction', fd)
      .then((res) => {
        const resData = res.data;
        if (resData.Failed) {
          this.setState({
            predicting: false,
            failed: resData.Reason,
          });
        } else {
          this.setState({
            predicting: false,
            prediction: resData.Prediction,
            probability: resData.Probability
          });
        }
      })
  }

  decideDisplayText() {
    var shouldUpdate;
    var displayText;
    if (this.state.fileSelected) {
      shouldUpdate = false;
      var fileName = this.state.file.name;
      if (fileName.length > 12) {
        fileName = fileName.substring(0, 6) + '...' +
          fileName.substring(fileName.length - 8);
      }
      displayText = "Selected: " + fileName;
    } else {
      shouldUpdate = true;
      displayText = "Choose an image"
    }
    return [shouldUpdate, displayText];
  }

  renderPredictButton() {
    console.log(this.state.serverOnline)
    if (this.state.failed) {
      return (<p><b>Failed.</b> Reason: {this.state.failed}</p>)
    } else if (this.state.prediction !== "None") {
      return (<p>I think this is a <b>{this.state.prediction} </b>
        with probability <b>{this.state.probability}</b>
      </p>)
    } else if (!this.state.fileSelected) {
      return
    } else if (!this.state.serverOnline) {
      return (<div>
        <img src={spinner} className="App-spinner" alt="" />
        <p>Waiting for AI to start (try refreshing after a minute if no change)</p>
        <p>Life is hard when you don't have money for 24/7 backends</p>
      </div>)
    } else if (this.state.predicting) {
      return (<div>
        <img src={spinner} className="App-spinner" alt="" />
        <p>Predicting...</p>
        <p>This may take a moment for larger images</p>
      </div>)
    } else {
      return (<PredictionButton onClick={this.handlePredictClick} />)
    }
  }

  render() {
    var shouldUpdate;
    var displayText;
    [shouldUpdate, displayText] = this.decideDisplayText();

    return (
      <div className="App">
        <br></br>

        <p><a
          href="https://github.com/Nanway/pug_vs_bulldog_frontend">
          GitHub repo and explanation
          </a>
        </p>
        <div className="navbar-nav">
          <div className="Upload-block">
            <UploadInput shouldUpdate={shouldUpdate}
              onClick={this.handleInputClick} />
            <UploadButton displayText={displayText} />
          </div>
          <div className="Upload-Image">
            {this.state.fileSelected &&
              <img src={this.state.fileURL} alt={this.state.fileName}
                className="Display-Image"
              />
            }
            <br></br>
            <div className="Predict-button-container">
              {this.renderPredictButton()}
            </div>
          </div>

        </div>
      </div>
    )
  }
}



export default App;
