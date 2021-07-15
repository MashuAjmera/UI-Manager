import React, { Component, useContext, useState, useEffect, useRef } from "react";
import { Button, Table, Input, Popconfirm, Form, Tooltip, message, Modal } from 'antd';
import { AppstoreAddOutlined, InfoCircleOutlined } from '@ant-design/icons';

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


const CollectionCreateForm = ({ visible, onCreate, onCancel, confirmLoading}) => {
  const [form] = Form.useForm();
  return (
    <Modal
      visible={visible}
      confirmLoading={confirmLoading}
      title="Create a new organization"
      okText="Add"
      onCancel={() => { form.resetFields(); onCancel(); }}
      onOk={() => {
        form
          .validateFields()
          .then((values) => {
            form.resetFields();
            values.retentionPeriod = values.rpw + 'w' + values.rpd + 'd' + values.rph + 'h' + values.rpm + 'm' + values.rps + 's';
            onCreate(values);
            console.log(values);
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
        }}>
        <Form.Item
          label="Organization Name"
          name="name"
          rules={[
            {
              required: true,
              message: 'Please input the organization name!',
            },
          ]}
        >
          <Input />
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


export default class Organizations extends Component {
  state = { confirmLoading: false, modal: false, orgs:[] };

  componentDidMount() {
    this.handleView();
  }

  handleView = () => {
    fetch('/api/db/org')
      .then(response => response.json())
      .then((data) => this.setState({ orgs: data }))
      .catch(error => message.warning({ content: error }));
  }

  handleDelete = (id) => {
    const key = 'updatable';
    message.loading({ content: 'Sending Request...', key, duration: 10 });
    fetch('/api/db/org', {
      method: 'DELETE',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ id })
    }).then(response => response.json())
      .then((data) => message.success({ content: data, key }))
      .then(() => this.handleView())
      .catch(error => message.warning({ content: error, key }));
  };

  handleAdd = (values) => {
    this.setState({ confirmLoading: true }, () =>
      fetch('/api/db/org', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(values)
      })
        .then(response => response.json())
        .then((data) => this.setState({ modal: false, confirmLoading: false }, message.success(data)))
        .then(() => this.handleView())
        .catch(error => message.warning(error)));
  };

  handleSave = (row) => {
    const key = 'updatable';
    message.loading({ content: 'Sending Request...', key, duration: 10 });
    fetch('/api/db/org', {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(row)
    }).then(response => response.json())
      .then((data) => message.success({ content: data, key }))
      .then(() => this.handleView())
      .catch(error => message.warning({ content: error, key }));
  };

  handleCancel = () => {
    this.setState({ modal: false });
  };

  handleModal=()=>{
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
        title: 'Description',
        dataIndex: 'description',
      },
      {
        title: 'Operation',
        dataIndex: 'operation',
        render: (_, record) =>
          this.state.orgs.length >= 1 ? (
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
          dataSource={this.state.orgs}
          columns={columns2}
          title={() => <>Organizations<Button
            icon={<AppstoreAddOutlined />}
            onClick={this.handleModal}
            style={{ float: 'right' }}
          >
            Add New
          </Button></>}
        />
        <CollectionCreateForm visible={this.state.modal} confirmLoading={this.state.confirmLoading} onCreate={this.handleAdd} onCancel={this.handleCancel} orgs={this.state.orgs} />
      </>
    );
  }
}