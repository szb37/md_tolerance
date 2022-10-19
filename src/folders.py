import os

src_dir = os.path.dirname(os.path.abspath(__file__))
codebase_dir = os.path.abspath(os.path.join(src_dir, os.pardir))
data_dir = os.path.abspath(os.path.join(codebase_dir, 'data'))
safety_vault_dir = os.path.abspath(os.path.join(data_dir, 'safety_vault'))
