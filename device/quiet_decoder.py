"""
Wrapper around OmiOpusDecoder that suppresses error output
"""
import sys
import io
from contextlib import redirect_stdout, redirect_stderr
from omi import OmiOpusDecoder as _OmiOpusDecoder

class QuietOmiOpusDecoder(_OmiOpusDecoder):
    """OmiOpusDecoder with suppressed error messages"""

    def decode_packet(self, data):
        """Decode without printing errors"""
        # Suppress stdout/stderr during decode
        with redirect_stdout(io.StringIO()), redirect_stderr(io.StringIO()):
            return super().decode_packet(data)
