import React, {Component} from "react";
import {Link } from "react-router-dom";
import { Layout, Menu } from 'antd';
import {
    SafetyCertificateOutlined,
    ControlOutlined,
    ApartmentOutlined,
    MonitorOutlined,
    HomeOutlined,
} from '@ant-design/icons';
import logo from '../static/favicon.png';

export default class Nav extends Component {
    state={menu:null,submenu:null};

    componentDidMount(){
        let y=window.location.pathname.split('/');
        this.setState({menu:y},()=>{if(y[1]==='software'){this.setState({submenu:"configuration"})}});
    }

    render(){
        const { Sider, Footer } = Layout;
        return(
        <Sider
        theme="dark"
            style={{
                overflow: 'auto',
                height: '100vh',
                position: 'fixed',
                left: 0,
            }}
        >
            <div className="logo" ><img src={logo} alt="ABB Logo" style={{ maxWidth: '90%' }} /></div>
            {this.state.menu&&<Menu theme="dark" mode="inline" defaultSelectedKeys={[this.state.menu[1]]}
          defaultOpenKeys={[this.state.submenu]} >
                <Menu.Item key="" icon={<HomeOutlined />}>
                    <Link to="/">Overview</Link>
                </Menu.Item>
                <Menu.Item key="certificates" icon={<SafetyCertificateOutlined />}>
                    <Link to="/certificates">Certificates</Link>
                </Menu.Item>
                <Menu.SubMenu key="configuration" icon={<ControlOutlined />} title="Configuration">
            <Menu.Item key="hardware">Hardware</Menu.Item>
            <Menu.Item key="software"><Link to="/software">Software</Link></Menu.Item>
            <Menu.Item key="network">Network</Menu.Item>
          </Menu.SubMenu>
                <Menu.Item key="diagnostics" icon={<ApartmentOutlined />}>
                    <Link to="/diagnostics">Diagnostics</Link>
                </Menu.Item>
                <Menu.Item key="monitoring" icon={<MonitorOutlined />}>
                    <Link to="/monitoring">Monitoring</Link>
                </Menu.Item>
            </Menu>}
                <Footer style={{position: 'fixed',bottom:0, background: 'none', paddingLeft:24, color:'#cccccc'}}>© 2021 ABB Ltd.</Footer>
        </Sider>
        );
    }
}