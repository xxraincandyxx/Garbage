import re
from utils import extract_function_body,extract_loop_count, extract_loop_body

# 函数调用路径解析
def parse_call_paths(code, functions):
    #block存储传入的函数代码块，function_name表示正在解析的函数名
    #递归解析函数调用
    def parse_inner_calls(block, function_name):
        #存储函数内部的调用路径
        inner_call_paths = []
        #将传入的函数体按行分割
        lines = block.splitlines()
        brace_count = 0
        i = 0
        print(f"调试信息：开始解析函数 {function_name} 的内部调用")  # 调试输出

        while i < len(lines):
            line = lines[i].strip()
            # 跳过空行或注释行
            if not line or line.startswith("//"):
                i += 1
                continue

            # 更新 brace_count
            brace_count += line.count('{') - line.count('}')

            # 检查 `for` 循环结构
            if line.startswith("for"):
                # 解析 for 循环语句并提取循环的次数
                loop_times = extract_loop_count(line)
                # 提取for循环体的代码块（包括嵌套的大括号）
                loop_body = extract_loop_body(lines[i:], brace_count)
                # 递归解析循环体内部调用,将嵌套调用的函数体存入loop_calls列表中，运用了深度优先搜索思想
                loop_calls = parse_inner_calls(loop_body, function_name)
                # 将循环体中的调用按次数重复
                inner_call_paths.extend(loop_calls * loop_times)
                i += len(loop_body.splitlines())
                continue

            # 检查函数调用，将function_name和functions字典里所有函数名作对比，防止递归调用自身
            for func in functions.keys():
                if func != function_name and re.search(r'\b' + func + r'\s*\(', line):  # 避免递归调用自身
                    inner_call_paths.append(f"{func}()")
                    print(f"调试信息：在函数 {function_name} 中发现函数调用 {func}")  # 调试输出
                    # 如果调用的函数内部还有调用，递归解析
                    #提取调用的内嵌函数体
                    inner_block = extract_function_body(code, func)
                    if inner_block:  # 确保内嵌函数体提取成功
                        print(f"调试信息：提取到函数 {func} 的代码块：\n{inner_block}")  # 调试输出
                        inner_calls = parse_inner_calls(inner_block, func)
                        inner_call_paths.extend(inner_calls)
            # 处理下一行
            i += 1

        return inner_call_paths #返回嵌套函数调用路径，包含for循环

    main_start = code.find("int main")
    main_block = code[main_start:]
    call_paths = {}
    lines = main_block.splitlines()
    i = 0

    # 初始化 main 函数路径
    main_path = ["main()"]
    additional_calls = []  # 用于记录在条件语句结束后的通用调用

    # 正则表达式，匹配行内带有缩进的条件语句
    if_pattern = re.compile(r'\s*if\s*\(([^)]+)\)\s*{?')  # 匹配 if 条件，允许后跟 {
    else_if_pattern = re.compile(r'\s*(?:}\s*)?else\s+if\s*\(\s*([^)]+)\s*\)\s*{?')  # 允许前面有 } 的 else if
    else_pattern = re.compile(r'\s*}?\s*else\b\s*{?')  # 匹配 else，允许 } 和 {

    end_of_condition_block = False  # 标志条件语句结束
    added_additional_calls = False  # 防止重复添加 additional_calls
    previous_if_ended = False  # 标记上一个 if 语句是否结束

    while i < len(lines):
        line = lines[i].strip()
        # 处理空行或注释行
        if not line or line.startswith("//"):
            i += 1
            continue

        # 使用正则表达式匹配条件语句
        if_match = if_pattern.match(line)
        else_if_match = else_if_pattern.match(line)
        else_match = else_pattern.match(line)

        # 处理 if、else if 和 else 条件
        if if_match or else_if_match or else_match:
            if if_match:
                condition = if_match.group(1).strip()
            elif else_if_match:
                condition = else_if_match.group(1).strip()
            else:
                condition = "else"  # 特别处理 else 条件

            # 如果前一个 `if` 语句已结束，重新生成路径
            if previous_if_ended:
                current_path = []  # 重置当前路径
                previous_if_ended = False  # 重置标志

            # 初始化条件路径
            current_path = []
            call_paths[f"condition == {condition}" ] = current_path

            # 手动初始化 brace_count
            brace_count = line.count('{') - line.count('}')
            i += 1
            has_function_call = False  # 检查该条件下是否有函数调用

            # 如果没有 {，检查下一行是否有 {
            if brace_count <= 0 and i < len(lines):
                next_line = lines[i].strip()
                if next_line.startswith('{'):
                    brace_count += 1
                    i += 1

            # 处理条件块内的代码
            while brace_count > 0 and i < len(lines):
                line = lines[i].strip()
                # 手动扫描字符，更新 brace_count
                for char in line:
                    if char == '{':
                        brace_count += 1
                    elif char == '}':
                        brace_count -= 1

                # 记录函数调用
                for func in functions.keys():
                    if func != "main" and re.search(r'\b' + func + r'\s*\(', line):
                        call_paths[f"condition == {condition}"].append(f"{func}()")
                        has_function_call = True
                        print(f"调试信息：在条件 {condition} 中发现函数调用 {func}")  # 调试输出

                        # 如果调用的函数内部还有调用，递归解析
                        inner_block = extract_function_body(code, func)
                        if inner_block:  # 确保内嵌函数体提取成功
                            print(f"调试信息：提取到函数 {func} 的代码块：\n{inner_block}")  # 调试输出
                            inner_calls = parse_inner_calls(inner_block, func)
                            call_paths[f"condition == {condition}"].extend(inner_calls)

                i += 1

            # 如果当前条件语句下没有函数调用，就不需要打印调用路径
            if not has_function_call:
                del call_paths[condition]
            end_of_condition_block = True
            previous_if_ended = True  # 当前 if 语句已结束
            print(f"调试信息：条件 {condition} 路径完成")  # 调试输出

        else:
            # 如果当前行是一个独立的 '}'，可能是结束了一个条件块
            if line == "}":
                end_of_condition_block = True
                i += 1
                continue
            # 检查在 main 函数内的一般函数调用，作为条件语句之后的通用调用
            for func in functions.keys():
                if re.search(r'\b' + func + r'\s*\(', line):
                    if func not in additional_calls:  # 确保不重复添加
                        additional_calls.append(f"{func}()")
                        print(f"调试信息：main函数中的一般调用路径添加函数 {func}")  # 调试输出

                    # 如果 main 调用的函数内部还有调用，递归解析
                    inner_block = extract_function_body(code, func)
                    if inner_block:
                        print(f"调试信息：提取到函数 {func} 的代码块：\n{inner_block}")  # 调试输出
                        inner_calls = parse_inner_calls(inner_block, func)
                        additional_calls.extend(inner_calls)
            # 如果条件语句已经结束，且有后续的通用调用，将其添加到所有条件路径
            if end_of_condition_block and additional_calls:
                for key in call_paths.keys():
                    call_paths[key] += additional_calls  # 将实际检测到的通用调用添加到路径中
                    end_of_condition_block = False  # 重置标志
                    added_additional_calls = True  # 防止重复添加 additional_calls
            # 如果 main 函数内没有条件语句且有一般调用，直接添加
            if not call_paths and additional_calls:
                call_paths["main()"] = additional_calls
            i += 1

    # 格式化调用路径
    formatted_paths = {key: "main() -> " + " -> ".join(path) for key, path in call_paths.items()}
    print("调试信息：最终的调用路径", formatted_paths)  # 调试输出
    return formatted_paths



