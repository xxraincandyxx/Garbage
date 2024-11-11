import tkinter as tk
from tkinter import filedialog, scrolledtext
from extract_function import extract_function_definitions
from parse_calls import parse_call_paths
from parse_parameters import parse_parameter_relations
from display import display_function_info,display_call_paths,display_parameter_relations
#在点击“分析代码”按钮时执行
def analyze_code():
    #获取从滚动文本框第一行第一列到最后一行最后一列的所有文本内容，并将其作为一个字符串返回
    code = text_area.get("1.0", tk.END)
    #调用extract_function_definitions函数进行函数定义分析
    functions = extract_function_definitions(code)
    #调用parse_call_paths函数进行调用路径分析
    call_paths = parse_call_paths(code, functions)
    #调用parse_parameter_relations函数进行相关性参数分析
    parameter_relations = parse_parameter_relations(code, functions)
    #展示结果result
    result = ""
    if var_function_info.get():
        result += display_function_info(functions)
    if var_call_paths.get():
        result += display_call_paths(call_paths)
    if var_parameter_relations.get():
        result += display_parameter_relations(parameter_relations)
    #将文本框的状态设置为可编辑
    result_text.configure(state='normal')
    #清空文本框中的所有内容
    result_text.delete("1.0", tk.END)
    #将新的结果内容插入到文本框中
    result_text.insert(tk.END, result)
    #再次将文本框设置为只读状态（disabled），以防止用户修改显示的分析结果
    result_text.configure(state='disabled')
#load_file() 函数，功能是从文件选择对话框中打开一个文件，并将文件内容加载到 text_area 组件中（即一个文本框）
def load_file():
    filepath = filedialog.askopenfilename(filetypes=[("C Files", "*.c"), ("Text Files", "*.txt"), ("All Files", "*.*")])
    if not filepath:
        return
    try:
        with open(filepath, "r") as file:
            code = file.read()
            text_area.delete("1.0", tk.END)
            text_area.insert(tk.END, code)
    except Exception as e:
        print(f"Error loading file: {e}")

root = tk.Tk()
root.title("代码分析工具")

frame = tk.Frame(root)
frame.pack(pady=10)

text_area = scrolledtext.ScrolledText(frame, wrap=tk.WORD, width=80, height=25, font=("Arial", 12))
text_area.grid(row=0, column=0, columnspan=4, padx=10, pady=5)

load_button = tk.Button(frame, text="加载文件", command=load_file)
load_button.grid(row=1, column=0, padx=5, pady=5)

analyze_button = tk.Button(frame, text="分析代码", command=analyze_code)
analyze_button.grid(row=1, column=1, padx=5, pady=5)

var_function_info = tk.BooleanVar(value=True)
var_call_paths = tk.BooleanVar(value=True)
var_parameter_relations = tk.BooleanVar(value=True)

tk.Checkbutton(frame, text="提取函数信息", variable=var_function_info).grid(row=1, column=2, padx=5, pady=5)
tk.Checkbutton(frame, text="解析调用路径", variable=var_call_paths).grid(row=1, column=3, padx=5, pady=5)
tk.Checkbutton(frame, text="解析相关性参数", variable=var_parameter_relations).grid(row=2, column=0, columnspan=2, padx=5, pady=5)

result_text = scrolledtext.ScrolledText(frame, wrap=tk.WORD, width=80, height=20, font=("Arial", 12), state='disabled')
result_text.grid(row=3, column=0, columnspan=4, padx=10, pady=5)
#程序运行，直到用户关闭窗口。
root.mainloop()

