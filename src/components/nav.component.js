import React, {Component} from "react";
import {Link } from "react-router-dom";
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

export default class Nav extends Component {
    render(){
        const { Sider, Footer } = Layout;
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
            <Menu theme="dark" mode="inline" defaultSelectedKeys={[window.location.pathname]}>
                <Menu.Item key="/" icon={<UserOutlined />}>
                    <Link to="/">Overview</Link>
                </Menu.Item>
                <Menu.Item key="/accounts" icon={<VideoCameraOutlined />}>
                    <Link to="/accounts">Accounts</Link>
                </Menu.Item>
                <Menu.Item key="/certificates" icon={<UploadOutlined />}>
                    <Link to="/certificates">Certificates</Link>
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
                <Footer style={{position: 'fixed',bottom:0, background: 'none', color: 'rgba(255,255,255,0.55)', paddingLeft:24}}>© 2021 ABB Ltd.</Footer>
        </Sider>
        );
    }
}