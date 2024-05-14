import os
import json
import sys
import autopep8

def load_and_convert(ipynb_file, save_graphs=False):
    '''
    args => ipynb file 
    steps => converting the file to json then then using 'cells' list to get
    1. 'cell_type'
    2. inside 'cell_type' we want to get only the ones that contain 'code' so
        if 'cell_type' == code we take what's inside which is...
    3. 'source' that contains the acutal code in written in a single cells and it's
        a list of strings
    4. extracting file name to save the python file with the same name
    5. saving graphs/output_texts from output (working on it)

    returns => list that contains the all the source code from all cells and file name
    '''
    with open(ipynb_file) as nb:
        data = json.load(nb)

    cells = data['cells']
    source_code_list = []
    output_list = []

    filename = os.path.splitext(os.path.basename(ipynb_file))[0]
    
    for cell in cells:
        if cell['cell_type'] == 'code':
            source_code = ''.join(cell['source'])
            source_code_list.append(source_code)

        output_list += cell['outputs']

    if save_graphs:

        for output in output_list:
            if 'image/png' in output['data']:
                plot = output['data']['image/png']
                

    return source_code_list, filename



def save_py(source_code_list, filename, prettify=False) -> None:
    '''
    args => source code list, file name, prettify code flag
    steps => - create a python file with the same name in ipynb file 
             - loop through the list of srtings (lines of code)
             - check if the line ends with '\n' (new line) then the line is added directly to the code
                string. if not a '\n' will be added
             - check if the user has set prettify to True will pass the code to autopep8 to prettify the code 
                and then it will be written into the file. if False the code will be written as it is
    '''
    dir_path = './convetred/'
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

    print('Converting file .....')

    py_file_path = f'{dir_path}{filename}.py'
    code = ''

    with open(py_file_path, 'w') as py_file:
        for line in source_code_list:
            if line.endswith('\n'):
                code += line
            else:
                code = code + line + '\n'

        if prettify:
            py_file.write(autopep8.fix_code(code))
        else:
            py_file.write(code)

    
    print(f'file {filename}.py has been saved in converted folder')


def main():
    # chcek if the user inserted the right number of args
    if len(sys.argv) < 3:
      ipynb_file = input('enter the ipynb file path please: ')
      prettify_flag = input('do you want to pretty the code? Type 1 for True, 0 for False: ')  
    else:
        ipynb_file = sys.argv[1]
        prettify_flag = sys.argv[2]

    try:
        code, filename = load_and_convert(ipynb_file)
        save_py(code, filename, prettify_flag)
    except:
        print('please make sure that the filepath or extension is correct..')

if __name__ == '__main__':
    print('py it!')
    print('================================')
    main()