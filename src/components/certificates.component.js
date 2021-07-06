import React, { Component } from "react";
import { Layout, Upload, message, Button, PageHeader } from 'antd';
import { UploadOutlined, DownloadOutlined } from '@ant-design/icons';

export default class Certificates extends Component {
  render() {

    const { Content } = Layout;

    const props = {
      name: 'file',
      action: '/api/uploader',
      headers: {
        authorization: 'authorization-text',
      },
      beforeUpload: file => {
        if (file.type !== 'application/x-x509-ca-cert') {
          message.error(`${file.name} is not a crt file`);
        }
        return file.type === 'application/x-x509-ca-cert' ? true : Upload.LIST_IGNORE;
      },
      onChange(info) {
        if (info.file.status !== 'uploading') {
          console.log(info.file, info.fileList);
        }
        if (info.file.status === 'done') {
          message.success(`${info.file.name} file uploaded successfully`);
        } else if (info.file.status === 'error') {
          message.error(`${info.file.name} file upload failed.`);
        }
      },
    };

    return (
      <Layout className="site-layout">
        <PageHeader
          ghost={false}
          onBack={() => window.history.back()}
          title="Certificate Authority"
          extra={[
            <Upload {...props}>
              <Button icon={<UploadOutlined />}>Upload Certificate</Button>
            </Upload>
          ]}
        ></PageHeader>
      <Content style={{ margin: '24px 16px 0', overflow: 'initial' }}>
        <div className="site-layout-background" style={{ padding: 24, textAlign: 'center' }}>
          <Button icon={<DownloadOutlined />} href='http://localhost:5000/api/downloader' download>Download Certificate</Button>
        </div>
      </Content>
      </Layout>
    );
  }
}