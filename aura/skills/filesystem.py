# aura/skills/filesystem.py
import os
import subprocess
import platform
import shutil
from pathlib import Path
import json
import re
from datetime import datetime

class AdvancedFileSystem:
    """Comprehensive file operations with voice command optimization"""
    
    def __init__(self):
        self.os_type = platform.system()
        self.common_locations = {
            'desktop': os.path.expanduser('~/Desktop'),
            'documents': os.path.expanduser('~/Documents'),
            'downloads': os.path.expanduser('~/Downloads'),
            'pictures': os.path.expanduser('~/Pictures'),
            'videos': os.path.expanduser('~/Videos'),
            'music': os.path.expanduser('~/Music'),
            'home': os.path.expanduser('~'),
            'current': os.getcwd()
        }
        
    def resolve_path(self, path_input: str) -> Path:
        """Intelligent path resolution with voice-friendly shortcuts"""
        if not path_input:
            return Path(os.getcwd())
            
        path_input = path_input.strip().strip('"').strip("'")
        
        # Handle common location shortcuts
        for location, actual_path in self.common_locations.items():
            if path_input.lower().startswith(location):
                remaining_path = path_input[len(location):].lstrip('/')
                if remaining_path:
                    return Path(actual_path) / remaining_path
                return Path(actual_path)
        
        # Expand user paths
        path_input = os.path.expanduser(path_input)
        
        # Convert to absolute path if relative
        if not os.path.isabs(path_input):
            path_input = os.path.join(os.getcwd(), path_input)
            
        return Path(path_input)
    
    def create_file(self, filename: str, content: str = "") -> dict:
        """Create a new file with optional content"""
        try:
            file_path = self.resolve_path(filename)
            
            # Create parent directories if they don't exist
            file_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Create the file
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
                
            return {
                "status": "success",
                "message": f"✅ Created '{file_path.name}' at {file_path.parent}",
                "path": str(file_path)
            }
            
        except Exception as e:
            return {
                "status": "error",
                "message": f"❌ Failed to create file: {str(e)}"
            }
    
    def read_file(self, filename: str, lines: int = None) -> dict:
        """Read file contents with optional line limit"""
        try:
            file_path = self.resolve_path(filename)
            
            if not file_path.exists():
                return {
                    "status": "error",
                    "message": f"❌ File '{filename}' not found"
                }
                
            if not file_path.is_file():
                return {
                    "status": "error", 
                    "message": f"❌ '{filename}' is not a file"
                }
            
            # Check file size for safety
            file_size = file_path.stat().st_size
            if file_size > 10 * 1024 * 1024:  # 10MB limit
                return {
                    "status": "warning",
                    "message": f"⚠️ File '{file_path.name}' is large ({file_size//1024//1024}MB). Reading first 100 lines...",
                    "content": self._read_file_lines(file_path, 100)
                }
            
            try:
                content = file_path.read_text(encoding='utf-8')
                
                # Limit output for voice response
                if lines:
                    content_lines = content.split('\n')[:lines]
                    content = '\n'.join(content_lines)
                elif len(content) > 1000:  # Limit for voice readability
                    content = content[:1000] + "..."
                    
                return {
                    "status": "success",
                    "message": f"📄 {file_path.name}:",
                    "content": content,
                    "path": str(file_path)
                }
                
            except UnicodeDecodeError:
                return {
                    "status": "error",
                    "message": f"❌ '{file_path.name}' appears to be a binary file"
                }
                
        except Exception as e:
            return {
                "status": "error",
                "message": f"❌ Error reading file: {str(e)}"
            }
    
    def _read_file_lines(self, file_path: Path, max_lines: int) -> str:
        """Read specific number of lines from file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = []
                for i, line in enumerate(f):
                    if i >= max_lines:
                        break
                    lines.append(line.rstrip())
                return '\n'.join(lines)
        except:
            return "Could not read file content"
    
    def edit_file(self, filename: str, content: str = None, append: bool = False) -> dict:
        """Edit file - either replace content or append to it"""
        try:
            file_path = self.resolve_path(filename)
            
            if not file_path.exists():
                # Create new file if it doesn't exist
                return self.create_file(filename, content or "")
            
            if content is not None:
                mode = 'a' if append else 'w'
                with open(file_path, mode, encoding='utf-8') as f:
                    if append:
                        f.write('\n' + content)
                    else:
                        f.write(content)
                        
                action = "appended to" if append else "updated"
                return {
                    "status": "success",
                    "message": f"✅ Successfully {action} '{file_path.name}'",
                    "path": str(file_path)
                }
            else:
                # Open file in system editor
                return self.open_file(filename, edit_mode=True)
                
        except Exception as e:
            return {
                "status": "error",
                "message": f"❌ Error editing file: {str(e)}"
            }
    
    def delete_file(self, filename: str, force: bool = False) -> dict:
        """Delete file or directory with safety checks"""
        try:
            file_path = self.resolve_path(filename)
            
            if not file_path.exists():
                return {
                    "status": "error",
                    "message": f"❌ '{filename}' not found"
                }
            
            # Safety check for important directories
            important_dirs = [str(Path.home()), "/", "C:\\", "/usr", "/System"]
            if str(file_path) in important_dirs and not force:
                return {
                    "status": "error",
                    "message": f"🛡️ Cannot delete system directory '{file_path.name}' for safety"
                }
            
            if file_path.is_file():
                file_path.unlink()
                return {
                    "status": "success",
                    "message": f"✅ Deleted file '{file_path.name}'"
                }
            elif file_path.is_dir():
                shutil.rmtree(file_path)
                return {
                    "status": "success", 
                    "message": f"✅ Deleted directory '{file_path.name}' and all contents"
                }
                
        except Exception as e:
            return {
                "status": "error",
                "message": f"❌ Error deleting: {str(e)}"
            }
    
    def open_file(self, filename: str, edit_mode: bool = False) -> dict:
        """Open file with system default application or editor"""
        try:
            file_path = self.resolve_path(filename)
            
            if not file_path.exists():
                return {
                    "status": "error",
                    "message": f"❌ '{filename}' not found"
                }
            
            if edit_mode:
                # Open in text editor
                editors = self._get_system_editors()
                for editor in editors:
                    try:
                        if isinstance(editor, list):
                            subprocess.Popen(editor + [str(file_path)])
                        else:
                            subprocess.Popen([editor, str(file_path)])
                        return {
                            "status": "success",
                            "message": f"✏️ Opening '{file_path.name}' in editor"
                        }
                    except:
                        continue
                        
                return {
                    "status": "error",
                    "message": "❌ No text editor found"
                }
            else:
                # Open with system default
                if self.os_type == "Windows":
                    os.startfile(str(file_path))
                elif self.os_type == "Darwin":
                    subprocess.Popen(["open", str(file_path)])
                else:
                    subprocess.Popen(["xdg-open", str(file_path)])
                    
                return {
                    "status": "success",
                    "message": f"📂 Opening '{file_path.name}'"
                }
                
        except Exception as e:
            return {
                "status": "error",
                "message": f"❌ Error opening file: {str(e)}"
            }
    
    def _get_system_editors(self) -> list:
        """Get available text editors for the current system"""
        if self.os_type == "Windows":
            return ["notepad", "code", "notepad++"]
        elif self.os_type == "Darwin":
            return ["code", ["open", "-a", "TextEdit"], "nano", "vim"]
        else:
            return ["code", "gedit", "nano", "vim"]
    
    def list_files(self, directory: str = ".", pattern: str = None, include_hidden: bool = False) -> dict:
        """List files in directory with optional pattern filtering"""
        try:
            dir_path = self.resolve_path(directory)
            
            if not dir_path.exists():
                return {
                    "status": "error",
                    "message": f"❌ Directory '{directory}' not found"
                }
                
            if not dir_path.is_dir():
                return {
                    "status": "error",
                    "message": f"❌ '{directory}' is not a directory"
                }
            
            # Get directory contents
            items = []
            for item in dir_path.iterdir():
                if not include_hidden and item.name.startswith('.'):
                    continue
                    
                if pattern and not re.search(pattern, item.name, re.IGNORECASE):
                    continue
                    
                item_info = {
                    "name": item.name,
                    "type": "directory" if item.is_dir() else "file",
                    "size": item.stat().st_size if item.is_file() else None,
                    "modified": datetime.fromtimestamp(item.stat().st_mtime).strftime("%Y-%m-%d %H:%M")
                }
                items.append(item_info)
            
            # Sort items: directories first, then files
            items.sort(key=lambda x: (x["type"] == "file", x["name"].lower()))
            
            # Format output for voice
            if not items:
                message = f"📁 '{dir_path.name}' is empty"
            else:
                files = [item for item in items if item["type"] == "file"]
                dirs = [item for item in items if item["type"] == "directory"]
                
                message = f"📁 '{dir_path.name}' contains:"
                if dirs:
                    message += f"\n📂 {len(dirs)} folders: {', '.join([d['name'] for d in dirs[:5]])}"
                    if len(dirs) > 5:
                        message += f" and {len(dirs) - 5} more"
                if files:
                    message += f"\n📄 {len(files)} files: {', '.join([f['name'] for f in files[:5]])}"
                    if len(files) > 5:
                        message += f" and {len(files) - 5} more"
            
            return {
                "status": "success",
                "message": message,
                "items": items,
                "path": str(dir_path)
            }
            
        except Exception as e:
            return {
                "status": "error",
                "message": f"❌ Error listing directory: {str(e)}"
            }
    
    def copy_file(self, source: str, destination: str) -> dict:
        """Copy file or directory to destination"""
        try:
            src_path = self.resolve_path(source)
            dst_path = self.resolve_path(destination)
            
            if not src_path.exists():
                return {
                    "status": "error",
                    "message": f"❌ Source '{source}' not found"
                }
            
            # Create destination parent directories
            dst_path.parent.mkdir(parents=True, exist_ok=True)
            
            if src_path.is_file():
                shutil.copy2(src_path, dst_path)
                return {
                    "status": "success",
                    "message": f"✅ Copied '{src_path.name}' to '{dst_path.parent.name}'"
                }
            elif src_path.is_dir():
                shutil.copytree(src_path, dst_path)
                return {
                    "status": "success",
                    "message": f"✅ Copied directory '{src_path.name}' to '{dst_path.parent.name}'"
                }
                
        except Exception as e:
            return {
                "status": "error",
                "message": f"❌ Error copying: {str(e)}"
            }
    
    def move_file(self, source: str, destination: str) -> dict:
        """Move/rename file or directory"""
        try:
            src_path = self.resolve_path(source)
            dst_path = self.resolve_path(destination)
            
            if not src_path.exists():
                return {
                    "status": "error",
                    "message": f"❌ Source '{source}' not found"
                }
            
            # Create destination parent directories
            dst_path.parent.mkdir(parents=True, exist_ok=True)
            
            shutil.move(str(src_path), str(dst_path))
            return {
                "status": "success",
                "message": f"✅ Moved '{src_path.name}' to '{dst_path.parent.name}'"
            }
            
        except Exception as e:
            return {
                "status": "error",
                "message": f"❌ Error moving: {str(e)}"
            }
    
    def search_files(self, directory: str, filename_pattern: str, content_pattern: str = None) -> dict:
        """Search for files by name and optionally content"""
        try:
            dir_path = self.resolve_path(directory)
            
            if not dir_path.exists():
                return {
                    "status": "error",
                    "message": f"❌ Directory '{directory}' not found"
                }
            
            matches = []
            
            # Search recursively
            for file_path in dir_path.rglob(filename_pattern):
                if file_path.is_file():
                    match_info = {
                        "name": file_path.name,
                        "path": str(file_path.relative_to(dir_path)),
                        "size": file_path.stat().st_size,
                        "modified": datetime.fromtimestamp(file_path.stat().st_mtime).strftime("%Y-%m-%d %H:%M")
                    }
                    
                    # Optional content search
                    if content_pattern:
                        try:
                            content = file_path.read_text(encoding='utf-8')
                            if re.search(content_pattern, content, re.IGNORECASE):
                                match_info["content_match"] = True
                                matches.append(match_info)
                        except:
                            continue  # Skip files that can't be read as text
                    else:
                        matches.append(match_info)
            
            if not matches:
                return {
                    "status": "info",
                    "message": f"🔍 No files matching '{filename_pattern}' found in '{dir_path.name}'"
                }
            
            message = f"🔍 Found {len(matches)} files matching '{filename_pattern}':"
            for match in matches[:5]:  # Limit output for voice
                message += f"\n📄 {match['name']} ({match['path']})"
            
            if len(matches) > 5:
                message += f"\n... and {len(matches) - 5} more files"
            
            return {
                "status": "success",
                "message": message,
                "matches": matches
            }
            
        except Exception as e:
            return {
                "status": "error",
                "message": f"❌ Search error: {str(e)}"
            }

# Legacy functions for backward compatibility
def open_path(params=None):
    fs = AdvancedFileSystem()
    path = (params or {}).get("path", "").strip()
    result = fs.open_file(path)
    return result["message"]

def list_dir(params=None):
    fs = AdvancedFileSystem()
    path = (params or {}).get("path", ".")
    result = fs.list_files(path)
    return result["message"]
