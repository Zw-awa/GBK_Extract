import os
import sys
import subprocess
import json
import re
from pathlib import Path

# 配置文件路径
CONFIG_FILE = Path.home() / ".gbk_extract_config.json"

def load_config():
    """加载配置文件"""
    config = {
        "sevenzip_path": None,  # 7z路径，如果为None则尝试在PATH中查找
        "encoding": "936",     # 默认编码（GBK对应的代码页是936）
    }
    
    if CONFIG_FILE.exists():
        try:
            with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                config.update(json.load(f))
        except Exception as e:
            print(f"加载配置文件失败: {e}")
    
    return config

def save_config(config):
    """保存配置文件"""
    try:
        with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
    except Exception as e:
        print(f"保存配置文件失败: {e}")

def find_7zip():
    """查找7z可执行文件"""
    # 尝试在PATH中查找
    if sys.platform == "win32":
        exe_names = ["7z.exe", "7z"]
    else:
        exe_names = ["7z", "7zz"]
    
    for exe_name in exe_names:
        try:
            if sys.platform == "win32":
                result = subprocess.run(["where", exe_name], 
                                      capture_output=True, text=True, shell=True)
            else:
                result = subprocess.run(["which", exe_name], 
                                      capture_output=True, text=True)
            
            if result.returncode == 0 and result.stdout.strip():
                return result.stdout.strip().split('\n')[0]
        except:
            continue
    
    # 检查常见安装位置
    common_paths = []
    if sys.platform == "win32":
        common_paths = [
            r"C:\Program Files\7-Zip\7z.exe",
            r"C:\Program Files (x86)\7-Zip\7z.exe",
        ]
    elif sys.platform == "darwin":  # macOS
        common_paths = [
            "/usr/local/bin/7z",
            "/opt/homebrew/bin/7z",
        ]
    else:  # Linux/Unix
        common_paths = [
            "/usr/bin/7z",
            "/usr/local/bin/7z",
        ]
    
    for path in common_paths:
        if os.path.exists(path):
            return path
    
    return None

def extract_with_encoding(zip_file, output_dir=None, encoding="936"):
    """用指定编码解压文件"""
    if not os.path.exists(zip_file):
        print(f"错误: 文件不存在 - {zip_file}")
        return False
    
    config = load_config()
    sevenzip = config.get("sevenzip_path")
    
    # 检查环境变量
    if not sevenzip:
        sevenzip = os.environ.get("GBK_EXTRACT_7Z_PATH")
    
    # 如果配置中没有7z路径，尝试查找
    if not sevenzip or not os.path.exists(sevenzip):
        found_path = find_7zip()
        if found_path:
            sevenzip = found_path
            config["sevenzip_path"] = sevenzip
            save_config(config)
        else:
            # 如果找不到，尝试使用你原来的路径
            if sys.platform == "win32":
                default_path = r"E:\未知\7z\7-Zip\7z.exe"
                if os.path.exists(default_path):
                    sevenzip = default_path
                    print(f"使用默认路径: {sevenzip}")
    
    if not sevenzip or not os.path.exists(sevenzip):
        print("错误: 找不到7z可执行文件")
        print("\n请通过以下方式指定7z路径:")
        print("  1. 运行: python GBK_Extract.py --config")
        print("  2. 设置环境变量 GBK_EXTRACT_7Z_PATH")
        print("  3. 确保7z已在系统PATH中")
        print("  4. 或者将7z安装到默认位置")
        return False
    
    # 确定输出目录
    if not output_dir:
        file_dir = os.path.dirname(zip_file)
        file_name = os.path.splitext(os.path.basename(zip_file))[0]
        # 清理文件名，移除可能不合法的字符
        file_name = re.sub(r'[<>:"/\\|?*]', '', file_name)  # 移除Windows文件名中的非法字符
        file_name = file_name.strip()
        if not file_name:  # 如果文件名变成空，使用默认名
            file_name = "extracted"
        output_dir = os.path.join(file_dir, file_name)
    
    # 如果输出目录不存在，创建它
    os.makedirs(output_dir, exist_ok=True)
    
    # 构建命令 - 使用你原来的格式
    # 你原来的格式是: "7z.exe" x "压缩包.zip" -mcp=936
    # 注意: 参数顺序是: 命令, 归档文件, 然后才是选项
    # 但在7z中，选项可以在归档文件前，也可以在归档文件后
    # 让我们先尝试你的原始格式
    cmd = [sevenzip, "x", zip_file, f"-mcp={encoding}", f"-o{output_dir}", "-y"]
    
    print(f"正在解压: {os.path.basename(zip_file)}")
    print(f"使用编码: {encoding} (GBK代码页)")
    print(f"输出到: {output_dir}")
    print(f"使用7z: {sevenzip}")
    print(f"执行命令: {' '.join(cmd)}")
    
    # 执行解压
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', errors='ignore')
        if result.returncode == 0:
            print("✓ 解压成功！")
            return True
        else:
            print("✗ 解压失败！")
            if result.stdout:
                print("输出信息:")
                print(result.stdout)
            if result.stderr:
                print("错误信息:")
                print(result.stderr)
            
            # 尝试不同的参数格式
            print("\n尝试备用格式1...")
            cmd1 = [sevenzip, "x", zip_file, f"-mcp={encoding}", "-y", f"-o{output_dir}"]
            result1 = subprocess.run(cmd1, capture_output=True, text=True, encoding='utf-8', errors='ignore')
            
            if result1.returncode == 0:
                print("✓ 使用备用格式1解压成功！")
                return True
            
            print("\n尝试备用格式2...")
            cmd2 = [sevenzip, "x", f"-mcp={encoding}", zip_file, f"-o{output_dir}", "-y"]
            result2 = subprocess.run(cmd2, capture_output=True, text=True, encoding='utf-8', errors='ignore')
            
            if result2.returncode == 0:
                print("✓ 使用备用格式2解压成功！")
                return True
            
            print("\n尝试备用格式3（无编码参数）...")
            cmd3 = [sevenzip, "x", zip_file, f"-o{output_dir}", "-y"]
            result3 = subprocess.run(cmd3, capture_output=True, text=True, encoding='utf-8', errors='ignore')
            
            if result3.returncode == 0:
                print("✓ 使用备用格式3解压成功！")
                print("注意: 文件名可能乱码，因为没有指定GBK编码")
                return True
            else:
                print("✗ 所有格式都失败")
                
                # 显示更多调试信息
                print("\n调试信息:")
                print(f"7z路径: {sevenzip}")
                print(f"文件是否存在: {os.path.exists(sevenzip)}")
                print(f"归档文件是否存在: {os.path.exists(zip_file)}")
                print(f"输出目录: {output_dir}")
                return False
                
    except FileNotFoundError:
        print(f"错误: 找不到7z程序: {sevenzip}")
        print("请确保7z已正确安装")
        return False
    except Exception as e:
        print(f"执行错误: {e}")
        return False

def test_7zip_command(sevenzip):
    """测试7z命令的兼容性"""
    if not sevenzip or not os.path.exists(sevenzip):
        return False, "7z路径不存在"
    
    try:
        # 测试7z是否可以运行
        result = subprocess.run([sevenzip, "--help"], capture_output=True, text=True, encoding='utf-8', errors='ignore')
        if result.returncode == 0 or result.returncode == 1:  # 7z --help 返回1
            return True, "7z可用"
        else:
            return False, f"7z返回错误代码: {result.returncode}"
    except Exception as e:
        return False, f"运行7z出错: {e}"

def configure_tool():
    """交互式配置工具"""
    config = load_config()
    
    print("=== GBK解压工具配置 ===")
    print("当前配置:")
    print(f"  7z路径: {config.get('sevenzip_path') or '自动检测'}")
    print(f"  默认编码(代码页): {config.get('encoding', '936')} (936=GBK)")
    print()
    print("常用代码页:")
    print("  936 - GBK (简体中文)")
    print("  950 - Big5 (繁体中文)")
    print("  65001 - UTF-8")
    print("  932 - Shift-JIS (日文)")
    print("  949 - EUC-KR (韩文)")
    
    # 测试当前7z
    sevenzip = config.get("sevenzip_path")
    if sevenzip and os.path.exists(sevenzip):
        status, message = test_7zip_command(sevenzip)
        print(f"当前7z状态: {'✓' if status else '✗'} {message}")
    else:
        print("当前7z状态: ✗ 未找到或未设置")
    
    new_sevenzip = input(f"\n输入7z路径 (留空使用当前: {sevenzip or '自动检测'}): ").strip()
    if new_sevenzip:
        config["sevenzip_path"] = new_sevenzip
        # 测试新路径
        status, message = test_7zip_command(new_sevenzip)
        if status:
            print(f"✓ 7z可用: {message}")
        else:
            print(f"⚠ 警告: 7z可能有问题: {message}")
            confirm = input("是否继续使用此路径? (y/n): ").lower()
            if confirm != 'y':
                print("取消修改7z路径")
                config["sevenzip_path"] = sevenzip
    
    encoding = input(f"\n输入代码页 (留空使用: {config.get('encoding', '936')}): ").strip()
    if encoding:
        config["encoding"] = encoding
    
    save_config(config)
    print("✓ 配置已保存！")

def show_help():
    """显示帮助信息"""
    print("=== GBK编码解压工具 ===")
    print("\n用法:")
    print("  python GBK_Extract.py [选项] [文件]")
    print("\n选项:")
    print("  文件                要解压的文件路径")
    print("  -o, --output DIR    指定输出目录")
    print("  -e, --encoding CODE 指定代码页 (默认: 936, GBK)")
    print("  --config            打开配置向导")
    print("  --test             测试7z命令")
    print("  --info             显示当前配置")
    print("  --help             显示此帮助信息")
    print("\n常用代码页:")
    print("  936  - GBK (简体中文)")
    print("  950  - Big5 (繁体中文)")
    print("  65001 - UTF-8")
    print("\n示例:")
    print("  python GBK_Extract.py archive.zip")
    print("  python GBK_Extract.py archive.zip -o output/")
    print("  python GBK_Extract.py archive.zip -e 936")
    print("  python GBK_Extract.py --config")
    print("\n拖放使用:")
    print("  也可以将文件拖放到此脚本上直接解压")

def show_info():
    """显示当前配置信息"""
    config = load_config()
    print("=== GBK解压工具信息 ===")
    print(f"7z路径: {config.get('sevenzip_path') or '未设置 (自动检测)'}")
    print(f"默认编码(代码页): {config.get('encoding', '936')}")
    print(f"配置文件: {CONFIG_FILE}")
    
    # 测试7z是否存在
    sevenzip = config.get("sevenzip_path")
    if not sevenzip or not os.path.exists(sevenzip):
        found = find_7zip()
        if found:
            print(f"自动检测到7z: {found}")
        else:
            print("警告: 未找到7z可执行文件")
    else:
        print(f"当前7z: {sevenzip}")
        status, message = test_7zip_command(sevenzip)
        print(f"7z状态: {'✓' if status else '✗'} {message}")

def main():
    # 解析命令行参数
    args = sys.argv[1:]
    
    if len(args) == 0:
        # 无参数，显示帮助
        show_help()
        return
    
    # 检查是否是特殊命令
    if args[0] in ["--help", "-h"]:
        show_help()
        return
    elif args[0] in ["--config", "-c"]:
        configure_tool()
        return
    elif args[0] in ["--info", "-i"]:
        show_info()
        return
    elif args[0] in ["--test", "-t"]:
        config = load_config()
        sevenzip = config.get("sevenzip_path")
        if not sevenzip or not os.path.exists(sevenzip):
            sevenzip = find_7zip()
        if sevenzip and os.path.exists(sevenzip):
            print(f"测试7z: {sevenzip}")
            status, message = test_7zip_command(sevenzip)
            print(f"结果: {'✓' if status else '✗'} {message}")
        else:
            print("错误: 找不到7z可执行文件")
        return
    
    # 解析其他参数
    zip_file = None
    output_dir = None
    encoding = "936"  # 默认使用GBK代码页
    
    i = 0
    while i < len(args):
        arg = args[i]
        
        if arg in ["-o", "--output"]:
            if i + 1 < len(args):
                output_dir = args[i + 1]
                i += 1
        elif arg in ["-e", "--encoding"]:
            if i + 1 < len(args):
                encoding = args[i + 1]
                i += 1
        elif not arg.startswith("-"):
            # 不是选项，应该是文件路径
            zip_file = arg
        
        i += 1
    
    if not zip_file:
        print("错误: 未指定要解压的文件")
        show_help()
        return
    
    # 执行解压
    success = extract_with_encoding(zip_file, output_dir, encoding)
    
    # 如果是通过双击或拖放运行，等待用户按键
    if sys.stdin.isatty() and not sys.stdout.isatty():
        input("\n按回车键退出...")

if __name__ == "__main__":
    main()