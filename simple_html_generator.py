"""Simple HTML generator without using Flock agent."""

import asyncio
import os
from datetime import datetime
from settings import APP_SETTINGS


def create_html_newspaper_template(title: str, short_summary: str, research_content: str, key_points: list) -> str:
    """Create a newspaper-style HTML template with the provided content."""
    
    # Convert key points to HTML list items
    key_points_html = '\n'.join([f'<li>{point}</li>' for point in key_points])
    
    # Split research content into paragraphs for better formatting
    paragraphs = research_content.split('\n\n')
    research_paragraphs_html = '\n'.join([f'<p>{para.strip()}</p>' for para in paragraphs if para.strip()])
    
    # Get current date
    current_date = datetime.now().strftime("%B %d, %Y")
    
    html_template = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Times New Roman', Times, serif;
            line-height: 1.6;
            color: #333;
            background-color: #f8f9fa;
        }}
        
        .newspaper {{
            max-width: 900px;
            margin: 20px auto;
            background: white;
            box-shadow: 0 0 20px rgba(0,0,0,0.1);
            border-radius: 8px;
            overflow: hidden;
        }}
        
        .masthead {{
            background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
            color: white;
            text-align: center;
            padding: 30px 20px;
            border-bottom: 3px solid #154a80;
        }}
        
        .masthead h1 {{
            font-size: 2.5rem;
            font-weight: bold;
            letter-spacing: 2px;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }}
        
        .masthead .tagline {{
            font-size: 1rem;
            opacity: 0.9;
            font-style: italic;
        }}
        
        .article-header {{
            background: #f1f3f4;
            padding: 30px;
            border-bottom: 1px solid #e0e0e0;
        }}
        
        .article-title {{
            font-size: 2.2rem;
            font-weight: bold;
            color: #1e3c72;
            margin-bottom: 15px;
            line-height: 1.3;
        }}
        
        .article-summary {{
            font-size: 1.2rem;
            color: #555;
            font-weight: 500;
            background: #e8f4fd;
            padding: 20px;
            border-left: 4px solid #2a5298;
            border-radius: 0 5px 5px 0;
            margin-bottom: 20px;
        }}
        
        .byline {{
            font-size: 0.9rem;
            color: #666;
            margin-bottom: 10px;
        }}
        
        .date {{
            font-size: 0.9rem;
            color: #888;
        }}
        
        .article-content {{
            padding: 30px;
        }}
        
        .content-section {{
            margin-bottom: 30px;
        }}
        
        .content-section h2 {{
            font-size: 1.5rem;
            color: #1e3c72;
            margin-bottom: 15px;
            border-bottom: 2px solid #e0e0e0;
            padding-bottom: 5px;
        }}
        
        .content-section p {{
            margin-bottom: 15px;
            text-align: justify;
            font-size: 1rem;
            line-height: 1.7;
        }}
        
        .key-points {{
            background: #f8f9fa;
            border: 1px solid #e0e0e0;
            border-radius: 8px;
            padding: 25px;
            margin: 25px 0;
        }}
        
        .key-points h3 {{
            font-size: 1.3rem;
            color: #1e3c72;
            margin-bottom: 15px;
            display: flex;
            align-items: center;
        }}
        
        .key-points h3::before {{
            content: "📋";
            margin-right: 10px;
            font-size: 1.2rem;
        }}
        
        .key-points ul {{
            list-style: none;
            margin-left: 0;
        }}
        
        .key-points li {{
            margin-bottom: 10px;
            padding-left: 25px;
            position: relative;
            font-size: 1rem;
        }}
        
        .key-points li::before {{
            content: "▶";
            color: #2a5298;
            font-weight: bold;
            position: absolute;
            left: 0;
        }}
        
        .footer {{
            background: #f1f3f4;
            padding: 20px 30px;
            border-top: 1px solid #e0e0e0;
            text-align: center;
            color: #666;
            font-size: 0.9rem;
        }}
        
        .powered-by {{
            margin-top: 10px;
            font-style: italic;
        }}
        
        @media (max-width: 768px) {{
            .newspaper {{
                margin: 10px;
                border-radius: 0;
            }}
            
            .masthead h1 {{
                font-size: 2rem;
            }}
            
            .article-title {{
                font-size: 1.8rem;
            }}
            
            .article-header, .article-content {{
                padding: 20px;
            }}
        }}
    </style>
</head>
<body>
    <div class="newspaper">
        <header class="masthead">
            <h1>AI Research Herald</h1>
            <div class="tagline">Intelligent Insights • Comprehensive Analysis • Future Forward</div>
        </header>
        
        <div class="article-header">
            <h1 class="article-title">{title}</h1>
            <div class="article-summary">{short_summary}</div>
            <div class="byline">By AI Research Agent</div>
            <div class="date">{current_date}</div>
        </div>
        
        <main class="article-content">
            <div class="content-section">
                <h2>Comprehensive Analysis</h2>
                {research_paragraphs_html}
            </div>
            
            <div class="key-points">
                <h3>Key Insights</h3>
                <ul>
                    {key_points_html}
                </ul>
            </div>
        </main>
        
        <footer class="footer">
            <div>© 2025 AI Research Herald. All rights reserved.</div>
            <div class="powered-by">Powered by Flock AI Agent Framework & Azure OpenAI</div>
        </footer>
    </div>
</body>
</html>"""
    
    return html_template


async def generate_simple_html(title: str, short_summary: str, research_content: str, key_points: list) -> dict:
    """Generate HTML without using the agent - just the template."""
    
    html_content = create_html_newspaper_template(title, short_summary, research_content, key_points)
    
    # Clean filename
    clean_filename = "".join(c for c in title if c.isalnum() or c in (' ', '-', '_')).rstrip()
    clean_filename = clean_filename.replace(' ', '_').lower()
    if not clean_filename.endswith('.html'):
        clean_filename += '.html'
    
    return {
        'html_content': html_content,
        'file_path': clean_filename,
        'css_classes': ['newspaper', 'article-title', 'key-points', 'masthead', 'article-header', 'article-content'],
        'is_mobile_responsive': True
    }


async def save_html_article(html_content: str, filename: str, output_dir: str = None) -> str:
    """Save HTML content to a file and return the full path."""
    # Use configured output directory if not specified
    if output_dir is None:
        output_dir = APP_SETTINGS.output_dir
    
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Clean filename
    clean_filename = "".join(c for c in filename if c.isalnum() or c in (' ', '-', '_')).rstrip()
    if not clean_filename.endswith('.html'):
        clean_filename += '.html'
    
    file_path = os.path.join(output_dir, clean_filename)
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    return os.path.abspath(file_path)
