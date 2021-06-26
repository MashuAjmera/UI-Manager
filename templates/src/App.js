import React, { Component } from "react";

export default class App extends Component {
  state={mac:null,notif:null,ip:null,info:null};

  componentDidMount(){
    fetch('/info').then(response => response.json()).then(data => this.setState({info:data}));
    this.getmac();
    this.getip();
  }

  getmac=()=>{
    fetch('/getmac').then(response => response.json()).then(data => this.setState({mac:data}));
  }

  getip=()=>{
    fetch('/getmac').then(response => response.json()).then(data => this.setState({ip:data}));
  }

  setmac=()=> {
    // mac='08:00:27:ec:c0:c9'
    this.setState({notif:null});
    fetch('/setmac', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ mac: '08:01:27:ec:c0:c9' })
    }).then(response => response.json())
        .then(data => this.setState({notif:data}))
        .then(() => this.getmac());
  };

  setip=()=> {
    // ip='192.168.29.201'
    this.setState({notif:null});
    fetch('/setip', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ ip: '192.168.29.200' })
    }).then(response => response.json())    
      .then(data => this.setState({notif:data}))
      .then(() => this.getip());
};

  render() {
    return (
      <div>
        <h1>Welcome to the dashboard</h1>
        <div>Your device MAC address is:  {this.state.mac}</div>
        <div>Your network IP address is:  {this.state.ip}</div>
        {this.state.info && Object.entries(this.state.info).map(([key,value],i)=><div key={i}><b>{key}</b>: {value}</div>)}
      </div>
    );
  }
}
