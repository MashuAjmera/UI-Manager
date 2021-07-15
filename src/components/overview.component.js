import React, { Component } from "react";
import { Layout, Table, Typography, message, Skeleton, Input } from 'antd';

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

  setmac = (value) => {
    // let value ='08:00:27:ec:c0:c9'
    fetch('/api/network/mac', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ mac: value })
    }).then(response => response.json())
      .then(data => message.success(data))
      .then(() => this.getmac())
      .catch(err => message.warning(err));
  };

  setip = (value) => {
    // let value='192.168.29.201'
    fetch('/api/network/ip', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ ip: value })
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
          <Input.Search placeholder="Enter MAC Address" onSearch={this.setmac} enterButton="Change" style={{ width: 250 }}  />
          <Input.Search placeholder="Enter IP Address" onSearch={this.setip} enterButton="Add" style={{ marginLeft: 8, width: 250 }}  />
          <Skeleton loading={this.state.loading} active title={{ width: '100%' }} paragraph={{ rows: 10, width: '100%' }}>
            {this.state.info && <Table columns={columns} dataSource={Object.entries(this.state.info)} style={{ marginTop: 30 }} />}
          </Skeleton>
        </div>
      </Content>
    );
  }
}