import React, { Component } from "react";
import { Layout, Button, Table, Typography, message, Skeleton } from 'antd';

export default class Overview extends Component {
  state = { info: null, loading: true };

  componentDidMount() {
    fetch('/api/info')
      .then(response => response.json())
      .then(data => this.setState({ info: { ...this.state.info, ...data }, loading: false }))
      .catch(error=>console.log(error));
    this.getmac();
    this.getip();
  }

  getmac = () => { 
    fetch('/api/network/mac')
      .then(response => response.json())
      .then(data => this.setState({ info: { ...this.state.info, "MAC Address": data } }))
      .catch(error => console.log(error)) 
  }

  getip = () => { 
    fetch('/api/network/ip')
      .then(response => response.json())
      .then(data => this.setState({ info: { ...this.state.info, "IP Address": data } }))
      .catch(error=>console.log(error))
  }

  setmac = () => {
    // mac='08:00:27:ec:c0:c9'
    fetch('/api/network/mac', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ mac: '08:01:27:ec:c0:c9' })
    }).then(response => response.json())
      .then(data => message.success(data))
      .then(() => this.getmac())
      .catch(err => message.warning(err));
  };

  setip = () => {
    // ip='192.168.29.201'
    fetch('/api/network/ip', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ ip: '192.168.29.200' })
    }).then(response => response.json())
      .then(data => message.success(data))
      .then(() => this.getip())
      .catch(err => message.warning(err));
  };

  render() {

    const { Title } = Typography;
    const columns = [
      {
        title: 'Property',
        dataIndex: 0,
        key: 0,
        render: (text) => <b>{text}</b>
      },
      {
        title: 'Value',
        dataIndex: 1,
        key: 1,
      }
    ];

    const { Content } = Layout;

    return (
      <Content style={{ margin: '24px 16px 0', overflow: 'initial' }}>
        <div className="site-layout-background" style={{ padding: 24, textAlign: 'center' }}>
          <Title>Welcome to the dashboard!</Title>
          <Button type="primary" onClick={this.setmac}>Change MAC</Button>
          <Button type="primary" style={{ marginLeft: 8 }} onClick={this.setip}>Change IP</Button>
          <Skeleton loading={this.state.loading} active title={{ width: '100%' }} paragraph={{ rows: 10, width: '100%' }}>
            {this.state.info && <Table columns={columns} dataSource={Object.entries(this.state.info)} style={{ marginTop: 30 }} />}
          </Skeleton>
        </div>
      </Content>
    );
  }
}