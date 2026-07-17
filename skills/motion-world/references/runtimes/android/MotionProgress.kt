package motionworld

import kotlin.math.max
import kotlin.math.min

object MotionProgress {
    fun clamp(value: Float): Float = if (value.isFinite()) min(1f, max(0f, value)) else 0f

    fun elapsed(nowMillis: Long, startMillis: Long, endMillis: Long): Float {
        val duration = endMillis - startMillis
        if (duration <= 0L) return if (nowMillis >= endMillis) 1f else 0f
        return clamp((nowMillis - startMillis).toFloat() / duration.toFloat())
    }

    fun countdown(remaining: Float, total: Float): Float {
        if (total <= 0f) return if (remaining <= 0f) 1f else 0f
        return clamp(1f - remaining / total)
    }

    fun count(current: Float, minimum: Float = 0f, goal: Float): Float {
        val range = goal - minimum
        if (range <= 0f) return if (current >= goal) 1f else 0f
        return clamp((current - minimum) / range)
    }
}
