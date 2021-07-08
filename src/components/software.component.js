import React, { Component } from "react";
import { Layout, Tabs } from 'antd';
import { AppleOutlined, DatabaseOutlined } from '@ant-design/icons';
import Database from "./database.component.js"

export default class Software extends Component {
  render() {

    const { TabPane } = Tabs;
    const { Content } = Layout;

    return (
      <Layout className="site-layout">
        <Content style={{ margin: '24px 16px 0', overflow: 'initial' }}>
          <div className="site-layout-background" style={{ padding: 24}}>
            <Tabs defaultActiveKey="1" centered>
              <TabPane tab={<span><DatabaseOutlined />Database</span>} key="1" ><Database /></TabPane>
              <TabPane tab={<span><AppleOutlined />Software 2</span>} key="2" >Tab 1</TabPane>
            </Tabs>
          </div>
        </Content>
      </Layout>
    );
  }
}