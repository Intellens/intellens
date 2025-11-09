// Technology icons mapping
const TECH_ICONS = {
    'Python': 'PY',
    'JavaScript': 'JS',
    'TypeScript': 'TS',
    'Java': 'JV',
    'C++': 'C+',
    'C': 'C',
    'Go': 'GO',
    'Rust': 'RS',
    'Ruby': 'RB',
    'PHP': 'PHP',
    'C#': 'C#',
    'Shell': 'SH',
    'HTML': 'HTML',
    'CSS': 'CSS',
    'SQL': 'SQL',
    'Docker': 'DOC',
    'Kubernetes': 'K8S',
    'AWS': 'AWS',
    'Azure': 'AZ',
    'GCP': 'GCP',
    'MongoDB': 'MDB',
    'PostgreSQL': 'PG',
    'MySQL': 'SQL',
    'Redis': 'RDS',
    'Nginx': 'NGX',
    'Apache': 'APH'
};

const AWS_ICONS = {
    'S3': 'S3',
    'EC2': 'EC2',
    'Lambda': 'LAM',
    'RDS': 'RDS',
    'DynamoDB': 'DDB',
    'API Gateway': 'API',
    'CloudWatch': 'CW',
    'IAM': 'IAM',
    'VPC': 'VPC',
    'ELB': 'ELB'
};

function createTechnicalDiagram(data) {
    const svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
    svg.setAttribute('width', '100%');
    svg.setAttribute('height', '600');
    svg.setAttribute('viewBox', '0 0 1000 600');
    svg.style.background = 'linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%)';
    svg.style.borderRadius = '15px';

    // Create layers
    const languageLayer = createLayer('Languages', data.languages, 50, 50, '#667eea');
    const serviceLayer = createLayer('Services', data.services, 550, 50, '#764ba2');
    
    // Add layers to SVG
    svg.appendChild(languageLayer);
    svg.appendChild(serviceLayer);
    
    // Add connections
    const connections = createConnections(data.comprehensive_diagram.edges);
    svg.appendChild(connections);
    
    return svg;
}

function createLayer(title, items, x, y, color) {
    const group = document.createElementNS('http://www.w3.org/2000/svg', 'g');
    
    // Layer background
    const rect = document.createElementNS('http://www.w3.org/2000/svg', 'rect');
    rect.setAttribute('x', x);
    rect.setAttribute('y', y);
    rect.setAttribute('width', '400');
    rect.setAttribute('height', '500');
    rect.setAttribute('fill', 'white');
    rect.setAttribute('stroke', color);
    rect.setAttribute('stroke-width', '2');
    rect.setAttribute('rx', '15');
    rect.setAttribute('opacity', '0.9');
    group.appendChild(rect);
    
    // Layer title
    const titleText = document.createElementNS('http://www.w3.org/2000/svg', 'text');
    titleText.setAttribute('x', x + 200);
    titleText.setAttribute('y', y + 30);
    titleText.setAttribute('text-anchor', 'middle');
    titleText.setAttribute('font-size', '20');
    titleText.setAttribute('font-weight', 'bold');
    titleText.setAttribute('fill', color);
    titleText.textContent = title;
    group.appendChild(titleText);
    
    // Add items
    let itemY = y + 60;
    Object.entries(items).forEach(([name, count], index) => {
        const itemGroup = createTechItem(name, count, x + 20, itemY, color);
        group.appendChild(itemGroup);
        itemY += 80;
    });
    
    return group;
}

function createTechItem(name, count, x, y, color) {
    const group = document.createElementNS('http://www.w3.org/2000/svg', 'g');
    
    // Item background
    const rect = document.createElementNS('http://www.w3.org/2000/svg', 'rect');
    rect.setAttribute('x', x);
    rect.setAttribute('y', y);
    rect.setAttribute('width', '360');
    rect.setAttribute('height', '60');
    rect.setAttribute('fill', color);
    rect.setAttribute('opacity', '0.1');
    rect.setAttribute('rx', '10');
    group.appendChild(rect);
    
    // Icon circle
    const circle = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
    circle.setAttribute('cx', x + 30);
    circle.setAttribute('cy', y + 30);
    circle.setAttribute('r', '20');
    circle.setAttribute('fill', color);
    circle.setAttribute('opacity', '0.2');
    group.appendChild(circle);
    
    // Icon text
    const icon = getIcon(name);
    const iconText = document.createElementNS('http://www.w3.org/2000/svg', 'text');
    iconText.setAttribute('x', x + 30);
    iconText.setAttribute('y', y + 35);
    iconText.setAttribute('text-anchor', 'middle');
    iconText.setAttribute('font-size', '10');
    iconText.setAttribute('font-weight', 'bold');
    iconText.setAttribute('fill', color);
    iconText.textContent = icon;
    group.appendChild(iconText);
    
    // Name text
    const nameText = document.createElementNS('http://www.w3.org/2000/svg', 'text');
    nameText.setAttribute('x', x + 70);
    nameText.setAttribute('y', y + 25);
    nameText.setAttribute('font-size', '16');
    nameText.setAttribute('font-weight', 'bold');
    nameText.setAttribute('fill', '#2c3e50');
    nameText.textContent = name;
    group.appendChild(nameText);
    
    // Count text
    const countText = document.createElementNS('http://www.w3.org/2000/svg', 'text');
    countText.setAttribute('x', x + 70);
    countText.setAttribute('y', y + 45);
    countText.setAttribute('font-size', '12');
    countText.setAttribute('fill', '#666');
    countText.textContent = `${count} ${name.includes('AWS') ? 'references' : 'files'}`;
    group.appendChild(countText);
    
    return group;
}

function createConnections(edges) {
    const group = document.createElementNS('http://www.w3.org/2000/svg', 'g');
    
    edges.forEach((edge, index) => {
        // Create curved connection line
        const path = document.createElementNS('http://www.w3.org/2000/svg', 'path');
        const startX = 450;
        const startY = 100 + (index * 30);
        const endX = 550;
        const endY = 100 + (index * 30);
        
        const d = `M ${startX} ${startY} Q ${(startX + endX) / 2} ${startY - 20} ${endX} ${endY}`;
        path.setAttribute('d', d);
        path.setAttribute('stroke', '#667eea');
        path.setAttribute('stroke-width', '2');
        path.setAttribute('fill', 'none');
        path.setAttribute('opacity', '0.6');
        
        // Add arrow marker
        const marker = document.createElementNS('http://www.w3.org/2000/svg', 'marker');
        marker.setAttribute('id', `arrow-${index}`);
        marker.setAttribute('markerWidth', '10');
        marker.setAttribute('markerHeight', '10');
        marker.setAttribute('refX', '9');
        marker.setAttribute('refY', '3');
        marker.setAttribute('orient', 'auto');
        
        const arrowPath = document.createElementNS('http://www.w3.org/2000/svg', 'path');
        arrowPath.setAttribute('d', 'M0,0 L0,6 L9,3 z');
        arrowPath.setAttribute('fill', '#667eea');
        marker.appendChild(arrowPath);
        
        path.setAttribute('marker-end', `url(#arrow-${index})`);
        
        group.appendChild(marker);
        group.appendChild(path);
    });
    
    return group;
}

function getIcon(name) {
    // Check for AWS services first
    for (const [service, icon] of Object.entries(AWS_ICONS)) {
        if (name.toUpperCase().includes(service)) {
            return icon;
        }
    }
    
    // Check for general technologies
    for (const [tech, icon] of Object.entries(TECH_ICONS)) {
        if (name.includes(tech)) {
            return icon;
        }
    }
    
    // Default icons based on category
    if (name.includes('AWS')) return 'AWS';
    if (name.includes('Database') || name.includes('DB')) return 'DB';
    if (name.includes('API')) return 'API';
    if (name.includes('Web')) return 'WEB';
    
    return 'SYS'; // Default system icon
}