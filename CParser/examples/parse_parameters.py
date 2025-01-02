### 4. `parse_parameters.py`
import re
from utils import extract_function_body, extract_loop_count, extract_loop_body

import logging


logger = logging.getLogger(__name__)


# 解析参数相关性函数
def parse_parameter_relations(code, functions):
    logger.info(f"arg: {functions}")
    # relations字典
    relations = {}
    main_start = code.find("int main")
    # main函数主体代码
    main_block = code[main_start:]
    # 存储变量赋值关系
    variable_assignments = {}
    # 存储当前条件
    current_conditions = []
    
    # Function Name; Whitespace; 
    function_call_pattern = re.compile(r'\b(\w+)\s*\(([^)]*)\)?;?')  # 修改正则，允许参数为空
    # Optional Identifier; Vairable Name; Function Name; Arguments;
    assignment_pattern = re.compile(r'(?:\w+\s+)?(\w+)\s*=\s*(\w+)\(([^)]*)\);')  # 变量赋值，支持可选数据类型
    # 标记是否发现相关性
    found_relevance = False

    for line in main_block.splitlines():
        line = line.strip()
        # 空行或者注释行跳过
        if not line or line.startswith("//"):
            continue

        logger.info(f"line: {line}")
        
        # 解析 if 语句
        if_match = re.search(r'if\s*\(([^)]+)\)', line)
        elif_match = re.search(r'else\s+if\s*\(([^)]+)\)', line)
        else_match = re.match(r'else\b', line)

        # 当匹配到 if 语句时
        if if_match:
            current_conditions.append(if_match.group(1).strip())

        # 当匹配到 else if 语句时
        if elif_match:
            current_conditions.append(elif_match.group(1).strip())

        # 当匹配到 else 语句时
        if else_match:
            current_conditions.append("else")

        # 解析变量赋值及函数调用
        assignment_match = assignment_pattern.match(line)
        if assignment_match:
            var_name, func_name, args = assignment_match.groups()
            var_name = var_name.strip()
            func_name = func_name.strip()
            # 只有在函数存在的情况下，才会继续执行后面的赋值操作
            if func_name in functions:
                variable_assignments.setdefault(var_name, {}).setdefault(tuple(current_conditions), []).append(func_name)

        func_call_match = function_call_pattern.match(line)
        if func_call_match:
            func_name, args = func_call_match.groups()
            func_name = func_name.strip()
            if func_name in functions:
                # 对拆分出来的每个参数 arg 进行 strip()，去掉两端的空格，使用 if arg.strip() 条件来过滤掉空字符串
                args_list = [arg.strip() for arg in args.split(',') if arg.strip()]
                for arg in args_list:
                    if arg in variable_assignments:
                        sources = variable_assignments[arg]
                        for conditions, funcs in sources.items():
                            for source_func in funcs:
                                # 将来源函数和当前函数的参数添加到 relations 字典中
                                relations.setdefault(func_name, {}).setdefault("value", []).append(
                                    (source_func, "return value"))  # 这里修改为 "return value"
                                found_relevance = True

        # 调用 extract_function_body 提取嵌套函数体
        for func_name in functions:
            if func_name in line:
                logger.info(f"function name: {func_name}")
                function_body = extract_function_body(code, func_name)
                logger.info(f"function body: \n{function_body}")
                # 分析函数体中的赋值和函数调用关系
                assign_func_call_match = re.search(r'(\w+)\s*=\s*(\w+)\s*\(([^)]*)\)', function_body)
                if assign_func_call_match:
                    var_name, called_func, args = assign_func_call_match.groups()
                    print(f"调试信息：在函数 {func_name} 中发现赋值：{var_name} = {called_func}({args})")
                    # 将赋值操作和函数调用的关系存入 relations
                    relations.setdefault(func_name, {}).setdefault(var_name, []).append(
                        (called_func, "return value"))  # 修改为 "return value"
                    found_relevance = True

        # 如果是 for 循环，解析循环次数
        if line.startswith("for"):
            loop_count = extract_loop_count(line)
            print(f"调试信息：循环次数为 {loop_count}")
            loop_body = extract_loop_body(main_block.splitlines(), 0)
            print(f"调试信息：循环体为：\n{loop_body}")

    # 解析结束后，去重参数关系中的函数调用
    for func in relations:
        for param in relations[func]:
            relations[func][param] = list(set(relations[func][param]))

    # 输出提示信息：如果没有发现任何相关性参数
    if not found_relevance:
        print("该代码没有相关性参数")
    return relations








