import React, { Component } from "react";
import { Layout, Typography, Upload, message, Button } from 'antd';
import 'antd/dist/antd.css';
import { UploadOutlined, DownloadOutlined } from '@ant-design/icons';

export default class Certificates extends Component {
  handleDownload=()=>{
    fetch('/api/downloader').then((data)=>console.log(data));
  }

  render() {

    const { Title } = Typography;
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
      <Content style={{ margin: '24px 16px 0', overflow: 'initial' }}>
        <div className="site-layout-background" style={{ padding: 24, textAlign: 'center' }}>
          <Title>Welcome to the Certification!</Title>
          <Upload {...props}>
            <Button icon={<UploadOutlined />}>Upload Certificate</Button>
          </Upload>
          <Button icon={<DownloadOutlined />} href='http://localhost:5000/api/downloader' download>Download Certificate</Button>
        </div>
      </Content>
    );
  }
}