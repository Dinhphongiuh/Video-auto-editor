# Video Player Structure

## Chức năng Video Player
Phát video thật thay vì hiển thị placeholder, hỗ trợ các format video phổ biến.

## Files và chức năng:

### Core Player Files:
- `video_player_core.py` - Core video player engine với OpenCV
- `video_frame_widget.py` - Widget hiển thị frame video 
- `video_controls_service.py` - Service quản lý playback controls
- `video_cache_manager.py` - Cache frames để performance tốt hơn

### Integration Files:
- `video_preview_widget.py` - Main preview widget (đã có, cần update)
- `playback_controls_widget.py` - Playback controls (đã có, cần sync)

## Workflow:
1. User chọn video từ Media Library
2. VideoPlayerCore load video với OpenCV
3. VideoFrameWidget hiển thị frames
4. VideoCacheManager cache frames để smooth playback
5. VideoControlsService đồng bộ controls với playback

## Dependencies:
- OpenCV: Đọc và decode video
- PyQt6: UI framework
- Threading: Background video processing
- NumPy: Frame data processing

## Performance Features:
- Frame caching
- Background loading
- Smooth seeking
- Multiple format support