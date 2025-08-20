# 子网掩码计算器 MCP 服务器

一个基于MCP框架的子网掩码计算器服务器，提供子网信息计算和网络规划建议功能。

## 功能特点

- 计算子网详细信息，包括：
  - 网络地址
  - 子网掩码和前缀长度
  - 可用IP地址范围（第一个和最后一个可用IP）
  - 可用IP地址总数
  - 广播地址
- 提供基于网络规模的局域网规划建议
- 支持不同类型网络（小型、中型、大型、企业级）的专门规划建议

## 安装与使用

### 前提条件

- Python 3.7+
- MCP框架

### 安装步骤

1. 克隆仓库git clone https://github.com/awakm618/subnet_calculator_mcp.git
2. cd subnet-calculator-mcp
3. 安装依赖pip install -r requirements.txt
4. 启动服务器python3 main.py
服务器将在默认端口启动，使用SSE传输方式，允许所有网络接口访问。

## API 使用

### 工具调用

#### 子网计算工具
- 名称: `calculate_subnet`
- 参数:
  - `ip_address`: 网络中的IP地址（例如: 192.168.1.100）
  - `subnet_mask`: 子网掩码（例如: 255.255.255.0）
- 返回: 包含子网详细信息的JSON对象

### 资源访问

#### 网络规划建议
- 资源路径: `network_advice://{network_type}`
- 参数:
  - `network_type`: 网络类型，可选值：small, medium, large, enterprise
- 返回: 对应网络类型的规划建议字符串

## 示例

计算192.168.1.100/255.255.255.0的子网信息：# 示例客户端调用
result = client.call_tool("calculate_subnet", {
    "ip_address": "192.168.1.100",
    "subnet_mask": "255.255.255.0"
})
print(result)
获取小型网络的规划建议：# 示例客户端资源访问
advice = client.get_resource("network_advice://small")
print(advice)
## 许可证

[MIT](LICENSE)
    
