import os
import re
from collections import defaultdict

def detect_language_from_content(content, filename):
    """Detect programming language from file content and patterns."""
    # Check file extension first for definitive matches
    ext = os.path.splitext(filename)[1].lower()
    ext_map = {
        '.py': 'Python', '.js': 'JavaScript', '.ts': 'TypeScript',
        '.java': 'Java', '.c': 'C', '.cpp': 'C++', '.go': 'Go',
        '.rs': 'Rust', '.rb': 'Ruby', '.php': 'PHP', '.cs': 'C#',
        '.sh': 'Shell', '.sql': 'SQL', '.html': 'HTML', '.css': 'CSS',
        '.yml': 'YAML', '.yaml': 'YAML', '.json': 'JSON'
    }
    
    # If we have a clear extension match, use it
    if ext in ext_map:
        return [ext_map[ext]]
    
    # Only use content patterns for files without clear extensions
    patterns = {
        'Python': [r'import\s+\w+', r'def\s+\w+\s*\(', r'if\s+__name__\s*==\s*["\']__main__["\']'],
        'JavaScript': [r'function\s+\w+\s*\(', r'var\s+\w+\s*=', r'console\.log'],
        'TypeScript': [r'interface\s+\w+', r'type\s+\w+\s*=', r'export\s+interface'],
        'Java': [r'public\s+class\s+\w+', r'import\s+java\.'],
        'Shell': [r'#!/bin/bash', r'#!/bin/sh']
    }
    
    # Return only the first match to avoid multiple detections
    for lang, lang_patterns in patterns.items():
        for pattern in lang_patterns:
            if re.search(pattern, content, re.MULTILINE):
                return [lang]
    
    return []

def detect_language_from_shebang(content):
    """Detect language from shebang line."""
    shebang_map = {
        'python': 'Python', 'node': 'JavaScript', 'bash': 'Shell',
        'sh': 'Shell', 'ruby': 'Ruby', 'php': 'PHP', 'perl': 'Perl'
    }
    
    first_line = content.split('\n')[0] if content else ''
    if first_line.startswith('#!'):
        for key, lang in shebang_map.items():
            if key in first_line.lower():
                return lang
    return None

def auto_detect_languages(folder_path):
    """Automatically detect all programming languages in the project."""
    languages = defaultdict(int)
    
    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.startswith('.'):
                continue
                
            full_path = os.path.join(root, file)
            detected_lang = None
            
            try:
                with open(full_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                
                # Check shebang first
                shebang_lang = detect_language_from_shebang(content)
                if shebang_lang:
                    detected_lang = shebang_lang
                else:
                    # Detect from content patterns (returns max 1 language now)
                    detected_langs = detect_language_from_content(content, file)
                    if detected_langs:
                        detected_lang = detected_langs[0]  # Take only the first match
                
                # Count only one language per file
                if detected_lang:
                    languages[detected_lang] += 1
                    
            except:
                continue
    
    return dict(languages)