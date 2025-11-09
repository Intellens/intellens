/**
 * Layered Architecture Renderer
 * Renders connected architecture layers with proper flow visualization
 */

function renderLayeredArchitecture(container, architectureData) {
    if (!architectureData || architectureData.style !== 'layered_architecture') {
        return renderFallbackDiagram(container, architectureData);
    }

    const { layers, connections, processing_order, title } = architectureData;
    
    container.innerHTML = `
        <div class="layered-architecture">
            <div class="arch-header">
                <h3>${title}</h3>
                <p class="arch-subtitle">Connected Architecture Layers with Processing Flow</p>
            </div>
            <div class="layers-container" id="layers-container"></div>
            <div class="processing-workflow" id="processing-workflow"></div>
        </div>
    `;

    const layersContainer = container.querySelector('#layers-container');
    const workflowContainer = container.querySelector('#processing-workflow');

    // Render layers in processing order
    renderArchitectureLayers(layersContainer, processing_order, connections);
    
    // Render processing workflow
    renderProcessingWorkflow(workflowContainer, architectureData.workflow_steps);
}

function renderArchitectureLayers(container, processing_order, connections) {
    container.innerHTML = '';
    
    processing_order.forEach(([layerName, layerInfo], index) => {
        if (layerInfo.services.length === 0) return;
        
        const layerDiv = document.createElement('div');
        layerDiv.className = 'architecture-layer';
        layerDiv.style.backgroundColor = layerInfo.color;
        
        layerDiv.innerHTML = `
            <div class="layer-header">
                <div class="layer-order">${layerInfo.order}</div>
                <div class="layer-info">
                    <h4 class="layer-title">${layerInfo.name}</h4>
                    <p class="layer-description">${layerInfo.description}</p>
                </div>
            </div>
            <div class="layer-services">
                ${layerInfo.services.map(service => `
                    <div class="service-component" data-service-id="${service.id}">
                        <div class="service-icon">${service.icon}</div>
                        <div class="service-name">${service.name}</div>
                        <div class="service-category">${service.category}</div>
                    </div>
                `).join('')}
            </div>
        `;
        
        container.appendChild(layerDiv);
        
        // Add connection arrows between layers
        if (index < processing_order.length - 1) {
            const connectionDiv = document.createElement('div');
            connectionDiv.className = 'layer-connection';
            
            const relevantConnections = connections.filter(conn => 
                layerInfo.services.some(s => s.id === conn.source) &&
                processing_order[index + 1][1].services.some(s => s.id === conn.target)
            );
            
            connectionDiv.innerHTML = `
                <div class="connection-arrow">↓</div>
                <div class="connection-details">
                    ${relevantConnections.map(conn => `
                        <div class="connection-item">
                            <span class="connection-type">${conn.type}</span>
                            <span class="connection-desc">${conn.description}</span>
                        </div>
                    `).join('')}
                </div>
            `;
            
            container.appendChild(connectionDiv);
        }
    });
    
    // Add service-to-service connection lines
    setTimeout(() => drawServiceConnections(container, connections), 100);
}

function drawServiceConnections(container, connections) {
    // Remove existing connection lines
    container.querySelectorAll('.connection-line').forEach(line => line.remove());
    
    connections.forEach(connection => {
        const sourceElement = container.querySelector(`[data-service-id="${connection.source}"]`);
        const targetElement = container.querySelector(`[data-service-id="${connection.target}"]`);
        
        if (sourceElement && targetElement) {
            const line = createConnectionLine(sourceElement, targetElement, connection);
            container.appendChild(line);
        }
    });
}

function createConnectionLine(sourceEl, targetEl, connection) {
    const sourceRect = sourceEl.getBoundingClientRect();
    const targetRect = targetEl.getBoundingClientRect();
    const containerRect = sourceEl.closest('.layers-container').getBoundingClientRect();
    
    const line = document.createElement('div');
    line.className = 'connection-line';
    line.setAttribute('data-connection-type', connection.type);
    
    const sourceX = sourceRect.left + sourceRect.width / 2 - containerRect.left;
    const sourceY = sourceRect.bottom - containerRect.top;
    const targetX = targetRect.left + targetRect.width / 2 - containerRect.left;
    const targetY = targetRect.top - containerRect.top;
    
    const length = Math.sqrt(Math.pow(targetX - sourceX, 2) + Math.pow(targetY - sourceY, 2));
    const angle = Math.atan2(targetY - sourceY, targetX - sourceX) * 180 / Math.PI;
    
    line.style.cssText = `
        position: absolute;
        left: ${sourceX}px;
        top: ${sourceY}px;
        width: ${length}px;
        height: 2px;
        background: linear-gradient(to right, #007bff, #0056b3);
        transform-origin: 0 0;
        transform: rotate(${angle}deg);
        z-index: 1;
        opacity: 0.7;
    `;
    
    // Add connection label
    const label = document.createElement('div');
    label.className = 'connection-label';
    label.textContent = connection.type;
    label.style.cssText = `
        position: absolute;
        left: ${sourceX + (targetX - sourceX) / 2}px;
        top: ${sourceY + (targetY - sourceY) / 2}px;
        background: white;
        padding: 2px 6px;
        border-radius: 4px;
        font-size: 10px;
        border: 1px solid #007bff;
        z-index: 2;
        transform: translate(-50%, -50%);
    `;
    
    const container = sourceEl.closest('.layers-container');
    container.appendChild(label);
    
    return line;
}

function renderProcessingWorkflow(container, workflowSteps) {
    if (!workflowSteps || workflowSteps.length === 0) {
        container.innerHTML = '<p>No processing workflow available</p>';
        return;
    }
    
    container.innerHTML = `
        <h4>Processing Workflow</h4>
        <div class="workflow-steps">
            ${workflowSteps.map(step => `
                <div class="workflow-step-detailed">
                    <div class="step-number">${step.step}</div>
                    <div class="step-content">
                        <h5>${step.title}</h5>
                        <p class="step-description">${step.description}</p>
                        <div class="step-services">
                            <strong>Services:</strong> ${step.services.join(', ')}
                        </div>
                        <div class="step-details">${step.processing_details}</div>
                    </div>
                </div>
            `).join('')}
        </div>
    `;
}

function renderFallbackDiagram(container, data) {
    // Fallback to existing diagram renderer
    if (window.renderAwsTechDiagram) {
        const diagram = window.renderAwsTechDiagram(data);
        container.innerHTML = '';
        container.appendChild(diagram);
    } else {
        container.innerHTML = '<p>Architecture diagram not available</p>';
    }
}

// Add CSS styles
const layeredArchStyles = `
<style>
.layered-architecture {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    max-width: 1000px;
    margin: 0 auto;
}

.arch-header {
    text-align: center;
    margin-bottom: 30px;
}

.arch-subtitle {
    color: #666;
    font-style: italic;
    margin: 10px 0;
}

.layers-container {
    position: relative;
    padding: 20px;
    background: #fafafa;
    border-radius: 8px;
    margin-bottom: 30px;
}

.architecture-layer {
    border: 2px solid #ddd;
    border-radius: 12px;
    margin: 20px 0;
    padding: 20px;
    background: white;
    box-shadow: 0 4px 8px rgba(0,0,0,0.1);
}

.layer-header {
    display: flex;
    align-items: center;
    margin-bottom: 15px;
}

.layer-order {
    width: 40px;
    height: 40px;
    border-radius: 50%;
    background: #007bff;
    color: white;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: bold;
    margin-right: 15px;
}

.layer-info {
    flex: 1;
}

.layer-title {
    margin: 0 0 5px 0;
    color: #333;
    font-size: 18px;
}

.layer-description {
    margin: 0;
    color: #666;
    font-size: 14px;
}

.layer-services {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 15px;
}

.service-component {
    border: 1px solid #e0e0e0;
    border-radius: 8px;
    padding: 15px;
    background: white;
    text-align: center;
    transition: all 0.3s ease;
    cursor: pointer;
}

.service-component:hover {
    border-color: #007bff;
    box-shadow: 0 2px 8px rgba(0,123,255,0.2);
    transform: translateY(-2px);
}

.service-icon {
    font-size: 32px;
    margin-bottom: 10px;
}

.service-name {
    font-weight: bold;
    color: #333;
    margin-bottom: 5px;
}

.service-category {
    font-size: 12px;
    color: #666;
    text-transform: uppercase;
}

.layer-connection {
    text-align: center;
    margin: 15px 0;
    position: relative;
}

.connection-arrow {
    font-size: 24px;
    color: #007bff;
    font-weight: bold;
}

.connection-details {
    margin-top: 10px;
}

.connection-item {
    display: inline-block;
    margin: 0 10px;
    padding: 5px 10px;
    background: #f8f9fa;
    border-radius: 15px;
    font-size: 12px;
    border: 1px solid #e9ecef;
}

.connection-type {
    font-weight: bold;
    color: #007bff;
}

.connection-desc {
    color: #666;
    margin-left: 5px;
}

.connection-line {
    pointer-events: none;
}

.connection-label {
    pointer-events: none;
    white-space: nowrap;
}

.processing-workflow {
    background: white;
    border-radius: 8px;
    padding: 20px;
    border: 1px solid #ddd;
}

.workflow-steps {
    margin-top: 15px;
}

.workflow-step-detailed {
    display: flex;
    align-items: flex-start;
    margin: 20px 0;
    padding: 15px;
    border-left: 4px solid #007bff;
    background: #f8f9fa;
    border-radius: 0 8px 8px 0;
}

.workflow-step-detailed .step-number {
    width: 30px;
    height: 30px;
    border-radius: 50%;
    background: #007bff;
    color: white;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: bold;
    margin-right: 15px;
    flex-shrink: 0;
}

.step-content {
    flex: 1;
}

.step-content h5 {
    margin: 0 0 8px 0;
    color: #333;
}

.step-description {
    margin: 0 0 10px 0;
    color: #666;
    font-size: 14px;
}

.step-services {
    margin: 8px 0;
    font-size: 13px;
    color: #495057;
}

.step-details {
    font-size: 12px;
    color: #6c757d;
    font-style: italic;
    margin-top: 8px;
}
</style>
`;

// Inject styles
if (!document.querySelector('#layered-arch-styles')) {
    const styleElement = document.createElement('div');
    styleElement.id = 'layered-arch-styles';
    styleElement.innerHTML = layeredArchStyles;
    document.head.appendChild(styleElement);
}

// Export for use
window.renderLayeredArchitecture = renderLayeredArchitecture;