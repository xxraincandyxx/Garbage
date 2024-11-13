import logging
from dataclasses import dataclass


logger = logging.getLogger(__name__)


@dataclass
class DOCS_EN:
    _SWITCHER_: str = "切换到中文"
    _WHILE_: str = "While"
    _END_WHILE_: str = ""
    _IF_: str = "If"
    _ELSE_: str = "Else"
    _RETURN_: str = "Return"
    _FUNCTION_: str = "Function"
    _ARGUMENT_: str = "Argument"
    _VARIABLE_: str = "Variable"
    _AND_: str = "And"
    _AND_NOT_: str = "And Not"
    _TYPE_: str = "Type"
    _LOAD_FILE_: str = "Load File"
    _PARSE_CODE_: str = "Parse Code"
    _FUNCTION_NAME_: str = "Function Name"
    _FUNCTION_ARGS_: str = "Function Arguments"
    _FUNCTION_ARGS_TYPE_: str = "Function Arguments Type"
    _FUNCTION_ARGS_VALUE_: str = "Function Arguments Value"
    _FUNCTION_ARGS_VALUE_TYPE_: str = "Function Arguments Value Type"
    _FUNCTION_STATES_: str = "Function States"
    _FUNCTION_REFS_: str = "Function Reference"
    _ARGUMENT_RELAS_: str = "Arguments Relations"
    _NONE_: str = "None"


@dataclass
class DOCS_CN:
    _SWITCHER_: str = "Switch to English"
    _WHILE_: str = "当"
    _END_WHILE_: str = "时"
    _IF_: str = "如果"
    _ELSE_: str = "否则"
    _RETURN_: str = "返回"
    _FUNCTION_: str = "函数"
    _ARGUMENT_: str = "参数"
    _VARIABLE_: str = "变量"
    _AND_: str = "并且"
    _AND_NOT_: str = "并且不"
    _TYPE_: str = "类型"
    _LOAD_FILE_: str = "读取文件"
    _PARSE_CODE_: str = "分析代码"
    _FUNCTION_NAME_: str = "函数名"
    _FUNCTION_ARGS_: str = "函数参数"
    _FUNCTION_ARGS_TYPE_: str = "函数参数类型"
    _FUNCTION_ARGS_VALUE_: str = "函数参数值"
    _FUNCTION_ARGS_VALUE_TYPE_: str = "函数参数值类型"
    _FUNCTION_STATES_: str = "函数信息"
    _FUNCTION_REFS_: str = "函数调用"
    _ARGUMENT_RELAS_: str = "参数调用"
    _NONE_: str = "无"
