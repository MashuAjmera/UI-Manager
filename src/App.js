import React, { Component } from "react";
import { BrowserRouter, Route, Switch } from "react-router-dom";
import Nav from "./components/nav.component.js"
import Overview from "./components/overview.component.js"
import Database from "./components/database.component.js"
import Software from "./components/software.component.js"
import Certificates from "./components/certificates.component.js"
import { Layout } from 'antd';
import logo from './static/logo.png';
// import 'antd/dist/antd.css';
import './static/antd.css';

export default class App extends Component {
  render() {
    const { Header } = Layout;

    return (
      <BrowserRouter>
        <Layout>
          {/* <Header style={{ position: 'fixed', zIndex: 1, width: '100%' }}>
            <div className="logo" ><img src={logo} alt="ABB Logo" style={{ maxHeight: "50px" }} /></div>
          </Header> */}
          <Layout className="site-layout" style={{marginLeft: 200, paddingBottom: 100 }}>
            <Nav />
            <Switch>
              <Route path="/" exact component={Overview} />
              <Route path="/certificates" component={Certificates} />
              <Route path="/software/database" component={Database} />
              <Route path="/software" component={Software} />
              <Route component={Overview} />
            </Switch>
          </Layout>
        </Layout>
      </BrowserRouter>
    );
  }
}