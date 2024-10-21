import React, { useState } from 'react';
import './index.css';
import {
    AppstoreOutlined,
    BarChartOutlined,
    CloudOutlined,
    ShopOutlined,
    TeamOutlined,
    UploadOutlined,
    UserOutlined,
    VideoCameraOutlined,
} from '@ant-design/icons';
import type { MenuProps } from 'antd';
import { Layout, Menu, theme } from 'antd';
import { Flex, Splitter, Typography } from 'antd';
const { Content, Footer, Sider } = Layout;

const siderStyle: React.CSSProperties = {
    overflow: 'auto',
    height: '100vh',
    position: 'fixed',
    insetInlineStart: 0,
    top: 0,
    bottom: 0,
    scrollbarWidth: 'thin',
    scrollbarColor: 'unset',
};

const menuItems = [
    { icon: AppstoreOutlined, label: 'Data Scenario' },
];

const items: MenuProps['items'] = menuItems.map((item, index) => ({
    key: String(index + 1),
    icon: React.createElement(item.icon),
    label: item.label,
}));

const App: React.FC = () => {
    const {
        token: { colorBgContainer, borderRadiusLG },
    } = theme.useToken();

    const [selectedMenu, setSelectedMenu] = useState('1');

    const handleMenuClick = (info: { key: string }) => {
        setSelectedMenu(info.key);
    };

    const renderContent = () => {
        const menuItem = menuItems[parseInt(selectedMenu) - 1];
        if(parseInt(selectedMenu) === 1)
        {
            return (
                <div>
                    <Splitter style={{ height: 1000, boxShadow: '0 0 10px rgba(0, 0, 0, 0.1)' }}>
                        <Splitter.Panel defaultSize="70%" min="20%" max="70%">

                            <h2>{menuItem.label} Content11111</h2>
                            <h2>{menuItem.label} Content11111</h2>
                            <p>This is the content for {menuItem.label}.</p>
                        </Splitter.Panel>
                        <Splitter.Panel>
                        </Splitter.Panel>
                    </Splitter>


                </div>
            );
        }

        return (
            <div>
                <h2>{menuItem.label} Content111</h2>
                <p>This is the content for {menuItem.label}.</p>
                {
                    Array.from({ length: 20 }, (_, index) => (
                        <React.Fragment key={index}>
                            <p>Additional content for {menuItem.label}</p>
                        </React.Fragment>
                    ))
                }
            </div>
        );
    };

    return (
        <Layout hasSider>
            <Sider style={siderStyle}>
                <div className="demo-logo-vertical" />
                <Menu
                    theme="dark"
                    mode="inline"
                    defaultSelectedKeys={['1']}
                    items={items}
                    onClick={handleMenuClick}
                />
            </Sider>
            <Layout style={{ marginInlineStart: 200 }}>
                <Content style={{ margin: '24px 16px 0', overflow: 'initial' }}>
                    <div
                        style={{
                            padding: 24,
                            textAlign: 'center',
                            background: colorBgContainer,
                            borderRadius: borderRadiusLG,
                        }}
                    >
                        {renderContent()}
                    </div>
                </Content>
                <Footer style={{ textAlign: 'center' }}>
                    Ant Design ©{new Date().getFullYear()} Created by Ant UED
                </Footer>
            </Layout>
        </Layout>
    );
};

export default App;