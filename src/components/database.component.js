import React, { Component } from "react";
import { Layout, Button, PageHeader, Breadcrumb } from 'antd';
import { UserAddOutlined, HomeOutlined } from '@ant-design/icons';

export default class Database extends Component {
  handleDownload=()=>{
    fetch('/api/downloader').then((data)=>console.log(data));
  }

  render() {

    const { Content } = Layout;

    return (
      <Layout className="site-layout">
        <PageHeader
      ghost={false}
      onBack={() => window.history.back()}
      breadcrumb={<Breadcrumb separator=">">
      <Breadcrumb.Item href="/"><HomeOutlined /></Breadcrumb.Item>
      <Breadcrumb.Item href="/software">Software</Breadcrumb.Item>
    </Breadcrumb>}
      title="Database"
      subTitle="InfluxDb"
      extra={[
      <Button icon={<UserAddOutlined />}>Create New Account</Button>
      ]}
    ></PageHeader>
      <Content style={{ margin: '24px 16px 0', overflow: 'initial' }}>
        <div className="site-layout-background" style={{ padding: 24, textAlign: 'center' }}>
        </div>
      </Content></Layout>
    );
  }
}