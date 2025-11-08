function renderAWSInfrastructureDiagram(container, data) {
    if (!data || !data.summary) {
        container.innerHTML = '<div class="item">🔧 No AWS services</div>';
        return;
    }
    
    const services = data.summary.service_types || [];
    const serviceEmojis = {
        'EC2': '🖥️',
        'S3': '🪣',
        'Lambda': '⚡',
        'RDS': '🗄️',
        'DynamoDB': '📊',
        'CloudFront': '🌐',
        'API Gateway': '🚪',
        'VPC': '🏠',
        'IAM': '🔐'
    };
    
    container.innerHTML = services.slice(0, 4).map(service => {
        const emoji = serviceEmojis[service] || '⚙️';
        return `<div class="item">${emoji} ${service}</div>`;
    }).join('');
}