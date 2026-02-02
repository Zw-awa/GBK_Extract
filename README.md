# GBK 编码解压工具
用于快速解压由于启动WIndows的Beta版：使用UnicodeUTF-8提供全球浯言支持（U）导致的解压文件乱码

## 功能特点

- 🎯 **智能编码识别**：自动使用GBK(936)编码解压，避免中文文件名乱码
- 🔧 **自动检测7-Zip**：自动查找系统上的7-Zip安装路径
- ⚙️ **灵活配置**：支持自定义编码和7-Zip路径
- 📁 **右键菜单集成**：一键添加到Windows右键菜单
- 🖥️ **命令行支持**：支持命令行参数，便于批量处理
- 📦 **多种编码支持**：支持GBK、BIG5、UTF-8等多种编码格式

## 快速开始

### 方法1：拖放使用
直接将压缩文件拖放到 `GBK解压.bat` 文件上即可自动解压。

### 方法2：命令行使用
```bash
# 解压单个文件
python GBK_Extract.py 文件名.zip

# 指定输出目录
python GBK_Extract.py 文件名.zip -o 输出目录

# 指定编码
python GBK_Extract.py 文件名.zip -e 936
```

### 方法3：右键菜单
运行 `增加右键菜单.bat` 后，可在任何文件上右键选择"用GBK编码解压"。

## 安装要求

1. **Python 3.6+**
2. **7-Zip** 软件
   - 从 https://www.7-zip.org/ 下载安装
   - 或通过脚本自动检测安装路径

## 使用方法

### 基本使用
```bash
# 显示帮助
python GBK_Extract.py --help

# 配置工具
python GBK_Extract.py --config

# 测试7-Zip
python GBK_Extract.py --test

# 查看当前配置
python GBK_Extract.py --info
```

### 命令行参数
| 参数 | 简写 | 说明 |
|------|------|------|
| `文件名` | - | 要解压的文件路径 |
| `-o, --output` | 目录 | 指定输出目录 |
| `-e, --encoding` | 代码页 | 指定编码（默认936） |
| `--config` | - | 打开配置向导 |
| `--test` | - | 测试7-Zip命令 |
| `--info` | - | 显示当前配置 |
| `--help` | - | 显示帮助信息 |

### 常用代码页
| 代码页 | 编码 | 说明 |
|--------|------|------|
| 936 | GBK | 简体中文（默认） |
| 950 | Big5 | 繁体中文 |
| 65001 | UTF-8 | Unicode编码 |
| 932 | Shift-JIS | 日文 |
| 949 | EUC-KR | 韩文 |

## 项目文件说明

| 文件 | 说明 |
|------|------|
| `GBK_Extract.py` | 主程序Python脚本 |
| `GBK解压.bat` | Windows批处理文件，支持拖放使用 |
| `增加右键菜单.bat` | 将工具添加到Windows右键菜单 |
| `移除右键菜单.bat` | 从Windows右键菜单中移除工具 |
| `.gbk_extract_config.json` | 配置文件（运行后自动生成） |

## 配置说明

### 首次运行配置
首次运行时，程序会自动：
1. 查找7-Zip安装路径
2. 创建配置文件（位于用户目录下）
3. 使用默认编码（GBK/936）

### 手动配置
运行配置向导：
```bash
python GBK_Extract.py --config
```

或在配置文件中手动修改：
```json
{
  "sevenzip_path": "C:\\Program Files\\7-Zip\\7z.exe",
  "encoding": "936"
}
```

### 环境变量
- `GBK_EXTRACT_7Z_PATH`：可设置7-Zip的可执行文件路径

## 常见问题

### 1. 找不到7-Zip怎么办？
- 确保已安装7-Zip
- 运行 `python GBK_Extract.py --config` 手动配置路径
- 或将7-Zip添加到系统PATH环境变量

### 2. 解压后文件名还是乱码？
- 尝试使用其他编码：`python GBK_Extract.py 文件.zip -e 65001`
- 检查压缩包的原始编码格式
- 运行配置向导重新设置编码

### 3. 如何移除右键菜单？
运行 `移除右键菜单.bat`

### 4. 支持哪些压缩格式？
支持7-Zip支持的所有格式，包括：
- ZIP, RAR, 7Z, TAR, GZIP, BZIP2, XZ等

## 高级用法

### 批量解压
```bash
# Windows批处理
for %%i in (*.zip) do python GBK_Extract.py "%%i"

# PowerShell
Get-ChildItem *.zip | ForEach-Object { python GBK_Extract.py $_ }
```

### 集成到其他脚本
```python
# 在其他Python脚本中使用
from subprocess import run
import sys

# 解压文件
run([sys.executable, "GBK_Extract.py", "文件.zip", "-o", "输出目录"])
```

## 工作原理

1. **检测编码**：通过命令行参数或配置指定文件编码
2. **调用7-Zip**：使用`-mcp=`参数指定代码页
3. **智能输出**：自动创建与压缩包同名的输出目录
4. **错误处理**：尝试多种参数格式以确保兼容性

## 注意事项

1. **编码兼容性**：不同压缩工具创建的压缩包可能使用不同编码
2. **文件名长度**：Windows有260个字符的路径长度限制
3. **特殊字符**：移除文件名中的非法字符（`<>:"/\|?*`）
4. **权限问题**：需要以管理员权限运行才能添加右键菜单

## 更新日志

### v1.0
- 初始版本发布
- 支持GBK编码解压
- 支持拖放使用
- 支持右键菜单
- 支持命令行参数
- 自动检测7-Zip

## 许可证

本项目采用 MIT 许可证 - 详见 LICENSE 文件。

## 贡献

欢迎提交Issue和Pull Request来改进这个项目。

## 支持

如果这个工具对您有帮助，请给项目点个Star⭐！

---

**注意**：本工具仅用于解决编码问题，请确保您有权限解压相关文件。
