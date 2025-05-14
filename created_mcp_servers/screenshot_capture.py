#!/usr/bin/env python3
import io
import asyncio
import base64
from typing import Dict

import mss
import mss.tools
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("screenshot_capture")

@mcp.tool()
async def capture_screenshot(save_path: str = "screenshot.png") -> Dict[str, str]:
    """
    Capture a full-screen screenshot and return it as a base64-encoded PNG string.
    Returns:
        A dict with key "image_base64" containing the PNG image data.
    """
    with mss.mss() as sct:
        screenshot = sct.grab(sct.monitors[0])
        png_bytes = mss.tools.to_png(screenshot.rgb, screenshot.size)
    
    with open(save_path, "wb") as f:
        f.write(png_bytes)
        
    b64 = base64.b64encode(png_bytes).decode("utf-8")
    return {"saved_to": save_path,
            "image_base64": b64}

if __name__ == "__main__":
    asyncio.run(mcp.run())