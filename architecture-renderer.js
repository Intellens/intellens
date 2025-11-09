// Professional architecture diagram renderer
const COMPONENT_ICONS = {
    'user': '👤',
    'database': '🗄️',
    'api': '🔌',
    'service': '⚙️',
    'frontend': '🖥️',
    'backend': '🔧',
    'cloud': '☁️',
    'code': '💻',
    'language': '📝',
    'storage': '📦'
};

const COMPONENT_COLORS = {
    'user': '#3498db',
    'database': '#e74c3c',
    'api': '#f39c12',
    'service': '#9b59b6',
    'frontend': '#2ecc71',
    'backend': '#34495e',
    'cloud': '#1abc9c',
    'language': '#e67e22',
    'storage': '#95a5a6'
};

function renderArchitectureDiagram(diagramData) {
    const container = document.createElement('div');
    container.className = 'architecture-diagram';
    container.style.cssText = `
        position: relative;
        width: 100%;
        height: 500px;
        background: linear-gradient(135deg, #f8f9ff 0%, #e8f0ff 100%);
        border-radius: 15px;
        overflow: visible;
        border: 2px solid #667eea;
        padding: 30px;
    `;
    
    // Create SVG for connections
    const svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
    svg.style.cssText = `
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        z-index: 10;
        pointer-events: none;
    `;
    
    // Add title
    const title = document.createElement('div');
    title.textContent = diagramData.title || 'Project Architecture';
    title.style.cssText = `
        position: absolute;
        top: 20px;
        left: 50%;
        transform: translateX(-50%);
        font-size: 24px;
        font-weight: bold;
        color: #2c3e50;
        z-index: 3;
    `;
    
    // Render components
    diagramData.components.forEach(component => {
        const componentEl = createComponent(component);
        container.appendChild(componentEl);
    });
    
    // Render flows
    diagramData.flows.forEach(flow => {
        const flowEl = createFlow(flow, diagramData.components, svg);
    });
    
    container.appendChild(svg);
    container.appendChild(title);
    
    // Add description
    if (diagramData.description) {
        const desc = document.createElement('div');
        desc.textContent = diagramData.description;
        desc.style.cssText = `
            position: absolute;
            bottom: 20px;
            left: 20px;
            right: 20px;
            background: rgba(255,255,255,0.9);
            padding: 15px;
            border-radius: 10px;
            font-size: 14px;
            color: #666;
            z-index: 3;
        `;
        container.appendChild(desc);
    }
    
    return container;
}

function createComponent(component) {
    const el = document.createElement('div');
    const color = COMPONENT_COLORS[component.type] || '#95a5a6';
    
    el.style.cssText = `
        position: absolute;
        left: ${component.position.x}px;
        top: ${component.position.y}px;
        width: 160px;
        min-height: 90px;
        background: white;
        border: 2px solid ${color};
        border-radius: 8px;
        padding: 12px;
        text-align: center;
        box-shadow: 0 3px 10px rgba(0,0,0,0.1);
        z-index: 5;
        transition: all 0.2s ease;
    `;
    
    el.addEventListener('mouseenter', () => {
        el.style.transform = 'scale(1.05)';
    });
    
    el.addEventListener('mouseleave', () => {
        el.style.transform = 'scale(1)';
    });
    
    // Icon
    const icon = document.createElement('div');
    icon.textContent = COMPONENT_ICONS[component.type] || '⚙️';
    icon.style.cssText = `
        font-size: 24px;
        margin: 0 auto 8px auto;
        width: 40px;
        height: 40px;
        display: flex;
        align-items: center;
        justify-content: center;
    `;
    
    // Name
    const name = document.createElement('div');
    name.textContent = component.name;
    name.style.cssText = `
        font-weight: bold;
        font-size: 14px;
        color: ${color};
        margin-bottom: 8px;
        line-height: 1.2;
    `;
    
    // Description
    const desc = document.createElement('div');
    desc.textContent = component.description;
    desc.style.cssText = `
        font-size: 11px;
        color: #666;
        line-height: 1.3;
        margin-top: 5px;
    `;
    
    el.appendChild(icon);
    el.appendChild(name);
    el.appendChild(desc);
    
    return el;
}

function createFlow(flow, components, svg) {
    const fromComp = components.find(c => c.id === flow.from);
    const toComp = components.find(c => c.id === flow.to);
    
    if (!fromComp || !toComp) return;
    
    const startX = fromComp.position.x + 70; // Center of component
    const startY = fromComp.position.y + 50;
    const endX = toComp.position.x + 70;
    const endY = toComp.position.y + 50;
    
    // Create arrow path
    const path = document.createElementNS('http://www.w3.org/2000/svg', 'path');
    const midX = (startX + endX) / 2;
    const midY = (startY + endY) / 2;
    
    // Create curved path to avoid overlaps
    const controlX = midX + (Math.random() - 0.5) * 100;
    const controlY = midY - 50;
    const d = `M ${startX} ${startY} Q ${controlX} ${controlY} ${endX} ${endY}`;
    path.setAttribute('d', d);
    path.setAttribute('stroke', '#ff4444');
    path.setAttribute('opacity', '1');
    path.setAttribute('stroke-width', '3');
    path.setAttribute('fill', 'none');
    path.setAttribute('marker-end', 'url(#arrowhead)');
    
    // Create arrowhead marker
    const defs = document.createElementNS('http://www.w3.org/2000/svg', 'defs');
    const marker = document.createElementNS('http://www.w3.org/2000/svg', 'marker');
    marker.setAttribute('id', 'arrowhead');
    marker.setAttribute('markerWidth', '15');
    marker.setAttribute('markerHeight', '10');
    marker.setAttribute('refX', '12');
    marker.setAttribute('refY', '5');
    marker.setAttribute('orient', 'auto');
    
    const polygon = document.createElementNS('http://www.w3.org/2000/svg', 'polygon');
    polygon.setAttribute('points', '0 0, 15 5, 0 10');
    polygon.setAttribute('fill', '#ff4444');
    
    marker.appendChild(polygon);
    defs.appendChild(marker);
    svg.appendChild(defs);
    svg.appendChild(path);
    
    // Add step number
    const stepCircle = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
    stepCircle.setAttribute('cx', midX);
    stepCircle.setAttribute('cy', midY);
    stepCircle.setAttribute('r', '15');
    stepCircle.setAttribute('fill', '#667eea');
    
    const stepText = document.createElementNS('http://www.w3.org/2000/svg', 'text');
    stepText.setAttribute('x', midX);
    stepText.setAttribute('y', midY + 4);
    stepText.setAttribute('text-anchor', 'middle');
    stepText.setAttribute('fill', 'white');
    stepText.setAttribute('font-weight', 'bold');
    stepText.setAttribute('font-size', '12');
    stepText.textContent = flow.step;
    
    svg.appendChild(stepCircle);
    svg.appendChild(stepText);
    
    // Add flow label with background
    const labelWidth = flow.label.length * 6 + 10;
    const labelBg = document.createElementNS('http://www.w3.org/2000/svg', 'rect');
    labelBg.setAttribute('x', midX - labelWidth/2);
    labelBg.setAttribute('y', midY - 25);
    labelBg.setAttribute('width', labelWidth);
    labelBg.setAttribute('height', '14');
    labelBg.setAttribute('fill', 'white');
    labelBg.setAttribute('stroke', '#667eea');
    labelBg.setAttribute('stroke-width', '1');
    labelBg.setAttribute('rx', '7');
    
    const label = document.createElementNS('http://www.w3.org/2000/svg', 'text');
    label.setAttribute('x', midX);
    label.setAttribute('y', midY - 16);
    label.setAttribute('text-anchor', 'middle');
    label.setAttribute('font-size', '9');
    label.setAttribute('fill', '#2c3e50');
    label.setAttribute('font-weight', '500');
    label.textContent = flow.label;
    
    svg.appendChild(labelBg);
    svg.appendChild(label);
}