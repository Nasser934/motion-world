package motionworld

import kotlin.math.roundToInt

object FrameSequence {
    fun index(progress: Float, frameCount: Int, reducedMotion: Boolean = false): Int {
        val count = frameCount.coerceAtLeast(1)
        var p = MotionProgress.clamp(progress)
        if (reducedMotion) p = if (p < 0.25f) 0f else if (p < 0.75f) 0.5f else 1f
        return (p * (count - 1)).roundToInt().coerceIn(0, count - 1)
    }

    fun fileName(progress: Float, frameCount: Int, reducedMotion: Boolean = false): String =
        "frame_%04d.webp".format(index(progress, frameCount, reducedMotion))
}
