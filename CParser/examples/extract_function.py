import re
#忽略非自定义函数
IGNORE_FUNCTIONS = {"printf", "scanf","main","if","else if","else","for","while"}
#函数定义、函数调用、赋值调用函数语句匹配
function_def_pattern = re.compile(r'^\s*(\w+)\s+(\w+)\s*\(([^)]*)\)')
function_call_pattern = re.compile(r'\b(\w+)\s*\(([^)]*)\);?')
assignment_pattern = re.compile(r'(?:\w+\s+)?(\w+)\s*=\s*(\w+)\(([^)]*)\);')# 变量赋值，支持可选数据类型，数据类型属于非捕获组
#提取函数定义
def extract_function_definitions(code):
    #functions为字典
    functions = {}
    for line in code.splitlines():
        match = function_def_pattern.match(line)
        if match:
            return_type, name, params = match.groups()
            if name not in IGNORE_FUNCTIONS:
                #param_list为列表
                param_list = []
                if params.strip():
                    for p in params.split(","):
                        p_split = p.strip().split()
                        if len(p_split) == 2:
                            param_type, param_name = p_split
                            param_list.append((param_name, param_type))
                #functions是外层字典，name是键；它的值是内层字典，有return_type和parameters两种键，嵌套字典
                functions[name] = {
                    "return_type": return_type.strip(),
                    "parameters": param_list if param_list else "无参数"
                }
    print("调试信息：提取的函数定义", functions)  # 调试输出
    return functions
