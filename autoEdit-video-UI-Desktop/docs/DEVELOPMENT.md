# Development Guide

## 🔧 AutoEdit Video UI Desktop - Development Documentation

### Getting Started

#### Prerequisites
- Python 3.8 or higher
- PyQt6 development environment
- VideoForge backend running
- Git for version control

#### Environment Setup
```bash
# Clone repository
git clone <repository-url>
cd autoEdit-video-UI-Desktop

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Install development dependencies
pip install -r requirements-dev.txt
```

#### Project Structure
```
src/
├── core/           # Application core logic
├── ui/             # User interface components
├── services/       # Business logic services
├── models/         # Data models
├── controllers/    # MVC controllers
└── utils/          # Utility functions
```

### Development Workflow

#### 1. Code Organization
- **Follow MVC Pattern**: Separate Model, View, Controller
- **Small Classes**: Maximum 200 lines per class
- **Single Responsibility**: One purpose per module
- **Clear Naming**: Descriptive class and method names

#### 2. UI Development
```python
# Example widget structure
class VideoPlayerWidget(QWidget):
    # Signals for communication
    video_loaded = pyqtSignal(str)
    playback_changed = pyqtSignal(bool)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        self.connect_signals()
    
    def setup_ui(self):
        # UI setup code
        pass
    
    def connect_signals(self):
        # Signal connections
        pass
```

#### 3. Service Layer
```python
# Example service structure
class VideoService:
    def __init__(self):
        self.api_service = APIService()
    
    def process_video(self, video_path, action, settings):
        # Business logic here
        result = self.api_service.send_request(...)
        return result
```

#### 4. Controller Pattern
```python
# Example controller structure
class MainController:
    def __init__(self, view, model):
        self.view = view
        self.model = model
        self.video_service = VideoService()
        self.connect_signals()
    
    def connect_signals(self):
        self.view.video_selected.connect(self.handle_video_selection)
```

### Code Standards

#### Python Style Guide
- **PEP 8**: Follow Python style guidelines
- **Type Hints**: Use type annotations
- **Docstrings**: Document all public methods
- **Import Organization**: Group imports logically

```python
"""
Module docstring describing purpose
"""

from typing import List, Optional
import sys
from pathlib import Path

from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import pyqtSignal

from ..models.video_model import VideoModel


class ExampleClass:
    """Class docstring with purpose and usage"""
    
    def __init__(self, param: str) -> None:
        """Initialize with parameter"""
        self.param = param
    
    def process_data(self, data: List[str]) -> Optional[str]:
        """
        Process data and return result
        
        Args:
            data: List of strings to process
            
        Returns:
            Processed result or None if failed
        """
        pass
```

#### Qt/PyQt Best Practices
- **Signal-Slot Pattern**: Use for component communication
- **Layout Management**: Use layout managers, not absolute positioning
- **Resource Management**: Properly clean up resources
- **Thread Safety**: Keep UI operations on main thread

### Testing Strategy

#### Unit Testing
```python
# tests/test_models/test_video_model.py
import pytest
from src.models.video_model import VideoModel

class TestVideoModel:
    def test_video_creation(self):
        video = VideoModel(
            id="test_1",
            name="test.mp4",
            file_path="test.mp4",
            size=1000000,
            format="mp4",
            duration=120.0,
            width=1920,
            height=1080,
            fps=30.0,
            bitrate=5000
        )
        assert video.resolution == "1920x1080"
        assert video.duration_str == "02:00"
```

#### UI Testing
```python
# tests/test_ui/test_widgets.py
import pytest
from PyQt6.QtWidgets import QApplication
from src.ui.widgets.video_player_widget import VideoPlayerWidget

@pytest.fixture
def app():
    return QApplication([])

def test_video_widget_creation(app):
    widget = VideoPlayerWidget()
    assert widget is not None
    assert hasattr(widget, 'play')
    assert hasattr(widget, 'pause')
```

#### Integration Testing
```python
# tests/test_integration/test_video_processing.py
def test_video_processing_workflow():
    # Test complete workflow
    service = VideoService()
    result = service.process_video("test.mp4", "compress", {"quality": "high"})
    assert result.success is True
```

### Debugging

#### Logging Setup
```python
import logging

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('debug.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)
```

#### Debug Tools
- **PyQt Inspector**: For UI debugging
- **pdb/debugger**: For code debugging
- **Memory Profiler**: For memory leak detection
- **Performance Profiler**: For performance optimization

### Build and Deployment

#### Creating Executable
```bash
# Using PyInstaller
pyinstaller --onefile --windowed main.py

# Custom spec file for advanced options
pyinstaller main.spec
```

#### Package Structure
```
dist/
├── AutoEditUI.exe          # Main executable
├── config/                 # Configuration files
├── resources/             # Resources (icons, styles)
└── libs/                  # Required libraries
```

### Performance Guidelines

#### Memory Management
- **Cleanup Resources**: Always clean up Qt objects
- **Avoid Memory Leaks**: Use context managers
- **Optimize Images**: Compress thumbnails and icons
- **Lazy Loading**: Load UI components when needed

#### UI Responsiveness
- **Threading**: Use QThread for long operations
- **Progress Updates**: Regular progress feedback
- **Cancellation**: Allow users to cancel operations
- **Async Operations**: Non-blocking UI calls

### Security Considerations

#### File Handling
- **Path Validation**: Validate all file paths
- **Permission Checks**: Verify file permissions
- **Size Limits**: Enforce file size restrictions
- **Format Validation**: Check file formats

#### API Communication
- **Input Validation**: Validate all API inputs
- **Error Handling**: Handle API errors gracefully
- **Timeout Handling**: Set appropriate timeouts
- **SSL/TLS**: Use secure connections

### Version Control

#### Git Workflow
```bash
# Feature branch workflow
git checkout -b feature/video-player
git add .
git commit -m "feat: implement video player widget"
git push origin feature/video-player

# Create pull request for review
```

#### Commit Messages
- **Format**: `type(scope): description`
- **Types**: feat, fix, docs, style, refactor, test
- **Examples**:
  - `feat(ui): add video player controls`
  - `fix(service): handle API timeout errors`
  - `docs(readme): update installation instructions`

### Documentation

#### Code Documentation
- **Docstrings**: All public methods and classes
- **Type Hints**: Function parameters and returns
- **Comments**: Complex logic explanations
- **README**: Project overview and setup

#### User Documentation
- **User Guide**: Feature explanations
- **Tutorials**: Step-by-step workflows
- **FAQ**: Common questions and issues
- **API Reference**: Technical reference

### Common Issues and Solutions

#### PyQt Issues
- **Import Errors**: Check PyQt6 installation
- **UI Freezing**: Move long operations to threads
- **Memory Leaks**: Properly parent Qt objects
- **Styling Issues**: Check QSS syntax

#### Video Processing Issues
- **Codec Support**: Verify FFmpeg installation
- **Large Files**: Implement streaming processing
- **Format Errors**: Add comprehensive validation
- **Performance**: Use hardware acceleration

### Development Tools

#### Recommended IDEs
- **PyCharm**: Full-featured Python IDE
- **VS Code**: Lightweight with Python extensions
- **Qt Creator**: For UI design (optional)
- **Spyder**: Scientific Python development

#### Useful Extensions
- **Python**: Language support
- **PyQt Integration**: UI development
- **Git**: Version control
- **Linting**: Code quality checking

---

*This guide should be updated as the project evolves and new patterns emerge.*
