from fastmcp import FastMCP
import os

mcp = FastMCP('File system mcp server')


@mcp.tool
def move_file(source: str, destination: str) -> str:
    """
    Move a file from source to destination.
    :param source: The path of the file to move.
    :param destination: The path where the file should be moved.
    :return: A message indicating the result of the operation.
    """
    import os
    try:
        os.rename(source, destination)
        return f"File moved from {source} to {destination}"
    except Exception as e:
        return str(e)
    

@mcp.tool
def list_files(directory: str) -> list:
    """
    List all files in the specified directory.
    :param directory: The path of the directory to list files from.
    :return: A list of files in the directory or an error message.
    """

    try:
        return os.listdir(directory)
    except Exception as e:
        return str(e)
    
@mcp.tool
def create_directory(path:str, directory: str) -> str:
    """
    Create a new directory at the specified path.
    :param path: The path where the directory should be created.
    :param directory: The name of the directory to create.
    :return: A message indicating the result of the operation.
    """
    try:
        os.makedirs(os.path.join(path, directory), exist_ok=True)
        return f"Directory {directory} created at {path}"
    except Exception as e:
        return str(e)
    

if __name__ == "__main__":
    mcp.run(transport='sse', port=3000, host='127.0.0.1')
