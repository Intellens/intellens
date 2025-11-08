import os
import re
from collections import defaultdict

def detect_language_from_content(content, filename):
    """Detect programming language from file content and patterns."""
    # Language indicators in content
    patterns = {
        'Python': [r'import\s+\w+', r'def\s+\w+', r'class\s+\w+', r'if\s+__name__\s*=='],
        'JavaScript': [r'function\s+\w+', r'var\s+\w+', r'let\s+\w+', r'const\s+\w+', r'=>'],
        'TypeScript': [r'interface\s+\w+', r'type\s+\w+', r':\s*\w+\s*=', r'export\s+'],
        'Java': [r'public\s+class', r'import\s+java\.', r'public\s+static\s+void\s+main'],
        'C++': [r'#include\s*<', r'using\s+namespace', r'std::', r'cout\s*<<'],
        'C': [r'#include\s*<stdio\.h>', r'int\s+main\s*\(', r'printf\s*\('],
        'Go': [r'package\s+\w+', r'func\s+\w+', r'import\s*\(', r'go\s+\w+'],
        'Rust': [r'fn\s+\w+', r'let\s+mut', r'use\s+\w+', r'impl\s+\w+'],
        'Ruby': [r'def\s+\w+', r'class\s+\w+', r'require\s+', r'puts\s+'],
        'PHP': [r'<\?php', r'function\s+\w+', r'\$\w+', r'echo\s+'],
        'C#': [r'using\s+System', r'namespace\s+\w+', r'public\s+class', r'Console\.'],
        'Shell': [r'#!/bin/bash', r'#!/bin/sh', r'echo\s+', r'if\s*\[\s*'],
        'SQL': [r'SELECT\s+', r'FROM\s+', r'WHERE\s+', r'INSERT\s+INTO'],
        'HTML': [r'<html>', r'<div>', r'<script>', r'<!DOCTYPE'],
        'CSS': [r'\{\s*\w+:', r'@media', r'\.[\w-]+\s*\{', r'#[\w-]+\s*\{'],
        'YAML': [r'^\s*\w+:\s*', r'^\s*-\s+\w+'],
        'JSON': [r'^\s*\{', r'"\w+":\s*', r'^\s*\[']
    }
    
    detected = []
    for lang, lang_patterns in patterns.items():
        for pattern in lang_patterns:
            if re.search(pattern, content, re.MULTILINE | re.IGNORECASE):
                detected.append(lang)
                break
    
    return detected

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
            
            try:
                with open(full_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                
                # Check shebang first
                shebang_lang = detect_language_from_shebang(content)
                if shebang_lang:
                    languages[shebang_lang] += 1
                    continue
                
                # Detect from content patterns
                detected_langs = detect_language_from_content(content, file)
                for lang in detected_langs:
                    languages[lang] += 1
                
                # Fallback: simple extension mapping for common cases
                ext = os.path.splitext(file)[1].lower()
                ext_map = {
                    '.py': 'Python', '.js': 'JavaScript', '.ts': 'TypeScript',
                    '.java': 'Java', '.c': 'C', '.cpp': 'C++', '.go': 'Go',
                    '.rs': 'Rust', '.rb': 'Ruby', '.php': 'PHP', '.cs': 'C#'
                }
                if ext in ext_map and not detected_langs:
                    languages[ext_map[ext]] += 1
                    
            except:
                continue
    
    return dict(languages)