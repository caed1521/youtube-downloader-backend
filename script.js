// API Configuration
const API_BASE_URL = window.APP_CONFIG ? window.APP_CONFIG.API_BASE_URL : 'http://localhost:8000';

// DOM Elements
const urlInput = document.getElementById('youtube-url');
const downloadBtn = document.getElementById('download-btn');
const formatRadios = document.querySelectorAll('input[name="format"]');
const qualitySelector = document.getElementById('quality-selector');
const qualityDropdown = document.getElementById('quality');
const statusSection = document.getElementById('status-section');
const statusMessage = document.getElementById('status-message');
const progressContainer = document.getElementById('progress-container');
const progressFill = document.getElementById('progress-fill');
const progressText = document.getElementById('progress-text');
const videoPreview = document.getElementById('video-preview');
const videoThumbnail = document.getElementById('video-thumbnail');
const videoTitle = document.getElementById('video-title');
const videoDetails = document.getElementById('video-details');
const finalDownloadBtn = document.getElementById('final-download-btn');
const downloadText = document.getElementById('download-text');

// State management
let currentVideoData = null;
let isProcessing = false;

// Initialize the app
document.addEventListener('DOMContentLoaded', function() {
    setupEventListeners();
    updateQualityVisibility();
});

// Event Listeners
function setupEventListeners() {
    // URL input validation
    urlInput.addEventListener('input', validateUrl);
    urlInput.addEventListener('paste', function() {
        setTimeout(validateUrl, 100); // Allow paste to complete
    });

    // Format selection
    formatRadios.forEach(radio => {
        radio.addEventListener('change', function() {
            updateQualityVisibility();
            validateUrl(); // Re-validate to update button state
        });
    });

    // Download button
    downloadBtn.addEventListener('click', handleDownload);
    finalDownloadBtn.addEventListener('click', handleFinalDownload);

    // Quality selector
    qualityDropdown.addEventListener('change', function() {
        if (currentVideoData) {
            updateDownloadButton();
        }
    });
}

// URL Validation and Analysis
function validateUrl() {
    const url = urlInput.value.trim();
    const isValid = isValidYouTubeUrl(url);
    
    // Update input styling
    urlInput.classList.remove('success', 'error');
    if (url.length > 0) {
        urlInput.classList.add(isValid ? 'success' : 'error');
        
        // If valid, analyze video to get available qualities
        if (isValid && !isProcessing) {
            analyzeVideoQualities(url);
        } else {
            resetQualitySelector();
        }
    } else {
        resetQualitySelector();
    }
    
    // Update download button
    downloadBtn.disabled = !isValid || isProcessing;
    
    return isValid;
}

// Analyze video to get available qualities
async function analyzeVideoQualities(url) {
    try {
        const response = await fetch(`${API_BASE_URL}/analyze-url`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ url: url })
        });
        
        if (response.ok) {
            const data = await response.json();
            updateQualitySelector(data.video_info.formats_available);
        }
    } catch (error) {
        console.warn('Error analyzing video qualities:', error);
        resetQualitySelector();
    }
}

// Update quality selector with available qualities
function updateQualitySelector(formatsAvailable) {
    const mp4Formats = formatsAvailable.mp4 || {};
    const qualities = Object.keys(mp4Formats).sort((a, b) => {
        const heightA = parseInt(a.replace('p', ''));
        const heightB = parseInt(b.replace('p', ''));
        return heightB - heightA; // Sort descending
    });
    
    // Clear existing options
    qualityDropdown.innerHTML = '';
    
    if (qualities.length > 0) {
        qualities.forEach(quality => {
            const option = document.createElement('option');
            option.value = quality;
            const formatInfo = mp4Formats[quality];
            option.textContent = formatInfo.label || quality;
            qualityDropdown.appendChild(option);
        });
        
        // Select 720p if available, otherwise the first option
        const preferredQuality = qualities.find(q => q === '720p') || qualities[0];
        qualityDropdown.value = preferredQuality;
    } else {
        // Fallback to default options
        resetQualitySelector();
    }
}

// Reset quality selector to default options
function resetQualitySelector() {
    qualityDropdown.innerHTML = `
        <option value="1080p">1080p (Full HD)</option>
        <option value="720p" selected>720p (HD)</option>
        <option value="480p">480p (SD)</option>
        <option value="360p">360p</option>
        <option value="240p">240p</option>
    `;
}

function isValidYouTubeUrl(url) {
    const youtubeRegex = /^(https?:\/\/)?(www\.)?(youtube\.com\/(watch\?v=|embed\/|v\/)|youtu\.be\/)[\w-]+(&[\w=]*)?$/;
    return youtubeRegex.test(url);
}

// Quality selector visibility
function updateQualityVisibility() {
    const selectedFormat = document.querySelector('input[name="format"]:checked').value;
    if (selectedFormat === 'mp3') {
        qualitySelector.style.display = 'none';
    } else {
        qualitySelector.style.display = 'block';
    }
}

// Download handling
async function handleDownload() {
    if (!validateUrl() || isProcessing) return;
    
    isProcessing = true;
    downloadBtn.disabled = true;
    
    const url = urlInput.value.trim();
    const format = document.querySelector('input[name="format"]:checked').value;
    const quality = format === 'mp4' ? qualityDropdown.value : null;
    
    try {
        // Show status section
        statusSection.style.display = 'block';
        statusSection.scrollIntoView({ behavior: 'smooth' });
        
        // Reset status
        showStatusMessage('Analizando video...', true);
        videoPreview.style.display = 'none';
        finalDownloadBtn.style.display = 'none';
        
        // Simulate API call for demo (replace with actual API call)
        await simulateVideoAnalysis(url, format, quality);
        
    } catch (error) {
        showError('Error al procesar el video. Por favor, verifica el enlace e intenta nuevamente.');
        console.error('Download error:', error);
    } finally {
        isProcessing = false;
        downloadBtn.disabled = false;
    }
}

// Real API integration for video analysis
async function simulateVideoAnalysis(url, format, quality) {
    try {
        // Step 1: Analyzing video
        showStatusMessage('Analizando video...', true);
        
        // Call backend API to analyze video
        const response = await fetch(`${API_BASE_URL}/analyze`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                url: url,
                format: format,
                quality: quality
            })
        });
        
        if (!response.ok) {
            let errorMessage = 'Error analyzing video';
            try {
                const errorData = await response.json();
                errorMessage = errorData.detail || errorData.message || `HTTP ${response.status}: ${response.statusText}`;
            } catch (e) {
                errorMessage = `HTTP ${response.status}: ${response.statusText}`;
            }
            console.error('Backend error response:', errorMessage);
            throw new Error(errorMessage);
        }
        
        const data = await response.json();
        
        // Step 2: Show video preview
        currentVideoData = {
            ...data.video_info,
            format,
            quality,
            download_id: data.download_id,
            estimated_size: data.estimated_size
        };
        
        showVideoPreview(data.video_info);
        showStatusMessage('¡Listo para descargar!', false);
        updateDownloadButton();
        finalDownloadBtn.style.display = 'flex';
        
    } catch (error) {
        console.error('Error in simulateVideoAnalysis:', error);
        console.error('Error details:', {
            message: error.message,
            stack: error.stack,
            name: error.name
        });
        throw new Error(`Error al analizar el video: ${error.message}`);
    }
}

// Get video info (simulated - replace with actual API)
async function getVideoInfo(url) {
    // Extract video ID from URL
    const videoId = extractVideoId(url);
    
    // Simulated video data (in real implementation, this would come from your backend)
    return {
        id: videoId,
        title: 'Video de YouTube - Título del video',
        thumbnail: `https://img.youtube.com/vi/${videoId}/maxresdefault.jpg`,
        duration: '3:45',
        views: '1.2M visualizaciones',
        uploader: 'Canal de YouTube'
    };
}

function extractVideoId(url) {
    const match = url.match(/(?:youtube\.com\/watch\?v=|youtu\.be\/|youtube\.com\/embed\/)([^&\n?#]+)/);
    return match ? match[1] : 'dQw4w9WgXcQ'; // Default to Rick Roll for demo
}

// UI Updates
function showStatusMessage(message, showSpinner) {
    const spinner = statusMessage.querySelector('.loading-spinner');
    const text = statusMessage.querySelector('span');
    
    text.textContent = message;
    spinner.style.display = showSpinner ? 'block' : 'none';
}

function showVideoPreview(videoData) {
    videoThumbnail.src = videoData.thumbnail;
    videoThumbnail.alt = videoData.title;
    videoTitle.textContent = videoData.title;
    videoDetails.textContent = `${videoData.duration} • ${videoData.views}`;
    
    videoPreview.style.display = 'flex';
}

function updateDownloadButton() {
    if (!currentVideoData) return;
    
    const { format, quality, estimated_size } = currentVideoData;
    const fileExtension = format.toUpperCase();
    const qualityText = format === 'mp4' ? ` (${quality})` : '';
    const sizeText = estimated_size || getEstimatedSize(format, quality);
    
    downloadText.textContent = `Descargar ${fileExtension}${qualityText} • ~${sizeText}`;
}

function getEstimatedSize(format, quality) {
    // Simulated file sizes (in real implementation, get from backend)
    const sizes = {
        'mp3': '3.2 MB',
        'mp4': {
            '240p': '8.5 MB',
            '360p': '15.2 MB',
            '480p': '25.8 MB',
            '720p': '45.6 MB',
            '1080p': '85.3 MB'
        }
    };
    
    return format === 'mp3' ? sizes.mp3 : sizes.mp4[quality] || '25 MB';
}

function showError(message) {
    statusSection.style.display = 'block';
    showStatusMessage(message, false);
    videoPreview.style.display = 'none';
    finalDownloadBtn.style.display = 'none';
    
    // Add error styling
    statusMessage.style.color = '#dc3545';
    setTimeout(() => {
        statusMessage.style.color = '#B3B3B3';
    }, 5000);
}

// Final download handling
async function handleFinalDownload() {
    if (!currentVideoData || !currentVideoData.download_id) return;
    
    try {
        // Show downloading state
        finalDownloadBtn.disabled = true;
        downloadText.textContent = 'Iniciando descarga...';
        
        // Start the download process on the backend
        const startResponse = await fetch(`http://localhost:8000/download/${currentVideoData.download_id}`, {
            method: 'POST'
        });
        
        if (!startResponse.ok) {
            const errorData = await startResponse.json();
            throw new Error(errorData.detail || 'Error starting download');
        }
        
        // Poll for download status
        await pollDownloadStatus(currentVideoData.download_id);
        
    } catch (error) {
        showError('Error durante la descarga. Por favor, intenta nuevamente.');
        console.error('Final download error:', error);
        finalDownloadBtn.disabled = false;
        updateDownloadButton();
    }
}

// Poll download status until completion
async function pollDownloadStatus(downloadId) {
    const maxAttempts = 60; // 5 minutes max
    let attempts = 0;
    
    // Show progress container
    progressContainer.style.display = 'block';
    updateProgress(0, 'Iniciando descarga...');
    
    while (attempts < maxAttempts) {
        try {
            const statusResponse = await fetch(`${API_BASE_URL}/status/${downloadId}`);
            
            if (!statusResponse.ok) {
                throw new Error('Error checking download status');
            }
            
            const statusData = await statusResponse.json();
            const progress = statusData.progress || 0;
            
            if (statusData.status === 'downloading') {
                updateProgress(progress, 'Descargando archivo...');
                downloadText.textContent = `Descargando... ${Math.round(progress)}%`;
            } else if (statusData.status === 'processing') {
                updateProgress(progress, 'Procesando archivo...');
                downloadText.textContent = 'Procesando archivo...';
            } else if (statusData.status === 'completed') {
                updateProgress(100, '¡Descarga completada!');
                
                // Download the file
                downloadText.textContent = 'Descargando archivo...';
                await downloadCompletedFile(downloadId);
                
                // Cleanup
                await cleanupDownload(downloadId);
                
                // Reset UI
                resetDownloadForm();
                showSuccessMessage();
                return;
                
            } else if (statusData.status === 'error') {
                throw new Error(statusData.error || 'Download failed');
            }
            
            // Wait before next poll
            await delay(2000); // 2 seconds for more responsive updates
            attempts++;
            
        } catch (error) {
            throw error;
        }
    }
    
    throw new Error('Download timeout - please try again');
}

// Update progress bar and text
function updateProgress(percentage, message) {
    const clampedPercentage = Math.max(0, Math.min(100, percentage));
    progressFill.style.width = `${clampedPercentage}%`;
    progressText.textContent = `${Math.round(clampedPercentage)}%`;
    
    if (message) {
        const spinner = statusMessage.querySelector('.loading-spinner');
        const text = statusMessage.querySelector('span');
        text.textContent = message;
        
        // Hide spinner when download starts
        if (clampedPercentage > 0) {
            spinner.style.display = 'none';
        }
    }
}

// Download the completed file
async function downloadCompletedFile(downloadId) {
    try {
        const response = await fetch(`${API_BASE_URL}/file/${downloadId}`);
        
        if (!response.ok) {
            throw new Error('Error downloading file');
        }
        
        // Get filename from response headers or use default
        const contentDisposition = response.headers.get('content-disposition');
        let filename = 'download';
        
        if (contentDisposition) {
            const filenameMatch = contentDisposition.match(/filename="(.+)"/);
            if (filenameMatch) {
                filename = filenameMatch[1];
            }
        }
        
        // Create blob and download
        const blob = await response.blob();
        const url = URL.createObjectURL(blob);
        
        const a = document.createElement('a');
        a.href = url;
        a.download = filename;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
        
    } catch (error) {
        throw new Error(`Error downloading file: ${error.message}`);
    }
}

// Cleanup download on backend
async function cleanupDownload(downloadId) {
    try {
        await fetch(`${API_BASE_URL}/cleanup/${downloadId}`, {
            method: 'DELETE'
        });
    } catch (error) {
        console.warn('Error cleaning up download:', error);
    }
}

// Simulate download process (replace with actual download logic)
async function simulateDownload() {
    const { format, quality } = currentVideoData;
    
    // Create a simulated download (in real implementation, this would be a server endpoint)
    const filename = `video.${format}`;
    const blob = new Blob(['Simulated file content'], { type: `video/${format}` });
    const url = URL.createObjectURL(blob);
    
    // Trigger download
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
    
    await delay(1000); // Simulate processing time
}

function resetDownloadForm() {
    urlInput.value = '';
    urlInput.classList.remove('success', 'error');
    downloadBtn.disabled = true;
    statusSection.style.display = 'none';
    progressContainer.style.display = 'none';
    progressFill.style.width = '0%';
    progressText.textContent = '0%';
    currentVideoData = null;
    resetQualitySelector();
}

function showSuccessMessage() {
    // You could show a toast notification or success message here
    console.log('Download completed successfully!');
}

// Utility functions
function delay(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

function scrollToSection(sectionId) {
    const section = document.getElementById(sectionId);
    if (section) {
        section.scrollIntoView({ behavior: 'smooth' });
    }
}

// Smooth scroll for contact button
window.scrollToSection = scrollToSection;

// Handle form submission with Enter key
urlInput.addEventListener('keypress', function(e) {
    if (e.key === 'Enter' && !downloadBtn.disabled) {
        handleDownload();
    }
});

// Add some visual feedback for better UX
document.addEventListener('click', function(e) {
    // Add ripple effect to buttons
    if (e.target.matches('.download-btn, .final-download-btn, .contact-btn')) {
        createRipple(e);
    }
});

function createRipple(event) {
    const button = event.currentTarget;
    const ripple = document.createElement('span');
    const rect = button.getBoundingClientRect();
    const size = Math.max(rect.width, rect.height);
    const x = event.clientX - rect.left - size / 2;
    const y = event.clientY - rect.top - size / 2;
    
    ripple.style.width = ripple.style.height = size + 'px';
    ripple.style.left = x + 'px';
    ripple.style.top = y + 'px';
    ripple.classList.add('ripple');
    
    button.appendChild(ripple);
    
    setTimeout(() => {
        ripple.remove();
    }, 600);
}

// Add ripple CSS
const rippleCSS = `
.download-btn, .final-download-btn, .contact-btn {
    position: relative;
    overflow: hidden;
}

.ripple {
    position: absolute;
    border-radius: 50%;
    background: rgba(255, 255, 255, 0.3);
    transform: scale(0);
    animation: ripple-animation 0.6s linear;
    pointer-events: none;
}

@keyframes ripple-animation {
    to {
        transform: scale(4);
        opacity: 0;
    }
}
`;

// Inject ripple CSS
const style = document.createElement('style');
style.textContent = rippleCSS;
document.head.appendChild(style);
