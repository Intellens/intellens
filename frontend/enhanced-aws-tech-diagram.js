/**
 * Enhanced AWS Tech Diagram with Connections
 * Keeps the original style but adds connection lines between services
 */

function renderAwsTechDiagramWithConnections(diagram) {
    const container = document.createElement('div');
    container.className = 'aws-tech-diagram-enhanced';
    
    // Create the original AWS tech diagram
    const originalDiagram = renderAwsTechDiagram(diagram);
    container.appendChild(originalDiagram);
    
    // Add connections if they exist
    if (diagram.connections && diagram.connections.length > 0) {
        setTimeout(() => {
            addConnectionLines(container, diagram.connections);
        }, 100);
    }
    
    return container;
}

function addConnectionLines(container, connections) {
    // Create connections overlay
    const connectionsOverlay = document.createElement('div');
    connectionsOverlay.className = 'connections-overlay';
    connectionsOverlay.style.cssText = `
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        pointer-events: none;
        z-index: 10;
    `;
    
    // Make container relative positioned
    container.style.position = 'relative';
    
    connections.forEach(connection => {
        const sourceElement = container.querySelector(`[data-service-id="${connection.source}"]`);
        const targetElement = container.querySelector(`[data-service-id="${connection.target}"]`);
        
        if (sourceElement && targetElement) {
            const line = createConnectionLine(sourceElement, targetElement, connection, container);
            connectionsOverlay.appendChild(line);
        }
    });
    
    container.appendChild(connectionsOverlay);
    
    // Add connection legend
    addConnectionLegend(container, connections);
}

function createConnectionLine(sourceEl, targetEl, connection, container) {
    const containerRect = container.getBoundingClientRect();
    const sourceRect = sourceEl.getBoundingClientRect();
    const targetRect = targetEl.getBoundingClientRect();
    
    const sourceX = sourceRect.left + sourceRect.width / 2 - containerRect.left;
    const sourceY = sourceRect.top + sourceRect.height / 2 - containerRect.top;
    const targetX = targetRect.left + targetRect.width / 2 - containerRect.left;
    const targetY = targetRect.top + targetRect.height / 2 - containerRect.top;
    
    const line = document.createElement('div');
    line.className = 'connection-line';
    
    const length = Math.sqrt(Math.pow(targetX - sourceX, 2) + Math.pow(targetY - sourceY, 2));
    const angle = Math.atan2(targetY - sourceY, targetX - sourceX) * 180 / Math.PI;
    
    // Different colors for different connection types
    const connectionColors = {
        'invoke': '#FF6B35',
        'query': '#4ECDC4', 
        'read/write': '#45B7D1',
        'data_flow': '#96CEB4',
        'origin': '#FFEAA7'
    };
    
    const color = connectionColors[connection.type] || '#007bff';
    
    line.style.cssText = `
        position: absolute;
        left: ${sourceX}px;
        top: ${sourceY}px;
        width: ${length}px;
        height: 3px;
        background: linear-gradient(to right, ${color}, ${color}aa);
        transform-origin: 0 50%;
        transform: rotate(${angle}deg);
        border-radius: 2px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.2);
    `;
    
    // Add arrow at the end
    const arrow = document.createElement('div');
    arrow.style.cssText = `
        position: absolute;
        right: -8px;
        top: -4px;
        width: 0;
        height: 0;
        border-left: 8px solid ${color};
        border-top: 5px solid transparent;
        border-bottom: 5px solid transparent;
    `;
    line.appendChild(arrow);
    
    // Add connection type label
    const label = document.createElement('div');
    label.className = 'connection-label';
    label.textContent = connection.type;
    label.style.cssText = `
        position: absolute;
        left: ${sourceX + (targetX - sourceX) / 2}px;
        top: ${sourceY + (targetY - sourceY) / 2 - 15}px;
        background: white;
        padding: 2px 6px;
        border-radius: 4px;
        font-size: 10px;
        font-weight: bold;
        color: ${color};
        border: 1px solid ${color};
        transform: translate(-50%, 0);
        white-space: nowrap;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    `;
    
    // Add hover effects
    line.addEventListener('mouseenter', () => {
        line.style.height = '4px';
        line.style.boxShadow = '0 2px 6px rgba(0,0,0,0.3)';
        label.style.background = color;
        label.style.color = 'white';
    });
    
    line.addEventListener('mouseleave', () => {
        line.style.height = '3px';
        line.style.boxShadow = '0 1px 3px rgba(0,0,0,0.2)';
        label.style.background = 'white';
        label.style.color = color;
    });
    
    // Return both line and label in a container
    const connectionContainer = document.createElement('div');
    connectionContainer.appendChild(line);
    connectionContainer.appendChild(label);
    
    return connectionContainer;
}

function addConnectionLegend(container, connections) {
    const connectionTypes = [...new Set(connections.map(c => c.type))];
    
    if (connectionTypes.length === 0) return;
    
    const legend = document.createElement('div');
    legend.className = 'connection-legend';
    legend.style.cssText = `
        position: absolute;
        top: 10px;
        right: 10px;
        background: white;
        border: 1px solid #ddd;
        border-radius: 6px;
        padding: 10px;
        font-size: 12px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        z-index: 20;
    `;
    
    const legendTitle = document.createElement('div');
    legendTitle.textContent = 'Connections';
    legendTitle.style.cssText = `
        font-weight: bold;
        margin-bottom: 8px;
        color: #333;
    `;
    legend.appendChild(legendTitle);
    
    const connectionColors = {
        'invoke': '#FF6B35',
        'query': '#4ECDC4', 
        'read/write': '#45B7D1',
        'data_flow': '#96CEB4',
        'origin': '#FFEAA7'
    };
    
    connectionTypes.forEach(type => {
        const legendItem = document.createElement('div');
        legendItem.style.cssText = `
            display: flex;
            align-items: center;
            margin: 4px 0;
        `;
        
        const colorBox = document.createElement('div');
        colorBox.style.cssText = `
            width: 16px;
            height: 3px;
            background: ${connectionColors[type] || '#007bff'};
            margin-right: 8px;
            border-radius: 2px;
        `;
        
        const typeLabel = document.createElement('span');
        typeLabel.textContent = type;
        typeLabel.style.color = '#666';
        
        legendItem.appendChild(colorBox);
        legendItem.appendChild(typeLabel);
        legend.appendChild(legendItem);
    });
    
    container.appendChild(legend);
}

// Add enhanced styles
const enhancedStyles = `
<style>
.aws-tech-diagram-enhanced {
    position: relative;
    overflow: visible;
}

.aws-tech-diagram-enhanced .aws-service {
    position: relative;
    z-index: 5;
    transition: all 0.3s ease;
}

.aws-tech-diagram-enhanced .aws-service:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    z-index: 15;
}

.connection-line {
    transition: all 0.2s ease;
    cursor: pointer;
}

.connection-label {
    transition: all 0.2s ease;
    cursor: pointer;
}

.connections-overlay {
    pointer-events: none;
}

.connection-legend {
    max-width: 150px;
}
</style>
`;

// Inject enhanced styles
if (!document.querySelector('#enhanced-aws-styles')) {
    const styleElement = document.createElement('div');
    styleElement.id = 'enhanced-aws-styles';
    styleElement.innerHTML = enhancedStyles;
    document.head.appendChild(styleElement);
}

// Export for use
window.renderAwsTechDiagramWithConnections = renderAwsTechDiagramWithConnections;