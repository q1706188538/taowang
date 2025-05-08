#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
简单的HTTP服务器，用于本地测试H5游戏
使用固定端口9003
"""

import http.server
import socketserver
import webbrowser
import os
import socket
import sys

class MyHttpRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate')
        return super().end_headers()

    def log_message(self, format, *args):
        # 减少日志输出
        if 'GET /favicon.ico' not in args[0]:
            return super().log_message(format, *args)

def find_free_port(start_port=8000, max_port=8100):
    """查找可用端口"""
    for port in range(start_port, max_port):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(('', port))
                return port
        except OSError:
            continue
    return None

def start_server():
    # 使用固定端口9003
    PORT = 9003

    # 创建服务器
    handler = MyHttpRequestHandler

    try:
        httpd = socketserver.TCPServer(("", PORT), handler)

        # 输出服务器信息
        print(f"服务器已启动在 http://localhost:{PORT}")
        print("按 Ctrl+C 停止服务器")

        # 启动服务器
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n服务器已停止")
        if 'httpd' in locals():
            httpd.server_close()
    except OSError as e:
        if e.errno == 10048:  # 端口已被占用
            print(f"错误: 端口 {PORT} 已被占用，请关闭占用该端口的应用后重试。")
        else:
            print(f"启动服务器时出错: {e}")
    except Exception as e:
        print(f"启动服务器时出错: {e}")

if __name__ == "__main__":
    start_server()
