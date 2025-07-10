#!/usr/bin/env python3
"""
VideoForge CLI - Main entry point for command line interface
"""

import sys
import click
from pathlib import Path
from typing import Optional

from ..core.video_processor import VideoProcessor
from ..core.batch_manager import BatchManager
from ..utils.logger import get_logger
from ..utils.config_loader import ConfigLoader
from ..utils.validators import validate_input_path, validate_output_path

# Optional API server import
try:
    from ..api.rest_server import start_server
    API_SERVER_AVAILABLE = True
except ImportError:
    start_server = None
    API_SERVER_AVAILABLE = False

logger = get_logger(__name__)


@click.group()
@click.version_option(version="0.1.0", prog_name="VideoForge")
@click.option("--config", "-c", help="Configuration file path")
@click.option("--verbose", "-v", is_flag=True, help="Enable verbose logging")
@click.option("--quiet", "-q", is_flag=True, help="Suppress output")
@click.pass_context
def cli(ctx, config: Optional[str], verbose: bool, quiet: bool):
    """
    VideoForge - Professional Video Processing Engine
    
    Forge your videos to perfection with AI-powered processing.
    """
    ctx.ensure_object(dict)
    
    # Set up logging level
    if verbose:
        logger.setLevel("DEBUG")
    elif quiet:
        logger.setLevel("ERROR")
    else:
        logger.setLevel("INFO")
    
    # Load configuration
    config_loader = ConfigLoader(config_path=config)
    ctx.obj["config"] = config_loader.load_config()
    
    logger.info("VideoForge CLI initialized")


@cli.command()
@click.option("--input", "-i", required=True, help="Input video file or directory")
@click.option("--output", "-o", required=True, help="Output directory")
@click.option("--resolution", "-r", help="Output resolution (e.g., 1920x1080)")
@click.option("--aspect-ratio", "-a", help="Aspect ratio (e.g., 16:9)")
@click.option("--speed", "-s", type=float, help="Speed multiplier (0.25-4.0)")
@click.option("--profile", "-p", help="Processing profile (youtube_shorts, instagram_reels, etc.)")
@click.option("--auto-subtitle", is_flag=True, help="Generate automatic subtitles")
@click.option("--remove-logo", is_flag=True, help="Automatically remove logos")
@click.option("--brightness", type=int, help="Brightness adjustment (-100 to 100)")
@click.option("--contrast", type=int, help="Contrast adjustment (-100 to 100)")
@click.option("--saturation", type=int, help="Saturation adjustment (-100 to 100)")
@click.option("--quality", type=click.Choice(["low", "medium", "high", "ultra"]), help="Output quality")
@click.option("--threads", "-t", type=int, help="Number of processing threads")
@click.option("--gpu", is_flag=True, help="Use GPU acceleration")
@click.option("--dry-run", is_flag=True, help="Preview operations without processing")
@click.pass_context
def process(ctx, **kwargs):
    """
    Process video files with specified parameters
    
    Examples:
    
    \b
    # Basic processing
    videoforge process -i ./videos -o ./processed
    
    \b
    # With AI features
    videoforge process -i ./videos -o ./processed --auto-subtitle --remove-logo
    
    \b
    # Using preset profile
    videoforge process -i ./videos -o ./processed --profile youtube_shorts
    
    \b
    # Advanced processing
    videoforge process -i ./video.mp4 -o ./output \\
        --resolution 1920x1080 \\
        --aspect-ratio 16:9 \\
        --speed 1.2 \\
        --brightness 10 \\
        --auto-subtitle \\
        --quality high
    """
    
    config = ctx.obj["config"]
    
    # Validate inputs
    input_path = Path(kwargs["input"])
    output_path = Path(kwargs["output"])
    
    if not validate_input_path(input_path):
        click.echo(f"Error: Invalid input path: {input_path}", err=True)
        sys.exit(1)
    
    if not validate_output_path(output_path):
        click.echo(f"Error: Invalid output path: {output_path}", err=True)
        sys.exit(1)
    
    # Process single file or batch
    if input_path.is_file():
        processor = VideoProcessor(config)
        _process_single_file(processor, input_path, output_path, kwargs)
    else:
        batch_manager = BatchManager(config)
        _process_batch(batch_manager, input_path, output_path, kwargs)


@cli.command()
@click.option("--port", "-p", default=8080, help="Server port")
@click.option("--host", "-h", default="localhost", help="Server host")
@click.option("--workers", "-w", type=int, default=1, help="Number of worker processes")
@click.pass_context
def serve(ctx, port: int, host: str, workers: int):
    """
    Start VideoForge background service
    
    This starts a REST API server that can be used by the desktop application
    or other clients to process videos.
    """
    if not API_SERVER_AVAILABLE:
        click.echo("❌ API server not available. Install with: pip install videoforge-core[ai]", err=True)
        sys.exit(1)
    
    config = ctx.obj["config"]
    
    click.echo(f"Starting VideoForge server on {host}:{port}")
    click.echo(f"Workers: {workers}")
    click.echo("Press Ctrl+C to stop")
    
    try:
        start_server(config, host=host, port=port, workers=workers)
    except KeyboardInterrupt:
        click.echo("\nShutting down server...")
    except Exception as e:
        click.echo(f"Error starting server: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.option("--list-profiles", is_flag=True, help="List available processing profiles")
@click.option("--show-config", is_flag=True, help="Show current configuration")
@click.option("--system-info", is_flag=True, help="Show system information")
@click.pass_context
def info(ctx, list_profiles: bool, show_config: bool, system_info: bool):
    """
    Show information about VideoForge configuration and system
    """
    config = ctx.obj["config"]
    
    if list_profiles:
        _show_profiles(config)
    
    if show_config:
        _show_config(config)
    
    if system_info:
        _show_system_info()


def _process_single_file(processor: VideoProcessor, input_path: Path, output_path: Path, options: dict):
    """Process a single video file"""
    click.echo(f"Processing: {input_path}")
    
    try:
        result = processor.process_video(
            input_path=str(input_path),
            output_path=str(output_path / input_path.name),
            **_filter_options(options)
        )
        
        if result.success:
            click.echo(f"✓ Successfully processed: {result.output_path}")
        else:
            click.echo(f"✗ Failed to process: {result.error}", err=True)
            
    except Exception as e:
        click.echo(f"✗ Error processing {input_path}: {e}", err=True)


def _process_batch(batch_manager: BatchManager, input_dir: Path, output_dir: Path, options: dict):
    """Process multiple video files"""
    click.echo(f"Batch processing: {input_dir}")
    
    try:
        results = batch_manager.process_directory(
            input_dir=str(input_dir),
            output_dir=str(output_dir),
            **_filter_options(options)
        )
        
        success_count = sum(1 for r in results if r.success)
        total_count = len(results)
        
        click.echo(f"\n📊 Batch processing completed:")
        click.echo(f"✓ Successful: {success_count}")
        click.echo(f"✗ Failed: {total_count - success_count}")
        click.echo(f"📁 Output directory: {output_dir}")
        
        # Show failed files if any
        failed_files = [r for r in results if not r.success]
        if failed_files:
            click.echo("\n❌ Failed files:")
            for result in failed_files:
                click.echo(f"  - {result.input_path}: {result.error}")
                
    except Exception as e:
        click.echo(f"✗ Error in batch processing: {e}", err=True)


def _filter_options(options: dict) -> dict:
    """Filter out None values and CLI-specific options"""
    filtered = {}
    
    # Map CLI options to processor options
    option_mapping = {
        'resolution': 'resolution',
        'aspect_ratio': 'aspect_ratio', 
        'speed': 'speed',
        'profile': 'profile',
        'auto_subtitle': 'auto_subtitle',
        'remove_logo': 'remove_logo',
        'brightness': 'brightness',
        'contrast': 'contrast',
        'saturation': 'saturation',
        'quality': 'quality',
        'threads': 'threads',
        'gpu': 'gpu',
        'dry_run': 'dry_run'
    }
    
    for cli_key, processor_key in option_mapping.items():
        if cli_key in options and options[cli_key] is not None:
            filtered[processor_key] = options[cli_key]
            
    return filtered


def _show_profiles(config: dict):
    """Show available processing profiles"""
    click.echo("\n📋 Available Processing Profiles:")
    
    profiles = config.get('profiles', {})
    if not profiles:
        click.echo("  No profiles configured")
        return
    
    for name, profile in profiles.items():
        click.echo(f"\n🎯 {name}:")
        for key, value in profile.items():
            click.echo(f"  {key}: {value}")


def _show_config(config: dict):
    """Show current configuration"""
    click.echo("\n⚙️ Current Configuration:")
    
    import json
    formatted_config = json.dumps(config, indent=2)
    click.echo(formatted_config)


def _show_system_info():
    """Show system information"""
    import platform
    
    # Optional imports
    try:
        import psutil
        HAS_PSUTIL = True
    except ImportError:
        HAS_PSUTIL = False
    
    try:
        import torch
        HAS_TORCH = True
    except ImportError:
        HAS_TORCH = False
    
    click.echo("\n💻 System Information:")
    click.echo(f"  OS: {platform.system()} {platform.release()}")
    click.echo(f"  Python: {platform.python_version()}")
    
    if HAS_PSUTIL:
        click.echo(f"  CPU: {psutil.cpu_count()} cores")
        click.echo(f"  Memory: {psutil.virtual_memory().total // (1024**3)} GB")
    else:
        click.echo("  CPU/Memory: Install psutil for detailed info")
    
    # Check GPU availability
    if HAS_TORCH and torch.cuda.is_available():
        click.echo(f"  GPU: {torch.cuda.get_device_name(0)}")
        click.echo(f"  CUDA: {torch.version.cuda}")
    else:
        click.echo("  GPU: Not available (install torch with CUDA for GPU support)")
    
    # Check FFmpeg
    import subprocess
    try:
        result = subprocess.run(['ffmpeg', '-version'], capture_output=True, text=True)
        if result.returncode == 0:
            version_line = result.stdout.split('\n')[0]
            click.echo(f"  FFmpeg: {version_line}")
        else:
            click.echo("  FFmpeg: Not installed")
    except FileNotFoundError:
        click.echo("  FFmpeg: Not found in PATH")


def main():
    """Main entry point for CLI"""
    try:
        cli()
    except KeyboardInterrupt:
        click.echo("\n⚠️ Operation cancelled by user")
        sys.exit(1)
    except Exception as e:
        click.echo(f"\n❌ Unexpected error: {e}", err=True)
        logger.exception("CLI error")
        sys.exit(1)


if __name__ == "__main__":
    main()
