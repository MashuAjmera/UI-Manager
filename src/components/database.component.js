import React from "react";
import { Layout, Row, Col } from 'antd';
import Buckets from "./buckets.component.js"
import OrganizationMembers from "./members.component.js"
import Users from "./users.component.js"
import Organizations from "./orgs.component.js"

export default function Database() {
  const rowSelection = {
    onChange: (selectedRowKeys, selectedRows) => {
      console.log(`selectedRowKeys: ${selectedRowKeys}`, 'selectedRows: ', selectedRows);
    }
  };

  return (
    <Layout className="site-layout">
      <Row gutter={{ xs: 8, sm: 16, md: 24, lg: 32 }}>
        <Col span={12} className="gutter-row">
          {/* <Organizations rowSelection={rowSelection} /> */}
        </Col>
        <Col span={12} className="gutter-row">
          {/* <Users rowSelection={rowSelection} /> */}
        </Col>
      </Row>
      <Buckets rowSelection={rowSelection} />
      {/* <OrganizationMembers rowSelection={rowSelection} /> */}
    </Layout>
  );
}