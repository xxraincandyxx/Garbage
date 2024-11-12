def display_function_info(functions):
    output = "函数信息：\n"
    for name, info in functions.items():
        param_str = ", ".join([f"{pname} ({ptype})" for pname, ptype in info["parameters"]]) if info[
                                                                                                    "parameters"] != "无参数" else "无参数"
        output += f"{info['return_type']} {name}()：函数名为 {name}，参数为：{param_str}。\n"
    return output


def display_call_paths(call_paths):
    output = "\n调用路径：\n"
    for condition, path in call_paths.items():
        output += f"{condition} ：{path}\n"
    return output


def display_parameter_relations(parameter_relations):
    # 如果没有相关性参数
    if not parameter_relations:
        return "该代码没有相关性参数"

    # 如果有相关性参数，格式化并返回
    output = "\n相关性参数：\n"
    for func, params in parameter_relations.items():
        for param, related_funcs in params.items():
            related_str = ", ".join([f"<{func_name}(), {var_name}>" for func_name, var_name in related_funcs])
            output += f"<{func}(), {param}> = {{ {related_str} }}\n"
    return output

