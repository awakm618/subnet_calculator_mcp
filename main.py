from mcp.server.fastmcp import FastMCP
import ipaddress

# 创建MCP服务器
mcp = FastMCP("SubnetCalculator")

# 添加子网掩码计算工具
@mcp.tool()
def calculate_subnet(ip_address: str, subnet_mask: str) -> dict:
    """
    计算子网信息，包括网络地址、可用IP范围、广播地址等
    
    参数:
        ip_address: 网络中的IP地址(例如: 192.168.1.100)
        subnet_mask: 子网掩码(例如: 255.255.255.0)
    
    返回:
        包含子网详细信息的字典
    """
    try:
        # 创建网络对象
        network = ipaddress.IPv4Network(f"{ip_address}/{subnet_mask}", strict=False)
        
        # 计算各种网络信息
        network_address = str(network.network_address)
        broadcast_address = str(network.broadcast_address)
        netmask = str(network.netmask)
        hostmask = str(network.hostmask)
        prefix_length = network.prefixlen
        
        # 计算可用IP地址范围
        hosts = list(network.hosts())
        first_available = str(hosts[0]) if hosts else "无可用地址"
        last_available = str(hosts[-1]) if hosts else "无可用地址"
        total_available = len(hosts)
        
        # 生成局域网规划建议
        suggestions = []
        if prefix_length >= 24:
            suggestions.append("该子网适合小型局域网(少于254台设备)")
        elif prefix_length >= 16:
            suggestions.append("该子网适合中型局域网(255-65534台设备)")
        else:
            suggestions.append("该子网适合大型局域网(超过65534台设备)")
            
        if total_available < 10:
            suggestions.append("警告: 可用地址较少，可能不适合未来扩展")
        elif total_available > 1000 and prefix_length < 22:
            suggestions.append("提示: 子网较大，建议考虑划分子网以提高安全性和管理效率")
        
        # 返回结果
        return {
            "状态": "成功",
            "IP地址": ip_address,
            "掩码": netmask,
            "前缀长度": prefix_length,
            "主机掩码": hostmask,
            "网络": network_address,
            "第一个可用": first_available,
            "最后可用": last_available,
            "可用地址总数": total_available,
            "广播": broadcast_address,
            "局域网规划建议": suggestions
        }
        
    except ValueError as e:
        return {"状态": "错误", "信息": str(e)}

# 添加一个网络规划资源
@mcp.resource("network_advice://{network_type}")
def get_network_advice(network_type: str) -> str:
    """
    获取特定类型网络的规划建议
    
    参数:
        network_type: 网络类型，如"small"、"medium"、"large"或"enterprise"
    
    返回:
        网络规划建议字符串
    """
    advice = {
        "small": "小型网络建议使用/24子网(255.255.255.0)，可容纳254台设备，便于管理和维护。",
        "medium": "中型网络建议使用/23或/22子网，或划分为多个/24子网，使用VLAN隔离不同部门。",
        "large": "大型网络应采用分层设计，使用CIDR划分子网，实施DHCP服务器管理IP地址分配。",
        "enterprise": "企业级网络建议采用模块化设计，结合VLSM进行子网划分，实施路由冗余和负载均衡，确保高可用性。"
    }
    return advice.get(network_type.lower(), "请提供有效的网络类型: small, medium, large, enterprise")

if __name__ == "__main__":
    mcp.settings.host = '0.0.0.0'  # 允许所有网络接口访问
    mcp.run(transport='sse')  # 使用SSE传输方式启动服务器
    