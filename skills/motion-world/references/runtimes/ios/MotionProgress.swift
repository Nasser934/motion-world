import Foundation

public enum MotionProgress {
    public static func clamp(_ value: Double) -> Double {
        guard value.isFinite else { return 0 }
        return min(1, max(0, value))
    }

    public static func elapsed(now: Date, start: Date, end: Date) -> Double {
        let duration = end.timeIntervalSince(start)
        guard duration > 0 else { return now >= end ? 1 : 0 }
        return clamp(now.timeIntervalSince(start) / duration)
    }

    public static func countdown(remaining: Double, total: Double) -> Double {
        guard total > 0 else { return remaining <= 0 ? 1 : 0 }
        return clamp(1 - remaining / total)
    }

    public static func count(current: Double, minimum: Double = 0, goal: Double) -> Double {
        let range = goal - minimum
        guard range > 0 else { return current >= goal ? 1 : 0 }
        return clamp((current - minimum) / range)
    }
}
