def generate_frontend_preview(languages, services, file_details):
    """Generate a simple HTML preview of what the frontend might look like."""
    
    # Analyze project type
    has_web = 'JavaScript' in languages or 'HTML' in languages or 'CSS' in languages
    has_api = any('api' in s.lower() or 'fastapi' in s.lower() or 'flask' in s.lower() for s in services.keys())
    has_data = any('database' in s.lower() or 'sql' in s.lower() for s in services.keys())
    
    if not has_web and not has_api:
        return None
    
    # Generate preview HTML based on detected patterns
    if has_api and has_data:
        return generate_dashboard_preview()
    elif has_api:
        return generate_api_interface_preview()
    elif has_web:
        return generate_web_app_preview()
    else:
        return generate_simple_interface_preview()

def generate_dashboard_preview():
    """Generate a data dashboard preview."""
    return """
    <div style="font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px;">
        <header style="background: #2c3e50; color: white; padding: 20px; border-radius: 8px; margin-bottom: 20px;">
            <h1 style="margin: 0;">Project Dashboard</h1>
            <p style="margin: 5px 0 0 0; opacity: 0.8;">Data Analytics & Management</p>
        </header>
        
        <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 15px; margin-bottom: 20px;">
            <div style="background: #3498db; color: white; padding: 20px; border-radius: 8px; text-align: center;">
                <h3 style="margin: 0;">1,234</h3>
                <p style="margin: 5px 0 0 0;">Total Records</p>
            </div>
            <div style="background: #27ae60; color: white; padding: 20px; border-radius: 8px; text-align: center;">
                <h3 style="margin: 0;">98.5%</h3>
                <p style="margin: 5px 0 0 0;">Uptime</p>
            </div>
            <div style="background: #e74c3c; color: white; padding: 20px; border-radius: 8px; text-align: center;">
                <h3 style="margin: 0;">5</h3>
                <p style="margin: 5px 0 0 0;">Active Users</p>
            </div>
        </div>
        
        <div style="background: white; border: 1px solid #ddd; border-radius: 8px; padding: 20px;">
            <h3>Data Visualization</h3>
            <div style="height: 200px; background: #f8f9fa; border-radius: 4px; display: flex; align-items: center; justify-content: center; color: #666;">
                📊 Interactive Charts & Graphs
            </div>
        </div>
    </div>
    """

def generate_api_interface_preview():
    """Generate an API testing interface preview."""
    return """
    <div style="font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px;">
        <header style="background: #34495e; color: white; padding: 20px; border-radius: 8px; margin-bottom: 20px;">
            <h1 style="margin: 0;">API Interface</h1>
            <p style="margin: 5px 0 0 0; opacity: 0.8;">REST API Testing & Documentation</p>
        </header>
        
        <div style="background: white; border: 1px solid #ddd; border-radius: 8px; padding: 20px; margin-bottom: 15px;">
            <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 15px;">
                <span style="background: #27ae60; color: white; padding: 4px 8px; border-radius: 4px; font-size: 12px;">GET</span>
                <code style="background: #f8f9fa; padding: 8px; border-radius: 4px; flex: 1;">/api/data</code>
                <button style="background: #3498db; color: white; border: none; padding: 8px 16px; border-radius: 4px; cursor: pointer;">Send</button>
            </div>
            <div style="background: #f8f9fa; padding: 15px; border-radius: 4px; font-family: monospace; font-size: 12px;">
                {<br>
                &nbsp;&nbsp;"status": "success",<br>
                &nbsp;&nbsp;"data": [...],<br>
                &nbsp;&nbsp;"count": 42<br>
                }
            </div>
        </div>
        
        <div style="background: white; border: 1px solid #ddd; border-radius: 8px; padding: 20px;">
            <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 15px;">
                <span style="background: #e67e22; color: white; padding: 4px 8px; border-radius: 4px; font-size: 12px;">POST</span>
                <code style="background: #f8f9fa; padding: 8px; border-radius: 4px; flex: 1;">/api/upload</code>
                <button style="background: #3498db; color: white; border: none; padding: 8px 16px; border-radius: 4px; cursor: pointer;">Send</button>
            </div>
            <textarea style="width: 100%; height: 80px; border: 1px solid #ddd; border-radius: 4px; padding: 10px; font-family: monospace;" placeholder='{"name": "example", "data": "..."}'></textarea>
        </div>
    </div>
    """

def generate_web_app_preview():
    """Generate a web application preview."""
    return """
    <div style="font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px;">
        <nav style="background: #2c3e50; color: white; padding: 15px 20px; border-radius: 8px; margin-bottom: 20px; display: flex; justify-content: space-between; align-items: center;">
            <h2 style="margin: 0;">MyApp</h2>
            <div style="display: flex; gap: 20px;">
                <a href="#" style="color: white; text-decoration: none;">Home</a>
                <a href="#" style="color: white; text-decoration: none;">About</a>
                <a href="#" style="color: white; text-decoration: none;">Contact</a>
            </div>
        </nav>
        
        <main style="background: white; border: 1px solid #ddd; border-radius: 8px; padding: 30px; text-align: center;">
            <h1 style="color: #2c3e50; margin-bottom: 20px;">Welcome to the Application</h1>
            <p style="color: #666; margin-bottom: 30px; line-height: 1.6;">
                This web application provides an intuitive interface for users to interact with the system.
                Features include data management, user authentication, and real-time updates.
            </p>
            
            <div style="display: flex; gap: 15px; justify-content: center; margin-bottom: 30px;">
                <button style="background: #3498db; color: white; border: none; padding: 12px 24px; border-radius: 6px; cursor: pointer;">Get Started</button>
                <button style="background: transparent; color: #3498db; border: 2px solid #3498db; padding: 12px 24px; border-radius: 6px; cursor: pointer;">Learn More</button>
            </div>
            
            <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 20px; margin-top: 40px;">
                <div style="padding: 20px; border: 1px solid #eee; border-radius: 8px;">
                    <h3 style="color: #2c3e50;">⚡ Fast</h3>
                    <p style="color: #666; font-size: 14px;">Optimized performance for quick response times</p>
                </div>
                <div style="padding: 20px; border: 1px solid #eee; border-radius: 8px;">
                    <h3 style="color: #2c3e50;">🔒 Secure</h3>
                    <p style="color: #666; font-size: 14px;">Built with security best practices in mind</p>
                </div>
                <div style="padding: 20px; border: 1px solid #eee; border-radius: 8px;">
                    <h3 style="color: #2c3e50;">📱 Responsive</h3>
                    <p style="color: #666; font-size: 14px;">Works seamlessly across all devices</p>
                </div>
            </div>
        </main>
    </div>
    """

def generate_simple_interface_preview():
    """Generate a simple interface preview."""
    return """
    <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px;">
        <div style="background: white; border: 1px solid #ddd; border-radius: 8px; padding: 30px; text-align: center;">
            <h1 style="color: #2c3e50; margin-bottom: 20px;">Application Interface</h1>
            <p style="color: #666; margin-bottom: 30px;">Simple and clean user interface for application interaction</p>
            
            <form style="max-width: 400px; margin: 0 auto;">
                <input type="text" placeholder="Enter data..." style="width: 100%; padding: 12px; border: 1px solid #ddd; border-radius: 6px; margin-bottom: 15px;">
                <textarea placeholder="Additional information..." style="width: 100%; height: 100px; padding: 12px; border: 1px solid #ddd; border-radius: 6px; margin-bottom: 20px; resize: vertical;"></textarea>
                <button type="submit" style="background: #3498db; color: white; border: none; padding: 12px 30px; border-radius: 6px; cursor: pointer; width: 100%;">Submit</button>
            </form>
        </div>
    </div>
    """