import React, { Component } from "react";
import Nav from "./components/nav.component.js"
import { Layout, Button, Table, Typography } from 'antd';
import logo from './static/logo.png';
import 'antd/dist/antd.css';

export default class App extends Component {
  state = { notif: null, info: null };

  componentDidMount() {
    fetch('/info').then(response => response.json()).then(data => this.setState({ info: { ...this.state.info, ...data } }));
    this.getmac();
    this.getip();
  }

  getmac = () => { fetch('/getmac').then(response => response.json()).then(data => this.setState({ info: { ...this.state.info, "MAC Address": data } })) }

  getip = () => { fetch('/getip').then(response => response.json()).then(data => this.setState({ info: { ...this.state.info, "IP Address": data } })) }

  setmac = () => {
    // mac='08:00:27:ec:c0:c9'
    this.setState({ notif: null });
    fetch('/setmac', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ mac: '08:01:27:ec:c0:c9' })
    }).then(response => response.json())
      .then(data => this.setState({ notif: data }))
      .then(() => this.getmac());
  };

  setip = () => {
    // ip='192.168.29.201'
    this.setState({ notif: null });
    fetch('/setip', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ ip: '192.168.29.200' })
    }).then(response => response.json())
      .then(data => this.setState({ notif: data }))
      .then(() => this.getip());
  };

  render() {

    const { Title } = Typography;
    const columns = [
      {
        title: 'Property',
        dataIndex: 0,
        key: 0,
        render: text => <b>{text}</b>,
      },
      {
        title: 'Value',
        dataIndex: 1,
        key: 1,
      }
    ];

    const { Header, Content, Footer } = Layout;

    return (
      <Layout>
        <Nav/>
        <Layout className="site-layout" style={{ marginLeft: 200 }}>
          <Header style={{ position: 'fixed', zIndex: 1, width: '100%' }}>
            <div className="logo" ><img src={logo} alt="ABB Logo" style={{ maxHeight: "50px" }} /></div>
          </Header>
          <Content style={{ margin: '24px 16px 0', overflow: 'initial', marginTop: 64 }}>
            <div className="site-layout-background" style={{ padding: 24, textAlign: 'center' }}>

            <Title>Welcome to the dashboard!</Title>
              <Button type="primary" onClick={this.setmac}>Change MAC</Button>
              <Button type="primary" style={{ marginLeft: 8 }} onClick={this.setip}>Change IP</Button>

            </div>

            {this.state.info && <Table columns={columns} dataSource={Object.entries(this.state.info)} />}
          </Content>
          <Footer style={{ textAlign: 'center' }}>ABB ©2021 Created by ABB Ltd.</Footer>
        </Layout>
      </Layout>
    );
  }
}