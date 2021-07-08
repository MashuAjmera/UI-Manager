import React, { Component } from "react";
import { Layout, Button, Table, Row, Col } from 'antd';
import { UserAddOutlined, UsergroupAddOutlined } from '@ant-design/icons';
import Buckets from "./buckets.component.js"
import Organizations from "./organizations.component.js"

export default class Database extends Component {
  state = { orgs: [{ name: "Jack", id: "da" }, { name: "Lucy", id: "da" }, { name: "Tom", id: "Tomss" }], users: [], org: {}, user: {} };

  componentDidMount() {

    // fetch('/api/db/organization')
    //   // .then(response => response.json())
    //   .then((data) => this.setState({orgs:data}))
    //   .catch(error => message.warning({ content: error}));
    // fetch('/api/db/user')
    //   // .then(response => response.json())
    //   .then((data) => this.setState({users:data}))
    //   .catch(error => message.warning({ content: error}));
  }

  render() {

    const columns = [
      {
        title: 'Name',
        dataIndex: 'name',
      },
      {
        title: 'Cash Assets',
        className: 'column-money',
        dataIndex: 'money',
        align: 'right',
      },
      {
        title: 'Address',
        dataIndex: 'address',
      },
    ];

    const rowSelection = {
      onChange: (selectedRowKeys, selectedRows) => {
        console.log(`selectedRowKeys: ${selectedRowKeys}`, 'selectedRows: ', selectedRows);
      }
    };

    const data = [
      {
        key: '1',
        name: 'John Brown',
        money: '￥300,000.00',
        address: 'New York No. 1 Lake Park',
      },
      {
        key: '2',
        name: 'Jim Green',
        money: '￥1,256,000.00',
        address: 'London No. 1 Lake Park',
      },
      {
        key: '3',
        name: 'Joe Black',
        money: '￥120,000.00',
        address: 'Sidney No. 1 Lake Park',
      },
    ];

    return (
      <Layout className="site-layout">
        <Row gutter={{ xs: 8, sm: 16, md: 24, lg: 32 }}>
          <Col span={12} className="gutter-row">
            <Organizations rowSelection={rowSelection} />
          </Col>
          <Col span={12} className="gutter-row">
            <Table style={{ paddingBottom: 24 }}
              rowSelection={{
                type: 'radio',
                ...rowSelection,
              }}
              pagination={false}
              columns={columns}
              dataSource={data}
              title={() => <>Users<Button icon={<UserAddOutlined />} style={{ float: 'right' }}>Add New</Button></>}
            /></Col>
        </Row>
        <Buckets rowSelection={rowSelection} />
        <Table
          rowSelection={{
            type: 'radio',
            ...rowSelection,
          }} style={{ paddingBottom: 24 }}
          pagination={false}
          columns={columns}
          dataSource={data}
          title={() => <>Organization Members<Button icon={<UsergroupAddOutlined />} style={{ float: 'right' }}>Add New</Button></>}
        />
      </Layout>
    );
  }
}