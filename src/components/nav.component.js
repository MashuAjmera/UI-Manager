import React from "react";
import { Layout, Menu } from 'antd';
import {
  AppstoreOutlined,
  BarChartOutlined,
  CloudOutlined,
  ShopOutlined,
  TeamOutlined,
  UserOutlined,
  UploadOutlined,
  VideoCameraOutlined,
} from '@ant-design/icons';

export default function Nav(props) {
    const { Sider } = Layout;
    return(
    <Sider
        style={{
            overflow: 'auto',
            height: '100vh',
            position: 'fixed',
            left: 0,
        }}
    >
        <div className="logo" />
        <Menu theme="dark" mode="inline" defaultSelectedKeys={['1']}>
            <Menu.Item key="1" icon={<UserOutlined />}>
                Overview
            </Menu.Item>
            <Menu.Item key="2" icon={<VideoCameraOutlined />}>
                Accounts
            </Menu.Item>
            <Menu.Item key="3" icon={<UploadOutlined />}>
                Certificates
            </Menu.Item>
            <Menu.Item key="4" icon={<BarChartOutlined />}>
                Configuration
            </Menu.Item>
            <Menu.Item key="5" icon={<CloudOutlined />}>
                Diagnostics
            </Menu.Item>
            <Menu.Item key="6" icon={<AppstoreOutlined />}>
                Information
            </Menu.Item>
            <Menu.Item key="7" icon={<TeamOutlined />}>
                Licenses
            </Menu.Item>
            <Menu.Item key="8" icon={<ShopOutlined />}>
                Networking
            </Menu.Item>
        </Menu>
    </Sider>);
}