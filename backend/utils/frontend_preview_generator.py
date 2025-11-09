def generate_frontend_preview(languages, services, file_details, extract_dir=None):
    """SAFELY preview uploaded HTML files containing 'index' in their name (e.g., index.html, home_index.html)."""
    try:
        import os
        import tempfile

        # ✅ SECURITY: Only allow temporary extract directories
        if not extract_dir or not extract_dir.startswith(tempfile.gettempdir()):
            return '<div style="padding: 20px; text-align: center;"><h3>Security Check Failed</h3><p>Only temp directories are allowed for preview.</p></div>'

        # ✅ FILTER: Only HTML files that contain the word 'index'
        html_files = [
            f for f in file_details
            if f.get('file', '').lower().endswith('.html') and 'index' in f.get('file', '').lower()
        ]

        if not html_files:
            return '<div style="padding: 20px; text-align: center;"><h3>No HTML files with "index" found</h3><p>This project may not have a frontend entry file.</p></div>'

        # ✅ Take the first "index" HTML file
        html_file = html_files[0]
        html_path = os.path.join(extract_dir, html_file['file'])

        # ✅ SECURITY: Prevent directory traversal
        if not os.path.abspath(html_path).startswith(os.path.abspath(extract_dir)):
            return '<div style="padding: 20px; text-align: center;"><h3>Security: Path traversal blocked</h3></div>'

        if os.path.exists(html_path):
            with open(html_path, 'r', encoding='utf-8') as f:
                html_content = f.read()

            # ✅ Render safely within a sandbox-style container
            return f'''
                <div style="border: 1px solid #ddd; border-radius: 8px; overflow: hidden;">
                    <div style="background: #f8f9fa; padding: 10px; border-bottom: 1px solid #ddd; font-weight: bold;">
                        📄 {html_file["file"]} (frontend preview)
                    </div>
                    <iframe srcdoc="{html_content.replace('"', '&quot;')}" style="width:100%;height:600px;border:none;"></iframe>
                </div>
            '''
        else:
            return f'<div style="padding: 20px; text-align: center;"><h3>File not found</h3><p>{html_file["file"]}</p></div>'

    except Exception as e:
        return f'<div style="padding: 20px; text-align: center;"><h3>Error</h3><p>{str(e)}</p></div>'
