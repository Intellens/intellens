/**
 * Layered File Architecture Renderer
 * Renders ASCII-style layered architecture with actual file names
 */

function renderLayeredFileArchitecture(container, layeredData) {
    if (!layeredData || layeredData.style !== 'layered_architecture') {
        container.innerHTML = '<p>No layered architecture data available</p>';
        return;
    }

    const { title, ascii_diagram, layers, layer_summary } = layeredData;
    
    container.innerHTML = `
        <div class="layered-file-architecture">
            <div class="arch-header">
                <h3>${title}</h3>
                <p class="arch-subtitle">File Organization by Architecture Layers</p>
            </div>
            
            <div class="ascii-diagram-container">
                <pre class="ascii-diagram">${ascii_diagram}</pre>
            </div>
            
            <div class="layer-details" id="layer-details"></div>
        </div>
    `;

    // Render layer details
    renderLayerDetails(container.querySelector('#layer-details'), layers, layer_summary);
}

function renderLayerDetails(container, layers, layer_summary) {
    const layerOrder = ["frontend", "backend", "data", "config"];
    
    container.innerHTML = `
        <h4>Layer Details</h4>
        <div class="layer-cards">
            ${layerOrder.map(layerKey => {
                const layer = layers[layerKey];
                const summary = layer_summary[layerKey];
                
                if (!layer.files || layer.files.length === 0) {
                    return '';
                }
                
                return `
                    <div class="layer-card" data-layer="${layerKey}">
                        <div class="layer-card-header">
                            <span class="layer-icon">${layer.icon}</span>
                            <div class="layer-info">
                                <h5>${layer.name}</h5>
                                <p class="layer-description">${layer.description}</p>
                            </div>
                            <div class="layer-stats">
                                <span class="file-count">${layer.files.length} files</span>
                                <span class="complexity ${summary.complexity.toLowerCase()}">${summary.complexity}</span>
                            </div>
                        </div>
                        
                        <div class="layer-files">
                            ${layer.files.slice(0, 5).map(file => `
                                <div class="file-item">
                                    <div class="file-name">${file.name}</div>
                                    <div class="file-tech">
                                        ${file.languages.map(lang => `<span class="tech-tag lang">${lang}</span>`).join('')}
                                        ${file.services.map(service => `<span class="tech-tag service">${service}</span>`).join('')}
                                    </div>
                                </div>
                            `).join('')}
                            
                            ${layer.files.length > 5 ? `
                                <div class="more-files">
                                    <button class="show-more-btn" onclick="toggleMoreFiles('${layerKey}')">
                                        Show ${layer.files.length - 5} more files
                                    </button>
                                    <div class="hidden-files" id="more-files-${layerKey}" style="display: none;">
                                        ${layer.files.slice(5).map(file => `
                                            <div class="file-item">
                                                <div class="file-name">${file.name}</div>
                                                <div class="file-tech">
                                                    ${file.languages.map(lang => `<span class="tech-tag lang">${lang}</span>`).join('')}
                                                    ${file.services.map(service => `<span class="tech-tag service">${service}</span>`).join('')}
                                                </div>
                                            </div>
                                        `).join('')}
                                    </div>
                                </div>
                            ` : ''}
                        </div>
                        
                        ${summary.languages.length > 0 || summary.services.length > 0 ? `
                            <div class="layer-summary">
                                ${summary.languages.length > 0 ? `
                                    <div class="summary-section">
                                        <strong>Languages:</strong> ${summary.languages.join(', ')}
                                    </div>
                                ` : ''}
                                ${summary.services.length > 0 ? `
                                    <div class="summary-section">
                                        <strong>Technologies:</strong> ${summary.services.join(', ')}
                                    </div>
                                ` : ''}
                            </div>
                        ` : ''}
                    </div>
                `;
            }).filter(card => card !== '').join('')}
        </div>
    `;
}

function toggleMoreFiles(layerKey) {
    const hiddenFiles = document.getElementById(`more-files-${layerKey}`);
    const button = hiddenFiles.previousElementSibling;
    
    if (hiddenFiles.style.display === 'none') {
        hiddenFiles.style.display = 'block';
        button.textContent = 'Show less';
    } else {
        hiddenFiles.style.display = 'none';
        const fileCount = hiddenFiles.children.length;
        button.textContent = `Show ${fileCount} more files`;
    }
}

// Add CSS styles
const layeredFileStyles = `
<style>
.layered-file-architecture {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    max-width: 1200px;
    margin: 0 auto;
    padding: 20px;
}

.arch-header {
    text-align: center;
    margin-bottom: 30px;
}

.arch-header h3 {
    margin: 0 0 10px 0;
    color: #333;
    font-size: 24px;
}

.arch-subtitle {
    color: #666;
    font-style: italic;
    margin: 0;
}

.ascii-diagram-container {
    background: #f8f9fa;
    border: 1px solid #e9ecef;
    border-radius: 8px;
    padding: 20px;
    margin-bottom: 30px;
    overflow-x: auto;
}

.ascii-diagram {
    font-family: 'Courier New', monospace;
    font-size: 14px;
    line-height: 1.2;
    margin: 0;
    color: #333;
    white-space: pre;
}

.layer-details h4 {
    margin: 0 0 20px 0;
    color: #333;
    font-size: 20px;
}

.layer-cards {
    display: grid;
    gap: 20px;
}

.layer-card {
    border: 1px solid #e9ecef;
    border-radius: 12px;
    background: white;
    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    overflow: hidden;
}

.layer-card-header {
    display: flex;
    align-items: center;
    padding: 20px;
    background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
    border-bottom: 1px solid #e9ecef;
}

.layer-icon {
    font-size: 32px;
    margin-right: 15px;
}

.layer-info {
    flex: 1;
}

.layer-info h5 {
    margin: 0 0 5px 0;
    color: #333;
    font-size: 18px;
}

.layer-description {
    margin: 0;
    color: #666;
    font-size: 14px;
}

.layer-stats {
    display: flex;
    flex-direction: column;
    align-items: flex-end;
    gap: 5px;
}

.file-count {
    font-weight: bold;
    color: #007bff;
    font-size: 14px;
}

.complexity {
    padding: 4px 8px;
    border-radius: 12px;
    font-size: 12px;
    font-weight: bold;
    text-transform: uppercase;
}

.complexity.low {
    background: #d4edda;
    color: #155724;
}

.complexity.medium {
    background: #fff3cd;
    color: #856404;
}

.complexity.high {
    background: #f8d7da;
    color: #721c24;
}

.layer-files {
    padding: 20px;
}

.file-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 12px 0;
    border-bottom: 1px solid #f1f3f4;
}

.file-item:last-child {
    border-bottom: none;
}

.file-name {
    font-family: 'Courier New', monospace;
    font-size: 13px;
    color: #333;
    flex: 1;
    margin-right: 15px;
    word-break: break-all;
}

.file-tech {
    display: flex;
    gap: 5px;
    flex-wrap: wrap;
}

.tech-tag {
    padding: 2px 6px;
    border-radius: 10px;
    font-size: 10px;
    font-weight: bold;
    text-transform: uppercase;
}

.tech-tag.lang {
    background: #e3f2fd;
    color: #1565c0;
}

.tech-tag.service {
    background: #f3e5f5;
    color: #7b1fa2;
}

.more-files {
    margin-top: 15px;
    padding-top: 15px;
    border-top: 1px solid #f1f3f4;
}

.show-more-btn {
    background: #f8f9fa;
    border: 1px solid #dee2e6;
    border-radius: 6px;
    padding: 8px 16px;
    font-size: 12px;
    color: #495057;
    cursor: pointer;
    transition: all 0.2s ease;
}

.show-more-btn:hover {
    background: #e9ecef;
    border-color: #adb5bd;
}

.hidden-files {
    margin-top: 15px;
}

.layer-summary {
    padding: 15px 20px;
    background: #f8f9fa;
    border-top: 1px solid #e9ecef;
}

.summary-section {
    margin-bottom: 8px;
    font-size: 13px;
    color: #495057;
}

.summary-section:last-child {
    margin-bottom: 0;
}

.summary-section strong {
    color: #333;
}
</style>
`;

// Inject styles
if (!document.querySelector('#layered-file-styles')) {
    const styleElement = document.createElement('div');
    styleElement.id = 'layered-file-styles';
    styleElement.innerHTML = layeredFileStyles;
    document.head.appendChild(styleElement);
}

// Export for use
window.renderLayeredFileArchitecture = renderLayeredFileArchitecture;
window.toggleMoreFiles = toggleMoreFiles;