import re
# 提取指定函数的代码块
def extract_function_body(code, func_name):
    """提取函数 func_name 的函数体"""
    func_pattern = re.compile(r'\b' + func_name + r'\s*\(([^)]*)\)\s*{([^}]*)}')
    match = func_pattern.search(code)
    if match:
        return match.group(2).strip()  # 返回函数体代码
    return None
#解析 for 循环语句并提取循环的次数
#形参for_line指包含for循环条件的字符串
def extract_loop_count(for_line):
    match = re.search(r'for\s*\(\s*[^;]+;\s*([^<>=]+)\s*<\s*(\d+);\s*[^)]+\)', for_line)
    if match:
        start_var, end_value = match.groups()
        try:
            return int(end_value)  # 返回循环次数
        except ValueError:
            print(f"调试信息：无法解析循环次数 {end_value}")
            return 1  # 如果无法解析，返回默认循环 1 次
    return 1

#提取for循环体的代码块（包括嵌套的大括号）
def extract_loop_body(lines, brace_count):
    #loop_body存储for循环体的每一行代码
    loop_body = []
    for line in lines:
        line = line.strip()
        loop_body.append(line)
        brace_count += line.count('{')
        brace_count -= line.count('}')
        if brace_count == 0:
            break
    return "\n".join(loop_body)
