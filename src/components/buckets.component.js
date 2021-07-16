import React, { Component, useContext, useState, useEffect, useRef } from "react";
import { Button, Table, Input, InputNumber, Popconfirm, Form, Tooltip, message, Modal, Select } from 'antd';
import { FolderAddOutlined, InfoCircleOutlined } from '@ant-design/icons';

const EditableContext = React.createContext(null);

const EditableRow = ({ index, ...props }) => {
  const [form] = Form.useForm();
  return (
    <Form form={form} component={false}>
      <EditableContext.Provider value={form}>
        <tr {...props} />
      </EditableContext.Provider>
    </Form>
  );
};

const EditableCell = ({
  title,
  editable,
  children,
  dataIndex,
  record,
  handleSave,
  ...restProps
}) => {
  const [editing, setEditing] = useState(false);
  const inputRef = useRef(null);
  const form = useContext(EditableContext);
  useEffect(() => {
    if (editing) {
      inputRef.current.focus();
    }
  }, [editing]);

  const toggleEdit = () => {
    setEditing(!editing);
    form.setFieldsValue({
      [dataIndex]: record[dataIndex],
    });
  };

  const save = async () => {
    try {
      const values = await form.validateFields();
      toggleEdit();
      handleSave({ ...record, ...values });
    } catch (errInfo) {
      console.log('Save failed:', errInfo);
    }
  };

  let childNode = children;

  if (editable) {
    childNode = editing ? (
      <Form.Item
        style={{
          margin: 0,
        }}
        name={dataIndex}
        rules={[
          {
            required: true,
            message: `${title} is required.`,
          },
        ]}
      >
        <Input ref={inputRef} onPressEnter={save} onBlur={save} suffix={
          <Tooltip title="Press Enter to Save">
            <InfoCircleOutlined style={{ color: 'rgba(0,0,0,.45)' }} />
          </Tooltip>
        } />
      </Form.Item>
    ) : (
      <Tooltip title="Click to Edit"
        className="editable-cell-value-wrap"
        onClick={toggleEdit}>
        {children}
      </Tooltip>
    );
  }

  return <td {...restProps}>{childNode}</td>;
};


const CollectionCreateForm = ({ visible, onCreate, onCancel, confirmLoading, orgs }) => {
  const [form] = Form.useForm();
  return (
    <Modal
      visible={visible}
      confirmLoading={confirmLoading}
      title="Create a new bucket"
      okText="Create"
      onCancel={() => { form.resetFields(); onCancel(); }}
      onOk={() => {
        form
          .validateFields()
          .then((values) => {
            form.resetFields();
            onCreate(values);
          })
          .catch((info) => {
            console.log('Validate Failed:', info);
          });
      }}
    >
      <Form form={form} name="form_in_modal"
        labelCol={{
          span: 8,
        }}
        wrapperCol={{
          span: 18,
        }}
        initialValues={{
          description: "",
        }}>
        <Form.Item
          label="Bucket Name"
          name="name"
          rules={[
            {
              required: true,
              message: 'Please input the bucket name!',
            },
          ]}
        >
          <Input />
        </Form.Item>
        <Form.Item
          label="Retention Persiod"
          name="retentionPeriod"
          rules={[
            {
              required: true,
              message: 'Please input the bucket name!',
            },
          ]}
        >
          <InputNumber min={3600} addonAfter={'s'} />
        </Form.Item>
        <Form.Item
          label="Organization"
          name="organization"
          rules={[
            {
              required: true,
              message: 'Please input the bucket name!',
            },
          ]}
        >
          <Select
            showSearch
            placeholder="Select"
            optionFilterProp="children"
            filterOption={(input, option) =>
              option.children.toLowerCase().indexOf(input.toLowerCase()) >= 0
            }
          >
            {orgs.map(org => <Select.Option key={org.id} value={org.id}>{org.name}</Select.Option>)}
          </Select>
        </Form.Item>
        <Form.Item
          label="Description"
          name="description"
        >
          <Input.TextArea />
        </Form.Item>
      </Form>
    </Modal>
  );
};


export default class Buckets extends Component {
  state = { bucket: {}, buckets: [], confirmLoading: false, modal: false, orgs: [] };

  componentDidMount() {
    this.handleList();
  }

  handleList = () => {
    fetch('/api/db/bucket')
      .then(response => response.json())
      .then((data) => this.setState({ buckets: data }))
      .catch(error => message.warning({ content: error }));
  }

  handleDelete = (id) => {
    const key = 'updatable';
    message.loading({ content: 'Sending Request...', key, duration: 10 });
    fetch('/api/db/bucket', {
      method: 'DELETE',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ id })
    }).then(response => response.json())
      .then((data) => {
        this.handleList();
        message.success({ content: data, key })
      })
      .catch(error => message.warning({ content: error, key }));
  };

  handleCreate = (values) => {
    this.setState({ confirmLoading: true }, () =>
      fetch('/api/db/bucket', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(values)
      })
        .then(response => response.json())
        .then((data) => this.setState({ modal: false, confirmLoading: false, buckets: [...this.state.buckets, data] }, message.success("successfully created")))
        .catch(error => message.warning(error)));
  };

  handleSave = (row) => {
    const newData = [...this.state.buckets];
    const index = newData.findIndex((item) => row.id === item.id);
    const item = newData[index];
    const key = 'updatable';
    message.loading({ content: 'Sending Request...', key, duration: 10 });
    var which;
    if (row.name !== item.name) {which="name"}
    else if (row.description !== item.description) { which="description" }
    else if (row.retentionPeriod !== item.retentionPeriod) { which="retentionPeriod" }
    fetch('/api/db/bucket', {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ id: row.id, [which]: row[which] })
    }).then(response => response.json())
    .then((data) => {
      newData.splice(index, 1, data);
      this.setState({ buckets: newData }, message.success({ content: "successfully updated", key }));
    })
      .catch(error => message.warning({ content: error, key }));
  };

  handleCancel = () => {
    this.setState({ modal: false });
  };

  handleModal = () => {
    this.setState({ modal: true });
    fetch('/api/db/org')
      .then(response => response.json())
      .then((data) => this.setState({ orgs: data }))
      .catch(error => message.warning({ content: error }));
  }

  render() {

    const columns = [
      {
        title: 'Name',
        dataIndex: 'name',
        width: '25%',
        editable: true,
      },
      {
        title: 'Retention Policy (ns)',
        dataIndex: 'retentionPeriod',
        width: '25%',
        editable: true,
      },
      {
        title: 'Organization',
        dataIndex: 'orgID',
      },
      {
        title: 'Description',
        dataIndex: 'description',
        editable: true,
      },
      {
        title: 'Operation',
        dataIndex: 'operation',
        render: (_, record) =>
          this.state.buckets.length >= 1 ? (
            <Popconfirm title="Sure to delete?" onConfirm={() => this.handleDelete(record.id)}>
              <Button type="link" size="small">Delete</Button>
            </Popconfirm>
          ) : null,
      },
    ];

    const components = {
      body: {
        row: EditableRow,
        cell: EditableCell,
      },
    };

    const columns2 = columns.map((col) => {
      if (!col.editable) {
        return col;
      }

      return {
        ...col,
        onCell: (record) => ({
          record,
          editable: col.editable,
          dataIndex: col.dataIndex,
          title: col.title,
          handleSave: this.handleSave,
        }),
      };
    });

    return (
      <>
        <Table
          components={components}
          rowClassName={() => 'editable-row'} style={{ paddingBottom: 24 }}
          rowSelection={{
            type: 'radio',
            ...this.props.rowSelection,
          }}
          pagination={false}
          dataSource={this.state.buckets}
          columns={columns2}
          title={() => <>Buckets<Button
            icon={<FolderAddOutlined />}
            onClick={this.handleModal}
            style={{ float: 'right' }}
          >
            Create New
          </Button></>}
        />
        <CollectionCreateForm visible={this.state.modal} confirmLoading={this.state.confirmLoading} onCreate={this.handleCreate} onCancel={this.handleCancel} orgs={this.state.orgs} />
      </>
    );
  }
}