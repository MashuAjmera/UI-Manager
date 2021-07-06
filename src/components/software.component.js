import React, { Component } from "react";
import { Layout, Button, PageHeader } from 'antd';
import { UserAddOutlined } from '@ant-design/icons';

export default class Database extends Component {
  handleDownload = () => {
    fetch('/api/downloader').then((data) => console.log(data));
  }

  render() {

    const { Content } = Layout;

    return (
      <Layout className="site-layout">
        <PageHeader
          ghost={false}
          onBack={() => window.history.back()}
          title="Software"
          subTitle=""
          extra={[
            <Button icon={<UserAddOutlined />} href="/software/database">Database</Button>
          ]}
        ></PageHeader>
        <Content style={{ margin: '24px 16px 0', overflow: 'initial' }}>
          <div className="site-layout-background" style={{ padding: 24, textAlign: 'center' }}>
          </div>
        </Content>
      </Layout>
    );
  }
}