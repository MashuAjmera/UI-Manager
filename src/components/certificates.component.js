import React, { Component } from "react";
import { Layout, Typography } from 'antd';
import 'antd/dist/antd.css';

export default class Certificates extends Component {
  render() {

    const { Title } = Typography;
    const { Content } = Layout;

    return (
      <Content style={{ margin: '24px 16px 0', overflow: 'initial' }}>
        <div className="site-layout-background" style={{ padding: 24, textAlign: 'center' }}>
          <Title>Welcome to the Certification!</Title>
        </div>
      </Content>
    );
  }
}