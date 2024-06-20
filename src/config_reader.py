def read_config(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    
    config = {}
    urls = []
    
    for line in lines:
        line = line.strip()
        if line.startswith("email="):
            config['email'] = line.split('=', 1)[1]
        elif line.startswith("password="):
            config['password'] = line.split('=', 1)[1]
        else:
            urls.append(line)
    
    return config, urls
